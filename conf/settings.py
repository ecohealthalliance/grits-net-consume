import logging

# Application constants

# debugging
_DEBUG = True

if (_DEBUG):
    logging.getLogger().setLevel(logging.DEBUG)

# command-line options
_ALLOWED_FILE_EXTENSIONS = ['.tsv']
_TYPES = ['airport', 'flight']

# default strftime format for a records date field
_STRFTIME_FORMAT = '%b %Y'

# mongodb collection names
_AIRPORT_COLLECTION_NAME = 'airports'
_FLIGHT_COLLECTION_NAME = 'flights'
_INVALID_RECORD_COLLECTION_NAME = 'invalidRecords'