import codecs
import json
import logging
import re
import xml.etree.ElementTree as ET

from bs4 import BeautifulSoup
import requests


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
        try:
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
        except ValueError as exc:
            logging.warning(exc)
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
                 'for BOLD record %s.' % obj['bold_id'])
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
        if genus_parent is None:
            return taxon
        elif genus_parent.endswith("nae"):
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
            try:
                if val['parentname']:
                    return val['parentname']
            except TypeError:
                logging.warning("BOLD returned uninformative JSON: " + "".join(req.text))
                return None


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


def get(url, payload):
    """Wrapper function for requests.get so we can use fake requests when
    writing unittests.
    :param url:
    :param params: payload
    :return: response object from requests.get
    """
    r = requests.get(url, params=payload)
    return r


def generate_output_content(all_ids, output_filename, seq_record):
    out = ""
    if all_ids is not None:
        for obj in all_ids:
            if 'tax_id' in obj:
                r = taxon_search(obj)

                if r is None:
                    continue
                obj['taxID'] = r['taxID']
                obj['division'] = r['division']
                # print "== obj", obj
                obj = taxon_data(obj)
                out += obj['id'] + ","
                out += obj['bold_id'] + ","
                out += obj['similarity'] + ","
                out += obj['division'] + ","
                out += process_classification(obj) + ","
                out += obj['tax_id'] + ","
                out += obj['collection_country']
                out += '\n'
        with codecs.open(output_filename, "a", "utf-8") as handle:
            handle.write(out)
    else:
        out = "nohit," + str(seq_record.id) + ","
        out += "nohit,nohit,nohit,nohit,nohit,nohit,nohit\n"
        with codecs.open(output_filename, "a", "utf-8") as handle:
            handle.write(out)


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
