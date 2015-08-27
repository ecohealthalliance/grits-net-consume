import os
import argparse
import logging
logging.getLogger().setLevel(logging.DEBUG)

from tools.grits_file_reader import GritsFileReader
from tools.grits_record import AirportType, FlightType
from tools.grits_mongo import GritsMongoConnection

_FILE_TYPES = ['.tsv']
_TYPES = ['airport', 'flight']
_INVALID_RECORDS_COLLECTION = 'invalidRecords'

class GritsConsumer(object):
    """ Command line tool to parse grits transportation network data """
    
    def __init__(self):
        self.parser = argparse.ArgumentParser(description='script to parse ' \
            'the grits transportation network data file and populate ' \
            'a mongodb collection.')
    
    @staticmethod
    def file_extension(file_obj):
        parts = os.path.splitext(file_obj.name)
        ext = ''
        if len(parts) > 1:
            ext = parts[-1].lower()
        return ext
    
    def is_valid_file_type(self, file_obj):
        ext = GritsConsumer.file_extension(file_obj)
        if ext not in _FILE_TYPES:
            return False
        return True
    
    def get_args(self):
        self.parser.add_argument('-v', '--verbose',
            action="store_true",
            help="verbose output" )
        
        self.parser.add_argument('-t', '--type', required=True,
            choices=_TYPES,
            help='the type of report to be parsed')
        
        self.parser.add_argument('-u', '--username',
            default=None,
            help='the username for mongoDB (Default: None)')
        
        self.parser.add_argument('-p', '--password',
            default=None,
            help='the password for mongoDB (Default: None)')
        
        self.parser.add_argument('-d', '--database',
            default='grits',
            help='the database for mongoDB (Default: grits)')
        
        self.parser.add_argument('-m', '--mongohost',
            default='localhost',
            help='the hostname for mongoDB (Default: localhost)')
        
        self.parser.add_argument('infile',
            type=argparse.FileType('rb'),
            help="the file to be parsed")
        
        return self.parser.parse_args()
    
    def run(self):
        program_args = self.get_args()
        if not self.is_valid_file_type(program_args.infile):
            msg = 'not a valid file type %r' % _FILE_TYPES
            self.parser.error(msg) #this calls sys.exit
        
        if program_args.type == 'airport':
            report_type = AirportType()
        else :
            report_type = FlightType()
            
        reader = GritsFileReader(report_type, program_args)
        reader.process_file()
        num_records = len(reader.records)
        num_invalid_records = len(reader.invalid_records)
        logging.debug('num_records: %d', num_records)
        logging.debug('num_invalid_records: %d', num_invalid_records)
        
        mongo = GritsMongoConnection(program_args)
        record_results = mongo.bulk_upsert(reader.type.collection_name, reader.type.key_name, reader.records)
        logging.debug('record_results: %r', record_results)
        
        invalid_record_results = mongo.insert_many(_INVALID_RECORDS_COLLECTION, reader.invalid_records)
        logging.debug('invalid_record_results: %r', invalid_record_results)
        
        logging.info('program_args:%r', program_args)
