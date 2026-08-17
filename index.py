import os
import requests
from flask import Flask, request

app = Flask(__name__)

BOT_TOKEN = os.environ.get("TELEGRAM_TOKEN")

if not BOT_TOKEN:
    raise RuntimeError("TELEGRAM_TOKEN environment variable is missing")

TELEGRAM_API = f"https://api.telegram.org/bot{BOT_TOKEN}"


def send_message(chat_id, text, reply_to=None):
    data = {
        "chat_id": chat_id,
        "text": text
    }

    if reply_to:
        data["reply_to_message_id"] = reply_to

    response = requests.post(
        f"{TELEGRAM_API}/sendMessage",
        json=data,
        timeout=15
    )

    print("Telegram response:", response.text)


@app.route("/", methods=["GET"])
def home():
    return "Telegram Auto Reply Bot is running!", 200


@app.route("/", methods=["POST"])
def telegram_webhook():
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
                    "👋 Welcome!\n\n"
                    "Send your advertisement or message here "
                    "and you will receive an automatic response."
                )
            else:
                send_message(
                    chat_id,
                    "✅ Message received!\n\n"
                    "Thank you. Your advertisement has been "
                    "received and is being reviewed.",
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
                "Thank you. Your advertisement has been "
                "received and is being reviewed.",
                message_id
            )

        return "OK", 200

    except Exception as error:
        print("ERROR:", error)
        return "Error", 500
