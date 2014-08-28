import unittest
import requests

from Bio import SeqIO

from bold_retriever import bold_retriever as br


class TestBoldRetriever(unittest.TestCase):

    def setUp(self):
        self.db = "COX1_L640bp"

    def test_request_id(self):
        filename = "ionx17.fas"
        for seq_record in SeqIO.parse(filename, "fasta"):
            seq = str(seq_record.seq)

        results = br.request_id(seq, seq_record.id, self.db)
        results = results[0]
        expected = {
                'bold_id': 'SAMOS029-09',
                'collection_country': 'Canada',
                'seq': 'AAAGAATTTTAATTCGAGCTGAATTAAGTCAACCAGGAATATTTATTGGAAATGACCAAATTTATAACGTAATTGTTACAGCTCATGCTTTTATTATAATTttttttATAGTAATACCTATTATAATT',
                'similarity': '1',
                'tax_id': 'Diptera',
                'id': 'IonX17_rvr_ZA2013-0055_HochstetterForland_28_7_2013_10_21_Sanderling_juvenile_98;size=2',
        }
        self.assertEqual(results, expected)

    def test_parse_bold_xml1(self):
        # normal request
        r = requests.get(
            url="http://boldsystems.org/index.php/Ids_xml",
            params={
                'db': 'COX1_L640bp',
                'sequence': 'AAAGAATTTTAATTCGAGCTGAATTAAGTCAACCAGGAATATTTATTGGAAATGACCAAATTTATAACGTAATTGTTACAGCTCATGCTTTTATTATAATTttttttATAGTAATACCTATTATAATT',
            }
        )
        request = r.text
        seq_object = 'AAAGAATTTTAATTCGAGCTGAATTAAGTCAACCAGGAATATTTATTGGAAATGACCAAATTTATAACGTAATTGTTACAGCTCATGCTTTTATTATAATTttttttATAGTAATACCTATTATAATT'
        id = 'IonX17_rvr_ZA2013-0055_HochstetterForland_28_7_2013_10_21_Sanderling_juvenile_98;size=2'
        all_ids = []
        taxon_list = []

        # get only taxon_list
        results = br.parse_bold_xml(request, seq_object, id, all_ids,
                                    taxon_list)[1]
        expected = ['Diptera', 'Culicidae', 'Ochlerotatus impiger']
        self.assertEqual(results, expected)

    def test_parse_bold_xml2(self):
        # malformed XML returned from BOLD
        request = []
        seq_object = 'AAAGAATTTTAATTCGAGCTGAATTAAGTCAACCAGGAATATTTATTGGAAATGACCAAATTTATAACGTAATTGTTACAGCTCATGCTTTTATTATAATTttttttATAGTAATACCTATTATAATT'
        id = 'IonX17_rvr_ZA2013-0055_HochstetterForland_28_7_2013_10_21_Sanderling_juvenile_98;size=2'
        all_ids = []
        taxon_list = []

        # get only taxon_list
        results = br.parse_bold_xml(request, seq_object, id, all_ids,
                                    taxon_list)[1]
        expected = []
        self.assertEqual(results, expected)

    def test_parse_bold_xml3(self):
        # malformed XML returned from BOLD
        request = None
        seq_object = 'AAAGAATTTTAATTCGAGCTGAATTAAGTCAACCAGGAATATTTATTGGAAATGACCAAATTTATAACGTAATTGTTACAGCTCATGCTTTTATTATAATTttttttATAGTAATACCTATTATAATT'
        id = 'IonX17_rvr_ZA2013-0055_HochstetterForland_28_7_2013_10_21_Sanderling_juvenile_98;size=2'
        all_ids = []
        taxon_list = []

        # get only taxon_list
        results = br.parse_bold_xml(request, seq_object, id, all_ids,
                                    taxon_list)[1]
        expected = []
        self.assertEqual(results, expected)

    def test_parse_bold_xml4(self):
        # malformed XML returned from BOLD
        request = "TEXT"
        seq_object = 'AAAGAATTTTAATTCGAGCTGAATTAAGTCAACCAGGAATATTTATTGGAAATGACCAAATTTATAACGTAATTGTTACAGCTCATGCTTTTATTATAATTttttttATAGTAATACCTATTATAATT'
        id = 'IonX17_rvr_ZA2013-0055_HochstetterForland_28_7_2013_10_21_Sanderling_juvenile_98;size=2'
        all_ids = []
        taxon_list = []

        # get only taxon_list
        results = br.parse_bold_xml(request, seq_object, id, all_ids,
                                    taxon_list)[1]
        expected = []
        self.assertEqual(results, expected)

    def test_parse_bold_xml5(self):
        # malformed XML returned from BOLD
        request = """<?xml version="1.0" encoding="UTF-8"?>
                     <!-- Edited by XMLSpy -->
                     <note>
                        <to>Tove</to>
                        <from>Jani</from>
                        <heading>Reminder</heading>
                        <body>Don't forget me this weekend!</body>
                     </note>
                  """
        seq_object = 'AAAGAATTTTAATTCGAGCTGAATTAAGTCAACCAGGAATATTTATTGGAAATGACCAAATTTATAACGTAATTGTTACAGCTCATGCTTTTATTATAATTttttttATAGTAATACCTATTATAATT'
        id = 'IonX17_rvr_ZA2013-0055_HochstetterForland_28_7_2013_10_21_Sanderling_juvenile_98;size=2'
        all_ids = []
        taxon_list = []

        # get only taxon_list
        results = br.parse_bold_xml(request, seq_object, id, all_ids,
                                    taxon_list)[1]
        expected = []
        self.assertEqual(results, expected)

    def test_taxon_search1(self):
        obj = {}
        obj['tax_id'] = "Ormosia"
        results = br.taxon_search(obj)
        self.assertEqual(results['division'], 'animal')
        self.assertEqual(results['taxID'], '297370')

    def test_taxon_search2(self):
        # when it is not an animal
        obj = {}
        obj['tax_id'] = "Pythium"
        results = br.taxon_search(obj)
        self.assertEqual(results['division'], 'not animal')
        self.assertEqual(results['taxID'], '23732')

    def test_taxon_data(self):
        taxID = '297370'
        obj = {'division': 'animal', 'taxID': taxID}
        obj['class'] = 'Insecta'
        obj['order'] = 'Diptera'
        obj['family'] = 'Limoniidae'
        obj['classification'] = 'true'
        results = br.taxon_data(obj)
        self.assertEqual(results, obj)

        taxID = '23732'
        obj = {'division': 'not animal', 'taxID': taxID}
        results = br.taxon_data(obj)
        print "\nthis results", results
        print "\nthis obj", obj
        self.assertEqual(results['family'], obj['family'])


if __name__ == "__main__":
    runner = unittest.TextTestRunner(verbosity = 2)
    unittest.main(testRunner=runner)
