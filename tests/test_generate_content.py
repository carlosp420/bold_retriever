import os
import unittest


from bold_retriever import bold_retriever as br


class TestGenerateContent(unittest.TestCase):

    def setUp(self):
        self.db = "COX1"

        this_path = os.path.abspath(os.path.dirname(__file__))
        self.filename = os.path.join(this_path, "otu_50.fas")
        self.output_filename = self.filename + "_output.csv"

    def test_generate_content(self):
        # test_headers
        expected = "seq_id,bold_id,similarity,division,class,order,family,species,collection_country\n"
        outputfile = br.create_output_file(self.filename)
        with open(outputfile, "r") as handle:
            results = handle.read()
        self.assertEqual(expected, results)

        results = br.generate_output_content_for_file(self.output_filename,
                                                      self.filename,
                                                      self.db)
        expected = 'Processed all sequences.'
        self.assertEqual(expected, results)

        with open(self.output_filename, "r") as handle:
            lines = handle.readlines()[1]
        expected = 'nohit,OTU_50'
        self.assertTrue(lines.startswith(expected))



if __name__ == "__main__":
    runner = unittest.TextTestRunner(verbosity=2)
    unittest.main(testRunner=runner)
