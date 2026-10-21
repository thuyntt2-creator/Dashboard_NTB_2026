# -*- coding: utf-8 -*-
import sys, gspread, pandas as pd
sys.stdout.reconfigure(encoding='utf-8')
from google.oauth2.credentials import Credentials

creds = Credentials.from_authorized_user_file('authorized_user.json', ['https://www.googleapis.com/auth/spreadsheets'])
gc = gspread.authorize(creds)
sh = gc.open_by_key('14cN4YAf01NqKtREtmhBngRP58OCdgby-PjVoixVlpZo')

# 1. Đọc hàng về hiện tại
ws_hv = sh.worksheet('hàng về')
rows_hv = ws_hv.get_all_values()
hv_dict = {}
for r in rows_hv[1:]:
    if len(r) >= 2 and r[0].strip():
        try: hv_dict[r[0].strip()] = int(r[1].replace(',', '').strip())
        except: pass

# 2. Đọc file 21/10 của Chị Thủy
path = r'C:\Users\lap4all\Downloads\Bao_cao_ton_dong_lay_giao_tra_2026-10-21_at_09_00_03.xlsx'
df = pd.read_excel(path, header=1)
df_giao = df[df['Loại đơn'].isin(['Giao', 'Ưu tiên giao'])]
agg = df_giao.groupby('Mã bưu cục')['Mã đơn hàng'].count().to_dict()

# So sánh 10 bưu cục cảnh báo
bc_ids = {
    '22425000': '(LDO) Tân Hà Lâm Hà',
    '20320000': '(KHO) Tây Nha Trang',
    '22759000': '(LDO) Hòa Ninh',
    '23189000': "(LDO) D'Ran",
    '21364000': '(DNO) Quảng Khê',
    '22051000': '(LDO) Lang Biang 1',
    '21687000': '(LDO) Lang Biang 2',
    '21479000': '(KHO) Bắc Cam Ranh',
    '21477000': '(DNO) Đức An',
    '22389000': '(LDO) Đức Trọng 1'
}

print("="*75)
print("SO SÁNH: TAB 'hàng về' HIỆN TẠI VS FILE EXCEL 9H HÔM NAY (21/10)")
print("="*75)
total_hv = sum(hv_dict.values())
total_excel = sum(agg.values())
print(f"Tổng Volume trên tab 'hàng về':  {total_hv:,} đơn")
print(f"Tổng Volume từ File 9h hôm nay:  {total_excel:,} đơn")
print(f"Chênh lệch tổng toàn vùng:       {total_excel - total_hv:+,} đơn")
print("-"*75)

for bc_id, name in bc_ids.items():
    v_sheet = hv_dict.get(bc_id, 0)
    v_excel = agg.get(int(bc_id), agg.get(bc_id, 0))
    diff = v_excel - v_sheet
    print(f"{name:<25} (ID: {bc_id}) | Tab hàng về: {v_sheet:<5} | File Excel 21/10: {v_excel:<5} | Lệch: {diff:+d}")
