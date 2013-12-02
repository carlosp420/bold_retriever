#!/usr/bin/env python

import xml.etree.ElementTree as ET
import sys
import requests
from Bio import SeqIO

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
        for match in root.findall('match'):
            similarity = match.find('similarity').text
            out['similarity'] = similarity
            tax_id = match.find('taxonomicidentification').text
            out['tax_id'] = tax_id
            break
    else:
        return None
    return out


def request_classification(obj):
    #obj['tax_id'] = "Morpho helenor"
    url = "http://www.boldsystems.org/index.php/API_Public/specimen/"
    payload = { 'taxon': obj['tax_id'], 'specimen_download': 'tsv' }
    r = requests.get(url, params=payload)
    if r.text != "":
        obj['classification'] = "true"
        tsv = r.text.split("\n")[1].split("\t")
        obj['class'] = tsv[11]
        obj['order'] = tsv[13]
        obj['family'] = tsv[15]
        return obj
    else:
        obj['classification'] = "false"
        return obj



if len(sys.argv) < 2:
    print "Error, you need to enter a FASTA file name as parameter"
    print "\n\tpython bold_retriever.py ZA2013.fasta"
    sys.exit()

f = sys.argv[1]

for seq_record in SeqIO.parse(f, "fasta"):
    out = "seq_id,similarity,taxon,class,order,family\n"

    obj = request_id(seq_record.seq, seq_record.id)
    if obj != None:
        obj = request_classification(obj)
        out += obj['id'] + "," + obj['similarity'] + "," + obj['tax_id'] + ","
        if obj['classification'] == "true":
            out += obj['class'] + "," + obj['order'] + "," + obj['family'] + "\n"
        else:
            out += "None,None,None\n"
    print out

