import os
import unittest


from bold_retriever import bold_retriever as br


class TestGetTaxIDFromWeb(unittest.TestCase):

    #def setUp(self):

    def test_when_scrapping_taxon_name_is_fail(self):
        obj = {
            'bold_id': 'GMGRE1022-13',
        }
        expected = {
            'bold_id': 'GMGRE1022-13',
        }
        result = br.get_tax_id_from_web(obj)
        self.assertEqual(expected, result)

    def test_when_scrapping_taxon_name_is_not_fail(self):
        obj = {
            'bold_id': 'NEUFI079-11',
        }
        expected = {
            'bold_id': 'NEUFI079-11',
            'tax_id': 'Hemerobius pini',
        }
        result = br.get_tax_id_from_web(obj)
        self.assertEqual(expected, result)

    def test_when_scrapping_taxon_name_is_fail2(self):
        obj = {
            'bold_id': 'NEUFI079-11aaaaaaaaaaaaaaaaaaaaaa',
            }
        expected = {
            'bold_id': 'NEUFI079-11aaaaaaaaaaaaaaaaaaaaaa',
            }
        result = br.get_tax_id_from_web(obj)
        self.assertEqual(expected, result)
