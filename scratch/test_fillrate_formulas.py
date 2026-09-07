import sys
sys.stdout.reconfigure(encoding='utf-8')
from google.oauth2.credentials import Credentials
import gspread
import pandas as pd
import numpy as np

creds = Credentials.from_authorized_user_file('authorized_user.json')
gc = gspread.authorize(creds)
sh = gc.open_by_key('1rfoi8QaZSZNiYf8IyKNN4QLrjAVxCCGrX9Yli0D8T84')
ws = sh.worksheet('DATA XỬ LÝ')
df_fill = pd.DataFrame(ws.get_all_records())
df_fill['Ngày_dt'] = pd.to_datetime(df_fill['Ngày'], errors='coerce')

# Convert numeric fields
for c in ['Kg-km đã chở', 'Kg-km khả dụng', 'Kg tiêu chuẩn', 'Tổng km']:
    df_fill[c] = pd.to_numeric(df_fill[c].astype(str).str.replace(',', '').str.strip(), errors='coerce').fillna(0)

# Check TLLĐ formula on D05 and D06
d05 = df_fill[df_fill['Ngày_dt'] == '2026-09-05']
d06 = df_fill[df_fill['Ngày_dt'] == '2026-09-06']
w35 = df_fill[(df_fill['Ngày_dt'] >= '2026-08-24') & (df_fill['Ngày_dt'] <= '2026-08-30')]
w36 = df_fill[(df_fill['Ngày_dt'] >= '2026-08-31') & (df_fill['Ngày_dt'] <= '2026-09-06')]

print("=== Check Daily 05/09 vs 06/09 ===")
for name, sub in [('05/09', d05), ('06/09', d06)]:
    tot_dacho = sub['Kg-km đã chở'].sum()
    tot_khadung = sub['Kg-km khả dụng'].sum()
    pct_weighted = (tot_dacho / tot_khadung * 100) if tot_khadung > 0 else 0
    print(f"Date {name}: {len(sub)} chuyến, Weighted TLLĐ = {pct_weighted:.1f}%")

print("\n=== By Kho for 05/09 vs 06/09 ===")
for kho in ['KTC Khánh Hòa', 'KCT Đức Trọng-Lâm Đồng', 'KCT Đắk Nông', 'KCT Bình Thuận', 'KCT Bảo Lộc-Lâm Đồng']:
    s05 = d05[d05['Kho'] == kho]
    s06 = d06[d06['Kho'] == kho]
    p05 = (s05['Kg-km đã chở'].sum() / s05['Kg-km khả dụng'].sum() * 100) if s05['Kg-km khả dụng'].sum() > 0 else 0
    p06 = (s06['Kg-km đã chở'].sum() / s06['Kg-km khả dụng'].sum() * 100) if s06['Kg-km khả dụng'].sum() > 0 else 0
    # check <10%, 10-20%, 20-30%
    c10 = len(s06[s06['Nhóm TLLĐ'].str.contains('<10%|Dưới 10%|N1.', na=False, case=False)])
    c20 = len(s06[s06['Nhóm TLLĐ'].str.contains('10-20%|10%-20%|N2.', na=False, case=False)])
    c30 = len(s06[s06['Nhóm TLLĐ'].str.contains('20-30%|20%-30%|N3.', na=False, case=False)])
    print(f"{kho}: 05/09={len(s05)} ({p05:.1f}%) | 06/09={len(s06)} ({p06:.1f}%) | <10%={c10}, 10-20%={c20}, 20-30%={c30}")

print("\n=== Check W35 vs W36 ===")
p35 = (w35['Kg-km đã chở'].sum() / w35['Kg-km khả dụng'].sum() * 100)
p36 = (w36['Kg-km đã chở'].sum() / w36['Kg-km khả dụng'].sum() * 100)
print(f"W35: {len(w35)} chuyến, TLLĐ={p35:.1f}%")
print(f"W36: {len(w36)} chuyến, TLLĐ={p36:.1f}% (Diff: {p36 - p35:+.1f}%p)")

print("\n=== W35 vs W36 By Kho ===")
for kho in ['KTC Khánh Hòa', 'KCT Đức Trọng-Lâm Đồng', 'KCT Đắk Nông', 'KCT Bình Thuận', 'KCT Bảo Lộc-Lâm Đồng']:
    s35 = w35[w35['Kho'] == kho]
    s36 = w36[w36['Kho'] == kho]
    p35_k = (s35['Kg-km đã chở'].sum() / s35['Kg-km khả dụng'].sum() * 100) if s35['Kg-km khả dụng'].sum() > 0 else 0
    p36_k = (s36['Kg-km đã chở'].sum() / s36['Kg-km khả dụng'].sum() * 100) if s36['Kg-km khả dụng'].sum() > 0 else 0
    c30_36 = len(s36[s36['Nhóm TLLĐ'].str.contains('N1.|N2.|N3.|<30%|< 30%', na=False, case=False)])
    print(f"{kho}: W35={len(s35)} ({p35_k:.1f}%) | W36={len(s36)} ({p36_k:.1f}%) | Diff={p36_k - p35_k:+.1f}%p | Chuyến<30% W36={c30_36}")
