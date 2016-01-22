import csv
import logging
import collections
import time
import sys

import _strptime
from pathos.threading import ThreadPool
from pathos.multiprocessing import ProcessingPool

from datetime import datetime

from conf import settings
from tools.grits_record import InvalidRecord
from tools.csv_helpers import UnicodeReader

class InvalidFileFormat(Exception):
    """ custom exception that is thrown when the file format is invalid """
    def __init__(self, message, *args, **kwargs):
        """ InvalidFileFormat constructor

            Parameters
            ----------
                message : str
                    A descriptive message of the error
        """
        super(InvalidFileFormat, self).__init__(message)

class GritsFileReader:
    """ the class responsible for reading the file """

    def __init__(self, provider_type, program_arguments):
        """ GritsFileReader constructor

            Parameters
            ----------
                provider_type : object
                    A provider type object from grits_provider_type.py
                program_arguments: dict
                    A dict containing the argparse program arguments

        """

        self.provider_type = provider_type
        self.program_arguments = program_arguments

        self.empty_row_count = 0 # number of empty rows encountered within record set
        self.end_of_data = False # flag that represents that the end of the data has been reached
        self.header_row = []

    @staticmethod
    def gen_chunks(reader, airports):
        """ yield chunks of the file for batch processing """
        chunk = [];
        for row_number, row in enumerate(reader):
            if (row_number % settings._CHUNK_SIZE == 0 and row_number > 0):
                yield chunk
                del chunk[:]
            chunk.append([row_number, row, airports])
        yield chunk

    def find_header(self, reader):
        """ find the header based off the provider_type """
        for row_number, line in enumerate(reader):
            if row_number == self.provider_type.header_position:
                # store the report header and continue
                if any(field.strip() for field in line):
                    for field in line:
                        self.header_row.append(field.strip().lower())
                else:
                    raise InvalidFileFormat("header at position [%d] is empty" % row_number)

                break

    def bulk_upsert(self, valid_records, invalid_records, mongo_connection):
        """ bulk upsert / inset many of the records """
        valid_result = mongo_connection.bulk_upsert(self.provider_type.collection_name, valid_records)
        invalid_result = mongo_connection.insert_many(settings._INVALID_RECORD_COLLECTION_NAME, invalid_records)
        logging.debug('valid_result: %r', valid_result)
        logging.debug('invalid_result: %r', invalid_result)

    def process(self, mongo_connection, airports):
        """ process a chunk of rows in the file """
        reader = UnicodeReader(self.program_arguments.infile, dialect=self.provider_type.dialect)
        self.find_header(reader)

        if settings._MULTIPROCESSING_ENABLED:
            ppool = ProcessingPool(nodes=settings._NODES)
            chunks = []

        if settings._THREADING_ENABLED:
            tpool = ThreadPool(nodes=settings._NODES)

        start = time.time()*1000.0
        for chunk in GritsFileReader.gen_chunks(reader, airports):
            # collections of valid and invaid records to be batch upsert / insert many
            valid_records = []
            invalid_records = []
            chunk_start = time.time()*1000.0
            # is multiprocessing enabled? processing time may increase if the
            # file is read into memory and processing is done by multiple
            # processors
            if settings._MULTIPROCESSING_ENABLED:
                chunks.append(chunk)
            # is threading enabled?  this may increase performance when mongoDB
            # is not running on localhost due to busy wait on finding an airport
            # in the case of FlightGlobalType.
            elif settings._THREADING_ENABLED:
                results = tpool.amap(self.process_row, chunk)
                while not results.ready():
                    # command-line spinner
                    for cursor in '|/-\\':
                        sys.stdout.write('\b%s' % cursor)
                        sys.stdout.flush()
                        time.sleep(.25)
                sys.stdout.write('\b')
                sys.stdout.flush()
                # async-poll is done, get the results
                result = results.get()
                if result:
                    valid_records = [ x[0] for x in result if x[0] is not None ]
                    invalid_records = [ x[1] for x in result if x[1] is not None ]
                    logging.debug('t-finish: %r', (time.time()*1000.0)-chunk_start)
                    self.bulk_upsert(valid_records, invalid_records, mongo_connection)
            # single-threaded synchronous processing
            else:
                for data in chunk:
                    valid, invalid = self.process_row(data)
                    if valid != None: valid_records.append(valid)
                    if invalid != None: invalid_records.append(invalid)
                logging.debug('s-finish: %r', (time.time()*1000.0)-chunk_start)
                self.bulk_upsert(valid_records, invalid_records, mongo_connection)

        if settings._MULTIPROCESSING_ENABLED:
            results = ppool.amap(self.process_chunk, chunks)
            while not results.ready():
                # command-line spinner
                for cursor in '|/-\\':
                    sys.stdout.write('\b%s' % cursor)
                    sys.stdout.flush()
                    time.sleep(.25)
            sys.stdout.write('\b')
            sys.stdout.flush()
            result = results.get()
            if result:
                records = [ x[0] for x in result if x[0] is not None ]
                valid_records = [ x[0] for x in records if x[0] is not None ]
                invalid_records = [ x[1] for x in records if x[1] is not None ]
                self.bulk_upsert(valid_records, invalid_records, mongo_connection)

        logging.debug('all-finish: %r', (time.time()*1000.0)-start)

    def process_chunk(self, chunk):
        """ during multiprocessing, each cpu will process of chunk of data """
        results = []
        for row in chunk:
            results.append(self.process_row(row))
        return results

    def process_row(self, args):
        """ process each row according to the record type contract

            Parameters
            ----------
                args[0] - row_count : int
                    the current row number
                args[1] - row: object
                    A python csv module row object
                args[2] - airports: object
                    A list of all airports
        """
        row_count = args[0]
        row = args[1]
        airports = args[2]

        if self.program_arguments.verbose:
            # echo the contents of the row in verbose mode
            print '%r' % row

        if row_count >= self.provider_type.data_position and not self.end_of_data:
            if any(row):
                header_row = self.header_row
                provider_map = self.provider_type.map
                collection_name = self.provider_type.collection_name

                # init the record object based on the type
                record = self.provider_type.record(header_row, provider_map, collection_name, row_count, airports)

                # create the record
                record.create(row)

                # validate
                if record.validate():
                    return [record,None]
                else:
                    invalid_record = InvalidRecord(record.validation_errors(), type(record).__name__, record.row_count)
                    if invalid_record.validate():
                        return [None,invalid_record]
            else:
                # check for special case where empty line signal end_of_data
                if self.provider_type.num_empty_rows_eod > 0:
                    self.empty_row_count += 1
                    logging.debug('empty_row_count: %d', empty_row_count)
                    if self.empty_row_count >= self.provider_type.num_empty_rows_eod:
                        self.end_of_data = True

        return [None,None]
