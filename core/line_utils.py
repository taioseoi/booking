import requests
from config import LINE_CHANNEL_ACCESS_TOKEN, LINE_CLIENT_ID, LINE_REDIRECT_URI
from urllib.parse import urlencode
from datetime import datetime

def push_flex_line(user_id, flex_content_json):
    headers = {
        "Authorization": f"Bearer {LINE_CHANNEL_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    body = {
        "to": user_id,
        "messages": [
            {"type": "flex", "altText": "แจ้งเตือนใกล้ถึงเวลาจองห้อง", "contents": flex_content_json}
        ]
    }
    r = requests.post("https://api.line.me/v2/bot/message/push", headers=headers, json=body)
    print("PUSH STATUS:", r.status_code)
    print("PUSH RESPONSE:", r.text)
    return r.status_code, r.text



def get_line_auth_url(room=None):
    state = f"ROOM_{room}" if room else "1234"
    scope = "profile openid email"
    auth_base = "https://access.line.me/oauth2/v2.1/authorize"
    params = {
        "response_type": "code",
        "client_id": LINE_CLIENT_ID,
        "redirect_uri": LINE_REDIRECT_URI,
        "scope": scope,
        "state": state
    }
    return f"{auth_base}?{urlencode(params)}"

def push_text_line(user_id, text):
    headers = {
        "Authorization": f"Bearer {LINE_CHANNEL_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    body = {
        "to": user_id,
        "messages": [
            {"type": "text", "text": text}
        ]
    }
    r = requests.post("https://api.line.me/v2/bot/message/push", headers=headers, json=body)
    print(r.status_code, r.text)
    return r.status_code, r.text