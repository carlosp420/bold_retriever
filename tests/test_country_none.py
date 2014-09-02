import unittest
import requests

from bold_retriever import bold_retriever as br


class TestBoldRetriever(unittest.TestCase):

    def setUp(self):
        self.db = "COX1_L640bp"

    def test_parse_bold_xml_country_none(self):
        # normal request
        seq_object = "AGCCTGAGCTGGAATAGTTGGTACTTCGTTAAGTATTATAATTCGAGCTGAATT" \
                     "AGGACACCCCGGTGCTTTAATTGGTGATGACCAAATTTATAATGTAATTGTTAC" \
                     "TGCTCATGCTTTTATTATAATTttttttATAGTAATACCTATTATAATTGGA"
        r = requests.get(
            url="http://boldsystems.org/index.php/Ids_xml",
            params={'db': 'COX1_L640bp', 'sequence': seq_object}
        )
        request = r.text
        id = "random_id"
        all_ids = []
        taxon_list = []

        all_ids, taxon_list = br.parse_bold_xml(request, seq_object, id,
                                                all_ids,
                                                taxon_list,
                                                )
        for i in all_ids:
            if i['tax_id'] == 'Nemorimyza posticata':
                results = i['collection_country']
        expected = 'None'
        self.assertEqual(results, expected)


if __name__ == "__main__":
    runner = unittest.TextTestRunner(verbosity=2)
    unittest.main(testRunner=runner)
