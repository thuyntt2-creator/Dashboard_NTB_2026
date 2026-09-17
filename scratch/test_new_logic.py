import sys
sys.stdout.reconfigure(encoding='utf-8')
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import pandas as pd
import numpy as np

creds = Credentials.from_authorized_user_file('authorized_user.json', ['https://www.googleapis.com/auth/spreadsheets'])
service = build('sheets', 'v4', credentials=creds)
work_id = '15Z-aMM6OFfiWUXd2Zwz6BFNq_Y0KWwHiVDqxkioHufM'

# 1. Load CoCauVung
res_cc = service.spreadsheets().values().get(spreadsheetId=work_id, range="CoCauVung!A1:D1000").execute()
rows_cc = res_cc.get('values', [])
bc_to_am = {}
if len(rows_cc) >= 2:
    df_cc = pd.DataFrame(rows_cc[1:], columns=rows_cc[0])
    bc_col = df_cc.iloc[:, 1].astype(str).str.strip()
    am_col = df_cc.iloc[:, 3].astype(str).str.strip()
    bc_to_am = dict(zip(bc_col, am_col))
print(f"CoCauVung loaded: {len(bc_to_am)} mappings")

# 2. Load RAW FD N-1 (HUB)
res_raw = service.spreadsheets().values().get(spreadsheetId=work_id, range="'RAW FD N-1 (HUB)'!A1:H").execute()
rows_raw = res_raw.get('values', [])
header = rows_raw[0]
df_raw = pd.DataFrame(rows_raw[1:], columns=header)
print(f"Raw rows: {len(df_raw)}")

# Parse columns
df_raw['dt'] = pd.to_datetime(df_raw['delivery_date'], errors='coerce')
df_raw['Total'] = pd.to_numeric(df_raw['Total đơn'].str.replace(',', ''), errors='coerce').fillna(0)
df_raw['Return'] = pd.to_numeric(df_raw['Đơn return'].str.replace(',', ''), errors='coerce').fillna(0)
df_raw['BC'] = df_raw['Tên bưu cục'].astype(str).str.strip()
df_raw['ID'] = df_raw['ID bưu cục'].astype(str).str.strip()

# AM assignment
if 'AM' in df_raw.columns:
    df_raw['AM'] = df_raw['AM'].astype(str).str.strip()
else:
    df_raw['AM'] = ''

mask_no_am = (df_raw['AM'] == '') | (df_raw['AM'] == 'None')
df_raw.loc[mask_no_am, 'AM'] = df_raw.loc[mask_no_am, 'BC'].map(bc_to_am).fillna('')

# Filter out empty AM or "kho giao hàng"
df_valid = df_raw[(df_raw['AM'] != '') & (~df_raw['BC'].str.lower().str.contains('kho giao hàng'))].copy()
print(f"Valid rows: {len(df_valid)}")

available_dates = sorted(df_valid['dt'].dropna().unique())
print("Available dates:", [pd.Timestamp(d).strftime('%Y-%m-%d') for d in available_dates])

if len(available_dates) >= 2:
    date_N = pd.Timestamp(available_dates[-1])
    date_N1 = pd.Timestamp(available_dates[-2])
elif len(available_dates) == 1:
    date_N = pd.Timestamp(available_dates[0])
    date_N1 = None
else:
    raise ValueError("No valid dates found!")

print(f"Date N: {date_N.strftime('%d/%m/%Y')}")
print(f"Date N-1: {date_N1.strftime('%d/%m/%Y') if date_N1 else 'None'}")

# Process Date N
df_N = df_valid[df_valid['dt'] == date_N].copy()
bc_N = df_N.groupby(['ID', 'BC', 'AM']).agg({'Total': 'sum', 'Return': 'sum'}).reset_index()
tot_don_N = bc_N['Total'].sum()
tot_ret_N = bc_N['Return'].sum()
fd_N = (tot_ret_N / tot_don_N * 100) if tot_don_N > 0 else 0.0
bc_N['%FD_N'] = (bc_N['Return'] / bc_N['Total'] * 100).round(2)
bc_N['Tỷ trọng return'] = (bc_N['Return'] / tot_ret_N * 100).round(2) if tot_ret_N > 0 else 0.0

# Process Date N-1
if date_N1 is not None:
    df_N1 = df_valid[df_valid['dt'] == date_N1].copy()
    bc_N1 = df_N1.groupby(['ID', 'BC']).agg({'Total': 'sum', 'Return': 'sum'}).reset_index()
    tot_don_N1 = bc_N1['Total'].sum()
    tot_ret_N1 = bc_N1['Return'].sum()
    fd_N1 = (tot_ret_N1 / tot_don_N1 * 100) if tot_don_N1 > 0 else 0.0
    bc_N1['%FD_N1'] = (bc_N1['Return'] / bc_N1['Total'] * 100).round(2)
    bc_merged = pd.merge(bc_N, bc_N1[['ID', 'BC', '%FD_N1']], on=['ID', 'BC'], how='left')
    bc_merged['vs_N1'] = (bc_merged['%FD_N'] - bc_merged['%FD_N1']).round(2)
else:
    bc_merged = bc_N.copy()
    bc_merged['%FD_N1'] = np.nan
    bc_merged['vs_N1'] = np.nan
    tot_don_N1 = 0
    tot_ret_N1 = 0
    fd_N1 = 0.0

all_bc_df = bc_merged.sort_values('%FD_N', ascending=False).reset_index(drop=True)
top10_bc = all_bc_df.head(10)

print("\n--- TOP 10 BƯU CỤC (N vs N-1) ---")
print(top10_bc[['BC', 'AM', 'Total', 'Return', '%FD_N', '%FD_N1', 'vs_N1', 'Tỷ trọng return']])

# Process AM
am_N = df_N.groupby('AM').agg({'Total': 'sum', 'Return': 'sum'}).reset_index()
am_N['%FD_N'] = (am_N['Return'] / am_N['Total'] * 100).round(2)
am_N['Tỷ trọng return'] = (am_N['Return'] / tot_ret_N * 100).round(2) if tot_ret_N > 0 else 0.0
am_N['Tỷ trọng sản lượng'] = (am_N['Total'] / tot_don_N * 100).round(2) if tot_don_N > 0 else 0.0

if date_N1 is not None:
    am_N1 = df_N1.groupby('AM').agg({'Total': 'sum', 'Return': 'sum'}).reset_index()
    am_N1['%FD_N1'] = (am_N1['Return'] / am_N1['Total'] * 100).round(2)
    am_merged = pd.merge(am_N, am_N1[['AM', '%FD_N1']], on='AM', how='left')
    am_merged['vs_N1'] = (am_merged['%FD_N'] - am_merged['%FD_N1']).round(2)
else:
    am_merged = am_N.copy()
    am_merged['%FD_N1'] = np.nan
    am_merged['vs_N1'] = np.nan

am_merged = am_merged.sort_values('%FD_N', ascending=False).reset_index(drop=True)
print("\n--- AM RANKING (N vs N-1) ---")
print(am_merged[['AM', 'Total', 'Return', '%FD_N', '%FD_N1', 'vs_N1', 'Tỷ trọng return', 'Tỷ trọng sản lượng']])
