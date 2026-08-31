import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
import sys
sys.stdout.reconfigure(encoding='utf-8')

JSON_FILE = r'C:\Users\lap4all\Desktop\Backlog_Automation\credentials.json'
SHEET_ID = '1LEmer5MUw2iC40NXOsFI4BHJ0WHLdkxn8FSKG7cZLsc'

creds = Credentials.from_service_account_file(
    JSON_FILE, 
    scopes=['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
)
gc = gspread.authorize(creds)
sh = gc.open_by_key(SHEET_ID)

# Read online raw data
ws = sh.worksheet('dataLTC TTS')
data = ws.get_all_values()
headers = data[0]
df = pd.DataFrame(data[1:], columns=headers)

# Mapping using online cocau
df_cocau = pd.DataFrame(sh.worksheet('cocau').get_all_values())
df_cocau.columns = df_cocau.iloc[0]
df_cocau = df_cocau.iloc[1:]
df_cocau['BC_norm'] = df_cocau['BC'].str.strip().str.upper()
bc_to_am = dict(zip(df_cocau['BC_norm'], df_cocau['Am']))

df['BC_norm'] = df['Chi tiết'].str.strip().str.upper()
df['AM_mapped'] = df['BC_norm'].map(bc_to_am)

subset = df[(df['AM_mapped'] == 'Phạm Bá Thành Công') & (df['Time'] == '2026/24')]
print("Online dataLTC TTS rows for Phạm Bá Thành Công in W24:")
print(subset[['Chi tiết', 'Volume', '%Gán', '%LTC']])

vol_tot = pd.to_numeric(subset['Volume'], errors='coerce').sum()
vol_gan = (pd.to_numeric(subset['Volume'], errors='coerce') * pd.to_numeric(subset['%Gán'], errors='coerce')).sum()
vol_ltc = (pd.to_numeric(subset['Volume'], errors='coerce') * pd.to_numeric(subset['%LTC'], errors='coerce')).sum()
pct_ltc_vol = vol_ltc / vol_tot if vol_tot > 0 else 0
print(f"Online LTC rate (vol_ltc / vol_tot): {pct_ltc_vol*100:.4f}%")
