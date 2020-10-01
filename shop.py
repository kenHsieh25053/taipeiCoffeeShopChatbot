import math
from copy import deepcopy


class Shop():

    def __init__(self):
        pass

    def __get_distance_between_two_locations(self, event, shop):
        lat1 = event.message.latitude
        lon1 = event.message.longitude
        lat2 = shop['latitude']
        lon2 = shop['longitude']
        radius = 6371  # km

        dlat = math.radians(lat2-lat1)
        dlon = math.radians(lon2-lon1)
        a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) \
            * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        distance = radius * c
        shop['distance'] = distance

        return shop

    def get_shops(self, mongodb):
        return mongodb.get_data()

    def get_nearby_shops_by_location(self, event, mongodb):
        nearby_locations = []
        shops = mongodb.get_data()
        for shop in shops:
            shop_with_distance = self.__get_distance_between_two_locations(
                event, shop)
            if shop_with_distance['distance'] < 1:
                nearby_locations.append(shop_with_distance)

        sorted_nearby_locations = sorted(
            nearby_locations, key=lambda s: s['distance'])

        return sorted_nearby_locations[:10]

    def add_into_my_favorites(self, event, mongodb):
        shopId = event.postback.data
        userId = event.sourse.userId
        mongodb.insert_data({'userId': userId, 'shopId': shopId})
        return 'ok'

    def get_favorites(self, event, mongodb):
        userId = event.sourse.userId
        return mongodb.get_data_by_user_id(userId)

    def delete_favorite_shop(self, event, mongodb):
        favorite_id = event.postback.data
        mongodb.delete_data_in_favorites(favorite_id)
        return 'ok'
