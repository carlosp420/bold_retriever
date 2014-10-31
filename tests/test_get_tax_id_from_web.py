from bold_retriever import engine
from twisted.internet import reactor, threads, defer
from twisted.trial import unittest
from twisted.web.error import Error


class TestGetTaxIDFromWeb(unittest.TestCase):



    def test_get_parentname(self):
        taxon = "Pardosa"
        expected = "Lycosidae"
        result = engine.get_parentname(taxon)
        self.assertEqual(expected, result)

        taxon = "Hemerobiinae"
        expected = "Hemerobiidae"
        result = engine.get_parentname(taxon)
        self.assertEqual(expected, result)

        taxon = "Pardosaaaaaaaaaaa"
        expected = None
        result = engine.get_parentname(taxon)
        self.assertEqual(expected, result)
