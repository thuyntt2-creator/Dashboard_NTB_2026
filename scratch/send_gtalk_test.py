import requests
import time
import urllib3

# Suppress insecure request warning as verify=False is used in app.py
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

channel_id = "2067164759710552066"
oa_token = "2067164759497973760:RfgqBJY4QtV18udu1wMEfhmoRNI4hgBv"

url = "https://mbff.ghn.vn/api/gtalk/send-message"
client_msg_id = str(int(time.time() * 1000))

message = """🚨 *[ACTION BOARD] - BÁO CÁO MẪU* 🚨
👤 *AM:* Nguyễn Văn A  |  📅 *Ngày:* 17/07/2026
──────────────────────────────

### 1. 📍 ĐƠN TRỄ LẤY TTS (Ngày n-1)
•  *Shop Lazada Mall* 
   └ Bưu cục: Cầu Giấy  |  Mã đơn: `LZ-982-1234`

### 2. ⚡ CẢNH BÁO CA 1 (Đơn chưa gán giao)
🔴 *Bưu cục Cầu Giấy:* `8 đơn` chưa gán giao.

### 3. ⏳ ĐƠN AGING > 5 NGÀY (Tồn lâu)
•  Bưu cục Cầu Giấy: `Lazada_99999` *(Tồn 6 ngày)*

### 4. 🛑 ĐƠN TREO LC & RỚT LC TTS
•  Bưu cục Cầu Giấy:
   ├ Treo LC: `4 đơn`
   └ Rớt LC TTS: `1 đơn` (`LZ-111-222`)

──────────────────────────────
💡 *Mẹo: Anh em chạm vào mã đơn để copy nhanh.*
📝 *[CLICK VÀO ĐÂY ĐỂ CẬP NHẬT TRÊN SHEET](https://docs.google.com/spreadsheets/)*
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
    print("Sending test message to GTalk...")
    res = requests.post(url, json=payload, headers=headers, timeout=15, verify=False)
    print("Status Code:", res.status_code)
    print("Response:", res.text)
except Exception as e:
    print("Error:", e)
