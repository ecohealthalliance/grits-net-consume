import logging
import os
import multiprocessing

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

# number of lines to split the file, multiprocessing will be faster the
# higher this is set but it will also consume more memory
_CHUNK_SIZE = 10000

# threading?
_THREADING_ENABLED = False
_THREADS = 5

# multiprocessing?
_MULTIPROCESSING_ENABLED = True
if multiprocessing.cpu_count() > 1:
    _CORES = multiprocessing.cpu_count() - 1
else:
    _CORES = 1

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
