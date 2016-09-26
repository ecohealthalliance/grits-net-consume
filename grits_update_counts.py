import sys
import argparse
import datetime
from tools.grits_mongo import GritsMongoConnection

from conf import settings

# def update_counts(flights, legs):

# def get_counts():
parser = argparse.ArgumentParser()

def add_args():
    """ add arguments to the argparse command-line program """
    parser.add_argument('-v', '--verbose',
        action="store_true",
        help="verbose output" )

    parser.add_argument('-u', '--username',
        default=settings._MONGO_USERNAME,
        help='the username for mongoDB (Default: None)')

    parser.add_argument('-p', '--password',
        default=settings._MONGO_PASSWORD,
        help='the password for mongoDB (Default: None)')

    parser.add_argument('-d', '--database',
        default=settings._MONGO_DATABASE,
        help='the database for mongoDB (Default: grits)')

    parser.add_argument('-m', '--mongohost',
        default=settings._MONGO_HOST,
        help='the hostname for mongoDB (Default: localhost)')

    parser.add_argument('infile',
        type=argparse.FileType('rb'),
        help="the file to be parsed")

if __name__ == '__main__':

  add_args()
  program_args = parser.parse_args(sys.argv)
  # print program_args
  # setup the mongoDB connection
  mongo_connection = GritsMongoConnection(program_args)
  db = mongo_connection.db;
  num_flights = db.flights.count();
  num_legs = db.legs.count();
  historyRecord = {
    'date': datetime.datetime.utcnow(),
    'counts': {
      'legs': num_legs,
      'flights': num_flights
    }
  }

  db.historicalData.insert(historyRecord)