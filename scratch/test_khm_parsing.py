import os
import sys
import gspread
from google.oauth2.service_account import Credentials
from dotenv import load_dotenv
import pandas as pd
import re
from datetime import datetime, timedelta

sys.stdout.reconfigure(encoding='utf-8')
load_dotenv()

JSON_FILE = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS') or r'C:\Users\lap4all\Desktop\Backlog_Automation\credentials.json'
if not os.path.exists(JSON_FILE):
    JSON_FILE = 'credentials.json'

sheet_id = "12VsqpIx1vLOqk6-JKHwgRmdrgu6fxSNPQcpyO0wpvdQ"
creds = Credentials.from_service_account_file(
    JSON_FILE, 
    scopes=['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
)
gc = gspread.authorize(creds)
sh = gc.open_by_key(sheet_id)

_MONTH_MAP = {f"thg {i}": i for i in range(1, 13)}

def parse_vn_date(s):
    s = str(s).strip()
    for m, num in _MONTH_MAP.items():
        if m in s:
            parts = re.findall(r"\d+", s)
            if len(parts) >= 2:
                return datetime(int(parts[-1]), num, int(parts[0]))
    return None

def ws_to_df(ss, name):
    print(f"  📥 {name} ...", end=" ", flush=True)
    # Use UNFORMATTED_VALUE to get raw numbers from sheet!
    data = ss.worksheet(name).get_all_values(value_render_option='UNFORMATTED_VALUE')
    if not data: print("trống"); return pd.DataFrame()
    df = pd.DataFrame(data[1:], columns=data[0])
    for col in df.columns:
        try:
            df[col] = pd.to_numeric(df[col], errors="ignore")
        except Exception: pass
    print(f"{len(df)} dòng ✅"); return df

print("Testing raw KHM loading and calculations...")
df_khm = ws_to_df(sh, "khách hàng mơi")
df_coc = ws_to_df(sh, "Cocauvung")

am_tinh = (df_coc[["AM","Tỉnh"]].dropna()
           .drop_duplicates("AM").set_index("AM")["Tỉnh"].to_dict())

def get_tinh(am):
    am = str(am).strip()
    if am in am_tinh: return am_tinh[am]
    for k, v in am_tinh.items():
        if am in k or k in am: return v
    return "Khác"

df_khm["Ngay"]           = df_khm["Ngày LTC đầu tiên"].apply(parse_vn_date)
df_khm["DoanhThu_NoVAT"] = pd.to_numeric(df_khm["DoanhThu_NoVAT"], errors="coerce").fillna(0)
df_khm["Volume"]         = pd.to_numeric(df_khm["Volume"],          errors="coerce").fillna(0)

# Filter KHM for NTB
df_ntb = df_khm[df_khm["AM"].isin(set(am_tinh.keys()))].copy()
df_ntb["Tinh"] = df_ntb["AM"].apply(get_tinh)

# Find last dates
dates = sorted(df_ntb["Ngay"].dropna().unique())
d_cur = dates[-1]
print(f"Current Date: {d_cur.date()}")

# Aggregate
mask_16 = (df_ntb["Ngay"] == d_cur)
sub_16 = df_ntb[mask_16]
gp_16 = sub_16.groupby("Tinh").agg(SLKH=("Mã KH","count"),Vol=("Volume","sum"),DT=("DoanhThu_NoVAT","sum"))
print("\nCalculated GroupBy for 16/06:")
print(gp_16)
