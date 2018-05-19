import codecs
import csv
from typing import List, Dict
import xml.etree.ElementTree as ET

from Bio.SeqIO import SeqRecord


HEADERS = [
    "ID", "OtuID", "BIN", "tax_id", "sequencedescription", "database", "citation",
    "taxonomicidentification", "similarity", "url", "country", "lat", "lon",
    "phylum", "class", "order", "family", "subfamily", "tribe", "genus", "species",
]


def generate_output_content(all_ids: List[Dict[str, str]], output_filename: str,
                            seq_record: SeqRecord):
    if all_ids:
        with open(output_filename, "a") as handle:
            csv_writer = csv.DictWriter(handle, fieldnames=HEADERS)
            for item in all_ids:
                del item["seq_record"]
                csv_writer.writerow(item)
    else:
        out = {"OtuID": seq_record.id}
        for header in HEADERS:
            if header not in out:
                out[header] = "nohit"
        with open(output_filename, "a") as handle:
            csv_writer = csv.DictWriter(handle, fieldnames=HEADERS)
            csv_writer.writerow(out)


def parse_id_engine_xml(xml: str) -> List[Dict[str, str]]:
    try:
        root = ET.fromstring(xml)
    except ET.ParseError as error:
        print("\n>> Error got malformed XML from BOLD: " + str(error))
    except TypeError as error:
        print("\n>> Error got malformed XML from BOLD: " + str(error))

    identifications = []

    for match in root.findall('match'):
        identification = dict()
        for element in match:
            if element.tag == "specimen":
                for element_child in element:
                    if element_child.tag == "collectionlocation":
                        for collection in element_child:
                            if collection.tag == "coord":
                                for coord in collection:
                                    identification[coord.tag] = coord.text
                            else:
                                identification[collection.tag] = collection.text
                    else:
                        identification[element_child.tag] = element_child.text
            else:
                identification[element.tag] = element.text
        identifications.append(identification)

    return identifications
