import os
import requests

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


def handler(request):
    if request.method != "POST":
        return {
            "statusCode": 200,
            "body": "Ad Reply Approve Bot is running!"
        }

    try:
        update = request.get_json()

        # Handle normal messages
        message = update.get("message")

        if message:
            chat_id = message["chat"]["id"]
            message_id = message["message_id"]
            text = message.get("text", "").strip()

            if text == "/start":
                send_message(
                    chat_id,
                    "👋 Welcome!\n\n"
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

        # Handle channel posts
        channel_post = update.get("channel_post")

        if channel_post:
            chat_id = channel_post["chat"]["id"]
            message_id = channel_post["message_id"]

            send_message(
                chat_id,
                "✅ Your advertisement has been received.\n\n"
                "Thank you! Your submission is being reviewed.",
                message_id
            )

        return {
            "statusCode": 200,
            "body": "OK"
        }

    except Exception as error:
        print("ERROR:", error)

        return {
            "statusCode": 500,
            "body": "Error"
        }
