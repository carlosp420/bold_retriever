from twisted.trial import unittest
from twisted.web.error import Error

import engine


class TestEngine(unittest.TestCase):

    def setUp(self):
        self.db = "COX1_L640bp"

    def test_parse_id_engine_xml(self):
        with open("tests/Data/id_engine.xml", "r") as handle:
            data = handle.read()
        result = engine.parse_id_engine_xml(data)
        self.assertIn("SAMOS029-09", result[0]["ID"])
        self.assertEqual("COI-5P", result[0]["sequencedescription"])
