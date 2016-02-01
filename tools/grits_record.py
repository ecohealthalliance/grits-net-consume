import json
import collections
import hashlib
import logging

from datetime import datetime
from datetime import timedelta
from cerberus import Validator
from bson import json_util
from math import radians, sin, cos, asin, sqrt
from conf import settings

class InvalidRecordProperty(Exception):
    """ custom exception that is thrown when the record is missing required
    properties """
    def __init__(self, message, *args, **kwargs):
        """ InvalidRecordProperty constructor

            Parameters
            ----------
                message : str
                    A descriptive message of the error
        """
        super(InvalidRecordProperty, self).__init__(message)

class InvalidRecordLength(Exception):
    """ custom exception that is thrown when the data to be inserted into the
    record does not match the header length """
    def __init__(self, message, *args, **kwargs):
        """ InvalidRecordLength constructor

            Parameters
            ----------
                message : str
                    A descriptive message of the error
        """
        super(InvalidRecordLength, self).__init__(message)

class InvalidRecord(object):
    """ class that represents the mondoDB format of an invalid record.  This
    is created when the file reader parses an invalid row."""

    @property
    def schema(self):
        """ the cerberus schema defination used for validation of a record """
        return {
            'Date': { 'type': 'datetime', 'required': True},
            'Errors': { 'type': 'dict', 'required': True},
            'RecordType': {'type': 'string', 'required': True},
            'RowNum': { 'type': 'integer', 'nullable': True}
        }

    def __init__(self, errors, record_type, row_num):
        """ InvalidRecord constructor

            Parameters
            ----------
                errors: list
                    List of validation errors with the last row containing
                    the records fields
                record_type: object
                    The type of record {AirportType, FlightType}
                row_num: int
                    The row number that the validation error occurred
        """
        self.fields = collections.OrderedDict()
        self.fields['Date'] = datetime.utcnow()
        self.fields['Errors'] = errors
        self.fields['RecordType'] = record_type
        self.fields['RowNum'] = row_num
        self.validator = Validator(self.schema)

    def validate(self):
        """ validates the record against the schema """
        return self.validator.validate(self.fields)

    def to_json(self):
        """ dumps the records fields into JSON format """
        return json.dumps(self.fields)

