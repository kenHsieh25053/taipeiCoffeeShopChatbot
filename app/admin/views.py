from flask.globals import request
from flask_restful import Resource
from flask import current_app as app
from flask import jsonify, abort
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    set_access_cookies, unset_jwt_cookies
)

from ..chatbot.model import ShopModel, FavoriteModel
from .serializer import ShopSchema, FavoriteSchema, UserSchema
from .model import User
from app import db

shop_list_schema = ShopSchema(many=True)
shop_schema = ShopSchema()
favorite_list_schema = FavoriteSchema(many=True)
user_schema = UserSchema()
user_list_schema = UserSchema(many=True)

jwt = JWTManager(app)


class Login(Resource):

    def post(self):
        email = request.json['email']
        password = request.json['password']

        isUserExist = User.query.filter_by(email=email).first()

        if isUserExist is None:
            return 'invalid email'

        if isUserExist.verify_password(password) is False:
            return 'invalid password'

        access_token = create_access_token(identity=email)
        resp = jsonify({'login': True})
        set_access_cookies(resp, access_token)

        return resp


class Logout(Resource):

    def post(self):
        resp = jsonify({'logout': True})
        unset_jwt_cookies(resp)
        return resp


class ShopItem(Resource):

    @jwt_required
    def get(self, shop_id):
        shop = ShopModel.query.get(shop_id)
        return shop_schema.dump(shop)

    @jwt_required
    def put(self, shop_id):
        shop = ShopModel.query.get(shop_id)

        for key, value in request.json.items():
            setattr(shop, key, value)

        db.session.add(shop)
        db.session.commit()
        return request.json

    @jwt_required
    def delete(self, shop_id):
        ShopModel.query.filter_by(id=shop_id).delete()
        db.session.commit()
        return 'The shop has been deleted!'


class ShopList(Resource):

    @jwt_required
    def get(self):
        shops = ShopModel.query.all()
        return shop_list_schema.dump(shops)

    @jwt_required
    def post(self):
        exists = ShopModel.query.filter_by(
            name=request.json['name']).first() is not None

        if exists:
            return 'the shop is already exit!'

        shop = ShopModel(
            request.json['id'],
            request.json['name'],
            request.json['address'],
            request.json['latitude'],
            request.json['longitude'],
            request.json['open_hour'],
            request.json['close_date'],
            request.json['style'],
            request.json['price_level'],
            request.json['space'],
            request.json['plug_number'],
            request.json['comment'],
            request.json['map_url'],
            request.json['facebook']
        )

        db.session.add(shop)
        db.session.commit()
        shop = ShopModel.query.filter_by(name=request.json['name']).first()
        return shop_schema.dump(shop)


class FavoriteList(Resource):

    @jwt_required
    def get(self):
        favorites = FavoriteModel.query.all()
        return favorite_list_schema.dump(favorites)


class UserItem(Resource):

    @jwt_required
    def get(self, user_id):
        user = User.query.get(user_id)
        return shop_schema.dump(user)

    @jwt_required
    def put(self, user_id):
        user = User.query.get(user_id)

        errors = user_schema.validate(request.json)
        if errors:
            return abort(400, str(errors))

        for key, value in request.json.items():
            setattr(user, key, value)

        db.session.add(user)
        db.session.commit()
        return request.json

    @jwt_required
    def delete(self, user_id):
        User.query.filter_by(id=user_id).delete()
        db.session.commit()
        return 'The user has been deleted!'


class UserList(Resource):

    @jwt_required
    def get(self):
        users = User.query.all()
        return user_list_schema.dump(users)

    @jwt_required
    def post(self):
        exists = User.query.filter_by(
            email=request.json['email']).first() is not None

        if exists:
            return abort(400, 'the user is already exit!')

        errors = user_schema.validate(request.json)
        if errors:
            return abort(400, str(errors))

        user_schema.load(request.json)

        user = User(
            request.json['id'],
            request.json['email'],
            request.json['password'],
            request.json['active'],
            request.json['roles']
        )

        db.session.add(user)
        db.session.commit()
        user = User.query.filter_by(email=request.json['email']).first()

        return user_schema.dump(user)
