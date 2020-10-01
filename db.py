from pymongo import MongoClient


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

    def get_data(self):
        db = self.client[self.DB_NAME]
        shops = db[self.COLLECTIONS[0]]
        return [shop for shop in shops.find()]

    def get_data_by_user_id(self, userId):
        db = self.client[self.DB_NAME]
        shops = db[self.COLLECTIONS[0]]
        favorites = db[self.COLLECTIONS[1]]
        favorite_shops = []
        favorite_shop_ids = [favorite for favorite in favorites.find(userId)]
        for favorite_shop_id in favorite_shop_ids:
            favorite_shop = shops.find_one(favorite_shop_id.shopId)
            favorite_shop['favorite_id'] = favorites.objectId
            favorite_shops.append(favorite_shop)
        return favorite_shops

    def delete_data_in_favorites(self, favorite_id):
        db = self.client[self.DB_NAME]
        favorites = db[self.COLLECTIONS[1]]
        favorites.delete_one(favorite_id)
