from flask import Blueprint
from flask_restful import Api

from .views import ShopList, ShopItem, FavoriteList, UserList, UserItem, Login, Logout

admin_bp = Blueprint('admin_bp', __name__)

api = Api(admin_bp)

# routers
api.add_resource(Login, '/api/login')
api.add_resource(Logout, '/api/logout')
api.add_resource(ShopItem, '/api/shop/<shop_id>')
api.add_resource(ShopList, '/api/shops')
api.add_resource(FavoriteList, '/api/favorites')
api.add_resource(UserItem, '/api/user/<user_id>')
api.add_resource(UserList, '/api/users')
