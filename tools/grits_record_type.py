from tools.grits_record import FlightRecord, AirportRecord
from tools.csv_helpers import TabDialect

from conf import settings

class FlightType(object):
    """ class that represents the .tsv format of Diio Mi Express 
    flight 'Extract' report """
    
    def __init__(self):
        """ FlightType constructor 
        
        Describes the 'contract' for the report, such as the positional
        processing rules.
        """
        self.collection_name = settings._FLIGHT_COLLECTION_NAME # name of the MongoDB collection
        self.record = FlightRecord
        # positional processing rules
        self.title_position = 0 # zero-based position of the record set title
        self.header_position = 2 # zero-based position of the record set header
        self.data_position = 4 # zero-based position of the record set
        self.num_empty_rows_eod = 2 # two empty rows signals end_of_data
        self.dialect=TabDialect()
        
class AirportType(object):
    """ class that represents the .tsv format of Diio Mi Express 'Airport' 
    report """
    
    def __init__(self):
        """ AirportType constructor 
        
        Describes the 'contract' for the report, such as the positional
        processing rules.
        """
        self.collection_name = settings._AIRPORT_COLLECTION_NAME # name of the MongoDB collection
        self.record = AirportRecord
        # positional processing rules
        self.title_position = 0 # zero-based position of the record set title
        self.header_position = 2 # zero-based position of the record set Longitude' in record:
        self.data_position = 4 # zero-based position of the record set
        self.num_empty_rows_eod = 0 # data runs until end of file
        self.dialect=TabDialect()