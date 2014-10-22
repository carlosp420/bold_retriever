import argparse
from argparse import RawTextHelpFormatter
import codecs
import json
import logging
from pprint import pformat
import re
import urllib

from Bio import SeqIO
from bs4 import BeautifulSoup
import requests
from twisted.internet.defer import DeferredSemaphore, gatherResults
from twisted.web.client import Agent, readBody
from twisted.internet import reactor
from twisted.web.http_headers import Headers

import engine


def taxon_search(obj):
    # obj['tax_id'] = "Morpho helenor"
    tax_id = obj['tax_id'].split(" ")
    if len(tax_id) > 1:
        tax_id = tax_id[0]
    url = "http://www.boldsystems.org/index.php/API_Tax/TaxonSearch/"
    # print "I am sending this %s" % tax_id
    payload = {
        'taxName': tax_id,
        'fuzzy': 'false',
    }
    r = get(url, payload)
    found_division = False
    if r.text != "":
        response = json.loads(r.text)
        if hasattr(response, 'items'):
            for k, v in response.items():
                try:
                    if v['tax_division'] == 'Animals':
                        # this is the taxID
                        found_division = True
                        return {'division': 'animal', 'taxID': k}
                except:
                    logging.warning("Error: %s" % str(r.text))

            if not found_division:
                for k, v in json.loads(r.text).items():
                    try:
                        if v['tax_division'] != 'Animals':
                            # this is the taxID
                            return {'division': 'not animal', 'taxID': k}
                    except:
                        logging.warning("Got funny reply from BOLD.")
        else:
            return None
    return None


def taxon_data(obj):
    this_tax_id = obj['taxID']
    url = "http://www.boldsystems.org/index.php/API_Tax/TaxonData/"
    payload = {'taxId': this_tax_id, 'dataTypes': 'basic',
               'includeTree': 'true'
               }
    req = get(url, payload)

    # this is a "list" then
    if req.text == '[]':
        obj = {'classification': 'false'}
        return obj
    # this is a string not a list
    elif isinstance(req.text, basestring):
        items = json.loads(req.text).items()
        for key, val in items:
            try:
                if val['tax_rank'] == 'class':
                    obj['class'] = val['taxon']
                if val['tax_rank'] == 'order':
                    obj['order'] = val['taxon']
                if val['tax_rank'] == 'family':
                    obj['family'] = val['taxon']
            except TypeError:
                logging.warning("Exception: No values for some of the keys.")
            obj['classification'] = "true"
        if 'family' in obj:
            return obj
        else:
            # The family name for this specimen is returned as `tax_id`
            # because this samples is not `public` by BOLD when using the API.
            # Try to get the tax_id from the webpage BIN.
            return get_tax_id_from_web(obj)


def get_tax_id_from_web(obj):
    """Try to get the tax_id from the webpage BIN."""
    logging.info('Trying to get the tax_id from the webpage Public_BIN.')

    # get cart token
    url = 'http://www.boldsystems.org/index.php/Public_BINSearch'
    payload = {
        'taxon': '',
        'searchMenu': 'bins',
        'query': obj['bold_id'],
    }
    r = get(url, payload)
    cart_token = re.search('= \'(general_.+)\';//', r.text).groups()[0]

    # get actual data using the cart token
    url = 'http://www.boldsystems.org/index.php/Public_Ajax_BinList'
    payload = {
        'offset': 0,
        'limit': 100,
        'query': obj['bold_id'],
        'cartToken': cart_token,
        'inc[]': 'ids::processid::' + obj['bold_id'],
        'contextOp': 'AND',
        '_': 1412165276887,
    }
    r = get(url, payload)
    soup = BeautifulSoup(r.text)
    for i in soup.find_all('span'):
        if 'Species' in i.get_text():
            taxon = i.next_sibling.string.strip()
            taxon = re.sub("\([0-9]+\)", "", taxon)
            taxon = re.sub(";", "", taxon)
            res = re.search('^(\w+\s?\w*\.*)', taxon.strip())
            if res:
                obj['tax_id'] = res.groups()[0]
                obj['family'] = get_family_name_for_taxon(obj['tax_id'])
            return obj
    logging.info('The BOLD webpage does not contain Genus and Species names '
                 'for BOLD record %s.' % obj['bold_id'] )
    return obj


