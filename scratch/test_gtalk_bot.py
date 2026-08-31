import requests
import urllib3
import sys

try:
    sys.stdout.reconfigure(encoding='utf-8')
except AttributeError:
    pass

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

token = "2067164759497973760:RfgqBJY4QtV18udu1wMEfhmoRNI4hgBv"
channel_id = "2067164759710552066"

headers = {
    "Content-Type": "application/json",
    "Authorization": token
}

# Testing different paths with Zalo OA style and standard style payloads
test_cases = [
    # 1. Standard Telegram style payload on various paths
    ("/api/v1/bot/sendMessage", {"chat_id": channel_id, "text": "🔔 Test bot GTalk 🚀"}),
    ("/api/v1/oa/message", {"recipient": {"channel_id": channel_id}, "message": {"text": "🔔 Test bot GTalk 🚀"}}),
    ("/api/v1/oa/message", {"recipient": {"chat_id": channel_id}, "message": {"text": "🔔 Test bot GTalk 🚀"}}),
    ("/api/v1/oa/message/send", {"recipient": {"channel_id": channel_id}, "message": {"text": "🔔 Test bot GTalk 🚀"}}),
    
    # 2. Other candidate paths
    ("/api/v1/oa/message/send", {"chat_id": channel_id, "text": "🔔 Test bot GTalk 🚀"}),
    ("/api/v1/oa/message", {"chat_id": channel_id, "text": "🔔 Test bot GTalk 🚀"}),
    ("/api/v1/bot/message/send", {"chat_id": channel_id, "text": "🔔 Test bot GTalk 🚀"}),
    ("/api/v1/chat/message/send", {"chat_id": channel_id, "text": "🔔 Test bot GTalk 🚀"}),
]

for idx, (path, payload) in enumerate(test_cases, 1):
    url = f"https://nhanh-api.ghn.vn{path}"
    print(f"Test {idx}: {url} | payload: {list(payload.keys())}")
    try:
        res = requests.post(url, json=payload, headers=headers, timeout=5, verify=False)
        print(f"Status: {res.status_code}")
        print(f"Response: {res.text.strip()}")
    except Exception as e:
        print(f"Error: {e}")
