import argparse
from argparse import RawTextHelpFormatter
from typing import Tuple
import urllib

from Bio import SeqIO
from twisted.internet.defer import DeferredSemaphore, gatherResults
from twisted.web.client import Agent, readBody
from twisted.internet import reactor, threads
from twisted.web.http_headers import Headers

from bold_retriever import engine


def create_output_file(output_filename: str) -> str:
    """Containing only column headers of the CSV file."""
    output = "seq_id,bold_id,similarity,division,class,order,family,species,"
    output += "collection_country\n"

    output_filename = output_filename.strip() + "_output.csv"
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


def async(seq_record, db, output_filename):
    print("Processing sequence for %s" % str(seq_record.id))

    domain = "http://boldsystems.org/index.php/Ids_xml"
    payload = {'db': db, 'sequence': str(seq_record.seq)}
    url = domain + '?' + urllib.urlencode(payload)

    agent = Agent(reactor)
    d = agent.request(
        'GET', url,
        Headers({'User-Agent': ['bold_retriever']}),
        None,
    )
    d.addCallback(cbRequest, seq_record=seq_record, output_filename=output_filename)

    def cbFinished(ignored):
        print("Finishing job", seq_record.id)
    d.addCallback(cbFinished)
    return d


def generate_jobs(output_filename, fasta_file, db):
    """Uses Twisted."""
    sem = DeferredSemaphore(50)
    jobs = []

    for seq_record in SeqIO.parse(fasta_file, "fasta"):
        jobs.append(sem.run(async, seq_record, db, output_filename))

    d = gatherResults(jobs)
    d.addCallback(lambda ignored: reactor.stop())
    reactor.run()
    print("Processed all sequences.")
    return "Processed all sequences."


def get_args(args) -> Tuple[str, str]:
    bold_database = args.db
    output_filename = args.fasta_file
    return output_filename, bold_database


def get_started(args):
    output_filename, bold_database = get_args(args)
    output_filename = create_output_file(output_filename)
    generate_jobs(output_filename, output_filename, bold_database)


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