import json
import os
import pymongo

class funcMongoDB:
    def __init__(self):
        self.config_file = os.path.join(os.path.dirname(__file__),"config.json")
        self.config = None
        self.client = None
        self.readConfig()
        self.connect_mongodb()

    def readConfig(self):
        with open(self.config_file, 'r') as f:
            self.config = json.load(f)


    def connect_mongodb(self):
        self.client = pymongo.MongoClient(
        host = os.getenv(self.config['mongodb']['host']),
        username=os.getenv(self.config['mongodb']['user']),
        password=os.getenv(self.config['mongodb']['password'])
        )

    def get_data(self):
        db = self.client[self.config['mongodb']['db_name']]
        collection = db['test']
        for x in collection.find():
            print(x)
    
    def update():
        db = self.client

test = funcMongoDB()
test.get_data()
