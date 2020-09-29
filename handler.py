from linebot import (
    LineBotApi, WebhookParser
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    TextMessage, TextSendMessage, FlexSendMessage
)

from shops import Shops

shops = Shops()


class Handler:

    def __init__(self, CHANNEL_ACCESS_TOKEN, CHANNEL_SECRET, mongodb):
        self.CHANNEL_ACCESS_TOKEN = CHANNEL_ACCESS_TOKEN
        self.CHANNEL_SECRET = CHANNEL_SECRET
        self.mongodb = mongodb

    def callback(self, signature, body):
        parser = WebhookParser(self.CHANNEL_SECRET)
        # handle webhook body
        try:
            events = parser.parse(body, signature)
            self.__handle_message(events)
        except InvalidSignatureError as e:
            print(e)

    def __handle_message(self, events):
        line_bot_api = LineBotApi(self.CHANNEL_ACCESS_TOKEN)
        for event in events:
            if event.message.type == 'location':
                nearby_shops = shops.get_nearby_shops_by_location(
                    event, self.mongodb)

                line_bot_api.reply_message(
                    event.reply_token,
                    FlexSendMessage(map(self.__flex_message(), nearby_shops))
                )
            else:
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text="didn't get you!"))

    def __flex_message(self, shop):
        pass

    # todo
    # simple factory
    # def __handle_text_message():
