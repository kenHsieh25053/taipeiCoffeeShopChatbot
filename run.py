from flask import Flask, request, abort
from handler import Handler
from db import MongoDb
import os

app = Flask(__name__)

os.environ.setdefault('STAGE', 'config.DevConfig')

app.config.from_object(os.environ['STAGE'])

CHANNEL_ACCESS_TOKEN = app.config['CHANNEL_ACCESS_TOKEN']
CHANNEL_SECRET = app.config['CHANNEL_SECRET']

MONGO_DB_URI = app.config['MONGO_DB_URI']
DB_NAME = app.config['DB_NAME']
COLLECTIONS = app.config['COLLECTIONS']

mongodb = MongoDb(MONGO_DB_URI, DB_NAME, COLLECTIONS)
handler = Handler(CHANNEL_ACCESS_TOKEN, CHANNEL_SECRET, mongodb)


@app.route('/callback', methods=['POST'])
def endpoint():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)

    handler.callback(signature, body)

    return 'OK'


if __name__ == "__main__":
    app.run(host=app.config['HOST'],
            port=app.config['PORT'], debug=app.config['DEBUG'],)
