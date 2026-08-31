import requests
import time
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

channel_id = "2067164759710552066"
oa_token = "2067164759497973760:RfgqBJY4QtV18udu1wMEfhmoRNI4hgBv"

url = "https://mbff.ghn.vn/api/gtalk/send-message"
client_msg_id = str(int(time.time() * 1000))

message = """🧪 *GTalk Markdown Formatting Test* 🧪
──────────────────────────────
1. Single asterisk: *This is bold in Telegram, but what about GTalk?*
2. Double asterisks: **Is this bold in GTalk?**
3. Underscores: _Is this italic in GTalk?_
4. Single backtick: `Monospace Code`
5. Triple backticks:
```
Block Code
```
6. Link: [Google Link](https://www.google.com)
"""

payload = {
    "channelId": channel_id,
    "clientMsgId": client_msg_id,
    "content": {
        "text": message,
        "parseMode": "MARKDOWN"
    },
    "oaToken": oa_token
}

headers = {
    "Content-Type": "application/json"
}

try:
    print("Sending formatting test to GTalk...")
    res = requests.post(url, json=payload, headers=headers, timeout=15, verify=False)
    print("Status Code:", res.status_code)
    print("Response:", res.text)
except Exception as e:
    print("Error:", e)