class Record(object):
    """ base record class

        A record is an object that contains fields (ordered dictionary) that
        are used to construct a mongoDB document.
    """

    @property
    def id(self):
        return self._id;

    @id.setter
    def id(self, val):
        self._id = val

    def __init__(self):
        """ Record constructor """
        self.fields = collections.OrderedDict()
        self.row_count = None
        self._id = None

    @staticmethod
    def is_empty_str(val):
        """ check if the val is an empty string"""
        s = str(val)
        if not isinstance(s, str):
            return False
        if not s.strip():
            return True
        else:
            return False

    @staticmethod
    def could_be_float(val):
        """ determines if the val is an instance of float or could be coerced
        to a float from a string """
        if val == None:
            return False

        if isinstance(val, float):
            return True

        # allow coercion from str
        if isinstance(val, (str, unicode)):
            try:
                f = float(val)
                if not isinstance(f, float):
                    raise ValueError
                else:
                    return True
            except:
                return False

        #otherwise
        return False

    @staticmethod
    def could_be_int(val):
        """ determines if the val is an instance of int or could be coerced
        to an int from a string """
        if val == None:
            return False

        if isinstance(val, int):
            return True

        # allow coercion from str
        if isinstance(val, (str, unicode)):
            try:
                i = int(val)
                if not isinstance(i, int):
                    raise ValueError
                else:
                    return True
            except:
                return False

        # otherwise
        return False

    @staticmethod
    def could_be_number(val):
        """ determines if the val is an instance of 'number' or could be coerced
        to a 'number' from a string """
        if val == None:
            return False

        if isinstance(val, (float, int, long)):
            return True

        # allow coercion from str
        if isinstance(val, (str, unicode)):
            try:
                n = float(val)
                if not isinstance(n, float):
                    raise ValueError
                else:
                    return True
            except:
                return False

        #otherwise
        return False

    @staticmethod
    def could_be_boolean(val):
        """ determines if the val is an instance of bool or could be coerced
        to a bool from a string or int, long"""
        if val == None:
            return False

        if isinstance(val, bool):
            return True

        if isinstance(val, (str, unicode)):
            if val.lower() in ['true', '1', 'false', '0']:
                return True

        if isinstance(val, (int, long)):
            if val in [0,1]:
                return True

        return False

    @staticmethod
    def could_be_datetime(val, fmt):
        """ determines if the val is an instance of datetime or could be coerced
        to a datetime from a string with the provided format"""

        if val == None or fmt == None:
            return False

        if isinstance(val, datetime):
            return True

        if isinstance(val, (str, unicode)):
            if Record.is_empty_str(val) or Record.is_empty_str(fmt):
                return False

            try:
                d = datetime.strptime(val, fmt)
                if not isinstance(d, datetime):
                    raise ValueError
                else:
                    return True
            except Exception as e:
                logging.error(e)
                return False

        #otherwise
        return False

    @staticmethod
    def parse_boolean(field):
        if Record.could_be_boolean(field):
            if Record.could_be_int(field):
                return bool(int(field))

            if isinstance(field, (str, unicode)):
                if field.lower() == 'true':
                    return True
                if field.lower() == 'false':
                    return False

            return bool(field)
        return None


    def set_field_by_schema(self, header, field):
        """ allows the records field to be set by matching against the schema

            NOTE: InvalidRecordProperty is raised if the header isn't located
            within the schema.  This check can be disabled through the
            constant '_DISABLE_SCHEMA_MATCH' in settings.py.
            The side-effect would be documents in the mongoDB would have
            different structure but added flexibility to the parser

            Parameters
            ----------
            header: str
                the name of the header
            field: str
                the corresponding column field of the row

            Raises
            ------
            InvalidRecordProperty
                If the header value is not located within the schema
        """
        if header not in self.schema.keys():
            if settings._DISABLE_SCHEMA_MATCH:
                return
            else:
                raise InvalidRecordProperty('Record schema does not have the property "%s"' % header)

        data_type = self.schema[header]['type'].lower()

        if data_type == 'string':
            if Record.is_empty_str(field):
                self.fields[header] = None
            else:
                self.fields[header] = field
            return

        if data_type == 'integer':
            if Record.could_be_int(field):
                self.fields[header] = int(field)
            else:
                self.fields[header] = None
            return

        if data_type == 'datetime':
            datetime_format = self.schema[header]['datetime_format'];
            if datetime_format == None:
                datetime_format = settings._STRFTIME_FORMAT
            if Record.could_be_datetime(field, datetime_format):
                self.fields[header] = datetime.strptime(field, datetime_format)
            else:
                self.fields[header] = None
            return

        if data_type == 'number':
            if Record.could_be_number(field):
                self.fields[header] = float(field)
            else:
                self.fields[header] = None
            return

        if data_type == 'float':
            if Record.could_be_float(field):
                self.fields[header] = float(field)
            else:
                self.fields[header] = None
            return

        if data_type == 'boolean':
            self.fields[header] = Record.parse_boolean(field)
            return

    def validation_errors(self):
        errors = self.validator.errors
        if len(errors.keys()) > 0:
            errors['fields'] = self.to_json()
        return errors

    def validate(self):
        """ validate the record

            This is a combination of checking the property _id is not None
            and that all fields within the schema are valid
        """
        if self.id == None:
            return False
        return self.validator.validate(self.fields)

    def map_header(self, header):
        if header.lower() in self.provider_map_keys_lower:
            return self.provider_map[header.lower()]['maps_to']
        return None

    def to_json(self):
        return json.dumps(self.fields, default=json_util.default)

