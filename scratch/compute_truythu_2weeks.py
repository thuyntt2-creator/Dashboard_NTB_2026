import pandas as pd
import numpy as np
import sys
import re
from datetime import datetime
import json
import os

sys.stdout.reconfigure(encoding='utf-8')

# Read truythu raw
tt = pd.read_csv('scratch/truythu_raw.csv', low_memory=False)

def parse_ghn_date(val):
    if not val or not isinstance(val, str):
        return None
    val = val.strip()
    m = re.search(r'(\d{1,2})\s+thg\s+(\d{1,2}),?\s+(\d{4})', val)
    if m:
        d, mth, y = int(m.group(1)), int(m.group(2)), int(m.group(3))
        return datetime(y, mth, d)
    m2 = re.search(r'(\d{4})-(\d{2})-(\d{2})', val)
    if m2:
        return datetime(int(m2.group(1)), int(m2.group(2)), int(m2.group(3)))
    m3 = re.search(r'(\d{1,2})/(\d{1,2})/(\d{4})', val)
    if m3:
        return datetime(int(m3.group(3)), int(m3.group(2)), int(m3.group(1)))
    return None

def parse_vn(s):
    try:
        return float(str(s).replace('.', '').replace(',', '.'))
    except:
        return 0.0

tt['date'] = tt['Ngày kết luận truy thu'].apply(parse_ghn_date)
tt['ban_dau'] = tt['Số tiền ban đầu'].apply(parse_vn)
tt['dieu_chinh'] = tt['Điều chỉnh (+|-)'].apply(parse_vn)
tt['da_thu'] = tt['Đã truy thu'].apply(parse_vn)
tt['can_thu'] = tt['Cần truy thu thêm'].apply(parse_vn)

# Filter 2 weeks
w_prev = tt[(tt['date'] >= datetime(2026, 9, 7)) & (tt['date'] <= datetime(2026, 9, 13))].copy()
w_curr = tt[(tt['date'] >= datetime(2026, 9, 14)) & (tt['date'] <= datetime(2026, 9, 20))].copy()

print(f"Tuần N-1 (07/09-13/09): {len(w_prev)} records | Ban đầu: {w_prev['ban_dau'].sum()/1e6:.1f} Tr | Cần thu: {w_prev['can_thu'].sum()/1e6:.1f} Tr")
print(f"Tuần N   (14/09-20/09): {len(w_curr)} records | Ban đầu: {w_curr['ban_dau'].sum()/1e6:.1f} Tr | Cần thu: {w_curr['can_thu'].sum()/1e6:.1f} Tr")

# Map AM
am_rows = tt[tt['Chức vụ'].astype(str).str.contains('Area Manager', na=False)].copy()
am_rows['ten_am'] = am_rows['Nhân viên'].astype(str).apply(lambda x: x.split('-', 1)[1].strip() if '-' in x else x)
bc_am_map = {}
for bc, group in am_rows.groupby('Nơi vi phạm'):
    top_am = group['ten_am'].value_counts().index[0]
    bc_am_map[bc] = top_am

# Load co_cau_ntb for BC -> Tỉnh & AM
bc_tinh_map = {}
if os.path.exists('co_cau_ntb.csv'):
    cc = pd.read_csv('co_cau_ntb.csv')
    cols = cc.columns.tolist()
    name_col = next((c for c in cols if 'bưu cục' in c.lower() or 'warehouse' in c.lower() or 'tên' in c.lower()), cols[1])
    prov_col = next((c for c in cols if 'tỉnh' in c.lower() or 'province' in c.lower()), cols[2])
    am_col = next((c for c in cols if 'am' in c.lower()), None)
    for _, row in cc.iterrows():
        bc_name = str(row[name_col]).strip()
        prov_name = str(row[prov_col]).strip()
        bc_tinh_map[bc_name] = prov_name
        if am_col and bc_name not in bc_am_map:
            bc_am_map[bc_name] = str(row[am_col]).strip()

# Helper function to extract province from '(KHO) Nha Trang' if not in map
def get_province(bc):
    if bc in bc_tinh_map and bc_tinh_map[bc] and bc_tinh_map[bc] != 'nan':
        return bc_tinh_map[bc]
    if '(KHO)' in bc: return 'Khánh Hòa'
    if '(LDO)' in bc: return 'Lâm Đồng'
    if '(DNO)' in bc: return 'Đắk Nông'
    if '(BTH)' in bc: return 'Bình Thuận'
    if '(NTH)' in bc: return 'Ninh Thuận'
    return 'Khác'

