import json
import os
import pymongo

class funcMongoDB:
    def __init__(self):
        self.config_file = os.path.join(os.path.dirname(__file__),"config.json")
        self.config = None
        self.readConfig()
    
    def readConfig(self):
        with open(self.config_file, 'r') as f:
            self.config = json.load(f)
        print(self.config)

    def connect_mongodb(self):
    client = pymongo.MongoClient(
        host = os.getenv(self.config['mongodb']['host']),
        username=os.getenv(self.config['mongodb']['user']),
        password=os.getenv(self.config['mongodb']['password']),
    )
    return client