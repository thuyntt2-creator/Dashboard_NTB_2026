# -*- coding: utf-8 -*-
import os
import sys
import time
import requests
from PIL import Image

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

sys.stdout.reconfigure(encoding='utf-8')

OA_TOKEN = "2077276776281051136:8hMHvBBU8qXKps3mLPzgKBucPLSQPg3Y"
CHANNEL_ID = "2077278419534073856"
IMAGE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bao_cao_gtc_15h.png")

caption = (
    "📢 <b>[TIẾN ĐỘ] CẬP NHẬT XỬ LÝ & GIAO THÀNH CÔNG (GTC) ĐƠN TTS</b>\n"
    "📊 <b>Tổng đơn:</b> 72 đơn (9 AM - 18 Bưu cục)\n"
    "✅ <b>Đã GTC:</b> <b>16 đơn (22.2%)</b> — Thưởng hiện tại: <b>160.000đ</b>\n"
    "⚡ <b>Đang đi giao:</b> <b>24 đơn (33.3%)</b> — Tiềm năng gom thêm: <b>+240.000đ</b>\n"
    "⏰ <b>Hạn chót:</b> Các đơn GTC trước <b>18h00 hôm nay</b> được thưởng 10k/đơn!"
)

def send_image_to_gtalk(image_path, channel_id, oa_token, caption_text):
    print("=" * 60)
    print(f"📡 Bắt đầu gửi ảnh sang GTalk...")
    print(f"👉 Channel ID: {channel_id}")
    print(f"👉 File ảnh: {image_path}")
    print("=" * 60)

    if not os.path.exists(image_path):
        print(f"❌ File ảnh không tồn tại: {image_path}")
        return False

    img = Image.open(image_path)
    width, height = img.size
    file_size = os.path.getsize(image_path)
    print(f"Kích thước: {width}x{height}, dung lượng: {file_size:,} bytes")

    # Step 1: Initiate Upload
    initiate_url = "https://mbff.ghn.vn/api/gtalk/initiate-upload"
    payload_init = {
        "ChannelId": str(channel_id),
        "FileName": os.path.basename(image_path),
        "FileSize": str(file_size),
        "MimeType": "image/png",
        "Metadata": f'{{"width": {width}, "height": {height}}}',
        "oaToken": oa_token
    }
    headers = {"Content-Type": "application/json"}
    
    print("⏳ Bước 1: Khởi tạo upload...")
    res_init = requests.post(initiate_url, json=payload_init, headers=headers, timeout=20, verify=False)
    if res_init.status_code != 200:
        print(f"❌ Lỗi HTTP Initiate: {res_init.status_code} - {res_init.text}")
        return False
    data_init = res_init.json()
    if data_init.get("errorCode") != "success":
        print(f"❌ Lỗi API Initiate: {data_init.get('error')}")
        return False
    
    presigned_url = data_init["data"]["PresignedURL"]
    upload_id = data_init["data"]["UploadId"]
    print(f"✅ Khởi tạo upload thành công! UploadId: {upload_id}")

    # Step 2: Upload S3
    print("⏳ Bước 2: Upload file lên S3...")
    with open(image_path, "rb") as f:
        headers_put = {"Content-Type": "image/png"}
        res_put = requests.put(presigned_url, data=f, headers=headers_put, timeout=60, verify=False)
        if res_put.status_code != 200:
            print(f"❌ Lỗi PUT S3: {res_put.status_code} - {res_put.text}")
            return False
    print("✅ Upload S3 thành công!")

    # Step 3: Complete Upload
    print("⏳ Bước 3: Hoàn tất upload...")
    complete_url = "https://mbff.ghn.vn/api/gtalk/complete-upload"
    payload_comp = {
        "oaToken": oa_token,
        "UploadId": upload_id
    }
    res_comp = requests.post(complete_url, json=payload_comp, headers=headers, timeout=20, verify=False)
    if res_comp.status_code != 200:
        print(f"❌ Lỗi Complete HTTP: {res_comp.status_code} - {res_comp.text}")
        return False
    data_comp = res_comp.json()
    if data_comp.get("errorCode") != "success":
        print(f"❌ Lỗi API Complete: {data_comp.get('error')}")
        return False
    file_id = data_comp["data"]["Id"]
    print(f"✅ Hoàn tất upload! FileId: {file_id}")

    # Step 4: Send Message with Attachment
    print("⏳ Bước 4: Gửi tin nhắn chứa ảnh...")
    send_url = "https://mbff.ghn.vn/api/gtalk/send-message"
    client_msg_id = str(int(time.time() * 1000))
    payload_send = {
        "channelId": str(channel_id),
        "clientMsgId": client_msg_id,
        "content": {
            "parseMode": "HTML",
            "attachment": {
                "caption": caption_text,
                "items": [
                    {
                        "image": {
                            "fileId": file_id,
                            "width": width,
                            "height": height
                        }
                    }
                ]
            }
        },
        "oaToken": oa_token
    }
    res_send = requests.post(send_url, json=payload_send, headers=headers, timeout=20, verify=False)
    if res_send.status_code == 200:
        data_send = res_send.json()
        if data_send.get("errorCode") == "success":
            print("🎉 GỬI ẢNH BÁO CÁO THÀNH CÔNG SANG GTALK!")
            return True
        else:
            print(f"❌ Lỗi API gửi tin: {data_send.get('error')}")
    else:
        print(f"❌ Lỗi HTTP gửi tin: {res_send.status_code} - {res_send.text}")
    return False

if __name__ == '__main__':
    send_image_to_gtalk(IMAGE_PATH, CHANNEL_ID, OA_TOKEN, caption)