w_prev['AM'] = w_prev['Nơi vi phạm'].map(bc_am_map).fillna('Chưa gán')
w_curr['AM'] = w_curr['Nơi vi phạm'].map(bc_am_map).fillna('Chưa gán')
w_prev['Tỉnh'] = w_prev['Nơi vi phạm'].apply(get_province)
w_curr['Tỉnh'] = w_curr['Nơi vi phạm'].apply(get_province)

# 1. AM Comparison
am_p = w_prev.groupby('AM').agg(ticket_prev=('Mã truy thu', 'count'), can_thu_prev=('can_thu', 'sum'))
am_c = w_curr.groupby('AM').agg(ticket_curr=('Mã truy thu', 'count'), can_thu_curr=('can_thu', 'sum'))
am_cmp = pd.concat([am_p, am_c], axis=1).fillna(0)
am_cmp['diff_ticket'] = am_cmp['ticket_curr'] - am_cmp['ticket_prev']
am_cmp['diff_can_thu'] = am_cmp['can_thu_curr'] - am_cmp['can_thu_prev']
am_cmp = am_cmp.sort_values('can_thu_curr', ascending=False)

print("\n--- SO SÁNH THEO AM (Top 15 Cần Thu Tuần N) ---")
for idx, r in am_cmp.head(15).iterrows():
    print(f"{idx:<22} | Ticket: {int(r['ticket_prev']):<4} -> {int(r['ticket_curr']):<4} ({int(r['diff_ticket']):+4}) | Cần thu: {r['can_thu_prev']/1e6:5.1f}Tr -> {r['can_thu_curr']/1e6:5.1f}Tr ({r['diff_can_thu']/1e6:+5.1f}Tr)")

# 2. Province Comparison
prov_p = w_prev.groupby('Tỉnh').agg(don_prev=('Mã truy thu', 'count'), can_thu_prev=('can_thu', 'sum'))
prov_c = w_curr.groupby('Tỉnh').agg(don_curr=('Mã truy thu', 'count'), can_thu_curr=('can_thu', 'sum'))
prov_cmp = pd.concat([prov_p, prov_c], axis=1).fillna(0)
prov_cmp['diff_don'] = prov_cmp['don_curr'] - prov_cmp['don_prev']
prov_cmp['diff_can_thu'] = prov_cmp['can_thu_curr'] - prov_cmp['can_thu_prev']
prov_cmp = prov_cmp.sort_values('can_thu_curr', ascending=False)

print("\n--- SO SÁNH THEO TỈNH ---")
for idx, r in prov_cmp.iterrows():
    print(f"{idx:<15} | Đơn: {int(r['don_prev']):<4} -> {int(r['don_curr']):<4} ({int(r['diff_don']):+4}) | Cần thu: {r['can_thu_prev']/1e6:5.1f}Tr -> {r['can_thu_curr']/1e6:5.1f}Tr ({r['diff_can_thu']/1e6:+5.1f}Tr)")

# 3. Top BC Comparison
bc_p = w_prev.groupby(['Nơi vi phạm', 'AM', 'Tỉnh']).agg(don_prev=('Mã truy thu', 'count'), can_thu_prev=('can_thu', 'sum'))
bc_c = w_curr.groupby(['Nơi vi phạm', 'AM', 'Tỉnh']).agg(don_curr=('Mã truy thu', 'count'), can_thu_curr=('can_thu', 'sum'))
bc_cmp = pd.concat([bc_p, bc_c], axis=1).fillna(0).reset_index()
bc_cmp['diff_don'] = bc_cmp['don_curr'] - bc_cmp['don_prev']
bc_cmp['diff_can_thu'] = bc_cmp['can_thu_curr'] - bc_cmp['can_thu_prev']
bc_cmp = bc_cmp.sort_values('can_thu_curr', ascending=False)

print("\n--- TOP 10 BC TRUY THU CAO NHẤT TUẦN N ---")
for _, r in bc_cmp.head(10).iterrows():
    print(f"{r['Nơi vi phạm']:<25} ({r['AM']}) | Đơn: {int(r['don_prev']):<4} -> {int(r['don_curr']):<4} ({int(r['diff_don']):+4}) | Cần thu: {r['can_thu_prev']/1e6:5.1f}Tr -> {r['can_thu_curr']/1e6:5.1f}Tr ({r['diff_can_thu']/1e6:+5.1f}Tr)")
