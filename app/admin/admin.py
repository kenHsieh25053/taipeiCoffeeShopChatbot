from flask import Blueprint, render_template
from flask import current_app as app
from flask_admin import Admin

from .. import db
from ..chatbot.model import ShopModel, FavoriteModel
from .views import ShopAdmin, FavoriteAdmin


admin_bp = Blueprint(
    'admin_bp', __name__
)


@admin_bp.route('/admin', methods=['GET'])
def admin():
    pass


# admin setting
admin = Admin(app, name='Chatbot Admin',
              template_mode='bootstrap4')

# register models
admin.add_view(ShopAdmin(ShopModel, db.session))
admin.add_view(FavoriteAdmin(FavoriteModel, db.session))