class FlightRecord(Record):
    """ class that represents the mondoDB Flight document """

    @property
    def schema(self):
        """ the cerberus schema definition used for validation of a record """
        return {
            # _id is md5 hash of (effectiveDate, carrier, flightNumber)
            'carrier' : { 'type': 'string', 'nullable': False, 'required': True},
            'flightNumber' : { 'type': 'integer', 'nullable': False, 'required': True},
            'serviceType' : {'type': 'string', 'nullable': True},
            'effectiveDate' : { 'type': 'datetime', 'required': True, 'datetime_format': '%d/%m/%Y'},
            'discontinuedDate' : { 'type': 'datetime', 'required': True, 'datetime_format': '%d/%m/%Y'},
            'day1' : { 'type': 'boolean', 'nullable': True},
            'day2' : { 'type': 'boolean', 'nullable': True},
            'day3' : { 'type': 'boolean', 'nullable': True},
            'day4' : { 'type': 'boolean', 'nullable': True},
            'day5' : { 'type': 'boolean', 'nullable': True},
            'day6' : { 'type': 'boolean', 'nullable': True},
            'day7' : { 'type': 'boolean', 'nullable': True},
            'departureAirport' : { 'type': 'dict', 'nullable': False, 'required': True},
            'departureCity' : { 'type': 'string', 'nullable': True},
            'departureState' : { 'type': 'string', 'nullable': True},
            'departureCountry' : { 'type': 'string', 'nullable': True},
            'departureTimePub' : { 'type': 'string', 'nullable': True},
            #'departureTimeActual' : { 'type': 'datetime', 'nullable': True, 'datetime_format': '%H:%M:%S'},
            'departureUTCVariance' : { 'type': 'string', 'nullable': True},
            #'departureTerminal' : { 'type': 'string', 'nullable': True},
            'arrivalAirport' : { 'type': 'dict', 'nullable': False, 'required': True},
            'arrivalCity' : { 'type': 'string', 'nullable': True},
            'arrivalState' : { 'type': 'string', 'nullable': True},
            'arrivalCountry' : { 'type': 'string', 'nullable': True},
            'arrivalTimePub' : { 'type': 'string', 'nullable': True},
            #'arrivalTimeActual' : { 'type': 'datetime', 'nullable': True, 'datetime_format': '%H:%M:%S'},
            'arrivalUTCVariance' : { 'type': 'string', 'nullable': True},
            #'arrivalTerminal' : { 'type': 'string', 'nullable': True},
            #'subAircraftCode' : { 'type': 'string', 'nullable': True},
            #'groupAircraftCode' : { 'type': 'string', 'nullable': True},
            #'classes' : { 'type': 'string', 'nullable': True},
            #'classesFull' : { 'type': 'string', 'nullable': True},
            #'trafficRestriction' : { 'type': 'string', 'nullable': True},
            'flightArrivalDayIndicator' : { 'type': 'integer', 'nullable': True},
            'stops' : { 'type': 'integer', 'nullable': True},
            'stopCodes' : { 'type': 'list', 'nullable': True},
            'legs' : { 'type': 'list', 'schema': {
                    'departureAirport': { 'type': 'dict', 'nullable': False, 'required': True},
                    'arrivalAirport': { 'type': 'dict', 'nullable': False, 'required': True},
                    'distance': {'type': 'number', 'required': True},
                    'time': {'type': 'number', 'required': True},
                }, 'nullable': True, 'calculated': True},
            #'stopRestrictions' : { 'type': 'string', 'nullable': True},
            #'stopsubAircraftCodes' : { 'type': 'integer', 'nullable': True},
            #'aircraftChangeIndicator' : { 'type': 'string', 'nullable': True},
            #'meals' : { 'type': 'string', 'nullable': True},
            #'flightDistance' : { 'type': 'integer', 'nullable': True},
            #'elapsedTime' : { 'type': 'integer', 'nullable': True},
            #'layoverTime' : { 'type': 'integer', 'nullable': True},
            #'inFlightService' : { 'type': 'string', 'nullable': True},
            #'SSIMcodeShareStatus' : { 'type': 'string', 'nullable': True},
            #'SSIMcodeShareCarrier' : { 'type': 'string', 'nullable': True},
            #'codeshareIndicator' :  { 'type': 'boolean', 'nullable': True},
            #'wetleaseIndicator' : { 'type': 'boolean', 'nullable': True},
            #'codeshareInfo' : { 'type': 'list', 'nullable': True},
            #'wetleaseInfo' : { 'type': 'string', 'nullable': True},
            #'operationalSuffix' : { 'type': 'string', 'nullable': True},
            #'ivi' : { 'type': 'integer', 'nullable': True},
            #'leg' : { 'type': 'integer', 'nullable': True},
            #'recordId' : { 'type': 'integer', 'nullable': True},
            #'daysOfOperation' : { 'type': 'string', 'nullable': True},
            #'totalFrequency' : { 'type': 'integer', 'nullable': True},
            'weeklyFrequency' : { 'type': 'integer', 'required': True, 'calculated': True},
            #'availSeatMi' : { 'type': 'integer', 'nullable': True},
            #'availSeatKm' : { 'type': 'integer', 'nullable': True},
            #'intStopArrivaltime' : { 'type': 'list', 'nullable': True},
            #'intStopDepartureTime' : { 'type': 'list', 'nullable': True},
            #'intStopNextDay' : { 'type': 'list', 'nullable': True},
            #'physicalLegKey' : { 'type': 'list', 'nullable': True},
            #'departureAirportName' : { 'type': 'string', 'nullable': True},
            #'departureCityName' : { 'type': 'string', 'nullable': True},
            #'departureCountryName' : { 'type': 'string', 'nullable': True},
            #'arrivalAirportName' : { 'type': 'string', 'nullable': True},
            #'arrivalCityName' : { 'type': 'string', 'nullable': True},
            #'arrivalCountryName' : { 'type': 'string', 'nullable': True},
            #'aircraftType' : { 'type': 'string', 'nullable': True},
            #'carrierName' : { 'type': 'string', 'nullable': True},
            'totalDistance': { 'type': 'number', 'required': True, 'calculated': True},
            'totalTime': { 'type': 'number', 'required': True, 'calculated': True},
            'totalSeats' : { 'type': 'integer', 'nullable': True}}
            #'firstClassSeats' : { 'type': 'integer', 'nullable': True},
            #'businessClassSeats' : { 'type': 'integer', 'nullable': True},
            #'premiumEconomyClassSeats' : { 'type': 'integer', 'nullable': True},
            #'economyClassSeats' : { 'type': 'integer', 'nullable': True},
            #'aircraftTonnage' : { 'type': 'integer', 'nullable': True}}

    def __init__(self, header_row, provider_map, collection_name, row_count, mongo_connection):
        """ FlightRecord constructor

            Parameters
            ----------
                header_row : list
                    The parsed header row
                collection_name: str
                    The name of the mongoDB collection corresponding to this
                    record
                mongo_connection: object
                    The mongoDB connection
        """
        super(FlightRecord, self).__init__()
        self.header_row = header_row
        if provider_map == None:
            raise InvalidRecordProperty('Record "provider_map" property is None')
        self.provider_map = provider_map
        self.provider_map_keys_lower = map(lambda x: x.lower(), provider_map.keys())
        self.collection_name = collection_name
        self.row_count = row_count
        self.mongo_connection = mongo_connection
        # initial values for calculated fields
        self.fields['weeklyFrequency'] = 0
        self.fields['totalDistance'] = 0
        self.fields['totalTime'] = 0
        self.fields['legs'] = []
        self.validator = Validator(self.schema, transparent_schema_rules=True)

    @staticmethod
    def haversine(lon1, lat1, lon2, lat2):
        """ http://stackoverflow.com/questions/4913349/haversine-formula-in-python-bearing-and-distance-between-two-gps-points
        Calculate the great circle distance between two points
        on the earth (specified in decimal degrees)
        """
        # convert decimal degrees to radians
        lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
        # haversine formula
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a))
        r = 3956 # Radius of earth in miles. Use 6371 for kilometers
        return c * r

    @staticmethod
    def weighted_time_over_distance(total_distance, leg_distance, total_time):
        if total_distance > 0:
            return total_time - (total_time * ((total_distance - leg_distance) / total_distance))

    @staticmethod
    def parse_offset(offset):
        if len(offset) != 5:
            raise InvalidRecordProperty('offset "%s" is not in the required format + / - HHmm' % offset)
        if not(offset[0] == u'+' or offset[0] == u'-'):
            raise InvalidRecordProperty('offset "%s" is not in the required format + / - HHmm' % offset)
        return int(offset[0:3])

    @staticmethod
    def total_distance(departure, arrival):
        return FlightRecord.haversine(
            departure['loc']['coordinates'][0],
            departure['loc']['coordinates'][1],
            arrival['loc']['coordinates'][0],
            arrival['loc']['coordinates'][1]
        )

    @staticmethod
    def create_leg(departure, arrival, total_distance, total_time):
        leg_distance = FlightRecord.total_distance(departure, arrival)
        return {
            'departureAirport': departure,
            'arrivalAirport': arrival,
            'distance': leg_distance,
            'time': FlightRecord.weighted_time_over_distance(
                total_distance,
                leg_distance,
                total_time
            )
        }

    @staticmethod
    def elapsed_time(begin_time, begin_offset, end_time, end_offset, days_indicator):
        """ calculate the elapsed time between times with offset and the number
        of days """
        # the current utc datetime
        now = datetime.utcnow()
        # how many clock changes occur from the tz offset
        clock_changes = 0

        # split the begin_time into HH:mm:ss
        split = begin_time.split(':')
        if len(split) != 3:
            raise InvalidRecordProperty('time "%s" is not in the required format HH:mm:ss' % begin_time)
        # hours plus the offset
        hours = int(split[0]) + FlightRecord.parse_offset(begin_offset)
        # if hours is less than zero, a clock change occured due to timezone
        if hours < 0:
            clock_changes += 1
            hours = 24 + hours
        # elif hours is greater then twenty-three, a clock change occured due to timezone
        elif hours > 23:
            clock_changes += 1
            hours = hours - 24
        # set the begin_date from the current utc date with the adjusted hour, minute, second
        begin_date = now.replace(hour=hours, minute=int(split[1]), second=int(split[2]))


        # split the end_time into HH:mm:ss
        split = end_time.split(':')
        if len(split) != 3:
            raise InvalidRecordProperty('time "%s" is not in the required format HH:mm:ss' % end_time)
        hours = int(split[0]) + FlightRecord.parse_offset(end_offset)
        # if hours is less than zero, a clock change occured due to timezone
        if hours < 0:
            clock_changes += 1
            hours = 24 + hours
        # elif hours is greater then twenty-three, a clock change occured due to timezone
        elif hours > 23:
            clock_changes += 1
            hours = hours - 24
        # set the end_date from the current utc date with the adjusted hour, minute, second
        end_date = now.replace(hour=hours, minute=int(split[1]), second=int(split[2]))

        # how many days have elapsed not including timezone clock changes?
        if not(days_indicator == '' or days_indicator == None):
            total_days = days_indicator - clock_changes
            # it total_days is a positive integer, add the total_days
            if total_days > 0:
                end_date = end_date + timedelta(days=total_days)

        # the difference between beginning and end
        time_delta = begin_date - end_date
        # return the absolute value of the delta total_seconds
        return abs(time_delta.total_seconds())

    def gen_key(self):
        """ generate a unique key for this record """

        if len(self.fields) == 0:
            return None

        # we do not call self.validate() here as self._id will always be null,
        # so we call self.validator.validate on the schema.  This will validate
        # that 'effectiveDate', 'carrier', and 'flightNumber' are not None
        # and of valid data type
        if self.validator.validate(self.fields) == False:
            return None

        h = hashlib.md5()
        h.update(self.fields['effectiveDate'].isoformat())
        h.update(str(self.fields['carrier']))
        h.update(str(self.fields['flightNumber']))
        self.id = h.hexdigest()

    def gen_weeklyFrequency(self):
        """ generate the weeklyFrequency for this record """
        if len(self.fields) == 0:
            return

        if self.validator.validate(self.fields) == False:
            return

        weeklyFrequency = 0
        dayFields = ['day1','day2','day3','day4','day5','day6','day7']
        for dayField in dayFields:
            if dayField in self.fields:
                if self.fields[dayField] == True:
                    weeklyFrequency += 1
        self.fields.weeklyFrequency = weeklyFrequency

    def gen_totalTime(self):
        if len(self.fields) == 0:
            return

        if self.validator.validate(self.fields) == False:
            return

        begin_time = self.fields['departureTimePub']
        begin_offset = self.fields['departureUTCVariance']
        end_time = self.fields['arrivalTimePub']
        end_offset = self.fields['arrivalUTCVariance']
        days_indicator = self.fields['flightArrivalDayIndicator']
        self.fields['totalTime'] = FlightRecord.elapsed_time(begin_time, begin_offset, end_time, end_offset, days_indicator)

    def gen_totalDistance(self):
        if len(self.fields) == 0:
            return

        if self.validator.validate(self.fields) == False:
            return

        total_distance = 0
        if self.fields['departureAirport']['_id'] == self.fields['arrivalAirport']['_id']:
            # edge case, we better have stops or raise invalid record error
            if len(self.fields['stopCodes']) == 0:
                raise InvalidRecordProperty('departureAirport and arrivalAirport are the same and without stops.')

        if len(self.fields['stopCodes']) > 0:
            previousAirport = None
            for airport in self.fields['stopCodes']:
                if previousAirport == None:
                    total_distance += FlightRecord.total_distance(self.fields['departureAirport'], airport)
                else:
                    total_distance += FlightRecord.total_distance(previousAirport, airport)
                previousAirport = airport

            if previousAirport != None:
                total_distance += FlightRecord.total_distance(previousAirport, self.fields['arrivalAirport'])
        else:
            total_distance = FlightRecord.total_distance(self.fields['departureAirport'], self.fields['arrivalAirport'])
        self.fields['totalDistance'] = total_distance

    def gen_legs(self):
        if len(self.fields) == 0:
            return

        if self.validator.validate(self.fields) == False:
            return

        legs = []
        if len(self.fields['stopCodes']) > 0:
            previousAirport = None
            for airport in self.fields['stopCodes']:
                if previousAirport == None:
                    legs.append(
                        FlightRecord.create_leg(
                            self.fields['departureAirport'],
                            airport,
                            self.fields['totalDistance'],
                            self.fields['totalTime']
                        )
                    )
                else:
                    legs.append(
                        FlightRecord.create_leg(
                            previousAirport,
                            airport,
                            self.fields['totalDistance'],
                            self.fields['totalTime'])
                    )
                previousAirport = airport
            if previousAirport != None:
                legs.append(
                    FlightRecord.create_leg(
                        previousAirport,
                        self.fields['arrivalAirport'],
                        self.fields['totalDistance'],
                        self.fields['totalTime'])
                )
        else:
            legs.append(
                FlightRecord.create_leg(
                    self.fields['departureAirport'],
                    self.fields['arrivalAirport'],
                    self.fields['totalDistance'],
                    self.fields['totalTime'])
            )
        self.fields['legs'] = legs

    def gen_calculated_fields(self):
        # order matters, we need time and distance before legs
        self.gen_weeklyFrequency()
        self.gen_totalTime()
        self.gen_totalDistance()
        self.gen_legs()

    def create(self, row):
        """ populate the fields with the row data

            The self.fields property will be populated with the column data. An
            ordered dictionary is used as insertion order is critical to
            maintaining positioning with the header.  The order of the headers
            within the file is irrelevant but the data must match.

            Parameters
            ----------
                row : object
                    The parsed row containing column data

            Raises
            ------
                InvalidRecordProperty
                    If the record is missing headers or the headers property
                    is None
                InvalidRecordLength
                    If the record length does not equal the header.
        """
        if not 'header_row' in self.__dict__:
            raise InvalidRecordProperty('Record is missing "header_row" property')
        if self.header_row == None:
            raise InvalidRecordProperty('Record "header_row" property is None')

        header_len = len(self.header_row)
        field_len = len(row)
        if header_len != field_len:
            raise InvalidRecordLength('Record length does not equal header_row')

        position = 0
        for field in row:
            header = self.map_header(self.header_row[position])
            position += 1

            # we ignore unmapped header
            if header == None:
                continue

            # we ignore empty headers
            if Record.is_empty_str(header):
                continue

            # special cases to convert to geoJSON
            if header.lower() == 'departureairport' or header.lower() == 'arrivalairport':
                db = self.mongo_connection.db
                airport = db[settings._AIRPORT_COLLECTION_NAME].find_one({'_id':field})
                self.fields[header] = airport
                continue

            # special case for stopCodes
            if header.lower() == 'stopcodes':
                codes = field.split('!')
                airports = []
                for code in codes:
                    airport = db[settings._AIRPORT_COLLECTION_NAME].find_one({'_id':code})
                    if airport != None: airports.append(airport)
                self.fields[header] = airports

            # all other cases set data-type based on schema
            self.set_field_by_schema(header, field)

        # calculated fields
        self.gen_calculated_fields()
        self.gen_key()

