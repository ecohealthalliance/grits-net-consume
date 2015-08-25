import os
import unittest

from tools.grits_record import Record, FlightRecord, AirportRecord
from tools.grits_record import InvalidRecordProperty, InvalidRecordLength

_SCRIPT_DIR = os.path.dirname(__file__)

class TestGritsRecord(unittest.TestCase):
    def setUp(self):
        self.row = [u'1', u'2', u'3', u'4']
        self.obj = Record()

    def test_create_without_headers(self):
        self.assertRaises(InvalidRecordProperty, self.obj.create, self.row)
    
    def test_validate_empty(self):
        self.assertRaises(InvalidRecordLength, self.obj.validate_required)
    
    def test_to_json_empty(self):
        self.assertEqual("{}", self.obj.to_json())

class TestGritsFlightRecord(unittest.TestCase):
    def setUp(self):
        self.headers = [u'Date', u'Mktg Al', u'Alliance', u'Op Al', u'Orig',
                        u'Dest', u'Miles', u'Flight', u'Stops', u'Equip',
                        u'Seats', u'Dep Term', u'Arr Term', u'Dep Time',
                        u'Arr Time', u'Block Mins', u'Arr Flag', u'Orig WAC',
                        u'Dest WAC', u'Op Days', u'Ops/Week', u'Seats/Week']
        self.row = [u'Jun 2015', u'W3', u'None', u'W3', u'LOS', u'JFK',
                    u'5,250', u'107', u'0', u'332', u'251', u'I ', u'4 ',
                    u'2330', u'0550', u'680', u'1', u'555', u'22', u'..3.5.7',
                    u'3', u'753']
        self.valid_obj = FlightRecord(self.headers)
        self.invalid_obj = FlightRecord(None)
    
    def test_create_invalid_obj(self):
        self.assertRaises(InvalidRecordProperty, self.invalid_obj.create, self.row)
    
    def test_validate_invalid_obj(self):
        self.assertRaises(InvalidRecordLength, self.invalid_obj.validate_required)
    
    def test_create_valid_obj(self):
        self.valid_obj.create(self.row)
        self.assertEqual(self.row, self.valid_obj.fields.values())
    
    def test_create_valid_obj_invalid_row(self):
        row = []
        self.assertRaises(InvalidRecordLength, self.valid_obj.create, row)
    
class TestGritsAirportRecord(unittest.TestCase):
    def setUp(self):
        self.headers = [u'Code', u'Name', u'City', u'State', u'State Name',
                        u'Latitude', u'Longitude', u'Country', u'Country Name',
                        u'Global Region', u'WAC', u'Notes']
        self.row = [u'AAA', u'Anaa', u'Anaa', u'', u'', u'-17.351700',
                    u'-145.497800', u'PF', u'French Polynesia', u'Australasia',
                    u'823', u'']
        self.valid_obj = AirportRecord(self.headers)
        self.invalid_obj = AirportRecord(None)
    
    def test_create_invalid_obj(self):
        self.assertRaises(InvalidRecordProperty, self.invalid_obj.create, self.row)
    
    def test_validate_invalid_obj(self):
        self.assertRaises(InvalidRecordLength, self.invalid_obj.validate_required)
    
    def test_create_valid_obj_valid_row(self):
        self.valid_obj.create(self.row)
        self.assertEqual(self.row, self.valid_obj.fields.values())
    
    def test_create_valid_obj_invalid_row(self):
        row = []
        self.assertRaises(InvalidRecordLength, self.valid_obj.create, row)
    
    def test_create_valid_obj_vaidate_required(self):
        self.valid_obj.create(self.row)
        self.assertEqual(True, self.valid_obj.validate_required())
    