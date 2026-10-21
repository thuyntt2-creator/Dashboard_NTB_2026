# -*- coding: utf-8 -*-
import sys, gspread, pandas as pd
sys.stdout.reconfigure(encoding='utf-8')
from google.oauth2.credentials import Credentials

creds = Credentials.from_authorized_user_file('authorized_user.json', ['https://www.googleapis.com/auth/spreadsheets'])
gc = gspread.authorize(creds)
sh = gc.open_by_key('1-p9VUXndK_7BoiT-a81UfTCbUi953XNmVBoXaTGis_c')
ws_bc = sh.worksheet('BaoCao')
rows = ws_bc.get_all_values()

# Header is row 4 (index 3)
headers = rows[3]
# Match column lengths
data_rows = []
for r in rows[4:]:
    if len(r) >= 9 and r[0].strip():
        data_rows.append(r[:9])

df = pd.DataFrame(data_rows, columns=headers[:9])
print(f"Tổng số nhân viên/rider trong BaoCao: {len(df)}")

df['Giao TC'] = pd.to_numeric(df['Giao TC'].str.replace(',', ''), errors='coerce').fillna(0)
df['Gán Giao'] = pd.to_numeric(df['Gán Giao'].str.replace(',', ''), errors='coerce').fillna(0)
agg = df.groupby('Bưu Cục').agg({'Giao TC': 'sum', 'Gán Giao': 'sum'}).reset_index()

bc_alert = ['Tân Hà', 'Quảng Khê', 'Lang Biang', 'Đức An', 'Hòa Ninh', 'Đức Trọng', 'Tây Nha Trang', "D'Ran", 'Bắc Cam Ranh']

print("\n=== NĂNG SUẤT GTC REALTIME LIVE TỪ TAB BAOCAO (GID 491121158) ===")
for bc in bc_alert:
    m = agg[agg['Bưu Cục'].str.contains(bc, case=False, na=False)]
    for _, r in m.iterrows():
        pct = (r['Giao TC'] / r['Gán Giao'] * 100) if r['Gán Giao'] > 0 else 0
        print(f"{r['Bưu Cục']:<32} | Gán: {r['Gán Giao']:<5.0f} | GTC Live: {r['Giao TC']:<5.0f} | %GTC: {pct:.1f}%")
