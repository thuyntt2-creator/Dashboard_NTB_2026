import requests
import time
import json
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

url = "https://mbff.ghn.vn/api/gtalk/send-message"
token = "2067164759497973760:RfgqBJY4QtV18udu1wMEfhmoRNI4hgBv"
channel_id = "2067164759710552066"

client_msg_id = str(int(time.time() * 1000))

payload = {
    "channelId": channel_id,
    "clientMsgId": client_msg_id,
    "content": {
        "text": "🔔 **Báo cáo vận hành NTB**\nKết nối bot GTalk thành công! 🚀",
        "parseMode": "MARKDOWN"
    },
    "oaToken": token
}

headers = {
    "Content-Type": "application/json"
}

print(f"Sending message to: {url}")
print(f"Payload: {json.dumps(payload, indent=2)}")

try:
    res = requests.post(url, json=payload, headers=headers, timeout=15, verify=False)
    print(f"Status Code: {res.status_code}")
    print(f"Response Headers: {dict(res.headers)}")
    print(f"Response Body: {res.text}")
except Exception as e:
    print(f"Error occurred: {e}")
