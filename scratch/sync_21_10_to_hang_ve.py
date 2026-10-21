# -*- coding: utf-8 -*-
import sys, gspread, os
import pandas as pd
sys.stdout.reconfigure(encoding='utf-8')
from google.oauth2.credentials import Credentials

path_21 = r'C:\Users\lap4all\Downloads\Bao_cao_ton_dong_lay_giao_tra_2026-10-21_at_09_00_03.xlsx'
if not os.path.exists(path_21):
    print("❌ Không tìm thấy file 21/10!")
    sys.exit(1)

print("1. Đang đọc dữ liệu từ file chốt 9h hôm nay (21/10)...")
df = pd.read_excel(path_21, header=1)
df_giao = df[df['Loại đơn'].isin(['Giao', 'Ưu tiên giao'])]
agg = df_giao.groupby('Mã bưu cục')['Mã đơn hàng'].count().reset_index()
agg.columns = ['Mã bưu cục', 'Số lượng đơn']

data_to_upload = [['Mã bưu cục', 'Số lượng đơn']] + [[str(r['Mã bưu cục']), str(r['Số lượng đơn'])] for _, r in agg.iterrows()]
total_vol = agg['Số lượng đơn'].sum()
print(f"-> Tổng hợp thành công: {len(agg)} bưu cục. Tổng Volume: {total_vol:,} đơn.")

# 2. Upload vào tab 'hàng về'
print("2. Đang ghi đè số liệu chốt 21/10 vào tab 'hàng về' trên Google Sheet...")
creds_path = 'authorized_user.json'
creds = Credentials.from_authorized_user_file(creds_path, ['https://www.googleapis.com/auth/spreadsheets'])
gc = gspread.authorize(creds)
sh = gc.open_by_key('14cN4YAf01NqKtREtmhBngRP58OCdgby-PjVoixVlpZo')
ws_hv = sh.worksheet('hàng về')
ws_hv.clear()
ws_hv.update(range_name='A1', values=data_to_upload)
print("-> ĐÃ ĐỒNG BỘ THÀNH CÔNG DỮ LIỆU CHỐT 21/10 VÀO TAB 'hàng về'!")
