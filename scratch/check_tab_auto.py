# -*- coding: utf-8 -*-
import sys, gspread
import pandas as pd
sys.stdout.reconfigure(encoding='utf-8')
from google.oauth2.credentials import Credentials

creds = Credentials.from_authorized_user_file('authorized_user.json', ['https://www.googleapis.com/auth/spreadsheets'])
gc = gspread.authorize(creds)
sh = gc.open_by_key('1-p9VUXndK_7BoiT-a81UfTCbUi953XNmVBoXaTGis_c')

ws_auto = sh.worksheet('auto')
rows = ws_auto.get_all_values()
print(f"Tổng số dòng tab 'auto': {len(rows)}")

headers = rows[3]
print("Headers:", headers)
data = rows[4:]
df = pd.DataFrame(data, columns=headers[:len(data[0]) if data else len(headers)])
print(df.head())

col_bc = headers[0]
col_gan = headers[4]
col_gtc = headers[5]

df[col_gtc] = pd.to_numeric(df[col_gtc].str.replace(',', ''), errors='coerce').fillna(0)
df[col_gan] = pd.to_numeric(df[col_gan].str.replace(',', ''), errors='coerce').fillna(0)

agg = df.groupby(col_bc).agg({col_gtc: 'sum', col_gan: 'sum'}).reset_index()

print("\n=== AGGREGATE TỪ TAB 'auto' ===")
bc_alert = ['Tân Hà', 'Quảng Khê', 'Lang Biang', 'Đức An', 'Hòa Ninh', 'Đức Trọng', 'Tây Nha Trang', "D'Ran", 'Bắc Cam Ranh']
for bc in bc_alert:
    m = agg[agg[col_bc].str.contains(bc, case=False, na=False)]
    for _, r in m.iterrows():
        pct = (r[col_gtc] / r[col_gan] * 100) if r[col_gan] > 0 else 0
        print(f"{r[col_bc]:<32} | Gán: {r[col_gan]:<5.0f} | GTC: {r[col_gtc]:<5.0f} | %GTC: {pct:.1f}%")
