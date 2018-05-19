import codecs
import os
import json
import unittest
from unittest.mock import patch

from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord

import bold_retriever as br
import engine


TEST_FILE_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                              "Data")


class TestBoldRetriever(unittest.TestCase):

    def setUp(self):
        self.db = "COX1_L640bp"

    @patch("bold_retriever.requests.get")
    def test_get_bin(self, mock_get):
        with open(os.path.join(TEST_FILE_PATH, "bin.json"), "r") as handle:
            data = handle.read()

            mock_get.return_value.json.return_value = json.loads(data)
            result = br.get_bin("some taxon id")
            self.assertEqual("BOLD:AAA3750", result)

    def test_create_output_file(self):
        result = br.create_output_file("my_fasta_file.fas")
        expected = "my_fasta_file.fas_output.csv"
        self.assertEqual(result, expected)

    def test_create_output_file2(self):
        expected = "my_fasta_file.fas_output.csv"
        if os.path.isfile(expected):
            os.remove(expected)
        br.create_output_file("my_fasta_file.fas")
        self.assertTrue(os.path.isfile(expected))

    def test_generate_output_content(self):
        output_filename = 'ionx13.fas_output.csv'
        seq = Seq("AATTTGATCAGGTTTAGTAGGAACTAGATTAAGTTTATTAATTCGAGCCGAATTAGGTCAACCAGGTTCATTAATTGGAGATGACCAAATTTATAATGTAATCGTAACTGCTCATGCATTTATTATAATTTTCTTCATAGTTATACCTATTGTTATTGGA")
        seq_record = SeqRecord(seq)
        seq_record.id = 'ionx13'

        if os.path.isfile(output_filename):
            os.remove(output_filename)
        engine.generate_output_content(
            [{'similarity': '1', 'collection_country': 'Canada', 'bold_id': 'SIOCA145-10', 'id': 'ionx13', 'tax_id': 'Psocoptera'}],
            output_filename,
            seq_record,
        )
        result = codecs.open(output_filename, "r", "utf-8").readlines()[1]
        self.assertIn("ionx13", result.strip())
        self.assertIn("SIOCA145-10", result.strip())
        self.assertIn("Canada", result.strip())

    def tearDown(self):
        files = ["ionx13.fas_output.csv", "my_fasta_file.fas_output.csv"]
        for filename in files:
            if os.path.isfile(filename):
                os.remove(filename)


if __name__ == "__main__":
    runner = unittest.TextTestRunner(verbosity=2)
    unittest.main(testRunner=runner)
