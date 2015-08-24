import functools
import json
import collections

from csv_helpers import TabDialect


class Record(object):
    """ base record class """
    
    def __init__(self):
        pass
    
    def create(self, row):
        position= 0
        for field in row:
            self.fields[self.headers[position]] = field
            position += 1
    
    def validate_required(self):
        """ the record must contain valid keys that are not None """
        valid = {}
        for required in self.required:
            if required in self.fields:
                if self.fields[required] != None:
                    valid[required] = True
                else:
                    valid[required] = False
            else:
                valid[required] = False
        
        return functools.reduce(lambda x,y: x and y, valid.values())
    
    def to_json(self):
        return json.dumps(self.fields)

class ExtractRecord(Record):
    """ class that represents the mondoDB document of Diio Mi Express 
    'Extract' report
    {
        "description": "An Extraction Report document",
        "type": "object",
        "properties": {
            "Date": { "type": "string" },
            "Mktg Al": { "type": "string" },
            "Alliance": { "type": "string" },
            "Op Al":{ "type": "string" },
            "Orig": { "type": "number" },
            "Dest": { "type": "number" },
            "Miles": { "type": "string"},
            "Flight": { "type": "string" },
            "Stops": { "type": "string" },
            "Equip": { "type": "number" },
            "Seats": { "type": "string" },
            "Dep Term": { "type": "string" },
            "Arr Term": { "type": "string" },
            "Dep Time": { "type": "string" },
            "Arr Time":{ "type": "string" },
            "Block Mins": { "type": "number" },
            "Arr Flag": { "type": "number" },
            "Orig WAC": { "type": "string"},
            "Dest WAC": { "type": "string" },
            "Op Days": { "type": "string" },
            "Ops/Week": { "type": "number" },
            "Seats/Week": { "type": "string" },
            "airports_id": { "type": "number"},
        },
        "required": ["Date", "Alliance", "Orig", "Dest", "Flight"],
        "dependencies": {
            "airports_id": {
                ["db.airports.collection"]
            }
        }
    }
    """
    
    def __init__(self, headers):
        self.headers = headers
        self.fields = collections.OrderedDict()
        self.required = ["Date", "Alliance", "Orig", "Dest", "Flight"]
        super(ExtractRecord, self).__init__()

class AirportRecord(Record):
    """ class that represents the mondoDB format of Diio Mi Express 
    'Airport' report 
    {
        "description": "An Airport document",
        "type": "object",
        "properties": {
            "Code": { "type": "string"},
            "Name": { "type": "string" },
            "City": { "type": "string" },
            "State": { "type": "string" },
            "State Name":{ "type": "string" },
            "Latitude": { "type": "number" },
            "Longitude": { "type": "number" },
            "Country": { "type": "string"},
            "Country Name": { "type": "string" },
            "Global Region": { "type": "string" },
            "WAC": { "type": "number" },
            "Notes": { "type": "string" },
        },
        "required": ["Code", "Name", "Latitude", "Longitude", "Country"],
        "dependencies": {}
    }
    """
    
    def __init__(self, headers):
        self.headers = headers
        self.fields = collections.OrderedDict()
        self.required = ["Code", "Name", "Latitude", "Longitude", "Country"]
        super(AirportRecord, self).__init__()

class ExtractType(object):
    """ class that represents the .tsv format of Diio Mi Express 
    'Extract Report' 
    
    MANIFEST:
    Schedule Weekly Extract Report for Passenger (All) flights from Western Hemisphere to West Africa for travel between December 2013 and June 2015 (down)
    
    Date    Mktg Al    Alliance    Op Al    Orig    Dest    Miles    Flight    Stops    Equip    Seats    Dep Term    Arr Term    Dep Time    Arr Time    Block Mins    Arr Flag    Orig WAC    Dest WAC    Op Days    Ops/Week    Seats/Week
    
    Dec 2013    DL    SkyTeam Alliance    DL    ACC    JFK    5,111    479    0    76W    226        4     2210    0438    688    1    529    22    .23.567    5    1,130
    ...
    Jun 2015    W3    None    W3    LOS    JFK    5,250    107    0    332    251    I     4     2330    0550    680    1    555    22    ..3.5.7    3    753
    
    
    Diio Mi Schedule Weekly Extract Report run on June 25, 2015 by ECOHEALTH-PH with Parameters:
        Trip Origin    Region: Western Hemisphere(102); 
        ...
        Travel Period    between December 2013 and June 2015 (down)
    EOF
    
    """
    
    def __init__(self):
        self.name = 'extract'
        self.record = ExtractRecord
        # positional processing rules
        self.title_position = 0 # zero-based position of the record set title
        self.header_position = 2 # zero-based position of the record set header
        self.data_position = 4 # zero-based position of the record set
        self.num_empty_rows_eod = 2 # two empty rows signals end_of_data
        self.dialect=TabDialect()

class AirportType(object):
    """ class that represents the .tsv format of Diio Mi Express 
    'Airport' report 
    
    MANIFEST:
    Airport Report
    
    Code    Name    City    State    State Name     Latitude      Longitude     Country    Country Name    Global Region    WAC    Notes    
    
    ---                               99    Unknown Country    Unknown Location    999        
    AAA    Anaa    Anaa               -17.351700    -145.497800    PF    French Polynesia    Australasia    823        
    ...
    ZZZ    Unknown    Unknown                       99    Unknown Country    Unknown Location    999        
    EOF
    """
    
    def __init__(self):
        self.name = 'airport'
        self.record = AirportRecord
        # positional processing rules
        self.title_position = 0 # zero-based position of the record set title
        self.header_position = 2 # zero-based position of the record set Longitude' in record:
        self.data_position = 4 # zero-based position of the record set
        self.num_empty_rows_eod = 0 # data runs until end of file
        self.dialect=TabDialect()