import os
import unittest
import math

from tools.grits_record import Record, FlightRecord, AirportRecord
from tools.grits_record import InvalidRecordProperty, InvalidRecordLength

_SCRIPT_DIR = os.path.dirname(__file__)

class TestGritsRecord(unittest.TestCase):
    def setUp(self):
        self.obj = Record()
    
    def test_to_json_empty(self):
        self.assertEqual("{}", self.obj.to_json())
    
    def test_is_empty_string(self):
        self.assertEqual(True, Record.is_empty_str(""))
        self.assertEqual(True, Record.is_empty_str(u""))
        self.assertEqual(False, Record.is_empty_str(u"adfasdf"))
        self.assertEqual(False, Record.is_empty_str(1234123))
        self.assertEqual(False, Record.is_empty_str(None))
    
    def test_could_be_boolean(self):
        self.assertEqual(True, Record.could_be_boolean("1"))
        self.assertEqual(True, Record.could_be_boolean(1))
        self.assertEqual(True, Record.could_be_boolean(True))
        self.assertEqual(True, Record.could_be_boolean(False))
        self.assertEqual(True, Record.could_be_boolean(0))
        self.assertEqual(True, Record.could_be_boolean("1"))
        self.assertEqual(False, Record.could_be_boolean("ABCD"))
        self.assertEqual(False, Record.could_be_boolean(1234))
        self.assertEqual(False, Record.could_be_boolean(None))
    
    def test_could_be_float(self):
        self.assertEqual(True, Record.could_be_float("1"))
        self.assertEqual(True, Record.could_be_float(u"1.1"))
        self.assertEqual(True, Record.could_be_float("0.1"))
        self.assertEqual(True, Record.could_be_float("000000000000000000000000.1"))
        self.assertEqual(True, Record.could_be_float(0000000000000000000000000.1))
        self.assertEqual(True, Record.could_be_float(10000000000000000000000000.1))
        self.assertEqual(True, Record.could_be_float(str(math.pow(2,63)-1)))
        self.assertEqual(False, Record.could_be_float(10000000000000000000000000))
        self.assertEqual(False, Record.could_be_float("abcd"))
        self.assertEqual(False, Record.could_be_float(None))
        self.assertEqual(False, Record.could_be_float("1111.10000000000.000000000"))
    
    def test_could_be_int(self):
        self.assertEqual(True, Record.could_be_int("1"))
        self.assertEqual(True, Record.could_be_int(0))
        self.assertEqual(True, Record.could_be_int(2147483647))
        self.assertEqual(True, Record.could_be_int(-2147483647))
        self.assertEqual(True, Record.could_be_int("-2147483647"))
        self.assertEqual(False, Record.could_be_int(math.pow(2,32)))
        self.assertEqual(False, Record.could_be_int(u"1.1"))
        self.assertEqual(False, Record.could_be_int("0.1"))
        self.assertEqual(False, Record.could_be_int("000000000000000000000000.1"))
        self.assertEqual(False, Record.could_be_int(0000000000000000000000000.1))
        self.assertEqual(False, Record.could_be_int(10000000000000000000000000))
        self.assertEqual(False, Record.could_be_int("abcd"))
        self.assertEqual(False, Record.could_be_int(None))
        self.assertEqual(False, Record.could_be_int("1111.10000000000.000000000"))
    
    def test_could_be_number(self):
        self.assertEqual(True, Record.could_be_number("1"))
        self.assertEqual(True, Record.could_be_number("1.1"))
        self.assertEqual(True, Record.could_be_number("0.1"))
        self.assertEqual(True, Record.could_be_number("000000000000000000000000.1"))
        self.assertEqual(True, Record.could_be_number(0000000000000000000000000.1))
        self.assertEqual(True, Record.could_be_number(10000000000000000000000000.1))
        self.assertEqual(True, Record.could_be_number(str(math.pow(2,63)-1)))
        self.assertEqual(True, Record.could_be_number(10000000000000000000000000))
        self.assertEqual(False, Record.could_be_number("abcd"))
        self.assertEqual(False, Record.could_be_number(None))
        self.assertEqual(False, Record.could_be_number("1111.10000000000.000000000"))
    
    def test_could_be_datetime(self):
        self.assertEqual(True, Record.could_be_datetime("Jan 2014", '%b %Y'))
        self.assertEqual(True, Record.could_be_datetime(u"September 1, 2014", '%B %m, %Y'))
        self.assertEqual(False, Record.could_be_datetime(None, None))
        self.assertEqual(False, Record.could_be_datetime("", ""))
        self.assertEqual(False, Record.could_be_datetime("Jan 2004", ""))

