import os
import unittest

from tools.grits_consumer import GritsConsumer

_SCRIPT_DIR = os.path.dirname(__file__)

class TestGritsConsumer(unittest.TestCase):
    def setUp(self):
        self.cmd = GritsConsumer()
        self.validFile = open(os.path.join(_SCRIPT_DIR, 'data/GlobalDirectsSample_20150728.csv'))
        self.invalidFile = open(os.path.join(_SCRIPT_DIR, 'data/GlobalDirectsSample_20150728.txt'))

    def test_is_valid_extension(self):
        self.assertEqual(True, self.cmd.is_valid_file_type(self.validFile))

    def test_is_invalid_extension(self):
        self.assertEqual(False, self.cmd.is_valid_file_type(self.invalidFile))
