import requests
import time
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

channel_id = "2067164759710552066"
oa_token = "2067164759497973760:RfgqBJY4QtV18udu1wMEfhmoRNI4hgBv"

url = "https://mbff.ghn.vn/api/gtalk/send-message"
client_msg_id = str(int(time.time() * 1000))

# GTalk Compatible formatting:
# - Double asterisks (**) for Bold.
# - No single backticks (they display literally). Use bold for waybills instead.
# - Real link to the spreadsheet provided by the user.
sheet_url = "https://docs.google.com/spreadsheets/d/1JZ1eRerRqrpwjZ4HBevQunjd8VquM_cvPFz12TaJfMQ/edit?gid=870632257#gid=870632257"

message = f"""🚨 **[ACTION BOARD] - ĐIỂM NÓNG VẬN HÀNH ĐẦU NGÀY** 🚨
👤 **AM:** Nguyễn Văn A  |  📅 **Ngày:** 17/07/2026
──────────────────────────────

### 1. 📍 ĐƠN TRỄ LẤY TTS (Ngày n-1)
*Các shop có đơn bị trễ chưa lấy, cần liên hệ bưu cục đôn đốc:*
•  **Shop Lazada Mall** 
   └ Bưu cục: Cầu Giấy  |  Mã đơn: **LZ-982-1234**
•  **Shop Shopee Express** 
   └ Bưu cục: Mỹ Đình  |  Mã đơn: **SP-771-5678**

### 2. ⚡ CẢNH BÁO CA 1 (Đơn chưa gán giao)
*Cần yêu cầu Trưởng bưu cục phân tuyến cho shipper đi giao gấp:*
🔴 **Bưu cục Cầu Giấy:** **8 đơn** chưa gán giao.
🟡 **Bưu cục Mỹ Đình:** **4 đơn** chưa gán giao.

### 3. ⏳ ĐƠN AGING > 5 NGÀY (Cảnh báo tồn kho lâu)
*Hàng đang kẹt tại bưu cục quá hạn, cần xử lý dứt điểm:*
•  Bưu cục Cầu Giấy: **Lazada-99999** *(Tồn 6 ngày)*
•  Bưu cục Mỹ Đình: **Shopee-88888** *(Tồn 5 ngày)*

### 4. 🛑 ĐƠN TREO LC & RỚT LC TTS (Lỗi kết nối)
•  **Bưu cục Cầu Giấy:**
   ├ Treo LC: **4 đơn**
   └ Rớt LC TTS: **1 đơn** (**LZ-111-222**)
•  **Bưu cục Mỹ Đình:**
   ├ Treo LC: **3 đơn**
   └ Rớt LC TTS: **1 đơn** (**SP-333-444**)

### 📊 5. CHỈ SỐ HIỆU SUẤT VẬN HÀNH HÔM QUA
•  Tỷ lệ GTC Ca 1: **82%** (Target: 90%) 🔴
•  Tỷ lệ GTC Chung: **93%** (Target: 95%) 🔴
* Bưu cục hoạt động kém nhất: Cầu Giấy (%GTC Ca 1: 75%).

──────────────────────────────
📝 **[CLICK VÀO ĐÂY ĐỂ CẬP NHẬT TRÊN SHEET]({sheet_url})**
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
    print("Sending final formatted report to GTalk...")
    res = requests.post(url, json=payload, headers=headers, timeout=15, verify=False)
    print("Status Code:", res.status_code)
    print("Response:", res.text)
except Exception as e:
    print("Error:", e)
