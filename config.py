from os import environ, path
from dotenv import load_dotenv
import os

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))


class Config:
    """Base config."""
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SESSION_COOKIE_NAME = os.environ.get('SESSION_COOKIE_NAME')
    CHANNEL_ACCESS_TOKEN = os.environ.get('CHANNEL_ACCESS_TOKEN')
    CHANNEL_SECRET = os.environ.get('CHANNEL_SECRET')


class ProdConfig(Config):
    FLASK_ENV = 'production'
    DEBUG = False
    TESTING = False
    DATABASE_URI = os.environ.get('PROD_DATABASE_URI')
    CHANNEL_ACCESS_TOKEN = os.environ.get('CHANNEL_ACCESS_TOKEN')
    CHANNEL_SECRET = os.environ.get('CHANNEL_SECRET')
    DB_NAME = os.environ.get('PRODUCTION_DB_NAME')
    COLLECTIONS = ('coffeeshops', 'favorites')
    MONGO_DB_URI = os.environ.get('DB_URI_PROD')
    HOST = os.environ.get('HEROKU_HOST')
    PORT = 80


class DevConfig(Config):
    FLASK_ENV = 'development'
    DEBUG = True
    TESTING = True
    DATABASE_URI = os.environ.get('DEV_DATABASE_URI')
    CHANNEL_ACCESS_TOKEN = os.environ.get('CHANNEL_ACCESS_TOKEN')
    CHANNEL_SECRET = os.environ.get('CHANNEL_SECRET')
    MONGO_DB_URI = os.environ.get('DB_URI_DEV')
    DB_NAME = 'devdb'
    COLLECTIONS = ('coffeeshops', 'favorites')
    HOST = '0.0.0.0'
    PORT = 5000
