import sys, os
sys.stdout.reconfigure(encoding='utf-8')
import gspread, pandas as pd
from google.oauth2.credentials import Credentials

creds_path = 'authorized_user.json'
scopes = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
creds = Credentials.from_authorized_user_file(creds_path, scopes=scopes)
gc = gspread.authorize(creds)
sh = gc.open_by_key('1-p9VUXndK_7BoiT-a81UfTCbUi953XNmVBoXaTGis_c')
ws_auto = sh.worksheet('auto')
rows = ws_auto.get_all_values()
headers = rows[3]
df = pd.DataFrame(rows[4:], columns=headers)
col_nv = headers[3]
col_bc = headers[0]
col_am = headers[1]
col_gan = headers[4]
col_gtc = headers[5]
col_pct = headers[6]

df[col_gan] = pd.to_numeric(df[col_gan].str.replace(',', ''), errors='coerce').fillna(0)
df[col_gtc] = pd.to_numeric(df[col_gtc].str.replace(',', ''), errors='coerce').fillna(0)

# Lọc nhân viên có gán thực tế (>= 20 đơn)
df_active = df[df[col_gan] >= 20].copy()
df_active['pct_val'] = df_active[col_gtc] / df_active[col_gan] * 100
df_worst = df_active.sort_values(by='pct_val', ascending=True).head(10)

print("=== TOP 10 NHÂN VIÊN GTC TỆ NHẤT TOÀN VÙNG (GÁN >= 20 ĐƠN) ===")
for idx, r in df_worst.iterrows():
    nv = r[col_nv]
    bc = r[col_bc]
    am = r[col_am]
    gan = int(r[col_gan])
    gtc = int(r[col_gtc])
    pct = r['pct_val']
    print(f"• {nv} ({bc} - AM {am}): Gán {gan} | GTC {gtc} -> {pct:.1f}%")
