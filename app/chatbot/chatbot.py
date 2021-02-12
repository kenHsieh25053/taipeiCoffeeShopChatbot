from flask import Blueprint, request

from .controller import Controller

chatbot_bp = Blueprint(
    'chatbot_bp', __name__,
)

controller = Controller()


@chatbot_bp.route('/callback', methods=['POST'])
def endpoint():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    controller.callback(signature, body)

    return 'OK'
