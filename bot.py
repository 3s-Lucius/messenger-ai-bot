from flask import Flask, request
import os

app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is running"

@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    if request.method == "GET":
        return request.args.get("hub.challenge", "")
    return "ok", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
