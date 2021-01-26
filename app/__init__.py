from flask import Flask, request
from .handler import Handler
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

db = SQLAlchemy()
handler = Handler()


def create_app(stage):  # Flask factory pattern

    app = Flask(__name__)

    app.config.from_object(stage)

    CHANNEL_ACCESS_TOKEN = app.config['CHANNEL_ACCESS_TOKEN']
    CHANNEL_SECRET = app.config['CHANNEL_SECRET']

    db.init_app(app)

    from .model import Shop

    admin = Admin(app, name='Tpe coffee shop chatbot admin',
                  template_mode='bootstrap4')

    admin.add_view(ModelView(Shop, db.session))

    @app.route('/callback', methods=['POST'])
    def endpoint():
        # get X-Line-Signature header value
        signature = request.headers['X-Line-Signature']

        # get request body as text
        body = request.get_data(as_text=True)

        handler.callback(signature, body)

        return 'OK'

    return app
