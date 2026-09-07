import sys, json
sys.stdout.reconfigure(encoding='utf-8')
from google.oauth2.credentials import Credentials
import gspread
import pandas as pd
import numpy as np

# 1. PROCESS FILL RATE DATA FROM GOOGLE SHEET
print("=== 1. PROCESSING FILL RATE (W35 & W36) ===")
creds = Credentials.from_authorized_user_file('authorized_user.json')
gc = gspread.authorize(creds)
sh = gc.open_by_key('1rfoi8QaZSZNiYf8IyKNN4QLrjAVxCCGrX9Yli0D8T84')
ws = sh.worksheet('DATA XỬ LÝ')
df_fill = pd.DataFrame(ws.get_all_records())

# Convert Ngày
df_fill['Ngày_dt'] = pd.to_datetime(df_fill['Ngày'], errors='coerce')
# Standardize numeric TLLĐ
def parse_pct(v):
    if pd.isna(v) or v == '': return np.nan
    if isinstance(v, (int, float)): return float(v)
    s = str(v).replace('%', '').strip()
    try: return float(s) / 100.0 if '%' in str(v) else float(s)
    except: return np.nan

# Check TLLĐ column
# In df_fill: 'TLLĐ chuyến (kg)' or 'TLLĐ chuyến (đơn)' or Kg-km đã chở / Kg-km khả dụng
# Let's inspect column names and values
print("Fill columns:", df_fill.columns.tolist()[:10])

# Let's see how TLLĐ is calculated in the sheet
w36 = df_fill[(df_fill['Ngày_dt'] >= '2026-08-31') & (df_fill['Ngày_dt'] <= '2026-09-06')].copy()
w35 = df_fill[(df_fill['Ngày_dt'] >= '2026-08-24') & (df_fill['Ngày_dt'] <= '2026-08-30')].copy()
d05 = df_fill[df_fill['Ngày_dt'] == '2026-09-05'].copy()
d06 = df_fill[df_fill['Ngày_dt'] == '2026-09-06'].copy()

print(f"Count: W35={len(w35)}, W36={len(w36)}, D05={len(d05)}, D06={len(d06)}")

# Let's check how 'Kho' is mapped
print("Kho values in W36:", w36['Kho'].value_counts())
