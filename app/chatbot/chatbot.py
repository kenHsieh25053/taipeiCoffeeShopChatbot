from flask import Blueprint, request

from .handler import Handler

chatbot_bp = Blueprint(
    'chatbot_bp', __name__,
)

handler = Handler()


@chatbot_bp.route('/callback', methods=['POST'])
def endpoint():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    handler.callback(signature, body)

    return 'OK'
