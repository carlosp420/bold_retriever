import unittest
from twisted.internet import reactor

from bold_retriever import engine


class TestBoldRetriever(unittest.TestCase):

    def setUp(self):
        self.db = "COX1_L640bp"

    def test_taxon_search1(self):
        obj = {'tax_id': 'Ormosia'}
        results = engine.taxon_search(obj)
        self.assertEqual(results['division'], 'animal')

    def test_taxon_search2(self):
        obj = {'tax_id': 'Ormosia'}
        results = engine.taxon_search(obj)
        self.assertEqual(results['taxID'], '297370')

    def test_taxon_search3(self):
        # when it is not an animal
        obj = {'tax_id': 'Pythium'}
        results = engine.taxon_search(obj)
        self.assertEqual(results['division'], 'not animal')

    def test_taxon_search4(self):
        # when it is not an animal
        obj = {'tax_id': 'Pythium'}
        results = engine.taxon_search(obj)
        self.assertEqual(results['taxID'], '23732')

    def test_taxon_search_tax_id_is_list1(self):
        obj = {'tax_id': 'Pythium acrogynum'}
        results = engine.taxon_search(obj)
        self.assertEqual(results['division'], 'not animal')

    def test_taxon_search_tax_id_is_list2(self):
        obj = {'tax_id': 'Pythium acrogynum'}
        results = engine.taxon_search(obj)
        self.assertEqual(results['taxID'], '23732')
