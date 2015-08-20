import os
import argparse
import logging
logging.basicConfig(level=logging.DEBUG)

_FILE_TYPES = ['.tsv']

class GritsConsumer(object):
    """ Command line tool to parse grits transportation network data """
    
    def __init__(self):
        self.verbose = False
        self.parser = argparse.ArgumentParser(description='script to parse ' \
            'the grits transportation network data file and populate ' \
            'a mongodb collection.')
    
    @staticmethod
    def file_extension(file):
        parts = os.path.splitext(file.name)
        ext = ''
        if len(parts) > 1:
            ext = parts[-1].lower()
        return ext
    
    def is_valid_file_type(self, file):
        ext = GritsConsumer.file_extension(file)
        if ext not in _FILE_TYPES:
            return False
        return True
    
    def get_args(self):
        self.parser.add_argument('-v', '--verbose',
            action="store_true",
            help="verbose output" )
        
        self.parser.add_argument('infile',
            type=argparse.FileType('r'),
            help="file to be parsed")
        
        return self.parser.parse_args()
    
    def run(self):
        args = self.get_args()
        file = args.infile
        if not self.is_valid_file_type(file):
            msg = 'not a valid file type %r' % _FILE_TYPES
            self.parser.error(msg)
        logging.debug('args:%r', args)

if __name__ == '__main__':
    cmd = GritsConsumer()
    cmd.run()