from flask import Flask, request
import requests
import os

app = Flask(__name__)

VERIFY_TOKEN = "3sbot"
PAGE_ACCESS_TOKEN = os.environ.get("EAAMpHdEsTpoBQYSeZCLhz0fQ8z7YQEA5sdswienq5TtV6tdhlZCG1bW7RJyjZBCQypunWNDSc20aMfJe8l5kfHw1dc7FZBcEsHTbNM8NkAf4JRqNUx4NMpPPpg75U2ZA5t9LRDPX8cBpldKjnB1ZAyUkUtvBRnjTnWK96NYY8TdEQptPNAdV2zQVXlffCNZCNlsy3SvjGV7XHYRqGwYPhNyEytgKXw0osflHnjVLwZDZD") or "DÁN_PAGE_TOKEN_VÀO_ĐÂY"

@app.route("/")
def home():
    return "Bot is running"

@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    if request.method == "GET":
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")
        if token == VERIFY_TOKEN:
            return challenge
        return "Sai token", 403

    data = request.get_json()
    print("EVENT:", data)  # 👈 LOG QUAN TRỌNG

    for entry in data.get("entry", []):
        for event in entry.get("messaging", []):
            sender_id = event.get("sender", {}).get("id")

            # BỎ QUA echo
            if event.get("message", {}).get("is_echo"):
                continue

            text = event.get("message", {}).get("text")
            if sender_id and text:
                send_message(sender_id, f"🤖 Bot nhận được: {text}")

    return "ok", 200

def send_message(psid, text):
    url = "https://graph.facebook.com/v18.0/me/messages"
    params = {"access_token": PAGE_ACCESS_TOKEN}
    payload = {
        "recipient": {"id": psid},
        "message": {"text": text}
    }

    r = requests.post(url, params=params, json=payload)
    print("SEND RESULT:", r.text)  # 👈 LOG QUAN TRỌNG

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
