# -*- coding: utf-8 -*-
import os
import sys
import time
import unicodedata
from collections import defaultdict
import requests
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

sys.stdout.reconfigure(encoding='utf-8')

SPREADSHEET_ID = "1JSbLo353RgRCTuGyyMmPH7jiB48tNIRMXR6KMze39jg"
GID = "1149501631"
SHEET_LINK = f"https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/edit?gid={GID}#gid={GID}"
GTALK_API_URL = "https://mbff.ghn.vn/api/gtalk/send-message"

def normalize_str(s):
    if not s:
        return ""
    return unicodedata.normalize("NFC", str(s)).strip()

def load_data():
    scopes = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
    creds = Credentials.from_authorized_user_file('authorized_user.json', scopes=scopes)
    service = build('sheets', 'v4', credentials=creds)

    res1 = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID, range='Sheet1').execute()
    sheet1_vals = res1.get('values', [])

    res3 = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID, range='Sheet3').execute()
    sheet3_vals = res3.get('values', [])

    token = None
    am_group_map = {}
    for r in sheet3_vals:
        if len(r) >= 2:
            k = normalize_str(r[0])
            v = normalize_str(r[1])
            if k.upper() == 'TOKEN':
                token = v
            elif k and v:
                am_group_map[k] = v

    orders_by_am = defaultdict(lambda: defaultdict(list))
    total_orders = 0

    for r in sheet1_vals[1:]:
        vung = normalize_str(r[0]) if len(r) > 0 else ''
        tinh = normalize_str(r[1]) if len(r) > 1 else ''
        bc = normalize_str(r[2]) if len(r) > 2 else ''
        madh = normalize_str(r[3]) if len(r) > 3 else ''
        am = normalize_str(r[4]) if len(r) > 4 else ''

        if madh and am:
            orders_by_am[am][bc].append(madh)
            total_orders += 1

    return token, am_group_map, orders_by_am, total_orders

def format_message(am_name, bc_dict):
    total_am_orders = sum(len(mads) for mads in bc_dict.values())
    total_bcs = len(bc_dict)

    lines = [
        f"🚨 <b>[THÔNG BÁO KHẨN] XỬ LÝ GẤP ĐƠN TTS TRƯỚC 15H</b>",
        f"👤 <b>AM: {am_name}</b>",
        f"📊 <b>Tổng cộng:</b> <b>{total_am_orders} đơn</b> ({total_bcs} bưu cục)",
        f"",
        f"🎁 <b>CHÍNH SÁCH THƯỞNG NÓNG:</b>",
        f"👉 <b>Mỗi đơn GTC trước 18h HÔM NAY sẽ được THƯỞNG 10.000đ/đơn!</b>",
        f"⏰ <b>Yêu cầu:</b> AM push Bưu cục xử lý gấp <b>trước 15h00 hôm nay</b>.",
        f"",
        f"📍 <b>DANH SÁCH ĐƠN HÀNG CẦN XỬ LÝ THEO BƯU CỤC:</b>"
    ]

    for idx, (bc, mads) in enumerate(bc_dict.items(), 1):
        lines.append(f"\n📦 <b>{idx}. Bưu cục: {bc}</b> (<b>{len(mads)}</b> đơn):")
        # Format MĐV list
        for m_idx, madh in enumerate(mads, 1):
            lines.append(f"   {m_idx}. <code>{madh}</code>")

    lines.append(f"\n🔗 <b>Chi tiết danh sách tại Sheet:</b>")
    lines.append(f"<a href=\"{SHEET_LINK}\">👉 Link Bảng Tính Google Sheet</a>")

    return "\n".join(lines)

if __name__ == '__main__':
    token, am_group_map, orders_by_am, total = load_data()
    print(f"Token: {token}")
    print(f"Total AMs: {len(orders_by_am)}, Total orders: {total}")
    for am, bcs in orders_by_am.items():
        gid = am_group_map.get(am)
        print(f"\n{'='*60}")
        print(f"AM: {am} | Group ID: {gid}")
        print(f"{'='*60}")
        msg = format_message(am, bcs)
        print(msg)