class TestGritsFlightRecord(unittest.TestCase):
    def setUp(self):
        self.headers = [u'Date', u'Mktg Al', u'Alliance', u'Op Al', u'Orig',
                        u'Dest', u'Miles', u'Flight', u'Stops', u'Equip',
                        u'Seats', u'Dep Term', u'Arr Term', u'Dep Time',
                        u'Arr Time', u'Block Mins', u'Arr Flag', u'Orig WAC',
                        u'Dest WAC', u'Op Days', u'Ops/Week', u'Seats/Week']
        self.row = [u'Jun 2015', u'W3', u'None', u'W3', {u'Code':u'LOS'},
                    {u'Code': u'JFK'}, u'5,250', u'107', u'0', u'332', u'251',
                    u'I ', u'4 ', u'2330', u'0550', u'680', u'1', u'555',
                    u'22', u'..3.5.7', u'3', u'753']
        self.valid_obj = FlightRecord(self.headers)
        self.invalid_obj = FlightRecord(None)
    
    def test_create_invalid_obj(self):
        self.assertRaises(InvalidRecordProperty, self.invalid_obj.create, self.row)
    
    def test_validate_invalid_obj(self):
        self.assertEquals(False, self.invalid_obj.validate())
    
    def test_create_valid_obj_is_validate(self):
        self.valid_obj.create(self.row)
        self.assertEquals(True, self.valid_obj.validate())
    
    def test_create_valid_obj_invalid_row(self):
        row = []
        self.assertRaises(InvalidRecordLength, self.valid_obj.create, row)
    
    def test_create_valid_obj_validate(self):
        self.valid_obj.create(self.row)
        self.assertEqual(True, self.valid_obj.validate())
    
class TestGritsAirportRecord(unittest.TestCase):
    def setUp(self):
        self.headers = [u'Code', u'Name', u'City', u'State', u'State Name',
                        u'Latitude', u'Longitude', u'Country', u'Country Name',
                        u'Global Region', u'WAC', u'Notes']
        self.row = [u'AAA', u'Anaa', u'Anaa', u'', u'', u'-17.351700',
                    u'-145.497800', u'PF', u'French Polynesia', u'Australasia',
                    u'823', u'']
        # setting a required field to empty string
        self.invalid_row = [u'', u'Anaa', u'Anaa', u'', u'', u'-17.351700',
                    u'-145.497800', u'PF', u'French Polynesia', u'Australasia',
                    u'823', u'']
        self.valid_obj = AirportRecord(self.headers)
        self.invalid_obj = AirportRecord(None)
    
    def test_create_invalid_obj(self):
        self.assertRaises(InvalidRecordProperty, self.invalid_obj.create, self.row)
    
    def test_validate_invalid_obj(self):
        self.assertEquals(False, self.invalid_obj.validate())
    
    def test_create_valid_obj_invalid_row(self):
        self.valid_obj.create(self.invalid_row)
        self.assertEquals(False, self.valid_obj.validate())
    
    def test_create_valid_obj_is_valid(self):
        self.valid_obj.create(self.row)
        self.assertEquals(True, self.valid_obj.validate())
    