import logging
import os

# Application constants

# debugging
_DEBUG = True

if (_DEBUG):
    logging.getLogger().setLevel(logging.DEBUG)

_DATA_DIR = '/data/'

# command-line options
_ALLOWED_FILE_EXTENSIONS = ['.tsv','.csv']
_TYPES = ['DiioAirport', 'FlightGlobal', 'FixAirports']

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

# drop indexes?  Setting this to 'true' will drop any existing indexes in the
# database.  This is most likely desirable, as bulk upserts should be faster
# without any indexes on the collection.  However, it is important to remember
# to then build the indexes through grits_ensure_index.py
_DROP_INDEXES = True

# default command-line options
# Allow environment variables for MONGO_HOST, MONGO_DATABASE, MONGO_USERNAME,
# and MONGO_PASSWORD to override these settings
if 'MONGO_HOST' in os.environ:
    _MONGO_HOST = os.environ['MONGO_HOST']
else:
    _MONGO_HOST = 'localhost'

if 'MONGO_DATABASE' in os.environ:
    _MONGO_DATABASE = os.environ['MONGO_DATABASE']
else:
    _MONGO_DATABASE = 'grits'

if 'MONGO_USERNAME' in os.environ:
    _MONGO_USERNAME = os.environ['MONGO_USERNAME']
else:
    _MONGO_USERNAME = None

if 'MONGO_PASSWORD' in os.environ:
    _MONGO_PASSWORD = os.environ['MONGO_PASSWORD']
else:
    #Warning: setting _MONGO_PASSWORD here will be saved as plain-text
    _MONGO_PASSWORD = None
