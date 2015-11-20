import logging

# Application constants

# debugging
_DEBUG = True

if (_DEBUG):
    logging.getLogger().setLevel(logging.DEBUG)

_DATA_DIR = '/data/'

# command-line options
_ALLOWED_FILE_EXTENSIONS = ['.tsv','.csv']
_TYPES = ['DiioAirport', 'FlightGlobal']

# default strftime format for a records date field
_STRFTIME_FORMAT = '%b %Y'

# mongodb collection names
_AIRPORT_COLLECTION_NAME = 'airports'
_FLIGHT_COLLECTION_NAME = 'flights'
_INVALID_RECORD_COLLECTION_NAME = 'invalidRecords'

# schema
_DISABLE_SCHEMA_MATCH = True #raise exception for headers not in the schema?

# number of lines to split the file
_CHUNK_SIZE = 5000

# threading?
_NODES = 5
_THREADING_ENABLED = True
