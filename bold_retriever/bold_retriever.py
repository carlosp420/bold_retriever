import argparse
from argparse import RawTextHelpFormatter
import codecs
import json
import logging
import re
import xml.etree.ElementTree as ET

from Bio import SeqIO
from bs4 import BeautifulSoup
import requests


def parse_bold_xml(request, seq_object, id, all_ids, taxon_list):
    try:
        root = ET.fromstring(request)
        for match in root.findall('match'):
            out = dict()
            out['seq'] = str(seq_object)
            out['id'] = str(id)
            similarity = match.find('similarity').text
            out['similarity'] = similarity
            tax_id = match.find('taxonomicidentification').text
            out['tax_id'] = tax_id

            if match.find('specimen/collectionlocation/country').text:
                ctry = match.find('specimen/collectionlocation/country').text
                out['collection_country'] = ctry
            else:

                out['collection_country'] = "None"

            myid = match.find('ID').text
            out['bold_id'] = myid
            if not out['tax_id'] in taxon_list:
                taxon_list.append(out['tax_id'])
                all_ids.append(out)
        return all_ids, taxon_list
    except ET.ParseError as e:
        print "\n>> Error got malformed XML from BOLD: " + str(e)
        return all_ids, taxon_list
    except TypeError as e:
        print "\n>> Error got malformed XML from BOLD: " + str(e)
        return all_ids, taxon_list


def request_id(seq_object, id, db, debug=False):
    """
    Sends a sequence to BOLD REST API for identification using a database
    specified by the user.

    :param seq_object: sequence as string
    :param id: sequence id as string
    :param db: BOLD database specified by user as string
    :return: two lists of diciontaries with some identification info
    """
    all_ids = []
    taxon_list = []
    url = "http://boldsystems.org/index.php/Ids_xml"
    payload = {'db': db, 'sequence': str(seq_object)}

    r = get(url, payload)
    r_text = r.text
    if debug is True:
        r_text = []

    if isinstance(r_text, basestring):
        all_ids, taxon_list = parse_bold_xml(r_text, seq_object, id, all_ids,
                                             taxon_list)
        if all_ids is not None and len(all_ids) > 0:
            # for i in all_ids:
            # print i['tax_id'], i['similarity']
            return all_ids
        else:
            return None
    else:
        return None


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


def generate_output_content_for_file(output_filename, fasta_file, db):
    for seq_record in SeqIO.parse(fasta_file, "fasta"):
        print("Processing sequence for %s" % str(seq_record.id))
        out = ""
        all_ids = request_id(seq_record.seq, seq_record.id, db)
        if all_ids is not None:
            for obj in all_ids:
                if 'tax_id' in obj:
                    r = taxon_search(obj)

                    if r is None:
                        continue
                    obj['taxID'] = r['taxID']
                    obj['division'] = r['division']
                    # print("== obj", obj)
                    obj = taxon_data(obj)

                    out += obj['id'] + ","
                    out += obj['bold_id'] + ","
                    out += obj['similarity'] + ","
                    out += obj['division'] + ","
                    out += process_classification(obj) + ","
                    out += obj['tax_id'] + ","
                    out += obj['collection_country'] + "\n"

            with codecs.open(output_filename, "a", "utf-8") as handle:
                handle.write(out)
        else:
            out = "nohit," + str(seq_record.id) + ","
            out += "nohit,nohit,nohit,nohit,nohit,nohit,nohit\n"
            with codecs.open(output_filename, "a", "utf-8") as handle:
                handle.write(out)
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


def main():
    parser = create_parser()
    args = parser.parse_args()
    get_started(args)


if __name__ == "__main__":
    main()
