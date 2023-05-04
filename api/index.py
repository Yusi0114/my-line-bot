from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('/H9NE43vOP43+/ChC1/mBFyVXdRQqANXBhzNjXxTmcePo42k4AINP5akLybyEEi1knYA7wca56rwkVrPVFKJIp2BRWQIfxz3QsCfhIt+im9+XPxfEm1kgtiGOMDDfYqMMtULOXsNUGikVdl+Y9SFqwdB04t89/1O/w1cDnyilFU=') # your access token
handler = WebhookHandler('26016dfbdd5f59b4faefded8639c27c0') # your channel secret

@app.route("/")
def home():
    return "LINE bot API Server is running"

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
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()