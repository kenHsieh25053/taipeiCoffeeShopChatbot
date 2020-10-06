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
from copy import deepcopy
from shop import Shop


class Handler:

    shop = Shop()

    def __init__(self, CHANNEL_ACCESS_TOKEN, CHANNEL_SECRET, mongodb):
        self.CHANNEL_ACCESS_TOKEN = CHANNEL_ACCESS_TOKEN
        self.CHANNEL_SECRET = CHANNEL_SECRET
        self.mongodb = mongodb
        self.shop = Shop()

    def callback(self, signature, body):
        parser = WebhookParser(self.CHANNEL_SECRET)

        try:
            events = parser.parse(body, signature)
            self.__handle_message(events[0])
        except InvalidSignatureError as e:
            print(e)

    def __handle_message(self, event):
        line_bot_api = LineBotApi(self.CHANNEL_ACCESS_TOKEN)
        if event.type == 'message':
            if event.message.type == 'location':
                nearby_shops = self.shop.get_nearby_shops_by_location(
                    event, self.mongodb)

                if nearby_shops:
                    with open('./templates/flexmessage.json') as file:
                        flex_message_template = json.load(file)
                    flex_messages = {
                        "type": "carousel",
                        "contents": [deepcopy(self.__flex_message(nearby_shop, flex_message_template)) for nearby_shop in nearby_shops]
                    }
                    line_bot_api.reply_message(
                        event.reply_token, FlexSendMessage(alt_text='店家資訊', contents=flex_messages))
                else:
                    line_bot_api.reply_message(
                        event.reply_token,
                        TextSendMessage(text="尚未探索這區～"))

            elif event.message.text == 'favorites':
                favorite_shops = self.shop.get_favorites(
                    event, self.mongodb)

                if favorite_shops:
                    with open('./templates/favorites.json') as file:
                        favorites_template = json.load(file)

                    line_bot_api.reply_message(
                        event.reply_token,
                        FlexSendMessage(alt_text='最愛清單', contents=self.__favorites_flex_message(
                            favorite_shops, favorites_template))
                    )
                else:
                    line_bot_api.reply_message(
                        event.reply_token,
                        TextSendMessage(text="尚未加入我的最愛"))
            else:
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text="對不起，我不了解您的問題"))
        else:
            # postback actions
            action = event.postback.data.split('_')[0]
            if action == 'favorite':
                favorite_shops = self.shop.get_favorites(
                    event, self.mongodb)
                if len(favorite_shops) > 9:
                    line_bot_api.reply_message(
                        event.reply_token,
                        TextSendMessage(text="最愛店家已達十筆，請先刪除店家再進行新增！"))
                    return None
                result = self.shop.add_into_my_favorites(
                    event, self.mongodb)
                if result:
                    line_bot_api.reply_message(
                        event.reply_token, TextSendMessage(text="加入成功"))
                else:
                    line_bot_api.reply_message(
                        event.reply_token, TextSendMessage(text="已加入"))
            elif action == 'deleteshop':
                favorite_shops = self.shop.get_favorites(
                    event, self.mongodb)

                with open('./templates/favoritesComfirmMessage.json') as file:
                    favorites_confirm_message_template = json.load(file)

                favorites_confirm_messages = {
                    "type": "carousel",
                    "contents": [deepcopy(self.__favorites_confirm_flex_message(favorite_shop, favorites_confirm_message_template)) for favorite_shop in favorite_shops]
                }
                line_bot_api.reply_message(
                    event.reply_token,
                    FlexSendMessage(alt_text='確認刪除清單',
                                    contents=favorites_confirm_messages)
                )
            else:
                result = self.shop.delete_favorite_shop(
                    event, self.mongodb)
                if result:
                    line_bot_api.reply_message(
                        event.reply_token,
                        TextSendMessage(text="已移除!"))
                else:
                    line_bot_api.reply_message(
                        event.reply_token,
                        TextSendMessage(text="找不到結果"))

    def __flex_message(self, nearby_shop, flex_message_template):
        flex_message_template['body']['contents'][0]['text'] = nearby_shop['shop_name']
        flex_message_template['body']['contents'][1]['contents'][0]['contents'][1]['text'] = nearby_shop['address']
        flex_message_template['body']['contents'][1]['contents'][1]['contents'][1]['text'] = nearby_shop['open_hour']
        flex_message_template['body']['contents'][1]['contents'][2]['contents'][1]['text'] = nearby_shop['close_date']
        flex_message_template['body']['contents'][1]['contents'][3]['contents'][1]['text'] = nearby_shop['style']
        flex_message_template['body']['contents'][1]['contents'][4]['contents'][1]['text'] = nearby_shop['plug_number']
        flex_message_template['body']['contents'][1]['contents'][5]['contents'][1]['text'] = nearby_shop['space']
        flex_message_template['body']['contents'][1]['contents'][6]['contents'][1]['text'] = nearby_shop['comment']
        flex_message_template['footer']['contents'][0]['action']['uri'] = nearby_shop['map_url']
        flex_message_template['footer']['contents'][1]['action']['uri'] = nearby_shop['facebook']
        flex_message_template['footer']['contents'][2]['action']['data'] = 'favorite' + \
            '_' + nearby_shop['shop_name'] + '_' + str(nearby_shop['_id'])

        return flex_message_template

    # todo
    def __favorites_flex_message(self, favorite_shops, favorites_template):
        for favorite_shop in favorite_shops:
            flex_message = {
                "type": "box",
                "layout": "vertical",
                "contents": [{
                    "type": "text",
                    "text": favorite_shop['shop_name'],
                    "weight": "regular",
                    "size": "sm",
                    "contents": []
                }]
            }
            favorites_template['body']['contents'].append(flex_message)
            favorites_template['footer']['contents'][0]['action']['data'] = 'deleteshop'

        return favorites_template

    def __favorites_confirm_flex_message(self, favorite_shop, favorites_confirm_message_template):
        favorites_confirm_message_template['body']['contents'][0]['text'] = favorite_shop['shop_name']
        favorites_confirm_message_template['footer']['contents'][0]['action']['data'] = str(
            favorite_shop['_id'])
        return favorites_confirm_message_template
