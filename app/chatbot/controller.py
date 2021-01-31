from flask import current_app as app
from linebot import WebhookParser
from linebot.exceptions import InvalidSignatureError
from copy import deepcopy

from .message import MessageHandler
from .shop import Shop
from .messagetemplates import favorites, flexmessage, comfirmMessage

# For  webparser use
CHANNEL_SECRET = app.config['CHANNEL_SECRET']

shop = Shop()
messageHandler = MessageHandler()


class Controller:

    def callback(self, signature, body):
        parser = WebhookParser(CHANNEL_SECRET)

        try:
            events = parser.parse(body, signature)
            self.__handle_message(events[0])
        except InvalidSignatureError as e:
            print(e)

    def __handle_message(self, event):
        if event.type == 'message':
            if event.message.type == 'location':
                self.__handle_location_message(event)
            elif event.message.text == 'search':
                self.__handle_quick_reply_action(event)
            elif event.message.text == 'favorites':
                self.__handle_favorites_message(event)
            else:
                message = '對不起，我不了解您的問題'
                messageHandler.send_textmessage(event, message)

        else:
            # postback actions
            action = event.postback.data.split('_')[0]
            if action == 'favorite':
                self.__handle_favorites_postback_action(event)
            elif action == 'deleteshop':
                self.__handle_delete_shop_postback_action(event)
            elif action == 'topics':
                self.__handle_topics_postback_action(event)
            else:
                result = shop.delete_favorite_shop(event)
                message = f"已將 {result} 移除!"
                if result:
                    messageHandler.send_textmessage(event, message)

    def __handle_location_message(self, event):
        nearby_shops = shop.get_nearby_shops_by_location(event)
        if nearby_shops:
            flex_messages = {
                "type": "carousel",
                "contents": [deepcopy(self.__insert_flex_message(nearby_shop, flexmessage.FLEX_MESSAGE)) for nearby_shop in nearby_shops]
            }
            alt_text = '店家資訊'
            contents = flex_messages
            messageHandler.send_flexmessage(event, alt_text, contents)
        else:
            message = '尚未探索這區～'
            messageHandler.send_textmessage(event, message)

    def __handle_favorites_message(self, event):
        favorite_shops = shop.get_favorites(event)
        if favorite_shops:
            alt_text = '最愛清單'
            contents = self.__insert_favorites_flex_message(
                favorite_shops, favorites.FAVORITE_MESSAGE)
            messageHandler.send_flexmessage(event, alt_text, contents)
        else:
            message = '尚未加入我的最愛'
            messageHandler.send_textmessage(event, message)

    def __handle_favorites_postback_action(self, event):
        favorite_shops = shop.get_favorites(event)
        if favorite_shops and len(favorite_shops) > 9:
            message = '最愛店家已達十筆，請先刪除店家再進行新增！'
            messageHandler.send_textmessage(event, message)
            return None

        result = shop.add_into_my_favorites(event)
        if result:
            message = f'已將 {result} 加入最愛！'
        else:
            message = '已經加入'

        messageHandler.send_textmessage(event, message)

    def __handle_delete_shop_postback_action(self, event):
        favorite_shops = shop.get_favorites(event)

        favorites_confirm_messages = {
            "type": "carousel",
            "contents": [deepcopy(self.__insert_favorites_confirm_flex_message(favorite_shop, comfirmMessage.COMFIRM_MESSAGE)) for favorite_shop in favorite_shops]
        }
        alt_text = '確認刪除清單'
        contents = favorites_confirm_messages
        messageHandler.send_flexmessage(event, alt_text, contents)

    def __handle_quick_reply_action(self, event):
        content = '選擇地點查詢開啟google map, 或是選擇其他主題分類'
        quick_reply_messages = [
            {'action': 'location', 'label': '地點查詢', 'type': 'location'},
            {'action': 'postback', 'label': '小幫手愛店',
                'data': 'topics_kensfavorites'},
            {'action': 'postback', 'label': '深夜咖啡館',
                'data': 'topics_nightcafe'},
            {'action': 'postback', 'label': '早鳥咖啡館',
                'data': 'topics_morningcafe'},
            {'action': 'postback', 'label': '寬敞聚會咖啡廳',
                'data': 'topics_spacious'}
        ]

        messageHandler.send_quickreplymessage(
            event, content, quick_reply_messages)

    def __handle_topics_postback_action(self, event):
        shops = shop.get_shops_by_topics(
            event)
        flex_messages = {
            "type": "carousel",
            "contents": [deepcopy(self.__insert_flex_message(shop, flexmessage.FLEX_MESSAGE))
                         for shop in shops]
        }
        alt_text = '店家資訊'
        contents = flex_messages
        messageHandler.send_flexmessage(event, alt_text, contents)

    def __insert_flex_message(self, nearby_shop, flex_message_template):
        flex_message_template['body']['contents'][0]['text'] = nearby_shop['name']
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
            '_' + nearby_shop['name'] + '_' + str(nearby_shop['id'])

        return flex_message_template

    def __insert_favorites_flex_message(self, favorite_shops, favorites_template):
        favorite_shop_contents = []
        for favorite_shop in favorite_shops:
            flex_message = {
                "type": "box",
                "layout": "vertical",
                "contents": [{
                    "type": "text",
                    "text": favorite_shop['shop'],
                    "weight": "regular",
                    "size": "sm",
                    "contents": []
                }]
            }
            favorite_shop_contents.append(flex_message)
        favorites_template['body']['contents'] = favorite_shop_contents

        return favorites_template

    def __insert_favorites_confirm_flex_message(self, favorite_shop, favorites_confirm_message_template):
        favorites_confirm_message_template['body']['contents'][0]['text'] = favorite_shop['shop']
        favorites_confirm_message_template['footer']['contents'][0]['action'][
            'data'] = f'{str(favorite_shop["id"])}_{favorite_shop["shop"]}'
        return favorites_confirm_message_template
