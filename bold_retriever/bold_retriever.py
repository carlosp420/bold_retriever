import xml.etree.ElementTree as ET
import requests
from Bio import SeqIO
import json
import codecs


def request_id(seq_object, id):
    # input a sequence object
    # sends sequence to BOLD REST API for Identification Engine db=COX1_L640bp
    # output a dictionary with the info
    all_ids = []
    taxon_list = []
    url = "http://boldsystems.org/index.php/Ids_xml"
    payload = { 'db': 'COX1_L640bp', 'sequence': str(seq_object) }
    r = requests.get(url, params=payload)
    if r.text != None:
        root = ET.fromstring(r.text)
        #print r.text
        for match in root.findall('match'):
            out = {}
            out['seq'] = str(seq_object)
            out['id'] = str(id)
            similarity = match.find('similarity').text
            out['similarity'] = similarity
            tax_id = match.find('taxonomicidentification').text
            out['tax_id'] = tax_id

            myid = match.find('ID').text
            out['bold_id'] = myid
            if not out['tax_id'] in taxon_list:
                taxon_list.append(out['tax_id'])
                all_ids.append(out)
    else:
        return None
    for i in all_ids:
        print i['tax_id'], i['similarity']
    return all_ids


def request_classification(obj):
    #obj['tax_id'] = "Morpho helenor"
    tax_id = obj['tax_id'].split(" ")
    if len(tax_id) > 1:
        tax_id = tax_id[0]
    url = "http://www.boldsystems.org/index.php/API_Tax/TaxonSearch/"
    print "i am sending this %s" % tax_id
    payload = {
            'taxName': tax_id,
            'fuzzy': 'true',
            }
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



def main():
    """
    if len(sys.argv) < 2:
        print "Error, you need to enter a FASTA file name as parameter"
        print "\n\tpython bold_retriever.py ZA2013.fasta"
        sys.exit()
    
    f = sys.argv[1]
    """
    
    out = "bold_id,seq_id,similarity,taxon,class,order,family\n"
    output_filename = f.strip() + "_output.csv"
    myfile = codecs.open(output_filename, "w", "utf-8")
    myfile.write(out)
    myfile.close()
    for seq_record in SeqIO.parse(f, "fasta"):
        out = ""
        all_ids = request_id(seq_record.seq, seq_record.id)
        for obj in all_ids:
            if 'tax_id' in obj:
                obj = request_classification(obj)
                out += obj['bold_id'] + ","
                out += obj['id'] + "," + obj['similarity'] + "," + obj['tax_id'] + ","
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
        myfile = codecs.open(output_filename, "a", "utf-8")
        myfile.write(out)
        myfile.close()
    

if __name__ == "__main__":
    main()
