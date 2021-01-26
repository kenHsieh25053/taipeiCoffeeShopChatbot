import math
from copy import deepcopy
import random


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
        return mongodb.get_data('shops')

    def get_shops_by_topics(self, event, mongodb):
        action = event.postback.data.split('_')[1]

        if action == 'kensfavorites':
            query = {
                'shop_name': {'$in': [
                    '鬧咖啡 NOW coffee',
                    '這間咖啡',
                    '515 Cafe&books'
                ]}
            }
            shops = mongodb.get_data('shops', query)
        elif action == 'nightcafe':
            nightcafe = [
                '鬧咖啡 NOW coffee',
                '這間咖啡',
                '515 Cafe&books',
                '杯盃 PuiBui Cafe & Lounge',
                'Cafe Kuroshio．咖啡黑潮',
                '未央咖啡店',
                '早秋咖啡 Cafe Macho',
                'picnic野餐咖啡',
                '自由51',
                '2J CAFE',
                '看電車咖啡館',
                '391tpe',
                '淡水長堤咖啡餐館',
                '咖啡小自由',
                'Congrats Café',
                'Remember Me_記得我．Café',
                '路上撿到一隻貓',
                '黑露咖啡館 OLO Coffee Roasters',
                'Uranium Cafe 鈾咖啡餐酒館'
            ]
            query = {
                'shop_name': {'$in': random.choices(nightcafe, k=10)}
            }
            shops = mongodb.get_data('shops', query)
        elif action == 'morningcafe':
            query = {
                'shop_name': {'$in': [
                    '學校咖啡館 Ecole Cafe',
                    '上島珈琲店(八德)',
                    '在一起 One&Together',
                    'Maven Coworking Cafe'
                ]}
            }
            shops = mongodb.get_data('shops', query)
        else:
            spacious = [
                '鬧咖啡 NOW coffee',
                '515 Cafe&books',
                '學校咖啡館 Ecole Cafe',
                'ImPerfect Café',
                '喜鵲咖啡',
                '璐巴咖啡店',
                '特有種商行',
                '上島珈琲店(八德)',
                'POLAR CAFE 西門旗艦店',
                '391tpe',
                '舒服生活 Truffles Living',
                'CAFE RACO',
                'Saturn Landing Turkish Coffee 登陸土星土耳其咖啡永康店',
                '在一起 One&Together'
            ]
            query = {
                'shop_name': {'$in': random.choices(spacious, k=10)}
            }
            shops = mongodb.get_data('shops', query)
        return shops

    def get_nearby_shops_by_location(self, event, mongodb):
        nearby_locations = []
        shops = mongodb.get_data('shops')
        for shop in shops:
            shop_with_distance = self.__get_distance_between_two_locations(
                event, shop)
            if shop_with_distance['distance'] < 1:
                nearby_locations.append(shop_with_distance)

        sorted_nearby_locations = sorted(
            nearby_locations, key=lambda s: s['distance'])

        return sorted_nearby_locations[:10]

    def add_into_my_favorites(self, event, mongodb):
        shop_name = event.postback.data.split('_')[1]
        shop_id = event.postback.data.split('_')[2]
        user_id = event.source.user_id
        query_statement = {
            "$and": [{"user_id": user_id}, {"shop_id": shop_id}]}
        print(query_statement)
        is_exist = mongodb.get_data('favorites', query_statement)
        if is_exist:
            return False
        else:
            mongodb.insert_data(
                {'user_id': user_id, 'shop_id': shop_id, 'shop_name': shop_name})
            return True

    def get_favorites(self, event, mongodb):
        user_id = event.source.user_id
        return mongodb.get_data_by_user_id(user_id)

    def delete_favorite_shop(self, event, mongodb):
        favorite_id = event.postback.data
        result = mongodb.delete_data_in_favorites(favorite_id)
        return result
