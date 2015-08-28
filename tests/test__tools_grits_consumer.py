import os
import unittest

from tools.grits_consumer import GritsConsumer

_SCRIPT_DIR = os.path.dirname(__file__)

class TestGritsConsumer(unittest.TestCase):
    def setUp(self):
        self.cmd = GritsConsumer()
        self.validFile = open(os.path.join(_SCRIPT_DIR, 'data/Schedule_Weekly_Extract_Report.tsv'))
        self.invalidFile = open(os.path.join(_SCRIPT_DIR, 'data/Schedule_Weekly_Extract_Report.csv'))

    def test_is_valid_extension(self):
        self.assertEqual(True, self.cmd.is_valid_file_type(self.validFile))
    
    def test_is_invalid_extension(self):
        self.assertEqual(False, self.cmd.is_valid_file_type(self.invalidFile))