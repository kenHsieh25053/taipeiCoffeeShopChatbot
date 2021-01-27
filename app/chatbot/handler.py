from linebot import (
    LineBotApi, WebhookParser
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    TextMessage, TextSendMessage, FlexSendMessage,
    QuickReply, QuickReplyButton, MessageAction, LocationAction, PostbackAction
)

import json
from copy import deepcopy
from flask import current_app as app
from .shop import Shop

CHANNEL_ACCESS_TOKEN = app.config['CHANNEL_ACCESS_TOKEN']
CHANNEL_SECRET = app.config['CHANNEL_SECRET']

shop = Shop()


class Handler:

    def callback(self, signature, body):
        parser = WebhookParser(CHANNEL_SECRET)

        try:
            events = parser.parse(body, signature)
            self.__handle_message(events[0])
        except InvalidSignatureError as e:
            print(e)

    def __handle_message(self, event):
        line_bot_api = LineBotApi(self.CHANNEL_ACCESS_TOKEN)
        if event.type == 'message':
            if event.message.type == 'location':
                self.__handle_location_message(event, line_bot_api)
            elif event.message.text == 'search':
                self.__handle_quick_reply_action(event, line_bot_api)
            elif event.message.text == 'topics':
                print(event)
            elif event.message.text == 'favorites':
                self.__handle_favorites_message(event, line_bot_api)
            else:
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text="對不起，我不了解您的問題"))
        else:
            # postback actions
            action = event.postback.data.split('_')[0]
            if action == 'favorite':
                self.__handle_favorites_postback_action(event, line_bot_api)
            elif action == 'deleteshop':
                self.__handle_delete_shop_postback_action(event, line_bot_api)
            elif action == 'topics':
                self.__handle_topics_postback_action(
                    event, line_bot_api)
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

    def __handle_location_message(self, event, line_bot_api):
        nearby_shops = self.shop.get_nearby_shops_by_location(
            event, self.mongodb)

        if nearby_shops:
            with open('./templates/flexmessage.json') as file:
                flex_message_template = json.load(file)
            flex_messages = {
                "type": "carousel",
                "contents": [deepcopy(self.__insert_flex_message(nearby_shop, flex_message_template)) for nearby_shop in nearby_shops]
            }
            line_bot_api.reply_message(
                event.reply_token, FlexSendMessage(alt_text='店家資訊', contents=flex_messages))
        else:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="尚未探索這區～"))

    def __handle_favorites_message(self, event, line_bot_api):
        favorite_shops = self.shop.get_favorites(
            event, self.mongodb)

        if favorite_shops:
            with open('./templates/favorites.json') as file:
                favorites_template = json.load(file)

            line_bot_api.reply_message(
                event.reply_token,
                FlexSendMessage(alt_text='最愛清單', contents=self.__insert_favorites_flex_message(
                    favorite_shops, favorites_template))
            )
        else:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="尚未加入我的最愛"))

    def __handle_favorites_postback_action(self, event, line_bot_api):
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

    def __handle_delete_shop_postback_action(self, event, line_bot_api):
        favorite_shops = self.shop.get_favorites(
            event, self.mongodb)

        with open('./templates/favoritesComfirmMessage.json') as file:
            favorites_confirm_message_template = json.load(file)

        favorites_confirm_messages = {
            "type": "carousel",
            "contents": [deepcopy(self.__insert_favorites_confirm_flex_message(favorite_shop, favorites_confirm_message_template)) for favorite_shop in favorite_shops]
        }

        line_bot_api.reply_message(
            event.reply_token,
            FlexSendMessage(alt_text='確認刪除清單',
                            contents=favorites_confirm_messages)
        )

    def __handle_quick_reply_action(self, event, line_bot_api):

        quick_reply_messages = [
            QuickReplyButton(action=LocationAction(
                label='地點查詢', type='location')),
            QuickReplyButton(action=PostbackAction(
                label='小幫手愛店', display_text='小幫手愛店', data='topics_kensfavorites')),
            QuickReplyButton(action=PostbackAction(
                label='深夜咖啡館', display_text='深夜咖啡館', data='topics_nightcafe')),
            QuickReplyButton(action=PostbackAction(
                label='早鳥咖啡館', display_text='早鳥咖啡館', data='topics_morningcafe')),
            QuickReplyButton(action=PostbackAction(
                label='寬敞聚會咖啡廳', display_text='寬敞聚會咖啡廳', data='topics_spacious'))
        ]

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='選擇地點查詢開啟google map, 或是選擇其他主題分類',
                            quick_reply=QuickReply(items=quick_reply_messages))
        )

    def __handle_topics_postback_action(self, event, line_bot_api):
        shops = self.shop.get_shops_by_topics(
            event, self.mongodb)

        with open('./templates/flexmessage.json') as file:
            flex_message_template = json.load(file)
        flex_messages = {
            "type": "carousel",
            "contents": [deepcopy(self.__insert_flex_message(shop, flex_message_template))
                         for shop in shops]
        }
        line_bot_api.reply_message(
            event.reply_token, FlexSendMessage(alt_text='店家資訊', contents=flex_messages))

    def __insert_flex_message(self, nearby_shop, flex_message_template):
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

    def __insert_favorites_flex_message(self, favorite_shops, favorites_template):
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

    def __insert_favorites_confirm_flex_message(self, favorite_shop, favorites_confirm_message_template):
        favorites_confirm_message_template['body']['contents'][0]['text'] = favorite_shop['shop_name']
        favorites_confirm_message_template['footer']['contents'][0]['action']['data'] = str(
            favorite_shop['_id'])
        return favorites_confirm_message_template
