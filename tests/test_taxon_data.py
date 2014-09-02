import unittest

from bold_retriever import bold_retriever as br


class TestBoldRetriever(unittest.TestCase):

    def test_taxon_data(self):
        taxID = '297370'
        obj = {'division': 'animal', 'taxID': taxID}
        obj['class'] = 'Insecta'
        obj['order'] = 'Diptera'
        obj['family'] = 'Limoniidae'
        obj['classification'] = 'true'
        results = br.taxon_data(obj)
        self.assertEqual(results, obj)

    def test_taxon_data_returns_false(self):
        taxID = '29737001928929'
        obj = {'classification': 'false', 'taxID': taxID}
        results = br.taxon_data(obj)
        self.assertEqual(results['classification'], 'false')


if __name__ == "__main__":
    runner = unittest.TextTestRunner(verbosity=2)
    unittest.main(testRunner=runner)
