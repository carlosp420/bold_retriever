import os
import subprocess
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

    def test_cmdline_main(self):
        cwd = os.path.abspath(os.path.dirname(__file__))
        bold_retriever = os.path.join(cwd, '..', 'bold_retriever',
                                      'bold_retriever.py')
        print(bold_retriever)
        cmd = "python " + bold_retriever + " -f " + os.path.join(cwd,
                                                                 'otu99.fas')
        cmd += " -db COX1_SPECIES"
        p = subprocess.check_call(cmd, shell=True)
        self.assertEqual(0, p)

    def test_get_args(self):
        args = self.parser.parse_args(['-f', 'ionx13.fas', '-db', 'COX1'])
        f, db = br.get_args(args)
        self.assertEqual(f, 'ionx13.fas')
        self.assertEqual(db, 'COX1')

    def test_get_started(self):
        test_folder = os.path.abspath(os.path.dirname(__file__))
        input_file = os.path.join(test_folder, 'ionx13.fas')
        result_file = os.path.join(test_folder, 'ionx13.fas_output.csv')

        args = self.parser.parse_args(['-f', input_file, '-db', 'COX1'])
        br.get_started(args)

        self.assertTrue(os.path.isfile(result_file))

    def test_otu99(self):
        """It should pass despite returning empty list for classification."""
        test_folder = os.path.abspath(os.path.dirname(__file__))
        input_file = os.path.join(test_folder, 'otu99.fas')
        args = self.parser.parse_args(['-f', input_file, '-db',
                                       'COX1_SPECIES'])
        br.get_started(args)
        result_file = os.path.join(test_folder, 'otu99.fas_output.csv')
        self.assertTrue(os.path.isfile(result_file))

    def test_insecta(self):
        """It should pass despite returning empty list for classification."""
        test_folder = os.path.abspath(os.path.dirname(__file__))
        input_file = os.path.join(test_folder, 'otu_insecta.fas')
        args = self.parser.parse_args(['-f', input_file, '-db',
                                       'COX1_SPECIES'])
        br.get_started(args)
        result_file = os.path.join(test_folder, 'otu_insecta.fas_output.csv')
        self.assertTrue(os.path.isfile(result_file))
