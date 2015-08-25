import os
import argparse
import logging
logging.getLogger().setLevel(logging.DEBUG)

from tools.grits_file_reader import GritsFileReader
from tools.grits_record import AirportType, FlightType


_FILE_TYPES = ['.tsv']
_TYPES = ['airport', 'flight']


class GritsConsumer(object):
    """ Command line tool to parse grits transportation network data """
    
    def __init__(self):
        self.verbose = False
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
            choices=_TYPES)
        
        self.parser.add_argument('infile',
            type=argparse.FileType('r'),
            help="file to be parsed")
        
        return self.parser.parse_args()
    
    def run(self):
        args = self.get_args()
        if not self.is_valid_file_type(args.infile):
            msg = 'not a valid file type %r' % _FILE_TYPES
            self.parser.error(msg) #this calls sys.exit
        
        if args.type == 'airport':
            report_type = AirportType()
        else :
            report_type = FlightType()
            
        reader = GritsFileReader(report_type, args)
        reader.process_file()
        
        logging.info('records: %d', len(reader.records))
        logging.info('args:%r', args)
