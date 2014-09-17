import os
import unittest

from Bio import SeqIO

from bold_retriever import bold_retriever as br


class TestBoldRetriever(unittest.TestCase):

    def setUp(self):
        self.db = "COX1_L640bp"

        this_path = os.path.abspath(os.path.dirname(__file__))
        filename = os.path.join(this_path, "ionx17.fas")
        for seq_record in SeqIO.parse(filename, "fasta"):
            self.seq = str(seq_record.seq)
            self.id = str(seq_record.id)

    def test_request_id(self):
        results = br.request_id(self.seq, self.id, self.db)
        expected = {
            'bold_id': 'SAMOS029-09',
            'collection_country': 'Canada',
            'seq': 'AAAGAATTTTAATTCGAGCTGAATTAAGTCAACCAGGAATATTTATTGGAAATGA'
                   'CCAAATTTATAACGTAATTGTTACAGCTCATGCTTTTATTATAATTttttttATA'
                   'GTAATACCTATTATAATT',
            'similarity': '1',
            'tax_id': 'Diptera',
            'id': 'IonX17_rvr_ZA2013-0055_HochstetterForland_28_7_2013_'
                  '10_21_Sanderling_juvenile_98;size=2',
        }
        self.assertEqual(results[0], expected)

    def test_request_id_when_request_returns_none(self):
        results = br.request_id("", self.id, self.db)
        self.assertEqual(results, None)

    def test_request_id_when_request_returns_none2(self):
        results = br.request_id("", self.id, "", debug=True)
        self.assertEqual(results, None)

if __name__ == "__main__":
    runner = unittest.TextTestRunner(verbosity=2)
    unittest.main(testRunner=runner)
