import argparse
from argparse import RawTextHelpFormatter
from typing import Tuple
from urllib.parse import urlencode

import requests
from Bio import SeqIO
from twisted.internet.defer import DeferredSemaphore, gatherResults
from twisted.web.client import Agent, readBody
from twisted.internet import reactor, threads
from twisted.web.http_headers import Headers

from engine import parse_id_engine_xml, generate_output_content


def create_output_file(input_filename: str) -> str:
    """Containing only column headers of the CSV file."""
    output = "id,bold_id,sequencedescription,database,citation,taxonomicidentification,similarity,url,country,lat,lon,class,order,family,species,"
    output += "collection_country\n"

    output_filename = input_filename.strip() + "_output.csv"
    print(f"Creating output file {output_filename}")
    with open(output_filename, "w") as handle:
        handle.write(output)
    return output_filename


def cbRequest(response, seq_record, output_filename):
    d = readBody(response)
    d.addCallback(cbBody, seq_record, output_filename)
    return d


def cbBody(body, seq_record, output_filename):
    all_ids = []
    taxon_list = []
    if isinstance(body, str):
        all_ids, taxon_list = engine.parse_bold_xml(
            body,
            seq_record.seq,
            seq_record.id,
            all_ids,
            taxon_list,
        )
        command = [(engine.generate_output_content, [all_ids, output_filename, seq_record], {})]
        threads.callMultipleInThread(command)


def id_engine(seq_record, db, output_filename):
    """Send a COI sequence to BOLD and retrieve its identification"""
    print(f"* Processing sequence for {seq_record.id}")

    domain = "http://boldsystems.org/index.php/Ids_xml"
    payload = {'db': db, 'sequence': str(seq_record.seq)}
    url = domain + '?' + urlencode(payload)

    res = requests.get(url, headers={'User-Agent': 'bold_retriever'})
    return res


def generate_jobs(output_filename, fasta_file, db):
    print(f"Reading sequences from {output_filename}")
    for seq_record in SeqIO.parse(fasta_file, "fasta"):
        print(f"* Reading seq {seq_record.name}")
        response = id_engine(seq_record, db, output_filename)
        seq_record_identifications = parse_id_engine_xml(response.text)
        generate_output_content(seq_record_identifications, output_filename, seq_record)



def get_args(args) -> Tuple[str, str]:
    input_filename = args.fasta_file
    bold_database = args.db
    return input_filename, bold_database


def get_started(args):
    input_filename, bold_database = get_args(args)
    output_filename = create_output_file(input_filename)
    generate_jobs(output_filename, input_filename, bold_database)


def create_parser():
    description = "send seqs to BOLD Systems API and retrieve results"
    parser = argparse.ArgumentParser(description=description,
                                     formatter_class=RawTextHelpFormatter,
                                     )
    parser.add_argument('-f', '--file', action='store', help='Fasta filename',
                        required=True, dest='fasta_file',
                        )
    parser.add_argument('-db', '--database', action='store',
                        help='Choose a BOLD database. Enter one option.',
                        choices=[
                            'COX1_SPECIES',
                            'COX1',
                            'COX1_SPECIES_PUBLIC',
                            'COX1_L640bp',
                            ],
                        required=True,
                        dest='db',
                        )
    return parser


def main():
    parser = create_parser()
    args = parser.parse_args()
    get_started(args)


if __name__ == "__main__":
    main()
