import csv
import logging

from tools.csv_helpers import UnicodeReader, TabDialect

class Record:
    pass

class TsvReader:
    def __init__(self, arguments):
        self.header = None
        self.title_position = 0 # accept this as command-line arguments?
        self.header_position = 2 # accept this as command-line arguments?
        self.data_position = 4 # accept this as command-line arguments?
        self.end_of_data = False
        self.arguments = arguments
        self.reader = UnicodeReader(arguments.infile, dialect=TabDialect())
        #process file on construction
        self.process_file()
    
    def process_file(self):
        try:
            row_count = 0
            for row in self.reader:
                self.process_row(row_count, row)
        except csv.Error, e:
            logging.error("file %r, line %d, %r" % (self.validFile.name, self.reader.line_num, e))
    
    def process_row(self, row_count, row):
        if self.arguments.verbose:
            print '%r' % row
        if row_count == self.title_position:
            self.title = row
            return
        if row_count == self.header_position:
            self.header = row
            return
        if row_count == self.data_position:
            # TODO: populate record class
            pass