from __future__ import unicode_literals
import os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import FollowEvent, MessageEvent, TextMessage, TextSendMessage, FlexSendMessage
import logging
import configparser
import sys
import re
from web_spider.web_spider import WebSpider
from boards import getBoards

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

@handler.add(FollowEvent)
def tip(event):
    text = 'Thank you for following us.\n\nType PTT to get board lists.\nOr type PTT {board} to get article list of the board.\n\nType NBA to get games status of today.'
    sendMessage = TextSendMessage(text=text)
    line_bot_api.reply_message(
        event.reply_token,
        sendMessage
    )

@handler.add(MessageEvent, message=TextMessage)
def broadcast(event):
    text = event.message.text
    pttMatch = re.findall("(?<=PTT ).*", text)
    ret = ''
    sendMessage = None
    if 'NBA' == text:
        spider = WebSpider()
    
        data = spider.grep(text)
        for info in data:
            ret += info['homeTeam'] + ': ' + str(info['homeScore']) + "\n"
            ret += info['awayTeam'] + ': ' + str(info['awayScore']) + "\n"
            ret += info['status'] + "\n"
            ret += "\n"

        if ret == '':
            ret = 'No Game Today.'

    elif 'PTT' == text:
        sendMessage = listAllBoards()

    elif [] != pttMatch:
        spider = WebSpider()
        data = spider.grep('PTT', pttMatch)
        for info in data:
            ret += info['title'] + "\n"
            ret += info['href'] + "\n"
            ret += "\n"

        if ret == '':
            ret = 'No Article. Please Type "PTT" and select a correct board'

    else:
        ret = text
    
    if None == sendMessage:
        sendMessage = TextSendMessage(text=ret)

    line_bot_api.reply_message(
        event.reply_token,
        sendMessage
    )

def listAllBoards():
    boards = getBoards().getBoards()

    count = 0
    contents = []
    bubbleContent = []
    rowBowContent = []
    for className, classBoards in boards.items():
        for board in classBoards:
            rowBowContent.append({
                'type': 'button',
                'action': {
                    'type': 'message',
                    'label': board,
                    'text': f'PTT {board}'
                }
            })

            count += 1

            if 0 == count % 2:
                bubbleContent.append({
                    'type': 'box',
                    'layout': 'horizontal',
                    'contents': rowBowContent
                })

                rowBowContent = []

            if count >= 20:
                contents.append({
                    'type': 'bubble',
                    'body': {
                        'type': 'box',
                        'layout': 'vertical',
                        'contents': bubbleContent
                    }
                })
                bubbleContent = []
                count = 0
    
    return FlexSendMessage(
        alt_text='Theme',
        contents={
            'type': 'carousel',
            'contents': contents
        }
    )


if __name__ == "__main__":
    app.run()

if __name__ != "__main__":
    gunicornLogger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicornLogger.handlers
    app.logger.setLevel(gunicornLogger.level)

