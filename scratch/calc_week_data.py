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

# 2. Read RAW FD N-1 (HUB)
res = service.spreadsheets().values().get(spreadsheetId=work_id, range="'RAW FD N-1 (HUB)'!A1:H").execute()
rows = res.get('values', [])
df = pd.DataFrame(rows[1:], columns=rows[0])
df['dt'] = pd.to_datetime(df['delivery_date'], errors='coerce')
df['Total'] = pd.to_numeric(df['Total đơn'].str.replace(',', ''), errors='coerce').fillna(0)
df['Return'] = pd.to_numeric(df['Đơn return'].str.replace(',', ''), errors='coerce').fillna(0)
df['BC'] = df['Tên bưu cục'].astype(str).str.strip()
df['ID'] = df['ID bưu cục'].astype(str).str.strip()

if 'AM' in df.columns:
    df['AM'] = df['AM'].astype(str).str.strip()
else:
    df['AM'] = ''

mask_no_am = (df['AM'] == '') | (df['AM'] == 'None')
df.loc[mask_no_am, 'AM'] = df.loc[mask_no_am, 'BC'].map(bc_to_am).fillna('')

# Filter valid
df_valid = df[(df['AM'] != '') & (df['AM'] != 'None') & (~df['BC'].str.lower().str.contains('kho giao hàng'))].copy()

# We only care about T2 (14/09) onwards!
start_date = pd.Timestamp('2026-09-14')
df_week = df_valid[df_valid['dt'] >= start_date].copy()

dates_in_week = sorted(df_week['dt'].dropna().unique())
print("Dates in week:", [pd.Timestamp(d).strftime('%Y-%m-%d (%a)') for d in dates_in_week])

# Let's inspect the 3 focus bưu cục
focus_bcs = [
    '(LDO) Lang Biang - Đà Lạt 1',
    '(DNO) Kiến Đức',
    '(KHO) Tây Nha Trang'
]

print("\n--- 3 FOCUS BƯU CỤC DAY BY DAY ---")
for bc in focus_bcs:
    sub = df_week[df_week['BC'] == bc]
    grp = sub.groupby('dt').agg({'Total': 'sum', 'Return': 'sum'}).reset_index()
    grp['%FD'] = (grp['Return'] / grp['Total'] * 100).round(2)
    tot_t = grp['Total'].sum()
    tot_r = grp['Return'].sum()
    pct_cum = (tot_r / tot_t * 100).round(2)
    print(f"\n{bc} (AM: {sub['AM'].iloc[0] if len(sub) else ''}):")
    for _, r in grp.iterrows():
        print(f"  {r['dt'].strftime('%d/%m (%a)')}: Total={r['Total']:,.0f}, Return={r['Return']:,.0f}, %FD={r['%FD']:.2f}%")
    print(f"  TOTAL ({len(dates_in_week)}N): Total={tot_t:,.0f}, Return={tot_r:,.0f}, %FD={pct_cum:.2f}%")

# Overall Vùng NTB
tot_vung_t = df_week['Total'].sum()
tot_vung_r = df_week['Return'].sum()
pct_vung = (tot_vung_r / tot_vung_t * 100).round(2)
print(f"\n--- TOÀN VÙNG NTB ({len(dates_in_week)}N) ---")
print(f"Total Gán: {tot_vung_t:,.0f}")
print(f"Total Return: {tot_vung_r:,.0f}")
print(f"%FD: {pct_vung:.2f}%")
print(f"Số bưu cục: {df_week['BC'].nunique()}")

# Top 10 Bưu cục toàn vùng lũy kế
bc_cum = df_week.groupby(['ID', 'BC', 'AM']).agg({'Total': 'sum', 'Return': 'sum'}).reset_index()
bc_cum['%FD'] = (bc_cum['Return'] / bc_cum['Total'] * 100).round(2)
bc_cum['Tỷ trọng return'] = (bc_cum['Return'] / tot_vung_r * 100).round(2)
bc_cum['Tỷ trọng sản lượng'] = (bc_cum['Total'] / tot_vung_t * 100).round(2)
top10 = bc_cum.sort_values('%FD', ascending=False).head(10).reset_index(drop=True)

print(f"\n--- TOP 10 BƯU CỤC LŨY KẾ ({len(dates_in_week)}N) ---")
print(top10[['ID', 'BC', 'AM', 'Total', 'Return', '%FD', 'Tỷ trọng return', 'Tỷ trọng sản lượng']])

# Xếp hạng AM lũy kế
am_cum = df_week.groupby('AM').agg({'Total': 'sum', 'Return': 'sum'}).reset_index()
am_cum['%FD'] = (am_cum['Return'] / am_cum['Total'] * 100).round(2)
am_cum['Tỷ trọng return'] = (am_cum['Return'] / tot_vung_r * 100).round(2)
am_cum['Tỷ trọng sản lượng'] = (am_cum['Total'] / tot_vung_t * 100).round(2)
am_ranking = am_cum.sort_values('%FD', ascending=False).reset_index(drop=True)

print(f"\n--- XẾP HẠNG 18 AM LŨY KẾ ({len(dates_in_week)}N) ---")
print(am_ranking[['AM', 'Total', 'Return', '%FD', 'Tỷ trọng return', 'Tỷ trọng sản lượng']])
