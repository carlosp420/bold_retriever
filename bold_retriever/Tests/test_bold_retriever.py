import os
import unittest

from Bio import SeqIO

from bold_retriever import bold_retriever as br


class TestBoldRetriever(unittest.TestCase):

    def test_request_id(self):
        filename = "ionx17.fas"
        for seq_record in SeqIO.parse(filename, "fasta"):
            seq = str(seq_record.seq)

        results = br.request_id(seq, seq_record.id)
        results = results[0]['tax_id']
        self.assertEqual(results, 'Aedes nigripes')

    def test_taxon_search(self):
        obj = {}
        obj['tax_id'] = "Ormosia"
        results = br.taxon_search(obj)
        self.assertEqual(results, '297370')

    def test_taxon_data(self):
        taxID = '297370'
        obj = {}
        obj['class'] = 'Insecta'
        obj['order'] = 'Diptera'
        obj['family'] = 'Limoniidae'
        obj['classification']  = 'true'
        results = br.taxon_data(taxID)
        self.assertEqual(results, obj)

if __name__ == "__main__":
    runner = unittest.TextTestRunner(verbosity = 2)
    unittest.main(testRunner=runner)
