import os
import unittest

import requests

from bold_retriever import bold_retriever as br


class TestBoldRetriever(unittest.TestCase):

    def setUp(self):
        self.db = "COX1_L640bp"

    def test_parse_bold_xml1(self):
        # normal request
        r = requests.get(
            url="http://boldsystems.org/index.php/Ids_xml",
            params={
                'db': 'COX1_L640bp',
                'sequence': 'AAAGAATTTTAATTCGAGCTGAATTAAGTCAACCAGGAATATTTAT'
                            'TGGAAATGACCAAATTTATAACGTAATTGTTACAGCTCATGCTTTT'
                            'ATTATAATTttttttATAGTAATACCTATTATAATT',
            }
        )
        request = r.text
        seq_object = 'AAAGAATTTTAATTCGAGCTGAATTAAGTCAACCAGGAATATTTATTGGAAAT' \
                     'GACCAAATTTATAACGTAATTGTTACAGCTCATGCTTTTATTATAATTttttt' \
                     'tATAGTAATACCTATTATAATT'
        id = 'IonX17_rvr_ZA2013-0055_HochstetterForland_28_7_2013_10_21_San' \
             'derling_juvenile_98;size=2'
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
        seq_object = 'AAAGAATTTTAATTCGAGCTGAATTAAGTCAACCAGGAATATTTATTGGAAAT' \
                     'GACCAAATTTATAACGTAATTGTTACAGCTCATGCTTTTATTATAATTttttt' \
                     'tATAGTAATACCTATTATAATT'
        id = 'IonX17_rvr_ZA2013-0055_HochstetterForland_28_7_2013_10_21_San' \
             'derling_juvenile_98;size=2'
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
        seq_object = 'AAAGAATTTTAATTCGAGCTGAATTAAGTCAACCAGGAATATTTATTGGAAAT' \
                     'GACCAAATTTATAACGTAATTGTTACAGCTCATGCTTTTATTATAATTttttt' \
                     'tATAGTAATACCTATTATAATT'
        id = 'IonX17_rvr_ZA2013-0055_HochstetterForland_28_7_2013_10_21_San' \
             'derling_juvenile_98;size=2'
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
        seq_object = 'AAAGAATTTTAATTCGAGCTGAATTAAGTCAACCAGGAATATTTATTGGAAAT' \
                     'GACCAAATTTATAACGTAATTGTTACAGCTCATGCTTTTATTATAATTttttt' \
                     'tATAGTAATACCTATTATAATT'
        id = 'IonX17_rvr_ZA2013-0055_HochstetterForland_28_7_2013_10_21_San' \
             'derling_juvenile_98;size=2'
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
        seq_object = 'AAAGAATTTTAATTCGAGCTGAATTAAGTCAACCAGGAATATTTATTGGAAAT' \
                     'GACCAAATTTATAACGTAATTGTTACAGCTCATGCTTTTATTATAATTttttt' \
                     'tATAGTAATACCTATTATAATT'
        id = 'IonX17_rvr_ZA2013-0055_HochstetterForland_28_7_2013_10_21_San' \
             'derling_juvenile_98;size=2'
        all_ids = []
        taxon_list = []

        # get only taxon_list
        results = br.parse_bold_xml(request, seq_object, id, all_ids,
                                    taxon_list)[1]
        expected = []
        self.assertEqual(results, expected)

    def test_create_output_file(self):
        result = br.create_output_file("my_fasta_file.fas", "output-contents")
        expected = "my_fasta_file.fas_output.csv"
        self.assertEqual(result, expected)

    def test_create_output_file2(self):
        expected = "my_fasta_file.fas_output.csv"
        if os.path.isfile(expected):
            os.remove(expected)
        br.create_output_file("my_fasta_file.fas", "output-contents")
        self.assertTrue(os.path.isfile(expected))

    def test_process_classification(self):
        obj = {
            'classification': 'true',
            'class': 'Insecta',
            'order': 'Lepidoptera',
            'family': 'Nymphalidae',
        }
        expected = "Insecta,Lepidoptera,Nymphalidae,\n"
        result = br.process_classification(obj)
        self.assertEqual(expected, result)

    def test_process_classification_class_none(self):
        obj = {
            'classification': 'true',
        }
        expected = "None,None,None,\n"
        result = br.process_classification(obj)
        self.assertEqual(expected, result)

    def test_process_classification_false(self):
        obj = {
            'classification': 'false',
        }
        expected = "None,None,None\n"
        result = br.process_classification(obj)
        self.assertEqual(expected, result)

    def test_generate_output_content_for_file(self):
        fasta_file = os.path.join(
            os.path.abspath(os.path.dirname(__file__)),
            'ionx13.fas',
        )
        result = br.generate_output_content_for_file(
            fasta_file,
            'COX1_SPECIES',
        )
        expected = "FIPSO166-14,ionx13,0.9796,Finland,animal,Psocoptera,Ins" \
                   "ecta,Psocoptera,None,"
        self.assertEqual(expected, result.split('\n')[0])


if __name__ == "__main__":
    runner = unittest.TextTestRunner(verbosity=2)
    unittest.main(testRunner=runner)
