import sys
sys.stdout.reconfigure(encoding='utf-8')
import gspread
from google.oauth2.credentials import Credentials as UserCredentials
import pandas as pd
import json

scopes = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
creds = UserCredentials.from_authorized_user_file(r'C:\Users\lap4all\Desktop\auto-report\authorized_user.json', scopes=scopes)
gc = gspread.authorize(creds)

sh2 = gc.open_by_key('1lmQv8KwHJzDFs_RMz64ydu4SOmG3M1YAzILNFGtzFec')
ws = sh2.worksheet('BC_canh_bao')
rows = ws.get_all_values()

print("BC_canh_bao rows:")
for i, r in enumerate(rows):
    # filter out trailing empties
    r_clean = [x for x in r if x != '']
    print(f"Row {i}: {r_clean[:10]}")

# Also inspect raw_buu_cuc_canh_bao for NTB
ws_raw = sh2.worksheet('raw_buu_cuc_canh_bao')
raw_rows = ws_raw.get_all_values()
df_raw = pd.DataFrame(raw_rows[1:], columns=raw_rows[0])
print("\nraw_buu_cuc_canh_bao columns:", list(df_raw.columns))
print("Vung counts:", df_raw['vung'].value_counts().to_dict())
df_ntb = df_raw[df_raw['vung'] == 'NTB']
print(f"NTB rows: {len(df_ntb)}")
for _, r in df_ntb.iterrows():
    print(f"{r['bc_id']} | {r['buu_cuc']} | {r['tinh_quan']} | {r['pct_gtc_7ngay']} | {r['pct_gtc_lich_su_tot_nhat']} | {r['canh_bao_gtc']}")

