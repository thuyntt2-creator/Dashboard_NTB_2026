import requests
import asyncio
from telethon import TelegramClient
from datetime import datetime, timezone
import re
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
import os
import io

# ========== CẤU HÌNH CỦA THỦY ==========
API_ID = 33980755
API_HASH = '27cb91d2027884b61393c554a4439dff'
PHONE = '+84368644943'
BOT_NAME = 'ghn_staff_bot'

ID_LIST = [
    "1909", "20745000", "20797000", "20336000", "22915000"]

FOLDER_PATH = r'C:\Users\lap4all\Desktop\Backlog_Automation'
JSON_FILE = os.path.join(FOLDER_PATH, 'credentials.json')
SESSION_FILE = os.path.join(FOLDER_PATH, 'session_thuy')
SHEET_ID_DICH = '1CbXJb_-HqGGcOep8R6Zf6qBn8gGi_8EyLkr8ebhEdzI'
TAB_NAME = '1'

headers = {
    'authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJvcmdDb2RlIjoiZ2huZXhwcmVzcyIsInBhcnRuZXJDb2RlIjoiIiwic2VlZCI6MTEyNDQwMDkxMTkxODg1MjQzMywic3NvSWQiOiIzMDY2MDIxIiwidXNlcklkIjoiNjRlMmUyYzI2MmNhZDU1YzZiODRlZTBkIn0.aG5YDpomKHC5CR1dpX6WdfHid3LZmnD7Up1-htmX1S0',
}

async def run_job():
    print(f"🚀 Bắt đầu chạy lúc: {datetime.now().strftime('%H:%M:%S')}")

    # A. GỬI YÊU CẦU GHN
    # A. GỬI YÊU CẦU GHN
    # A. GỬI YÊU CẦU GHN
    json_data = {"hub_ids": ID_LIST, "is_all_hub": False, "type": 1, "customer_id": None, "ward_code": None, "is_count": False}
    try:
        # Thêm verify=False vào cuối lệnh requests.post
        response = requests.post('https://nhanh-api.ghn.vn/api/core/oss/v1/report/export-backlog-transport', headers=headers, json=json_data, timeout=30, verify=False)
        response.raise_for_status()
        print(f"📡 Đã gửi yêu cầu GHN thành công.")
    except Exception as e:
        print(f"❌ Lỗi API GHN: {e}")
        return

    trigger_time = datetime.now(timezone.utc)

    # B. LẤY LINK TỪ TELEGRAM
    client = TelegramClient(SESSION_FILE, API_ID, API_HASH)
    await client.start(phone=PHONE)
    file_url = None
    for _ in range(60): 
        await asyncio.sleep(10)
        async for message in client.iter_messages(BOT_NAME, limit=3):
            if message.date > trigger_time and 'online-gateway.ghn.vn' in (message.text or ''):
                urls = re.findall(r'https?://online-gateway\.ghn\.vn[^\s)]+', message.text)
                if urls:
                    file_url = urls[0]
                    break
        if file_url: break
    await client.disconnect()

    # C. CẬP NHẬT TAB "1"
    if file_url:
        # Thay đổi ở đây: In ra link bot tìm thấy
        print(f"🔗 Link file tìm được: {file_url}")
        print(f"✅ Đang tải và xử lý dữ liệu...")
        try:
            res = requests.get(file_url)
            df = pd.read_excel(io.BytesIO(res.content), header=1, dtype=str).fillna("")

            # Thay đổi ở đây: Đếm số lượng đơn hàng (số dòng của file excel sau khi load)
            total_orders = len(df)
            print(f"📦 Đã tải xuống thành công: {total_orders} đơn hàng.")

            print(f"📊 Đang kết nối và xóa dữ liệu cũ tại tab '{TAB_NAME}'...")
            creds = Credentials.from_service_account_file(JSON_FILE, scopes=['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive'])
            gc = gspread.authorize(creds)
            
            # Mở sheet và tab chỉ định
            sh = gc.open_by_key(SHEET_ID_DICH)
            worksheet = sh.worksheet(TAB_NAME)
            
            # Xóa trắng tab cũ trước khi ghi
            worksheet.clear()

            # Chuẩn bị dữ liệu và ghi đè
            all_values = [df.columns.values.tolist()] + df.values.tolist()
            
            # Sử dụng USER_ENTERED để giữ định dạng số/ngày tháng chuẩn
            worksheet.update(all_values, value_input_option='USER_ENTERED')
            
            # Thay đổi ở đây: Báo cáo kết quả cuối cùng kèm số lượng đơn
            print(f"🎉 XONG! Đã replace xong {total_orders} đơn hàng vào tab '{TAB_NAME}' rồi nhé Thủy!")

        except Exception as e:
            print(f"❌ Lỗi xử lý file hoặc cập nhật Sheet: {e}")
    else:
        print("❌ Không tìm thấy link file từ Telegram.")

if __name__ == '__main__':
    asyncio.run(run_job())