class AirportRecord(Record):
    """ class that represents the mondoDB airport document """

    @property
    def schema(self):
        """ the cerberus schema definition used for validation of a record """
        return {
            # _id is the airport 'Code'
            'name': { 'type': 'string', 'required': True},
            'city': { 'type': 'string', 'nullable': True},
            'state': { 'type': 'string', 'nullable': True},
            'stateName':{ 'type': 'string', 'nullable': True},
            'loc': { 'type': 'dict', 'schema': {
                'type': {'type': 'string'},
                'coordinates': {'type': 'list'}}, 'nullable': False},
            'country': { 'type': 'integer', 'nullable': True},
            'countryName': { 'type': 'string', 'nullable': True},
            'globalRegion': { 'type': 'string', 'nullable': True},
            'WAC': { 'type': 'integer', 'nullable': True},
            'notes': { 'type': 'string', 'nullable': True}}

    def __init__(self, header_row, provider_map, collection_name, row_count, mongo_connection):
        super(AirportRecord, self).__init__()
        self.header_row = header_row
        self.provider_map = provider_map
        self.provider_map_keys_lower = map(lambda x: x.lower(), provider_map.keys())
        self.collection_name = collection_name
        self.row_count = row_count
        self.mongo_connection = mongo_connection
        self.validator = Validator(self.schema)

    @staticmethod
    def is_valid_coordinate_pair(coordinates):
        """ validates that a pair of coordinates are floats representing
        longitudes and latitudes

            Parameters
            ----------
                coordinates: list
                    The coordinate pair as [longitude,latitude]
        """
        longitude = coordinates[0]
        latitude = coordinates[1]

        if longitude == None or latitude == None:
            return False

        if latitude < -90.0 or latitude > 90.0:
            return False

        if longitude < -180.0 or longitude > 180.0:
            return False

        return True

    def create(self, row):
        """ populate the fields with the row data

            The self.fields property will be populated with the column data. An
            ordered dictionary is used as insertion order is critical to
            maintaining positioning with the header.  The order of the headers
            within the file is irrelevant but the data must match.

            Parameters
            ----------
                row : object
                    The parsed row containing column data

            Raises
            ------
                InvalidRecordProperty
                    If the record is missing headers or the headers property
                    is None
                InvalidRecordLength
                    If the record length does not equal the header.
        """
        if not 'header_row' in self.__dict__:
            raise InvalidRecordProperty('Record is missing "header_row" property')
        if self.header_row == None:
            raise InvalidRecordProperty('Record "header_row" property is None')

        header_len = len(self.header_row)
        field_len = len(row)
        if header_len != field_len:
            raise InvalidRecordLength('Record length does not equal header_row')

        # default coordinates are null
        coordinates = [None, None]

        position= 0
        for field in row:
            header = self.map_header(self.header_row[position])
            #logging.debug('self.header_row[position]: %r', self.header_row[position])
            #logging.debug('header: %r', header)
            position += 1

            # we ignore none header
            if header == None:
                continue

            # we ignore empty header
            if Record.is_empty_str(header):
                continue

            # special case for unique id
            if header.lower() == 'code':
                if not Record.is_empty_str(field):
                    self.id = field;
                continue

            # special cases to convert to geoJSON
            # Always list coordinates in longitude, latitude order.
            if header.lower() == 'longitude':
                if Record.could_be_float(field):
                    coordinates[0] = float(field)
                continue
            if header.lower() == 'latitude':
                if Record.could_be_float(field):
                    coordinates[1] = float(field)
                continue

            # all other cases set data-type based on schema
            self.set_field_by_schema(header, field)

        #we cannot have invalid geoJSON objects in mongoDB
        if AirportRecord.is_valid_coordinate_pair(coordinates):
            loc = {
                'type': 'Point',
                'coordinates': coordinates
            }
        else:
            loc = None

        #add the geoJSON 'loc'
        self.fields['loc'] = loc
