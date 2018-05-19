from datetime import datetime, timedelta
from typing import Dict, Optional
from urllib.parse import urlencode

from Bio import SeqIO
import click
import dataset
import requests

from engine import generate_output_content, parse_id_engine_xml


DATABASE_URL = "sqlite:///bold.sqlite"
DB = dataset.connect(DATABASE_URL)


@click.command()
@click.option('-f', '--filename', type=str, help='Fasta filename', required=True)
@click.option('-db',
              '--database',
              type=click.Choice([
                  'COX1_SPECIES', 'COX1', 'COX1_SPECIES_PUBLIC', 'COX1_L640bp',
              ]),
              help='Choose a BOLD database. Enter one option.',
              required=True,
              )
def bold(filename, database):
    "Send seqs to BOLD Systems API and retrieve results"
    click.echo(filename +  " "  +  database)
    output_filename = create_output_file(filename)
    generate_jobs(output_filename, filename, database)


def create_output_file(input_filename: str) -> str:
    """Containing only column headers of the CSV file."""
    output = "id,bold_id,sequencedescription,database,citation,taxonomicidentification,similarity,url,country,lat,lon,class,order,family,species,"
    output += "collection_country\n"

    output_filename = input_filename.strip() + "_output.csv"
    print(f"Creating output file {output_filename}")
    with open(output_filename, "w") as handle:
        handle.write(output)
    return output_filename


def generate_jobs(output_filename: str, fasta_file: str, db: str):
    print(f"Reading sequences from {fasta_file}")

    for seq_record in SeqIO.parse(fasta_file, "fasta"):
        print(f"* Reading seq {seq_record.name}")
        response = id_engine(seq_record, db, output_filename)
        seq_record_identifications = parse_id_engine_xml(response.text)

        # add our seq id to the list of identifications
        for seq_record_identification in seq_record_identifications:
            seq_record_identification["OtuID"] = seq_record.id
            taxonomy = get_taxonomy(seq_record_identification)
            seq_record_identification.update(taxonomy)
        generate_output_content(seq_record_identifications, output_filename, seq_record)


def id_engine(seq_record, db, output_filename):
    """Send a COI sequence to BOLD and retrieve its identification"""
    print(f"* Processing sequence for {seq_record.id}")

    domain = "http://boldsystems.org/index.php/Ids_xml"
    payload = {'db': db, 'sequence': str(seq_record.seq)}
    url = domain + '?' + urlencode(payload)

    res = requests.get(url, headers={'User-Agent': 'bold_retriever'})
    return res


def get_taxonomy(seq_record: Dict[str, str]) -> Optional[Dict[str, str]]:
    tax_id = get_tax_id(seq_record)
    if tax_id:
        taxonomy = get_higher_level_taxonomy(tax_id)
        return taxonomy


def get_tax_id(seq_record: Dict[str, str]):
    tax_id = get_tax_id_from_db(seq_record)
    if tax_id:
        return tax_id

    domain = "http://boldsystems.org/index.php/API_Tax/TaxonSearch?taxName="
    url = domain + seq_record["taxonomicidentification"]
    res = requests.get(url, headers={'User-Agent': 'bold_retriever'})
    response_json = res.json()
    try:
        tax_id = response_json["top_matched_names"][0]["taxid"]
    except (KeyError, IndexError):
        tax_id = None

    if tax_id:
        table = DB["tax_ids"]
        data = {
            "taxon": seq_record["taxonomicidentification"],
            "tax_id": tax_id,
        }
        table.insert(data)
    return tax_id


def get_tax_id_from_db(seq_record: Dict[str, str]) -> Optional[str]:
    table = DB["tax_ids"]
    element = table.find_one(taxon=seq_record["taxonomicidentification"])
    if element:
        return element["tax_id"]


def get_higher_level_taxonomy(tax_id):
    table = DB["taxonomy"]
    element = table.find_one(tax_id=tax_id)
    if element:
        del element["id"]
        return element

    url = f"http://boldsystems.org/index.php/API_Tax/TaxonData?taxId={tax_id}&dataTypes=basic&includeTree=true"
    res = requests.get(url, headers={'User-Agent': 'bold_retriever'})
    response_json = res.json()
    taxonomy = dict()

    for id in response_json.keys():
        category = response_json[id]
        value = category["taxon"]
        key = category["tax_rank"]
        taxonomy[key] = value

    taxonomy["tax_id"] = tax_id
    table.insert(taxonomy)
    return taxonomy


if __name__ == '__main__':
    bold()
