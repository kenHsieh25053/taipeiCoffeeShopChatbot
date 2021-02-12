from linebot import LineBotApi
from linebot.models import (
    TextSendMessage, FlexSendMessage, QuickReply,
    QuickReplyButton, LocationAction, PostbackAction
)

from flask import current_app as app

CHANNEL_ACCESS_TOKEN = app.config['CHANNEL_ACCESS_TOKEN']


class MessageHandler():

    line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)

    def send_textmessage(self, event, message):
        return self.line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=message))

    def send_flexmessage(self, event, alt_text, contents):
        return self.line_bot_api.reply_message(
            event.reply_token,
            FlexSendMessage(alt_text=alt_text, contents=contents)
        )

    def send_quickreplymessage(self, event, content, quick_reply_messages):
        quickrepley_buttons = []
        for quick_reply_message in quick_reply_messages:
            if quick_reply_message['action'] == 'location':
                quickrepley_button = QuickReplyButton(action=LocationAction(
                    label=quick_reply_message['label'], type='location'))
            else:
                quickrepley_button = QuickReplyButton(action=PostbackAction(
                    label=quick_reply_message['label'], display_text=quick_reply_message['label'], data=quick_reply_message['data']))
            quickrepley_buttons.append(quickrepley_button)

        return self.line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content, quick_reply=QuickReply(items=quickrepley_buttons)))
