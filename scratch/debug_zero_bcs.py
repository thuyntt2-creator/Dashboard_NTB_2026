# -*- coding: utf-8 -*-
import sys, os, gspread, unicodedata
from google.oauth2.credentials import Credentials

sys.stdout.reconfigure(encoding='utf-8')
AUTH_FILE = r'C:\Users\lap4all\Documents\Auto report\authorized_user.json'
creds = Credentials.from_authorized_user_file(AUTH_FILE, scopes=['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive'])
gc = gspread.authorize(creds)

from send_realtime_and_target_gtalk import load_target_data, read_baocao_realtime

t_map, l_date = load_target_data()
rt_data = read_baocao_realtime()

bcs = [
    '(BTH) Hàm Liêm', '(BTH) Hàm Thuận', '(BTH) Hàm Thắng', '(BTH) Hàm Tân',
    '(BTH) Liên Hương', '(BTH) Lương Sơn', '(BTH) Phan Rí Cửa', '(BTH) Phú Thủy',
    '(BTH) Phước Hội', '(BTH) Tuyên Quang', '(BTH) Đồng Kho', '(BTH) Đức Linh',
    '(DNO) Cư Jút', '(DNO) Krông Nô', '(DNO) Nhân Cơ 1', '(DNO) ĐL Nam Gia Nghĩa 2'
]

print("\n=== KIỂM TRA TARGET DATA MAP ===")
for b in bcs:
    norm_b = unicodedata.normalize('NFC', b).strip()
    match = t_map.get(norm_b)
    if not match:
        for k, v in t_map.items():
            if norm_b in k or k in norm_b:
                match = v
                break
    if match:
        print(f"{b:<28} -> ID: {match['bc_id']:<10} | Vol Today: {match['vol_today']:<6} | GTC Now: {match['gtc_now']:<6}")
    else:
        print(f"{b:<28} -> KHÔNG CÓ TRONG TARGET MAP")

print("\n=== KIỂM TRA BAOCAO REALTIME ===")
for am_block in rt_data:
    for bc_name, staff in am_block['bcs']:
        for b in bcs:
            if b.lower() in bc_name.lower():
                total_gan = sum(s['gan'] for s in staff)
                total_tc = sum(s['tc'] for s in staff)
                print(f"{bc_name:<28} (AM: {am_block['am']}) -> {len(staff)} NV | Gán: {total_gan} | Giao TC: {total_tc}")
                for s in staff:
                    print(f"     • {s['name']} (Mã: {s['ma_nv']}) | Gán: {s['gan']} | TC: {s['tc']} | LTC: {s['ltc']}")
                break
