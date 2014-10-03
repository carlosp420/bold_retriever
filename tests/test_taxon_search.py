import unittest

from bold_retriever import bold_retriever as br


class TestBoldRetriever(unittest.TestCase):

    def setUp(self):
        self.db = "COX1_L640bp"

    def test_taxon_search1(self):
        obj = {'tax_id': 'Ormosia'}
        results = br.taxon_search(obj)
        self.assertEqual(results['division'], 'animal')
        self.assertEqual(results['taxID'], '297370')

    def test_taxon_search2(self):
        # when it is not an animal
        obj = {'tax_id': 'Pythium'}
        results = br.taxon_search(obj)
        self.assertEqual(results['division'], 'not animal')
        self.assertEqual(results['taxID'], '23732')

    def test_taxon_search_tax_id_is_list(self):
        obj = {'tax_id': 'Pythium acrogynum'}
        results = br.taxon_search(obj)
        self.assertEqual(results['division'], 'not animal')
        self.assertEqual(results['taxID'], '23732')


if __name__ == "__main__":
    runner = unittest.TextTestRunner(verbosity=2)
    unittest.main(testRunner=runner)