def get_family_name_for_taxon(tax_id):
    """Send genus name and get family name from the `parentname` result form
    the API."""
    taxon = tax_id.split(" ")[0]
    if taxon.endswith("dae"):
        # This is already a family name
        return taxon
    elif taxon.endswith("nae"):
        result = get_parentname(taxon)
        return result
    else:
        # this might be a genus
        genus_parent = get_parentname(taxon)
        if genus_parent.endswith("nae"):
            # this is a subfamily then do another search
            subfamily_parent = get_parentname(genus_parent)
            return subfamily_parent
        else:
            return genus_parent


def get_parentname(taxon):
    url = 'http://www.boldsystems.org/index.php/API_Tax/TaxonSearch'
    params = {'taxName': taxon}
    req = get(url, params)

    if req.text == '[]':
        return None
    elif isinstance(req.text, basestring):
        items = json.loads(req.text).items()
        for key, val in items:
            if val['parentname']:
                return val['parentname']


def create_output_file(f):
    """Containing only column headers of the CSV file."""
    output = "seq_id,bold_id,similarity,division,class,order,family,species,"
    output += "collection_country\n"

    output_filename = f.strip() + "_output.csv"
    myfile = codecs.open(output_filename, "w", "utf-8")
    myfile.write(output)
    myfile.close()
    return output_filename


def process_classification(obj):
    out = ""
    if obj['classification'] == "true":
        if 'class' in obj:
            out += obj['class'] + ","
        else:
            out += "None,"

        if 'order' in obj:
            out += obj['order'] + ","
        else:
            out += "None,"

        if 'family' in obj:
            out += obj['family']
        else:
            out += "None"
    else:
        out += "None,None,None"
    return out

def cbRequest(response, seq_record):
    print 'Response version:', response.version
    print 'Response code:', response.code
    print 'Response phrase:', response.phrase
    print 'Response headers:'
    print pformat(list(response.headers.getAllRawHeaders()))
    d = readBody(response)
    d.addCallback(cbBody, seq_record)
    return d


def cbBody(body, seq_record):
    print 'Response body:'

    all_ids = []
    taxon_list = []
    if isinstance(body, basestring):
        all_ids, taxon_list = engine.parse_bold_xml(
            body,
            seq_record.seq,
            seq_record.id,
            all_ids,
            taxon_list,
        )
        if all_ids is not None and len(all_ids) > 0:
            # for i in all_ids:
            # print i['tax_id'], i['similarity']
            print(all_ids)
            return all_ids
        else:
            return None
    else:
        return None


def async(seq_record, db):
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
    d.addCallback(cbRequest, seq_record=seq_record)

    def cbFinished(ignored):
        print("Finishing job", seq_record.id)
    d.addCallback(cbFinished)
    return d



def generate_output_content_for_file(output_filename, fasta_file, db):
    """
    Use Twisted.
    """
    sem = DeferredSemaphore(50)
    jobs = []
    append = jobs.append

    for seq_record in SeqIO.parse(fasta_file, "fasta"):
        append(sem.run(async, seq_record, db))

    d = gatherResults(jobs)
    d.addCallback(lambda ignored: reactor.stop())
    reactor.run()
    print("Processed all sequences.")
    return "Processed all sequences."


def get(url, payload):
    """Wrapper function for requests.get so we can use fake requests when
    writing unittests.
    :param url:
    :param params: payload
    :return: response object from requests.get
    """
    r = requests.get(url, params=payload)
    return r


def get_args(args):
    db = args.db
    f = args.fasta_file
    return f, db


def get_started(args):
    fasta_file, db = get_args(args)
    output_filename = create_output_file(fasta_file)
    generate_output_content_for_file(output_filename, fasta_file, db)


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
