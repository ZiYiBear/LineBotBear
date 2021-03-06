"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template, Flask, request, abort
from FlaskWebProjectLineBotBear import app

#Line機器人所需套件 說明文件:https://github.com/line/line-bot-sdk-python
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

#Line機器人申請參數
LINE_CHANNEL_ACCESS_TOKEN = "mQVYL9n3SSe3W7LWU8vSEHLeu2Wr9Bk7B/e8lLTvbBIiqjCGWWc88YkCWIFrUtKH2oA+U5i8YO8FC4EEy2XAFdsXG7D6y7DVPFlk5zgEff205cB3rQ+jF2ilszTcE7wwcNEmg802/gAHBXJAlJ8WqAdB04t89/1O/w1cDnyilFU="
LINE_CHANNEL_SECRET = "2d88fd33111410911fb8fe0ce0d55e45"

line_bot_api = LineBotApi('LINE_CHANNEL_ACCESS_TOKEN')
handler = WebhookHandler('LINE_CHANNEL_SECRET')

#Line API控制事件
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))

#Visual Studio 基本功能頁面
@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
    )

@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Your contact page.'
    )

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='這個會透過Flask來建立可和Line Message API連線的服務'
    )
