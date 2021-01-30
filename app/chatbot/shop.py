import math
import random
import uuid
from .model import ShopModel, FavoriteModel
from app import db


class Shop():

    def get_shops_by_topics(self, event):
        action = event.postback.data.split('_')[1]

        if action == 'kensfavorites':
            names = (
                '鬧咖啡 NOW coffee',
                '這間咖啡',
                '515 Cafe&books'
            )
        elif action == 'nightcafe':
            names = [
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
        elif action == 'morningcafe':
            names = [
                '學校咖啡館 Ecole Cafe',
                '上島珈琲店(八德)',
                '在一起 One&Together',
                'Maven Coworking Cafe'
            ]
        else:
            names = [
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

        if len(names) > 12:
            names = random.sample(names, 12)

        raw_data = ShopModel.query.filter(ShopModel.name.in_(names)).all()
        shops = [data.__dict__ for data in raw_data]

        return shops

    def get_nearby_shops_by_location(self, event):
        nearby_locations = []
        raw_data = ShopModel.query.all()
        shops = [data.__dict__ for data in raw_data]

        for shop in shops:
            shop_with_distance = self.__get_distance_between_two_locations(
                event, shop)
            if shop_with_distance['distance'] < 1:
                nearby_locations.append(shop_with_distance)

        sorted_nearby_locations = sorted(
            nearby_locations, key=lambda s: s['distance'])

        return sorted_nearby_locations[:10]

    def add_into_my_favorites(self, event):
        shop = event.postback.data.split('_')[1]
        user_id = event.source.user_id

        exists = FavoriteModel.query.filter_by(
            user_id=user_id, shop=shop).first() is not None
        if exists:
            return False
        favorite = FavoriteModel(user_id, shop)
        db.session.add(favorite)
        db.session.commit()
        return shop

    def get_favorites(self, event):
        user_id = event.source.user_id
        exists = FavoriteModel.query.filter_by(
            user_id=user_id).first() is not None
        if exists:
            favorites = FavoriteModel.query.filter_by(user_id=user_id).all()
            favorites = [favorite.__dict__ for favorite in favorites]
            return favorites
        else:
            return False

    def delete_favorite_shop(self, event):
        shop_id = event.postback.data.split('_')[0]
        shop = event.postback.data.split('_')[1]
        FavoriteModel.query.filter_by(id=shop_id).delete()
        db.session.commit()
        return shop

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
