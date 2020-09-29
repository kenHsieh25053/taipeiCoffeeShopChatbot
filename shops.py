from db import MongoDb
import math


class Shops():

    def __init__(self):
        pass

    def __get_distance_between_two_locations(self, lat1, lon1, lat2, lon2):
        radius = 6371  # km

        dlat = math.radians(lat2-lat1)
        dlon = math.radians(lon2-lon1)
        a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) \
            * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        distance = radius * c

        return distance

    def get_shops(self, mongodb):
        return mongodb.get_data()

    def get_nearby_shops_by_location(self, event, mongodb):
        nearby_locations = []
        shops = mongodb.get_data()
        for shop in shops:
            distance = self.__get_distance_between_two_locations(
                event.message.latitude, event.message.longitude, shop['latitude'], shop['longitude'])
            if distance < 1:
                nearby_locations.append(shop)

        return nearby_locations

    def add_into_my_favorites(self):
        pass
