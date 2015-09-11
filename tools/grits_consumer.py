import os
import argparse
import logging

from tools.grits_file_reader import GritsFileReader
from tools.grits_record_type import AirportType, FlightType
from tools.grits_mongo import GritsMongoConnection

from conf import settings

class GritsConsumer(object):
    """ Command line tool to parse grits transportation network data """
    
    def __init__(self):
        self.parser = argparse.ArgumentParser(description='script to parse ' \
            'the grits transportation network data file and populate ' \
            'a mongodb collection.')
    
    @staticmethod
    def file_extension(file_obj):
        """ get the file extension from a file object
            
            The method uses os.path.spittext to get the parts of a file
            object by its name.  The last part is the file extension
            
            Parameters
            ----------
                file_obj : object
                    File object
            
            Returns
            -------
                str
                    String value or None
        """
        parts = os.path.splitext(file_obj.name)
        ext = ''
        if len(parts) > 1:
            ext = parts[-1].lower()
        return ext
    
    def is_valid_file_type(self, file_obj):
        """ validate the file extension is valid
            
            Validation method to determine if the file_obj has a valid
            extension.  The list of valid extensions are defined in
            conf/settings.py
            
            Parameters
            ----------
                file_obj : object
                    File object
            
            Returns
            -------
                bool
                    True or False
        """
        ext = GritsConsumer.file_extension(file_obj)
        if ext not in settings._ALLOWED_FILE_EXTENSIONS:
            return False
        return True
    
    def add_args(self):
        """ add arguments to the argparse command-line program """
        self.parser.add_argument('-v', '--verbose',
            action="store_true",
            help="verbose output" )
        
        self.parser.add_argument('-t', '--type', required=True,
            choices= settings._TYPES,
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
        """ kickoff the program """
        program_args = self.add_args()
        # validate the filename extension
        if not self.is_valid_file_type(program_args.infile):
            msg = 'not a valid file extension %r' % settings._ALLOWED_FILE_EXTENSIONS
            self.parser.error(msg) #this calls sys.exit
        # determine the record type from the program_args
        if program_args.type == 'airport':
            report_type = AirportType()
        else :
            report_type = FlightType()
        # setup the mongoDB connection
        mongo_connection = GritsMongoConnection(program_args)
        
        # create a new file reader object of the specified report type
        reader = GritsFileReader(report_type, program_args, mongo_connection)
        reader.process_file()
        
        # get counts for debugging
        num_records = len(reader.records)
        num_invalid_records = len(reader.invalid_records)
        logging.debug('num_records: %d', num_records)
        logging.debug('num_invalid_records: %d', num_invalid_records)
        
        # bulk upsert reader.records into mongodb
        record_results = mongo_connection.bulk_upsert(reader.type.collection_name, reader.records)
        logging.debug('record_results: %r', record_results)
        
        # get list of the invalid fields (dict) for insertion into mongoDB
        invalid_record_results = mongo_connection.insert_many(settings._INVALID_RECORD_COLLECTION_NAME, reader.invalid_records)
        logging.debug('invalid_record_results: %r', invalid_record_results)
        
        # addition debug info
        logging.debug('program_args:%r', program_args)
