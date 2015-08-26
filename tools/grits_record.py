import json
import collections
import logging

from datetime import datetime
from csv_helpers import TabDialect
from cerberus import Validator

_STRFTIME_FORMAT = '%b %Y'

class InvalidRecordProperty(Exception):
    """ custom exception that is thrown when the record is missing required
    properties """
    def __init__(self, message, *args, **kwargs):
        super(InvalidRecordProperty, self).__init__(message)

class InvalidRecordLength(Exception):
    """ custom exception that is thrown when the data to be inserted into the
    record does not match the header length """
    def __init__(self, message, *args, **kwargs):
        super(InvalidRecordLength, self).__init__(message)

class Record(object):
    """ base record class """
    
    def __init__(self):
        self.fields = collections.OrderedDict()
    
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
    
    def set_field_by_schema(self, header, field):
        if header not in self.schema.keys():
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
            if Record.could_be_datetime(field, _STRFTIME_FORMAT):
                self.fields[header] = datetime.strptime(field, _STRFTIME_FORMAT)
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
            if Record.could_be_boolean(field):
                self.fields[header] = bool(field)
            else:
                self.fields[header] = None
            return
    
    def to_json(self):
        return json.dumps(self.fields)

class FlightRecord(Record):
    """ class that represents the mondoDB Flight document generated by the
    Diio Mi Express 'Extract' report """
    
    @property
    def schema(self):
        return {
            'Date': { 'type': 'datetime', 'required': True},
            'Mktg Al': { 'type': 'string', 'nullable': True},
            'Alliance': { 'type': 'string', 'nullable': True},
            'Op Al':{ 'type': 'string', 'nullable': True},
            'Orig': { 'type': 'dict'}, #airport
            'Dest': { 'type': 'dict'}, #airport
            'Miles': { 'type': 'number', 'nullable': True},
            'Flight': { 'type': 'integer', 'nullable': True},
            'Stops': { 'type': 'integer', 'nullable': True},
            'Equip': { 'type': 'string', 'nullable': True},
            'Seats': { 'type': 'integer', 'nullable': True},
            'Dep Term': { 'type': 'string', 'nullable': True},
            'Arr Term': { 'type': 'string', 'nullable': True},
            'Dep Time': { 'type': 'number', 'nullable': True},
            'Arr Time':{ 'type': 'number', 'nullable': True},
            'Block Mins': { 'type': 'number', 'nullable': True},
            'Arr Flag': { 'type': 'boolean', 'nullable': True},
            'Orig WAC': { 'type': 'integer', 'nullable': True},
            'Dest WAC': { 'type': 'integer', 'nullable': True},
            'Op Days': { 'type': 'string', 'nullable': True},
            'Ops/Week': { 'type': 'integer', 'nullable': True},
            'Seats/Week': { 'type': 'integer', 'nullable': True}}
    
    def __init__(self, headers):
        super(FlightRecord, self).__init__()
        self.validator = Validator(self.schema)
        self.headers = headers
    
    def validate(self):
        return self.validator.validate(self.fields)
    
    def create(self, row):
        """ populate the fields with the row data """
        
        if not 'headers' in self.__dict__:
            raise InvalidRecordProperty('Record is missing "headers" property')
        if self.headers == None:
            raise InvalidRecordProperty('Record "headers" property is None')
        
        header_len = len(self.headers)
        field_len = len(row)
        if header_len != field_len:
            raise InvalidRecordLength('Record length does not equal header')
        
        position= 0
        for field in row:
            header = self.headers[position]
            position += 1
            
            # we ignore empty headers
            if Record.is_empty_str(header):
                continue
            
            if header.lower() == 'orig' or header.lower() == 'dest':
                #TODO - query mongo for the actual airport to embed
                airport = {
                    'Code': 'JST',
                    'Name': 'Johnstown/Cambria',
                    'City': 'Johnstown',
                    'State': 'PA',
                    'State Name': 'Pennsylvania',
                    'loc': {
                        'type': 'Point',
                        'coordinates': [40.3228957, -78.92277688]
                    },
                    'Country': 'US',
                    'Country Name': 'United States',
                    'Global Region': 'North America',
                    'WAC': 23,
                    'Notes': ''
                }
                self.fields[header] = airport
                continue
            
            # all other cases set data-type based on schema
            self.set_field_by_schema(header, field)

class FlightType(object):
    """ class that represents the .tsv format of Diio Mi Express 
    flight 'Extract' report """
    
    def __init__(self):
        self.name = 'extract'
        self.record = FlightRecord
        # positional processing rules
        self.title_position = 0 # zero-based position of the record set title
        self.header_position = 2 # zero-based position of the record set header
        self.data_position = 4 # zero-based position of the record set
        self.num_empty_rows_eod = 2 # two empty rows signals end_of_data
        self.dialect=TabDialect()

class AirportRecord(Record):
    """ class that represents the mondoDB format of Diio Mi Express 
    'Airport' report """
    
    @property
    def schema(self):
        return {
            'Code': { 'type': 'string', 'required': True},
            'Name': { 'type': 'string', 'required': True},
            'City': { 'type': 'string', 'nullable': True},
            'State': { 'type': 'string', 'nullable': True},
            'State Name':{ 'type': 'string', 'nullable': True},
            'loc': { 'type': 'dict', 'schema': {
                'type': {'type': 'string'},
                'coordinates': {'type': 'list', 'required': True}}},
            'Country': { 'type': 'integer', 'nullable': True},
            'Country Name': { 'type': 'string', 'nullable': True},
            'Global Region': { 'type': 'string', 'nullable': True},
            'WAC': { 'type': 'integer', 'nullable': True},
            'Notes': { 'type': 'string', 'nullable': True}}
    
    def __init__(self, headers):
        super(AirportRecord, self).__init__()
        self.validator = Validator(self.schema)
        self.headers = headers
    
    def validate(self):
        return self.validator.validate(self.fields)
    
    def create(self, row):
        """ populate the fields with the row data """
        
        if not 'headers' in self.__dict__:
            raise InvalidRecordProperty('Record is missing "headers" property')
        if self.headers == None:
            raise InvalidRecordProperty('Record "headers" property is None')
        
        header_len = len(self.headers)
        field_len = len(row)
        if header_len != field_len:
            raise InvalidRecordLength('Record length does not equal header')
        
        # default coordinates are null
        coordinates = [None, None]
        
        position= 0
        for field in row:
            header = self.headers[position]
            position += 1
            
            # we ignore empty headers
            if Record.is_empty_str(header):
                continue
            
            # special cases to convert to geoJSON
            if header.lower() == 'latitude':
                if Record.could_be_float(field):
                    coordinates[0] = float(field)
                continue
            if header.lower()  == 'longitude':
                if Record.could_be_float(field):
                    coordinates[1] = float(field)
                continue
            
            # all other cases set data-type based on schema
            self.set_field_by_schema(header, field)
        
        #add the geoJSON 'loc'
        loc = {
            'type': 'Point',
            'coordinates': coordinates
        }
        self.fields['loc'] = loc

class AirportType(object):
    """ class that represents the .tsv format of Diio Mi Express 'Airport' 
    report """
    
    def __init__(self):
        self.name = 'airport'
        self.record = AirportRecord
        # positional processing rules
        self.title_position = 0 # zero-based position of the record set title
        self.header_position = 2 # zero-based position of the record set Longitude' in record:
        self.data_position = 4 # zero-based position of the record set
        self.num_empty_rows_eod = 0 # data runs until end of file
        self.dialect=TabDialect()