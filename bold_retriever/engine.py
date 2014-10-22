import xml.etree.ElementTree as ET


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