import pymongo
import logging

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
        self.ensure_indexes()
    
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
    
    def ensure_indexes(self):
        """ creates indexes on the collections if they do not exist """
        airports = pymongo.collection.Collection(self._db, 'airports')
        airports.create_index([("key", pymongo.ASCENDING)], unique=True)
        airports.create_index([("loc", pymongo.GEOSPHERE)])
        flights = pymongo.collection.Collection(self._db, 'flights')
        flights.create_index([("key", pymongo.ASCENDING)], unique=True)
        flights.create_index([("Orig.Code", pymongo.ASCENDING)])
        flights.create_index([("Dest.Code", pymongo.ASCENDING)])
        flights.create_index([("Orig.loc", pymongo.GEOSPHERE)])
        flights.create_index([("Dest.loc", pymongo.GEOSPHERE)])
    
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
        
    
    def bulk_upsert(self, collection_name, key_name, records):
        """ bulk upsert of documents into mongodb collection 
            
            Parameters
            ----------
                collection_name: str
                    The name of the mongoDB collection
                key_name: str
                    The name of the unique key to find existing records,
                    required for the concept of an upsert
                records: list
                    A list of record.fields.
        """
        if len(records) == 0:
            return
        
        collection = pymongo.collection.Collection(self._db, collection_name)
        bulk = collection.initialize_ordered_bulk_op()
        for record in records:
            bulk.find({key_name: record[key_name]}).upsert().update({
                '$set': record})
        
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
                    A list of record.fields.
        """
        if len(records) == 0:
            return
        
        collection = pymongo.collection.Collection(self._db, collection_name)
        
        result = None
        try:
            result = collection.insert_many(records)
        except Exception as e:
            logging.error(e)
            
        return GritsMongoConnection.format_insert_many_results(result)