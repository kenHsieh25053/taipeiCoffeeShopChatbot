from linebot import (
    LineBotApi, WebhookParser
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    TextMessage, TextSendMessage, FlexSendMessage
)
import json
from bson.objectid import ObjectId
from copy import deepcopy
from shop import Shop

shop = Shop()


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
                nearby_shops = shop.get_nearby_shops_by_location(
                    event, self.mongodb)

                if len(nearby_shops) < 1:
                    line_bot_api.reply_message(
                        event.reply_token,
                        TextSendMessage(text="尚未探索這區～"))
                    return

                with open('flexmessage.json') as file:
                    template = json.load(file)

                flex_messages = {
                    "type": "carousel",
                    "contents": [deepcopy(self.__flex_message(nearby_shop, template)) for nearby_shop in nearby_shops]
                }

                line_bot_api.reply_message(
                    event.reply_token, FlexSendMessage(alt_text='店家資訊', contents=flex_messages))
            elif event.message.type == 'postback':
                if event.message.label == '加入最愛':
                    shop.add_into_my_favorites(event, self.mongodb)
                    line_bot_api.reply_message(
                        event.reply_token, TextSendMessage(text="已加入!"))
                else:
                    shop.delete_favorite_shop(event, self.mongodb)
                    line_bot_api.reply_message(
                        event.reply_token,
                        TextSendMessage(text="已移除!"))
            elif event.message.text == '我的最愛':
                favorite_shops = shop.get_favorites(event, self.mongodb)
                favorites_flex_messages = map(
                    self.__favorites_flex_message(template), favorite_shops)
                line_bot_api.reply_message(
                    event.reply_token,
                    FlexSendMessage(json.dumps(favorites_flex_messages))
                )
            else:
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text="don't get you!"))

    def __flex_message(self, nearby_shop, template):
        template['body']['contents'][0]['text'] = nearby_shop['shop_name']
        template['body']['contents'][1]['contents'][0]['contents'][1]['text'] = nearby_shop['address']
        template['body']['contents'][1]['contents'][1]['contents'][1]['text'] = nearby_shop['open_hour']
        template['body']['contents'][1]['contents'][2]['contents'][1]['text'] = nearby_shop['close_date']
        template['body']['contents'][1]['contents'][3]['contents'][1]['text'] = nearby_shop['style']
        template['body']['contents'][1]['contents'][4]['contents'][1]['text'] = nearby_shop['plug_number']
        template['body']['contents'][1]['contents'][5]['contents'][1]['text'] = nearby_shop['space']
        template['body']['contents'][1]['contents'][6]['contents'][1]['text'] = nearby_shop['comment']
        template['footer']['contents'][0]['action']['uri'] = nearby_shop['map_url']
        template['footer']['contents'][1]['action']['uri'] = nearby_shop['facebook']
        template['footer']['contents'][2]['action']['data'] = str(
            nearby_shop['_id'])

        return template

    def __favorites_flex_message(self, shop, favorites, template):
        template.body.contents[0].text = favorites.favoritesName
        template.body.contents[1].contents[1].text = favorites.address
        template.body.contents[2].contents[1].text = favorites.openHour
        template.body.contents[3].contents[1].text = favorites.closeDate
        template.body.contents[4].contents[1].text = favorites.style
        template.body.contents[5].contents[1].text = favorites.plugNumber
        template.body.contents[6].contents[1].text = favorites.space
        template.body.contents[7].contents[1].text = favorites.comment
        template.footer.contents[1].action.uri = shop.map_url
        template.footer.contents[2].action.data = favorites.favorite_id

        return template
