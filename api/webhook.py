import os
import requests
from flask import Flask, request

app = Flask(__name__)

BOT_TOKEN = os.environ.get("TELEGRAM_TOKEN")
TELEGRAM_API = f"https://api.telegram.org/bot{BOT_TOKEN}"


def send_message(chat_id, text, reply_to=None):
    data = {
        "chat_id": chat_id,
        "text": text
    }

    if reply_to:
        data["reply_to_message_id"] = reply_to

    requests.post(
        f"{TELEGRAM_API}/sendMessage",
        json=data,
        timeout=10
    )


@app.route("/", methods=["GET"])
def home():
    return "Ad Reply Approve Bot is running!"


@app.route("/", methods=["POST"])
def webhook():
    try:
        update = request.get_json(silent=True) or {}

        # Messages sent directly to the bot
        message = update.get("message")

        if message:
            chat_id = message["chat"]["id"]
            message_id = message["message_id"]
            text = message.get("text", "").strip()

            if text == "/start":
                send_message(
                    chat_id,
                    "👋 Welcome to Ad Reply Approve Bot!\n\n"
                    "Send your advertisement here and "
                    "you will receive an automatic reply."
                )
            else:
                send_message(
                    chat_id,
                    "✅ Advertisement received!\n\n"
                    "Your submission has been received "
                    "and is being reviewed.",
                    message_id
                )

        # Posts made in a Telegram channel
        channel_post = update.get("channel_post")

        if channel_post:
            chat_id = channel_post["chat"]["id"]
            message_id = channel_post["message_id"]

            send_message(
                chat_id,
                "✅ Advertisement received!\n\n"
                "Thank you! Your submission is being reviewed.",
                message_id
            )

        return "OK", 200

    except Exception as error:
        print("ERROR:", error)
        return "Error", 500
