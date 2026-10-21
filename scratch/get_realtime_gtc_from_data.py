# -*- coding: utf-8 -*-
import sys, gspread, pandas as pd
sys.stdout.reconfigure(encoding='utf-8')
from google.oauth2.credentials import Credentials

creds = Credentials.from_authorized_user_file('authorized_user.json', ['https://www.googleapis.com/auth/spreadsheets'])
gc = gspread.authorize(creds)
sh = gc.open_by_key('1-p9VUXndK_7BoiT-a81UfTCbUi953XNmVBoXaTGis_c')
ws_data = sh.worksheet('Data')
rows = ws_data.get_all_values()
headers = rows[0]
df = pd.DataFrame(rows[1:], columns=headers)

df_today = df[df['Thời gian ghi'].str.contains('21/10/2026', na=False)].copy()
print(f"Tổng số bản ghi chuyến đi hôm nay (21/10): {len(df_today)}")

df_today['GTC_num'] = pd.to_numeric(df_today['Giao thành công'].str.replace(',', ''), errors='coerce').fillna(0)
df_today['Giao_num'] = pd.to_numeric(df_today['Giao'].str.replace(',', ''), errors='coerce').fillna(0)

# Lấy bản ghi mới nhất của mỗi DriverID
# hoặc tổng hợp theo Bưu cục
agg = df_today.groupby('Bưu cục').agg({'GTC_num': 'sum', 'Giao_num': 'sum'}).reset_index()

bc_alert = ['Tân Hà', 'Quảng Khê', 'Lang Biang', 'Đức An', 'Hòa Ninh', 'Đức Trọng', 'Tây Nha Trang', "D'Ran", 'Bắc Cam Ranh']

print("\n=== NĂNG SUẤT GTC REALTIME LIVE CHUẨN XÁC TỪ TAB DATA (21/10) ===")
for bc in bc_alert:
    m = agg[agg['Bưu cục'].str.contains(bc, case=False, na=False)]
    for _, r in m.iterrows():
        gtc = r['GTC_num']
        giao = r['Giao_num']
        pct = (gtc / giao * 100) if giao > 0 else 0
        print(f"{r['Bưu cục']:<32} | Đã gán giao: {giao:<5.0f} | Đã GTC: {gtc:<5.0f} | %GTC: {pct:.1f}%")
