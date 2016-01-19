import pymongo
import logging

from conf import settings

class GritsMongoConnection(object):
    """ class that contains the connection details to mongo

        Also contains common methods that are more complicated than a simple
        find_one query, such as bulk_upsert and insert_many.
    """
    @property
    def db(self):
        """ pymongo Database object """
        return self._db

    def __init__(self, program_arguments, *args, **kwargs):
        """ GritsMongoConnection constructor
            Parameters
            ----------
                program_arguments : dict
                    A dictionary of arguments collected by the argparse
                    command-line program
        """
        #self._program_arguments = program_arguments
        self._hostname = program_arguments.mongohost
        self._username = program_arguments.username
        self._password = program_arguments.password
        self._database = program_arguments.database
        self._client = None
        self._db = self.connect()

    def connect(self):
        """ connect to mongoDB

            The method creates the uri to connect to the mongoDB using
            the supplied command-line arguments or default values.
        """
        if self._username != None or self._password != None:
            uri = 'mongodb://%s:%s@%s/%s?authMechanism=MONGODB-CR' % \
                (self._username, self._password, self._hostname, self._database)
        else:
            uri = 'mongodb://%s/%s' % \
                (self._hostname, self._database)
        self._client = pymongo.MongoClient(uri)
        return pymongo.database.Database(self._client, self._database)

    def ensure_indexes(self, *args):
        """ creates indexes on the collections if they do not exist """
        airports = pymongo.collection.Collection(self._db, settings._AIRPORT_COLLECTION_NAME)
        airports.create_index([("loc", pymongo.GEOSPHERE)])
        airports.create_index([
				("_id", pymongo.ASCENDING),
				("name", pymongo.TEXT),
				("city", pymongo.TEXT),
				("state", pymongo.TEXT),
				("stateName", pymongo.TEXT),
				("country", pymongo.TEXT),
				("countryName", pymongo.TEXT),
				("globalRegion", pymongo.TEXT),
				("notes", pymongo.TEXT)
			],
			weights={
				"notes": 1,
				"globalRegion": 2,
				"countryName": 3,
				"country": 4,
				"stateName": 5,
				"state": 6,
				"city": 7,
				"name": 8
			},
			name="idxAirports")
        flights = pymongo.collection.Collection(self._db, settings._FLIGHT_COLLECTION_NAME)
        flights.create_index([("departureAirport.loc", pymongo.GEOSPHERE)])
        flights.create_index([("arrivalAirport.loc", pymongo.GEOSPHERE)])
        # Stand-alone dates (min/max date ranges)
        flights.create_index([
                ("effectiveDate", pymongo.DESCENDING)
            ], name="idxFlights_EffectiveDateDescending")
        flights.create_index([
                ("discontinuedDate", pymongo.DESCENDING)
            ], name="idxFlights_DiscontinuedDateDescending")
        # Departure Airport Combinations
        flights.create_index([
                ("departureAirport._id", pymongo.ASCENDING),
                ("discontinuedDate", pymongo.ASCENDING),
                ("effectiveDate", pymongo.ASCENDING),
                ("stops", pymongo.ASCENDING),
                ("totalSeats", pymongo.ASCENDING),
                ("weeklyFrequency", pymongo.ASCENDING)
            ], name="idxFlights_DepartureAirportDatesStopsTotalSeatsWeeklyFrequency")
        return "Indexes have been applied."

    @staticmethod
    def format_bulk_write_results(result):
        """ BulkWriteResult object, as defined:

            http://api.mongodb.org/python/current/api/pymongo/results.html#pymongo.results.BulkWriteResult
        """
        if result == None:
            return {}

        keys = ['nInserted', 'nMatched', 'nModified', 'nRemoved', 'nUpserted']
        formatted_result = {}

        for key in keys:
            if key in result:
                formatted_result[key] = result[key]

        return formatted_result

    @staticmethod
    def format_insert_many_results(result):
        """ InsertManyResult object, as defined:

            http://api.mongodb.org/python/current/api/pymongo/results.html#pymongo.results.InsertManyResult
        """
        if result == None:
            return {}

        formatted_result = {}

        ids = result.inserted_ids
        formatted_result['nInserted'] = len(ids)

        return formatted_result


    def bulk_upsert(self, collection_name, records):
        """ bulk upsert of documents into mongodb collection

            Parameters
            ----------
                collection_name: str
                    The name of the mongoDB collection
                records: list
                    A list of record.fields.
        """
        if len(records) == 0:
            return

        collection = pymongo.collection.Collection(self._db, collection_name)
        bulk = collection.initialize_ordered_bulk_op()
        for record in records:
            bulk.find({'_id': record.id}).upsert().update({
                '$set': record.fields})

        result = None
        try:
            result = bulk.execute()
        except pymongo.errors.BulkWriteError as e:
            logging.error(e.details)

        return GritsMongoConnection.format_bulk_write_results(result)

    def insert_many(self, collection_name, records):
        """ inserts many documents into mongodb collection
            Parameters
            ----------
                collection_name: str
                    The name of the mongoDB collection
                records: list
                    A list of records.
        """
        if len(records) == 0:
            return

        record_fields = map(lambda x: x.fields, records)

        collection = pymongo.collection.Collection(self._db, collection_name)

        result = None
        try:
            result = collection.insert_many(record_fields)
        except Exception as e:
            logging.error(e)

        return GritsMongoConnection.format_insert_many_results(result)
