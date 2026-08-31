import requests

bot_token = "2067164759497973760:RfgqBJY4QtV18udu1wMEfhmoRNI4hgBv"
# Telegram group IDs are negative. Supergroups start with -100.
# We will test multiple variations of the provided group ID.
group_ids = [
    "-1002067164759710552066", 
    "-2067164759710552066", 
    "2067164759710552066"
]

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

for g_id in group_ids:
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": g_id,
        "text": message,
        "parse_mode": "Markdown"
    }
    try:
        response = requests.post(url, json=payload)
        print(f"Testing Group ID: {g_id}")
        print("Status Code:", response.status_code)
        print("Response:", response.text)
        print("-" * 40)
    except Exception as e:
        print(f"Error testing Group ID {g_id}:", e)
