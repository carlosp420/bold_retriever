import unittest

from bold_retriever import bold_retriever as br


class CmdlineTest(unittest.TestCase):

    def setUp(self):
        self.parser = br.create_parser()

    # User does not enter any argument
    def test_cmdline_emtpy_args(self):
        with self.assertRaises(SystemExit):
            self.parser.parse_args([])

    # User enters only one argument
    def test_cmdline_file(self):
        with self.assertRaises(SystemExit):
            self.parser.parse_args(['-f', 'ionx23b.fas'])

    # User enters both arguments
    def test_cmdline(self):
        args = self.parser.parse_args(['-f', 'ionx23b.fas', '-db', 'COX1'])
        expected = 'COX1'
        self.assertEqual(expected, args.db)
