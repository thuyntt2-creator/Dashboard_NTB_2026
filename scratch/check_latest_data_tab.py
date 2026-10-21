# -*- coding: utf-8 -*-
import sys, gspread
import pandas as pd
sys.stdout.reconfigure(encoding='utf-8')
from google.oauth2.credentials import Credentials

creds = Credentials.from_authorized_user_file('authorized_user.json', ['https://www.googleapis.com/auth/spreadsheets'])
gc = gspread.authorize(creds)
sh = gc.open_by_key('1-p9VUXndK_7BoiT-a81UfTCbUi953XNmVBoXaTGis_c')
ws = sh.worksheet('Data')
rows = ws.get_all_values()
headers = rows[0]
df = pd.DataFrame(rows[1:], columns=headers)

col_gtc = [c for c in headers if 'giao thành công' in c.lower()][0]
col_giao = [c for c in headers if c.strip().lower() == 'giao'][0]
col_bc = [c for c in headers if 'bưu cục' in c.lower()][0]

df[col_gtc] = pd.to_numeric(df[col_gtc], errors='coerce').fillna(0)
df[col_giao] = pd.to_numeric(df[col_giao], errors='coerce').fillna(0)

agg = df.groupby(col_bc).agg({col_gtc: 'sum', col_giao: 'sum'}).reset_index()

print("="*65)
print(f"{'BƯU CỤC':<28} | {'GÁN':<6} | {'GTC LIVE':<8} | {'%GTC'}")
print("="*65)
for bc in ['Đức Trọng 1', 'Tân Hà', 'Quảng Khê', 'Lang Biang', 'Bắc Cam Ranh', 'Hòa Ninh', 'Đức An', 'Tây Nha Trang', "D'Ran"]:
    m = agg[agg[col_bc].str.contains(bc, case=False, na=False)]
    for _, r in m.iterrows():
        pct = (r[col_gtc] / r[col_giao] * 100) if r[col_giao] > 0 else 0
        print(f"{r[col_bc]:<28} | {r[col_giao]:<6.0f} | {r[col_gtc]:<8.0f} | {pct:.1f}%")
print("="*65)
