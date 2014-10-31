import codecs
import os

from Bio.SeqRecord import SeqRecord
from Bio.Seq import Seq
import requests
from twisted.trial import unittest
from twisted.internet import reactor, defer
from unipath import Path

from bold_retriever import engine


class TestBoldRetriever(unittest.TestCase):

    def setUp(self):
        self.db = "COX1_L640bp"

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
