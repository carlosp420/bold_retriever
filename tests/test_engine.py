from twisted.trial import unittest
from twisted.web.error import Error

from bold_retriever import engine


class TestEngine(unittest.TestCase):

    def setUp(self):
        self.db = "COX1_L640bp"

    def test_get_tax_id_from_web_1(self):
        # test_when_scrapping_taxon_name_is_fail
        obj = {
            'bold_id': 'GMGRE1022-13',
        }
        expected = {
            'bold_id': 'GMGRE1022-13',
        }
        result = engine.get_tax_id_from_web(obj)
        self.assertEqual(expected, result)

    """
    def test_get_tax_id_from_web_2(self):
        # test_when_scrapping_taxon_name_is_not_fail
        obj = {
            'bold_id': 'NEUFI079-11',
        }
        expected = {
            'bold_id': 'NEUFI079-11',
            'tax_id': u'Hemerobius pini',
            'family': 'Hemerobiidae',
        }
        try:
            result = engine.get_tax_id_from_web(obj)
        except Error, exc:
            print(exc)
        reactor.callFromThread(reactor.stop)
        reactor.run()
        self.assertEqual(expected, result)
    """

    def test_get_tax_id_from_web_3(self):
        # test_when_scrapping_taxon_name_is_fail
        obj = {
            'bold_id': 'NEUFI079-11aaaaaaaaaaaaaaaaaaaaaa',
        }
        expected = {
            'bold_id': 'NEUFI079-11aaaaaaaaaaaaaaaaaaaaaa',
        }
        result = engine.get_tax_id_from_web(obj)
        self.assertEqual(expected, result)

    """
    def test_get_tax_id_from_web_4(self):
        # test_when_scrapping_taxon_name_is_fail
        obj = {
            'bold_id': 'GRAFW1731-12',
        }
        expected = {
            'bold_id': 'GRAFW1731-12',
            'tax_id': 'Cryptinae sp.',
            'family': 'Ichneumonidae',
        }
        result = engine.get_tax_id_from_web(obj)
        self.assertEqual(expected, result)
    """

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

    def test_get_family_name_for_taxon1(self):
        tax_id = 'Hemerobiidae'
        expected = 'Hemerobiidae'
        try:
            result = engine.get_family_name_for_taxon(tax_id)
        except Error as exc:
            print(exc)
        self.assertEqual(expected, result)

    """
    def test_get_family_name_for_taxon2(self):
        tax_id='Hemerobiinae'
        expected='Hemerobiidae'
        try:
            result = engine.get_family_name_for_taxon(tax_id)
        except Error, exc:
            print(exc)
        reactor.callFromThread(reactor.stop)
        reactor.run()
        self.assertEqual(expected, result)

        def tearDown(self):
            print("teardown()")

    def test_get_family_name_for_taxon3(self):
        def this_run(tax_id):
            result = engine.get_family_name_for_taxon(tax_id)
            self.assertEqual(expected, result)

        tax_id = 'Hemerobius pini'
        expected = 'Hemerobiidae'
        commands = [(this_run, [tax_id], {})]
        threads.callMultipleInThread(commands)
        reactor.run()
    """

    def test_process_classification(self):
        obj = {
            'classification': 'true',
            'class': 'Insecta',
            'order': 'Lepidoptera',
            'family': 'Nymphalidae',
            }
        expected = "Insecta,Lepidoptera,Nymphalidae"
        result = engine.process_classification(obj)
        self.assertEqual(expected, result)

    def test_process_classification_class_none(self):
        obj = {
            'classification': 'true',
            }
        expected = "None,None,None"
        result = engine.process_classification(obj)
        self.assertEqual(expected, result)

    def test_process_classification_false(self):
        obj = {
            'classification': 'false',
            }
        expected = "None,None,None"
        result = engine.process_classification(obj)
        self.assertEqual(expected, result)
