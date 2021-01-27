from flask import Blueprint
from flask import current_app as app
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from .. import db
from ..chatbot.model import Shop


admin_bp = Blueprint(
    'admin_bp', __name__,
    template_folder='templates'
)


@admin_bp.route('/admin', methods=['GET'])
def admin():
    pass


admin = Admin(app, name='Tpe coffee shop chatbot admin',
              template_mode='bootstrap4')

admin.add_view(ModelView(Shop, db.session))
