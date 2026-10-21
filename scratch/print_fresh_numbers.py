# -*- coding: utf-8 -*-
import sys, gspread, unicodedata, pandas as pd
sys.stdout.reconfigure(encoding='utf-8')
from google.oauth2.credentials import Credentials

def norm(s):
    return unicodedata.normalize('NFC', str(s)).strip().lower()

creds = Credentials.from_authorized_user_file('authorized_user.json', ['https://www.googleapis.com/auth/spreadsheets'])
gc = gspread.authorize(creds)
sh = gc.open_by_key('1-p9VUXndK_7BoiT-a81UfTCbUi953XNmVBoXaTGis_c')
ws = sh.worksheet('Data')
rows = ws.get_all_values()
df = pd.DataFrame(rows[1:], columns=rows[0])

df['GTC'] = pd.to_numeric(df['Giao thành công'], errors='coerce').fillna(0)
df['Gan'] = pd.to_numeric(df['Giao'], errors='coerce').fillna(0)
df['bc_norm'] = df['Bưu cục'].apply(norm)

agg = df.groupby('Bưu cục').agg({'GTC': 'sum', 'Gan': 'sum'}).reset_index()
agg['bc_norm'] = agg['Bưu cục'].apply(norm)

print("="*75)
print(f"{'BƯU CỤC':<32} | {'GÁN':<6} | {'GTC LIVE':<8} | {'%GTC'}")
print("="*75)

check_bcs = ['đức trọng 1', 'tân hà', 'quảng khê', 'lang biang', 'bắc cam ranh', 'hòa ninh', 'đức an', 'tây nha trang', "d'ran"]
for bc in check_bcs:
    m = agg[agg['bc_norm'].str.contains(bc, na=False)]
    for _, r in m.iterrows():
        pct = (r['GTC'] / r['Gan'] * 100) if r['Gan'] > 0 else 0
        print(f"{r['Bưu cục']:<32} | {r['Gan']:<6.0f} | {r['GTC']:<8.0f} | {pct:.1f}%")
print("="*75)
