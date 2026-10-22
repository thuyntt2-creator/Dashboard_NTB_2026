import sys, os
sys.stdout.reconfigure(encoding='utf-8')
import gspread, pandas as pd
from google.oauth2.credentials import Credentials

creds_path = 'authorized_user.json'
scopes = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
creds = Credentials.from_authorized_user_file(creds_path, scopes=scopes)
gc = gspread.authorize(creds)
sh = gc.open_by_key('1-p9VUXndK_7BoiT-a81UfTCbUi953XNmVBoXaTGis_c')

# 1. Kiểm tra tab auto
ws_auto = sh.worksheet('auto')
rows = ws_auto.get_all_values()
headers = rows[3]
print('Headers in auto:', headers)
df = pd.DataFrame(rows[4:], columns=headers)
col_bc = headers[0]
col_gan = headers[4]
col_gtc = headers[5]
df[col_gan] = pd.to_numeric(df[col_gan].str.replace(',', ''), errors='coerce').fillna(0)
df[col_gtc] = pd.to_numeric(df[col_gtc].str.replace(',', ''), errors='coerce').fillna(0)
agg = df.groupby(col_bc).agg({col_gan: 'sum', col_gtc: 'sum'}).reset_index()
agg = agg[agg[col_gan] > 0]
agg['%GTC'] = agg[col_gtc] / agg[col_gan] * 100
agg_sorted = agg.sort_values(by='%GTC', ascending=True)

print('\n=== TOP 10 BƯU CỤC %GTC TỆ NHẤT TOÀN VÙNG (TỪ TAB AUTO) ===')
for idx, r in agg_sorted.head(15).iterrows():
    print(f"{r[col_bc]}: Gán={int(r[col_gan])}, GTC={int(r[col_gtc])}, %GTC={r['%GTC']:.2f}%")

print('\n=== TOP 5 BƯU CỤC %GTC TỐT NHẤT TOÀN VÙNG ===')
for idx, r in agg_sorted.tail(5).iloc[::-1].iterrows():
    print(f"{r[col_bc]}: Gán={int(r[col_gan])}, GTC={int(r[col_gtc])}, %GTC={r['%GTC']:.2f}%")
