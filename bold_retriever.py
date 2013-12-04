#!/usr/bin/env python

import xml.etree.ElementTree as ET
import sys
import requests
from Bio import SeqIO
import json
import codecs


def request_id(seq_object, id):
    # input a sequence object
    # sends sequence to BOLD REST API for Identification Engine db=COX1_L640bp
    # output a dictionary with the info
    out = {}
    out['seq'] = str(seq_object)
    out['id'] = str(id)
    url = "http://boldsystems.org/index.php/Ids_xml"
    payload = { 'db': 'COX1_L640bp', 'sequence': str(seq_object) }
    r = requests.get(url, params=payload)
    if r.text != None:
        root = ET.fromstring(r.text)
        #print r.text
        for match in root.findall('match'):
            similarity = match.find('similarity').text
            out['similarity'] = similarity
            tax_id = match.find('taxonomicidentification').text
            out['tax_id'] = tax_id

            myid = match.find('ID').text
            out['bold_id'] = myid
            break
    else:
        return None
    return out


def request_classification(obj):
    #obj['tax_id'] = "Morpho helenor"
    tax_id = obj['tax_id'].split(" ")
    if len(tax_id) > 1:
        tax_id = tax_id[0]
    url = "http://www.boldsystems.org/index.php/API_Tax/TaxonSearch/"
    print "i am sending this %s" % tax_id
    payload = { 'taxName': tax_id }
    r = requests.get(url, params=payload)
    if r.text != "":
        for k, v in json.loads(r.text).items():
            taxID = k
            break
        print taxID
        url = "http://www.boldsystems.org/index.php/API_Tax/TaxonData/"
        payload = { 'taxId': taxID, 'dataTypes': 'basic', 'includeTree': 'true' }
        req = requests.get(url, params=payload)
        if req.text != "":
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
    else:
        obj['classification'] = "false"
        return obj



if len(sys.argv) < 2:
    print "Error, you need to enter a FASTA file name as parameter"
    print "\n\tpython bold_retriever.py ZA2013.fasta"
    sys.exit()

f = sys.argv[1]

out = "bold_id,seq_id,similarity,taxon,class,order,family\n"
myfile = codecs.open("output.csv", "w", "utf-8")
myfile.write(out)
myfile.close()
for seq_record in SeqIO.parse(f, "fasta"):
    out = ""
    obj = request_id(seq_record.seq, seq_record.id)
    if 'tax_id' in obj:
        obj = request_classification(obj)
        out += obj['bold_id'] + ","
        out += obj['id'] + "," + obj['similarity'] + "," + obj['tax_id'] + ","
        if obj['classification'] == "true":
            out += obj['class'] + "," + obj['order'] + "," + obj['family'] + "\n"
        else:
            out += "None,None,None\n"
    myfile = codecs.open("output.csv", "a", "utf-8")
    myfile.write(out)
    myfile.close()

