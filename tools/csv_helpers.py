import csv
import codecs
import cStringIO

class TabDialect(csv.Dialect):
    """ dialect for tab separated values """
    def __init__(self):
        self.delimiter = '\t'
        self.quotechar = '"'
        self.escapechar = None
        self.doublequote = True
        self.skipinitialspace = False
        self.lineterminator = '\r\n'
        self.quoting = csv.QUOTE_MINIMAL
        csv.Dialect.__init__(self)

class CommaDialect(csv.Dialect):
    """ dialect for comma separated values """
    def __init__(self):
        self.delimiter = ','
        self.quotechar = '"'
        self.escapechar = None
        self.doublequote = True
        self.skipinitialspace = False
        self.lineterminator = '\r\n'
        self.quoting = csv.QUOTE_MINIMAL
        csv.Dialect.__init__(self)

""" unicode support from https://docs.python.org/2/library/csv.html#csv-examples """
class UTF8Recoder:
    """
    Iterator that reads an encoded stream and reencodes the input to UTF-8
    """
    def __init__(self, f, encoding):
        self.reader = codecs.getreader(encoding)(f)

    def __iter__(self):
        return self

    def next(self):
        return self.reader.next().encode("utf-8")

class UnicodeReader:
    """
    A CSV reader which will iterate over lines in the CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        f = UTF8Recoder(f, encoding)
        self.reader = csv.reader(f, dialect=dialect, **kwds)

    def next(self):
        row = self.reader.next()
        return [unicode(s, "utf-8") for s in row]

    def __iter__(self):
        return self
