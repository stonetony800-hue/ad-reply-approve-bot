import os
import json
import requests
from http.server import BaseHTTPRequestHandler

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


class handler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(
            b"Ad Reply Approve Bot is running!"
        )

    def do_POST(self):
        try:
            content_length = int(
                self.headers.get("Content-Length", 0)
            )

            body = self.rfile.read(content_length)
            update = json.loads(body.decode("utf-8"))

            # Normal bot messages
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

            # Channel posts
            channel_post = update.get("channel_post")

            if channel_post:
                chat_id = channel_post["chat"]["id"]
                message_id = channel_post["message_id"]

                send_message(
                    chat_id,
                    "✅ Advertisement received!\n\n"
                    "Thank you! Your submission is being "
                    "reviewed.",
                    message_id
                )

            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(b"OK")

        except Exception as error:
            print("ERROR:", error)

            self.send_response(500)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(b"Error")
