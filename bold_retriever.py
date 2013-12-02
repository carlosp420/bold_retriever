#!/usr/bin/env python

import xml.etree.ElementTree as ET
import sys
import requests
from Bio import SeqIO

def request_id(seq_object, id):
    # input a sequence object
    # sends sequence to BOLD REST API for Identification Engine db=COX1_L640bp
    url = "http://boldsystems.org/index.php/Ids_xml"
    payload = { 'db': 'COX1_L640bp', 'sequence': str(seq_object) }
    r = requests.get(url, params=payload)
    if r.text != None:
        root = ET.fromstring(r.text)
        for child in root:
            if child.tag != None:
                print id


if len(sys.argv) < 2:
    print "Error, you need to enter a FASTA file name as parameter"
    print "\n\tpython bold_retriever.py ZA2013.fasta"
    sys.exit()

f = sys.argv[1]

for seq_record in SeqIO.parse(f, "fasta"):
    print request_id(seq_record.seq, seq_record.id)

