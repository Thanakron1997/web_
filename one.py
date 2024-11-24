import json
import os
import pymongo

class funcMongoDB:
    def __init__(self):
        self.config_file = os.path.join(os.path.dirname(__file__),"config.json")
        self.config = None
        self.client = None
        self.db = None
        self.collection = None
        self.readConfig()
        self.connect_mongodb()
        self.index_ = 'subjectNumber'
    def readConfig(self):
        with open(self.config_file, 'r') as f:
            self.config = json.load(f)

    def connect_mongodb(self,collectionName = 'test',dbName = None):
        self.client = pymongo.MongoClient(
        host = self.config['mongodb']['host'],
        username= self.config['mongodb']['user'],
        password=self.config['mongodb']['password']
        )
        if dbName:
            self.db = self.client[dbName]
        else:
            self.db = self.client[self.config['mongodb']['db_name']]
        self.collection = self.db[collectionName]

    def get_data(self):
        # data = self.collection.find({},{'_id':0}):
        data = self.collection.find({})
        return data
    
    def addNewData(self,newData):
        insertedID = self.collection.insert_one(newData)
        return insertedID.inserted_id
    
    def update(self,data):
        self.collection.update_one({self.index_: str(data[self.index_])}, {'$set': data}, upsert=True)
    
    def delete9(self,subject):
        self.collection.delete_one({self.index_ : str(subject)})



test = funcMongoDB()
test.get_data()
