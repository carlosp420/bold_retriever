from Bio import SeqIO
import click
import requests
from urllib.parse import urlencode

from engine import generate_output_content, parse_id_engine_xml


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
    print(f"Reading sequences from {output_filename}")
    for seq_record in SeqIO.parse(fasta_file, "fasta"):
        print(f"* Reading seq {seq_record.name}")
        response = id_engine(seq_record, db, output_filename)
        seq_record_identifications = parse_id_engine_xml(response.text)
        print(seq_record_identifications)
        generate_output_content(seq_record_identifications, output_filename, seq_record)


def id_engine(seq_record, db, output_filename):
    """Send a COI sequence to BOLD and retrieve its identification"""
    print(f"* Processing sequence for {seq_record.id}")

    domain = "http://boldsystems.org/index.php/Ids_xml"
    payload = {'db': db, 'sequence': str(seq_record.seq)}
    url = domain + '?' + urlencode(payload)

    res = requests.get(url, headers={'User-Agent': 'bold_retriever'})
    return res


if __name__ == '__main__':
    bold()
