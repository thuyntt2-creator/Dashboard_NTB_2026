import pandas as pd
import numpy as np
import sys
import re
from datetime import datetime
import json
import os

sys.stdout.reconfigure(encoding='utf-8')

print("🚀 Testing truy thu comparison with full W38 data from w38.csv...")

def parse_ghn_date(val):
    if not val or not isinstance(val, str):
        return None
    val = val.strip()
    m = re.search(r'(\d{1,2})\s+thg\s+(\d{1,2}),?\s+(\d{4})', val)
    if m:
        return datetime(int(m.group(3)), int(m.group(2)), int(m.group(1)))
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

# 1. Load W38
df_w38 = pd.read_csv(r'C:\Users\lap4all\Downloads\w38.csv', low_memory=False)
df_w38['date'] = df_w38['Ngày kết luận truy thu'].apply(parse_ghn_date)
df_w38['ban_dau'] = df_w38['Số tiền ban đầu'].apply(parse_vn)
df_w38['dieu_chinh'] = df_w38['Điều chỉnh (+|-)'].apply(parse_vn)
df_w38['da_thu'] = df_w38['Đã truy thu'].apply(parse_vn)
df_w38['can_thu'] = df_w38['Cần truy thu thêm'].apply(parse_vn)

# Filter exact W38: 14/09/2026 to 20/09/2026
prev_start = datetime(2026, 9, 14)
prev_end = datetime(2026, 9, 20)
w_prev = df_w38[(df_w38['date'] >= prev_start) & (df_w38['date'] <= prev_end)].copy()

# 2. Load W39 from sheet_truythu.csv
df_w39 = pd.read_csv('sheet_truythu.csv', low_memory=False)
df_w39['date'] = df_w39['Ngày kết luận truy thu'].apply(parse_ghn_date)
df_w39['ban_dau'] = df_w39['Số tiền ban đầu'].apply(parse_vn)
df_w39['dieu_chinh'] = df_w39['Điều chỉnh (+|-)'].apply(parse_vn)
df_w39['da_thu'] = df_w39['Đã truy thu'].apply(parse_vn)
df_w39['can_thu'] = df_w39['Cần truy thu thêm'].apply(parse_vn)

# Filter exact W39: 21/09/2026 to 27/09/2026
curr_start = datetime(2026, 9, 21)
curr_end = datetime(2026, 9, 27)
w_curr = df_w39[(df_w39['date'] >= curr_start) & (df_w39['date'] <= curr_end)].copy()

print(f"W38 (14/09 - 20/09): {len(w_prev):,} records")
print(f"W39 (21/09 - 27/09): {len(w_curr):,} records")

# Summary metrics
rec_prev = len(w_prev)
rec_curr = len(w_curr)
diff_rec = rec_curr - rec_prev
pct_diff_rec = (diff_rec / rec_prev * 100) if rec_prev else 0

bd_prev = w_prev['ban_dau'].sum()
bd_curr = w_curr['ban_dau'].sum()
diff_bd = bd_curr - bd_prev
pct_diff_bd = (diff_bd / bd_prev * 100) if bd_prev else 0

ct_prev = w_prev['can_thu'].sum()
ct_curr = w_curr['can_thu'].sum()
diff_ct = ct_curr - ct_prev
pct_diff_ct = (diff_ct / ct_prev * 100) if ct_prev else 0

print("\n=== SUMMARY RECALCULATED ===")
print(f"Tổng Ticket: W38 = {rec_prev:,} -> W39 = {rec_curr:,} (Δ = {diff_rec:+d} | {pct_diff_rec:+.1f}%)")
print(f"Số tiền ban đầu: W38 = {bd_prev:,.0f} đ -> W39 = {bd_curr:,.0f} đ (Δ = {diff_bd:+,.0f} đ | {pct_diff_bd:+.1f}%)")
print(f"Số tiền cần thu: W38 = {ct_prev:,.0f} đ -> W39 = {ct_curr:,.0f} đ (Δ = {diff_ct:+,.0f} đ | {pct_diff_ct:+.1f}%)")

# By Loai truy thu comparison
print("\n=== TOP LOẠI TRUY THU (W38 vs W39) ===")
types_prev = w_prev.groupby('Loại truy thu').agg(don_prev=('Mã ticket', 'count'), can_thu_prev=('can_thu', 'sum'))
types_curr = w_curr.groupby('Loại truy thu').agg(don_curr=('Mã ticket', 'count'), can_thu_curr=('can_thu', 'sum'))
types_cmp = pd.concat([types_prev, types_curr], axis=1).fillna(0)
types_cmp['diff_don'] = types_cmp['don_curr'] - types_cmp['don_prev']
types_cmp['diff_can_thu'] = types_cmp['can_thu_curr'] - types_cmp['can_thu_prev']
types_cmp = types_cmp.sort_values('can_thu_curr', ascending=False)
for idx, r in types_cmp.head(8).iterrows():
    print(f"- {idx}: W38={r['don_prev']:.0f} đơn ({r['can_thu_prev']:,.0f} đ) -> W39={r['don_curr']:.0f} đơn ({r['can_thu_curr']:,.0f} đ) | Δ đơn={r['diff_don']:+.0f}, Δ tiền={r['diff_can_thu']:+,.0f} đ")
