from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app(stage):  # Flask factory pattern

    app = Flask(__name__)

    app.config.from_object(stage)

    db.init_app(app)

    # 導入 Blueprints
    with app.app_context():
        from .chatbot import chatbot
        from .admin import admin
        app.register_blueprint(chatbot.chatbot_bp)
        app.register_blueprint(admin.admin_bp)

    return app
