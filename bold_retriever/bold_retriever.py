import argparse
from argparse import RawTextHelpFormatter
import codecs
import json
import xml.etree.ElementTree as ET

from Bio import SeqIO
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


def request_id(seq_object, id, db):
    # input a sequence object
    # sends sequence to BOLD REST API for Identification Engine db=COX1_L640bp
    # output a dictionary with the info
    all_ids = []
    taxon_list = []
    url = "http://boldsystems.org/index.php/Ids_xml"
    payload = {'db': db, 'sequence': str(seq_object)}
    r = requests.get(url, params=payload)
    if r.text is not None:
        all_ids, taxon_list = parse_bold_xml(r.text, seq_object, id, all_ids,
                                             taxon_list)
    else:
        return None

    if all_ids is not None:
        for i in all_ids:
            print i['tax_id'], i['similarity']
        return all_ids
    else:
        return None


def taxon_search(obj):
    # obj['tax_id'] = "Morpho helenor"
    tax_id = obj['tax_id'].split(" ")
    if len(tax_id) > 1:
        tax_id = tax_id[0]
    url = "http://www.boldsystems.org/index.php/API_Tax/TaxonSearch/"
    print "I am sending this %s" % tax_id
    payload = {
        'taxName': tax_id,
        'fuzzy': 'false',
    }
    r = requests.get(url, params=payload)
    found_division = False
    if r.text != "":
        for k, v in json.loads(r.text).items():
            try:
                if v['tax_division'] == 'Animals':
                    # this is the taxID
                    found_division = True
                    return {'division': 'animal', 'taxID': k}
            except:
                print "\n>> Error: " + str(r.text)

        if not found_division:
            for k, v in json.loads(r.text).items():
                try:
                    if v['tax_division'] != 'Animals':
                        # this is the taxID
                        found_division = True
                        return {'division': 'not animal', 'taxID': k}
                except:
                    out_msg = "\n>> Error got funny reply from BOLD: "
                    out_msg += str(r.text)
                    print(out_msg)
    return None


def taxon_data(obj):
    this_tax_id = obj['taxID']
    url = "http://www.boldsystems.org/index.php/API_Tax/TaxonData/"
    payload = {'taxId': this_tax_id, 'dataTypes': 'basic',
               'includeTree': 'true'
               }
    req = requests.get(url, params=payload)

    # this is a "list" then
    if req.text == '[]':
        obj = {'classification': 'false'}
        return obj
    # this is a string not a list
    elif isinstance(req.text, basestring):
        for key, val in json.loads(req.text).items():
            if val['tax_rank'] == 'class':
                obj['class'] = val['taxon']
            if val['tax_rank'] == 'order':
                obj['order'] = val['taxon']
            if val['tax_rank'] == 'family':
                obj['family'] = val['taxon']
            obj['classification'] = "true"
        print obj
        return obj


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
    out = "bold_id,seq_id,similarity,collection_country,division,taxon,"
    out += "class,order,family\n"
    output_filename = f.strip() + "_output.csv"
    myfile = codecs.open(output_filename, "w", "utf-8")
    myfile.write(out)
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
            out += obj['family'] + ","
        else:
            out += "None,"
        out += "\n"
    else:
        out += "None,None,None\n"
    return out


def main():
    parser = create_parser()
    args = parser.parse_args()

    db = args.db
    f = args.fasta_file

    output_filename = create_output_file(f)
    for seq_record in SeqIO.parse(f, "fasta"):
        out = ""
        all_ids = request_id(seq_record.seq, seq_record.id, db)
        for obj in all_ids:
            if 'tax_id' in obj:
                r = taxon_search(obj)

                if r is None:
                    continue
                obj['taxID'] = r['taxID']
                obj['division'] = r['division']
                print "== obj", obj
                obj = taxon_data(obj)
                out += obj['bold_id'] + ","
                out += obj['id'] + "," + obj['similarity'] + ","
                out += obj['collection_country'] + ","
                out += obj['division'] + ","
                out += obj['tax_id'] + ","
                out += process_classification(obj)

        myfile = codecs.open(output_filename, "a", "utf-8")
        myfile.write(out)
        myfile.close()


if __name__ == "__main__":
    main()
