import json
import os
import pymongo
from bson.objectid import ObjectId

class funcMongoDB:
    def __init__(self,index_ = None):
        self.config_file = os.path.join(os.path.dirname(__file__),"config.json")
        self.config = None
        self.client = None
        self.db = None
        self.collection = None
        self.readConfig()
        # self.connect_mongodb()
        if index_:
            self.index_ = index_
        else:
            self.index_ = '_id'
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

    def loginUser(self,usersName):
        client = pymongo.MongoClient(
        host = self.config['mongodb']['host'],
        username= self.config['mongodb']['login'],
        password=self.config['mongodb']['loginPass']
        )
        
        db = client['login']
        collection = db['users']
        users_ = collection.find_one({'user':usersName})
        client.close()
        return users_
    
    def get_data(self):
        # data = self.collection.find({},{'_id':0}):
        data = self.collection.find({})
        return data.to_list()
    
    def findOne(self,id):
        if self.index_ == '_id':
            data = self.collection.find_one({self.index_:ObjectId(id)})
        else:
            data = self.collection.find_one({self.index_:str(id)})
        return data

    def addNewData(self,newData):
        insertedID = self.collection.insert_one(newData)
        return insertedID.inserted_id
    
    def update(self,data):
        
        if self.index_ == '_id':
            id_ = data[self.index_]
            if '_id' in data:
                data.pop('_id')
            self.collection.update_one({self.index_: ObjectId(id_)}, {'$set': data}, upsert=True)
        else:
            self.collection.update_one({self.index_: str(data[self.index_])}, {'$set': data}, upsert=True)
    
    def delete(self,subject):
        if self.index_ == '_id':
            self.collection.delete_one({self.index_ : ObjectId(subject)})
        else:
            self.collection.delete_one({self.index_ : str(subject)})

    def stopClient(self,stopConnect=False):
        if stopConnect:
            self.client.close()

# test = funcMongoDB(index_='name')
# data = test.get_data()
# print(data)
# x = test.addNewData({'name':'test2','email':'test2@mail.com','age':22})
# if x:
#     print("update!")
# # test.delete("tdfsfd")