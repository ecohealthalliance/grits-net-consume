import os
import unittest
import math
import mongomock
import logging

from tools.grits_record import Record, FlightRecord, AirportRecord
from tools.grits_record import InvalidRecordProperty, InvalidRecordLength
from tools.grits_provider_type import FlightGlobalType, DiioAirportType

from conf import settings

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

    def test_parse_boolean(self):
        self.assertEqual(True, Record.parse_boolean("1"))
        self.assertEqual(None, Record.parse_boolean("100"))
        self.assertEqual(True, Record.parse_boolean("TrUe"))
        self.assertEqual(False, Record.parse_boolean("FaLSe"))
        self.assertEqual(True, Record.parse_boolean("true"))
        self.assertEqual(False, Record.parse_boolean("false"))
        self.assertEqual(False, Record.parse_boolean("0"))
        self.assertEqual(None, Record.parse_boolean("ABCD"))
        self.assertEqual(True, Record.parse_boolean(True))
        self.assertEqual(False, Record.parse_boolean(False))
        self.assertEqual(False, Record.parse_boolean(0))
        self.assertEqual(True, Record.parse_boolean(1))
        self.assertEqual(None, Record.parse_boolean(None))

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


class TestTimeDelta(unittest.TestCase):
    def setUp(self):
        pass
    def test_noclockchange_sameoffset(self):
        seconds = FlightRecord.elapsed_time('10:00:00', '-0500', '15:00:00', '-0500', 0)
        self.assertEqual(seconds, 18000.0)
    def test_noclockchange_differentoffset(self):
        seconds = FlightRecord.elapsed_time('10:00:00', '-0500', '15:00:00', '-0200', 0)
        self.assertEqual(seconds, 28800.0)
    def test_clockchange_sameoffset(self):
        seconds = FlightRecord.elapsed_time('21:40:00', '-0700', '00:29:00', '-0700', 1)
        self.assertEqual(seconds, 10140.0)
    def test_clockchange_differentoffset(self):
        seconds = FlightRecord.elapsed_time('22:00:00', '+0200', '01:05:00', '+0300', 1)
        self.assertEqual(seconds, 14700.0)
    def test_noclockchange_differentoffset_multiday(self):
        seconds = FlightRecord.elapsed_time('15:10:00', '-0600', '01:05:00', '+1100', 2)
        self.assertEqual(seconds, 183300.0)
    def test_clockchange_differentoffset_multiday(self):
        seconds = FlightRecord.elapsed_time('17:30:00', '+0100', '0:45:00', '-0500', 2)
        self.assertEqual(seconds, 90900.0)


class TestGritsFlightRecord(unittest.TestCase):
    def setUp(self):
        self.headers = ["carrier","flightnumber","serviceType","effectiveDate",
        "discontinuedDate","day1","day2","day3","day4","day5","day6","day7",
        "departureAirport","departureCity","departureState","departureCountry",
        "departureTimePub","departureTimeActual","departureUTCVariance",
        "departureTerminal","arrivalAirport","arrivalCity","arrivalState",
        "arrivalCountry","arrivalTimePub","arrivalTimeActual",
        "arrivalUTCVariance","arrivalTerminal","subAircraftCode",
        "groupAircraftCode","classes","classesFull","trafficRestriction",
        "flightArrivalDayIndicator","stops","stopCodes","stopRestrictions",
        "stopsubAircraftCodes","aircraftChangeIndicator","meals",
        "flightDistance","elapsedTime","layoverTime","inFlightService",
        "SSIMcodeShareStatus","SSIMcodeShareCarrier","codeshareIndicator",
        "wetleaseIndicator","codeshareInfo","wetleaseInfo","operationalSuffix",
        "ivi","leg","recordId","daysOfOperation","totalFrequency",
        "weeklyFrequency","availSeatMi","availSeatKm","intStopArrivaltime",
        "intStopDepartureTime","intStopNextDay","physicalLegKey",
        "departureAirportName","departureCityName","departureCountryName",
        "arrivalAirportName","arrivalCityName","arrivalCountryName",
        "aircraftType","carriername","totalSeats","firstClassSeats",
        "businessClassSeats","premiumEconomyClassSeats","economyClassSeats",
        "aircraftTonnage"]
        self.row = ["AA","5020","J","05/11/2015","12/03/2016","1","1","1","1",
        "1","1","1","ABE","ABE","PA","US","08:30:00","08:30:00","-0500","",
        "BNA","BNA","TN","US","11:59:00","11:59:00","-0600","","CR9","CRJ",
        "FY","FAPYBHKMLWVSNQOG","","0","1","CLT"," ","CR9!CR9","0","","685",
        "196","73","","X","OH","0","1","","/PSA AIRLINES AS AMERICAN EAGLE",
        "","12","1","407554","1234567","7","7","402780","647976","10:22",
        "11:35","0","AA|5020|12|1/AA|5020|12|2",
        "Lehigh Valley International Airport","Allentown","United States",
        "Nashville Metropolitan Airport","Nashville","United States",
        "Jet-engined aircraft","American Airlines","84","4","0","3","80","1859"]

        provider_type = FlightGlobalType()
        self.provider_map = provider_type.map
        self.collection_name = provider_type.collection_name

        self.mongo_connection = mongomock.MongoClient()
        # fake the find_one method with a lambda
        self.mongo_connection.db[settings._AIRPORT_COLLECTION_NAME].find_one = lambda x: {
                    '_id': 'JST',
                    'name': 'Johnstown/Cambria',
                    'city': 'Johnstown',
                    'state': 'PA',
                    'stateName': 'Pennsylvania',
                    'loc': {
                        'type': 'Point',
                        'coordinates': [40.3228957, -78.92277688]
                    },
                    'country': 'US',
                    'countryName': 'United States',
                    'globalRegion': 'North America',
                    'wac': 23,
                    'notes': ''}

        self.valid_obj = FlightRecord(self.headers, self.provider_map, self.collection_name, 300, self.mongo_connection)
        self.invalid_obj = FlightRecord(None, self.provider_map, None, None, self.mongo_connection)

    def test_create_invalid_obj(self):
        self.assertRaises(InvalidRecordProperty, self.invalid_obj.create, self.row)

    def test_validate_invalid_obj(self):
        self.assertEquals(False, self.invalid_obj.validate())

    def test_create_valid_obj_is_validate(self):
        self.valid_obj.create(self.row)
        self.valid_obj.validate()
        logging.debug('errors: %r', self.valid_obj.validation_errors())
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

        provider_type = DiioAirportType()
        self.provider_map = provider_type.map
        self.collection_name = provider_type.collection_name

        self.mongo_connection = mongomock.MongoClient()
        self.valid_obj = AirportRecord(self.headers, self.provider_map, self.collection_name, 300, self.mongo_connection)
        self.invalid_obj = AirportRecord(None, self.provider_map, self.collection_name, None, self.mongo_connection)

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
