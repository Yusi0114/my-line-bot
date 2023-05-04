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
webhook_handler = WebhookHandler('26016dfbdd5f59b4faefded8639c27c0') # your channel secret

# 設定 OpenAI API 密鑰
openai.api_key = os.environ["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"]
# openai.api_key = "OPENAI_API_KEY"

# 設定 GPT-3.5 模型的檢索引擎
model_engine = "text-davinci-003"

# 設定生成的文本長度
output_length = 300


@app.route("/")
def home():
    return "LINE BOT API Server is running."

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        webhook_handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@webhook_handler.add(MessageEvent, message=TextMessage)
def handle_message(event):

    # 使用 GPT-3.5 模型生成文本
    response = openai.Completion.create(
        engine=model_engine,
        prompt=event.message.text,
        max_tokens=output_length,
    )

    # 取得生成的文本
    output_text = response.choices[0].text.strip()

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=output_text))


if __name__ == "__main__":
    app.run()