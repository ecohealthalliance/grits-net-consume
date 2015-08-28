import csv
import logging
import collections

from datetime import datetime

from tools.grits_record import InvalidRecord
from tools.csv_helpers import UnicodeReader

class InvalidFileFormat(Exception):
    """ custom exception that is thrown when the file format is invalid """
    def __init__(self, message, *args, **kwargs):
        super(InvalidFileFormat, self).__init__(message)

class GritsFileReader:
    """ the class responsible for reading the file"""
    def __init__(self, record_type, program_arguments, mongo_connection):
        self.type= record_type
        self.arguments = program_arguments
        
        self.mongo_connection = mongo_connection
        
        self.records = set() #collection of records
        self.invalid_records = set() #collection of invalid records
        
        self.empty_row_count = 0 # number of empty rows encountered within record set
        self.end_of_data = False # flag that represents that the end of the data has been reached
        self.header = collections.OrderedDict() # ordered dict to hold the fields of each data row
        self.reader = UnicodeReader(program_arguments.infile, dialect=self.type.dialect)
    
    def process_file(self):
        """ iterate over each row in the file"""
        try:
            row_count = 0
            for row in self.reader:
                self.process_row(row_count, row)
                row_count += 1
        except csv.Error, e:
            logging.error("file %r, line %d, %r" % (self.validFile.name, self.reader.line_num, e))
    
    def process_row(self, row_count, row):
        """ process each row according to the record type contract """
        if self.arguments.verbose:
            print '%r' % row
            pass
        if row_count == self.type.title_position:
            if any(field.strip() for field in row):
                self.title = row
            else:
                raise InvalidFileFormat("title at position [%d] is empty" % row_count)
            return
        if row_count == self.type.header_position:
            if any(field.strip() for field in row):
                for field in row:
                    self.header[field.strip()] = None
            else:
                raise InvalidFileFormat("header at position [%d] is empty" % row_count)
            return
        if row_count > self.type.data_position and not self.end_of_data:
            if any(row):
                headers = self.header.keys() # in order
                record = self.type.record(headers, self.type.collection_name, self.mongo_connection)
                record.create(row)
                if record.validate():
                    self.records.add(record)
                else:
                    invalid_record = InvalidRecord(datetime.utcnow(), record.validation_errors(), type(record).__name__, row_count)
                    if invalid_record.validate():
                        self.invalid_records.add(invalid_record)
            else:
                if self.type.num_empty_rows_eod > 0:
                    self.empty_row_count += 1
                    if self.empty_row_count >= self.type.num_empty_rows_eod:
                        self.end_of_data = True
