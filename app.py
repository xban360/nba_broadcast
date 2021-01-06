from __future__ import unicode_literals
import os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import logging
import configparser
import sys
from web_spider.web_spider import WebSpider

app = Flask(__name__)

config = configparser.ConfigParser()
config.read('config.ini')

line_bot_api = LineBotApi(config.get('line-bot', 'channel_access_token'))
handler = WebhookHandler(config.get('line-bot', 'channel_secret'))

@app.route("/")
def home():
    return "Welcome Hook"

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    
    try:
        print(body, signature)
        handler.handle(body, signature)
        
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def echo(event):
    spider = WebSpider()
    data = spider.grep(event.message.text)
    ret = ''
    if isinstance(data, list):
        for info in data:
            for key, val in info.items():
                ret += key+" : "+str(val)+"\n"
            ret += "\n"
    
    if ret == '':
        ret = event.message.text
    
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=ret)
    )

if __name__ == "__main__":
    app.run()

if __name__ != "__main__":
    gunicornLogger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicornLogger.handlers
    app.logger.setLevel(gunicornLogger.level)

