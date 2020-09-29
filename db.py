from pymongo import MongoClient


class MongoDb():

    def __init__(self, MONGO_DB_URI, DB_NAME, COLLECTION):
        self.client = MongoClient(MONGO_DB_URI)
        self.DB_NAME = DB_NAME
        self.COLLECTION = COLLECTION

    def insert_bulk_data(self, data):
        db = self.client[self.DB_NAME]
        shops = db[self.COLLECTION]
        shops.insert_many(data)

    def get_data(self):
        db = self.client[self.DB_NAME]
        shops = db[self.COLLECTION]
        return [shop for shop in shops.find()]

    def get_data_by(self):
        pass
