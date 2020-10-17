from pymongo import MongoClient
from bson.objectid import ObjectId


class MongoDb():

    def __init__(self, MONGO_DB_URI, DB_NAME, COLLECTIONS):
        self.client = MongoClient(MONGO_DB_URI)
        self.DB_NAME = DB_NAME
        self.COLLECTIONS = COLLECTIONS

    def insert_data(self, data):
        db = self.client[self.DB_NAME]
        my_favorites = db[self.COLLECTIONS[1]]
        my_favorites.insert_one(data)

    def insert_bulk_data(self, data):
        db = self.client[self.DB_NAME]
        shops = db[self.COLLECTIONS[0]]
        shops.insert_many(data)

    def get_data(self, from_table, query=None):
        db = self.client[self.DB_NAME]
        if from_table == 'shops':
            shops = db[self.COLLECTIONS[0]]
            return [shop for shop in shops.find(query)]
        else:
            favorites = db[self.COLLECTIONS[1]]
            return [shop for shop in favorites.find(query)]

    def get_data_by_user_id(self, user_id):
        db = self.client[self.DB_NAME]
        favorites = db[self.COLLECTIONS[1]]
        favorite_shops = [
            favorite for favorite in favorites.find({'user_id': user_id})]
        return favorite_shops

    def delete_data_in_favorites(self, favorite_id):
        db = self.client[self.DB_NAME]
        favorites = db[self.COLLECTIONS[1]]
        result = favorites.delete_one(
            {"_id": ObjectId(favorite_id)}).deleted_count
        return result
