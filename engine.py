import codecs
import csv
from typing import List, Dict
import xml.etree.ElementTree as ET

from Bio.SeqIO import SeqRecord


def generate_output_content(all_ids: List[Dict[str, str]], output_filename: str,
                            seq_record: SeqRecord):
    if all_ids:
        headers = all_ids[0].keys()
        with open(output_filename, "w") as handle:
            csv_writer = csv.DictWriter(handle, fieldnames=headers)
            csv_writer.writeheader()
            for item in all_ids:
                csv_writer.writerow(item)
    else:
        out = "nohit," + str(seq_record.id) + ","
        out += "nohit,nohit,nohit,nohit,nohit,nohit,nohit\n"
        with codecs.open(output_filename, "a", "utf-8") as handle:
            handle.write(out)


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
