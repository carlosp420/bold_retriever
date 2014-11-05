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
            'tax_id': u'Hemerobius pini',
            'family': 'Hemerobiidae',
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

    def test_when_scrapping_taxon_name_is_fail3(self):
        obj = {
            'bold_id': 'GRAFW1731-12',
        }
        expected = {
            'bold_id': 'GRAFW1731-12',
            'tax_id': 'Cryptinae sp.',
            'family': 'Ichneumonidae',
        }
        result = br.get_tax_id_from_web(obj)
        self.assertEqual(expected, result)

    def test_get_family_name_for_taxon(self):
        tax_id = 'Hemerobiidae'
        expected = 'Hemerobiidae'
        result = br.get_family_name_for_taxon(tax_id)
        self.assertEqual(expected, result)

        tax_id = 'Hemerobiinae'
        expected = 'Hemerobiidae'
        result = br.get_family_name_for_taxon(tax_id)
        self.assertEqual(expected, result)

        tax_id = 'Hemerobius pini'
        expected = 'Hemerobiidae'
        result = br.get_family_name_for_taxon(tax_id)
        self.assertEqual(expected, result)


    def test_get_parentname(self):
        taxon = "Pardosa"
        expected = "Lycosidae"
        result = br.get_parentname(taxon)
        self.assertEqual(expected, result)

        taxon = "Hemerobiinae"
        expected = "Hemerobiidae"
        result = br.get_parentname(taxon)
        self.assertEqual(expected, result)

        taxon = "Pardosaaaaaaaaaaa"
        expected = None
        result = br.get_parentname(taxon)
        self.assertEqual(expected, result)
