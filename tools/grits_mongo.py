import pymongo
import logging

class GritsMongoConnection(object):
    
    @property
    def db(self):
        return self._db
    
    def __init__(self, program_arguments, *args, **kwargs):
        #self._program_arguments = program_arguments
        self._hostname = program_arguments.mongohost
        self._username = program_arguments.username
        self._password = program_arguments.password
        self._database = program_arguments.database
        self._client = None
        self._db = self.connect()
        self.ensure_indexes()
    
    def connect(self):
        if self._username != None or self._password != None:
            uri = 'mongodb://%s:%s@%s/%s?authMechanism=MONGODB-CR' % \
                (self._username, self._password, self._hostname, self._database)
        else:
            uri = 'mongodb://%s/%s' % \
                (self._hostname, self._database)
        self._client = pymongo.MongoClient(uri)
        return pymongo.database.Database(self._client, self._database)
    
    def ensure_indexes(self):
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
    def format_bulk_results(result):
        if result == None:
            return {}
        
        keys = ['nInserted', 'nMatched', 'nModified', 'nRemoved', 'nUpserted']
        formatted_result = {}
        
        for key in keys:
            if key in result:
                formatted_result[key] = result[key]
        
        return formatted_result
    
    def bulk_upsert(self, collection_name, key_name, records):
        if len(records) == 0:
            return
        
        collection = pymongo.collection.Collection(self._db, collection_name)
        bulk = collection.initialize_ordered_bulk_op()
        for record in records:
            bulk.find({key_name: record.fields[key_name]}).upsert().update({
                '$set': record.fields})
        
        result = None
        try:
            result =  bulk.execute()
        except pymongo.errors.BulkWriteError as e:
            logging.error(e.details)
        
        return GritsMongoConnection.format_bulk_results(result)
    
    def insert_many(self, collection_name, records):
        if len(records) == 0:
            return
        
        collection = pymongo.collection.Collection(self._db, collection_name)
        return collection.insert_many(records)