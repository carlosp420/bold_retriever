import subprocess
import inspect
import unittest
import os
from unipath import Path


class CmdlineTest(unittest.TestCase):

    def setUp(self):
        self.br_path = self.get_boldretriever_path()

    def get_boldretriever_path(self):
        cur_frame = inspect.currentframe()
        cur_file = inspect.getframeinfo(cur_frame)[0]
        br_path = Path(cur_file).ancestor(2)
        br_path = os.path.join(br_path, 'bold_retriever.py')
        return br_path

    def test_cmdline(self):
        self.assertEqual("", self.br_path)
