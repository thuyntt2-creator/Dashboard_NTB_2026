import os, sys, re, json
import pandas as pd
import numpy as np

sys.stdout.reconfigure(encoding='utf-8')

def is_ck_po(name):
    if not name or pd.isna(name):
        return False
    s = str(name).strip().lower()
    # Match CK as a distinct word or prefix like (KHO) CK, CK Diên Điền, BCCK, etc.
    return bool(re.search(r'(^|\s|\(|\/|-)ck(\s|\)|\/|-|$)|bcck|cồng kềnh|cong kenh', s))

# Load the 2 raw sheets
df_ops = pd.read_csv("scratch/sheet_sl_10kg_raw.csv")
df_tao = pd.read_csv("scratch/sheet_tren10kg_raw.csv")

print(f"Loaded df_ops: {df_ops.shape}, df_tao: {df_tao.shape}")

# Parse Date
df_ops['date'] = df_ops['Time'].astype(str).apply(lambda x: x.split(' - ')[0].strip() if ' - ' in str(x) else str(x).strip())
df_tao['date'] = df_tao['ngay_tao_don'].astype(str).str.strip()

# Numeric conversions
df_ops['Volume'] = pd.to_numeric(df_ops['Volume'], errors='coerce').fillna(0)
df_ops['Sản Lượng Giao Thành Công'] = pd.to_numeric(df_ops['Sản Lượng Giao Thành Công'], errors='coerce').fillna(0)
df_ops['Hàng Mới Về Trong Ngày'] = pd.to_numeric(df_ops['Hàng Mới Về Trong Ngày'], errors='coerce').fillna(0)
df_ops['Leadtime'] = pd.to_numeric(df_ops['Leadtime'], errors='coerce').fillna(0)
df_ops['Sản Lượng Tồn'] = pd.to_numeric(df_ops['Sản Lượng Tồn'], errors='coerce').fillna(0)

df_tao['so_don'] = pd.to_numeric(df_tao['so_don'], errors='coerce').fillna(0)
df_tao['warehouse_name'] = df_tao['warehouse_name'].fillna('Không xác định')

# Clean PO names
df_ops['po_name'] = df_ops['Chi tiết'].fillna('Không xác định').astype(str).str.strip()
df_tao['po_name'] = df_tao['warehouse_name'].fillna('Không xác định').astype(str).str.strip()

df_ops['is_ck'] = df_ops['po_name'].apply(is_ck_po)
df_tao['is_ck'] = df_tao['po_name'].apply(is_ck_po)

print(f"CK POs in df_ops: {df_ops[df_ops['is_ck']]['po_name'].unique()}")
print(f"CK POs in df_tao: {df_tao[df_tao['is_ck']]['po_name'].unique()}")

# Dates list
all_ops_dates = sorted(df_ops['date'].unique())
latest_date = all_ops_dates[-1]
prev_7_dates = [d for d in all_ops_dates if d < latest_date][-7:]

print(f"\nAll dates: {all_ops_dates}")
print(f"Latest date: {latest_date}, Baseline 7 days: {prev_7_dates}")

# 1. PO Aggregation on Latest Date vs Baseline in df_ops
ops_latest = df_ops[df_ops['date'] == latest_date].groupby(['po_name', 'Tỉnh', 'AM', 'is_ck']).agg({
    'Volume': 'sum',
    'Sản Lượng Giao Thành Công': 'sum',
    'Hàng Mới Về Trong Ngày': 'sum',
    'Sản Lượng Tồn': 'sum',
    'Leadtime': 'mean'
}).reset_index().rename(columns={
    'Volume': 'vol_actual_latest',
    'Sản Lượng Giao Thành Công': 'gtc_actual_latest',
    'Hàng Mới Về Trong Ngày': 'incoming_actual_latest',
    'Sản Lượng Tồn': 'ton_actual_latest',
    'Leadtime': 'leadtime_latest'
})

ops_prev = df_ops[df_ops['date'].isin(prev_7_dates)].groupby('po_name')['Volume'].agg(['mean', 'max', 'count']).reset_index().rename(columns={
    'mean': 'vol_actual_avg_prev',
    'max': 'vol_actual_max_prev',
    'count': 'days_count_prev'
})

# 2. PO Aggregation in df_tao (Tạo đơn)
tao_latest = df_tao[df_tao['date'] == latest_date].groupby('po_name')['so_don'].sum().reset_index().rename(columns={'so_don': 'vol_created_latest'})
tao_prev = df_tao[df_tao['date'].isin(prev_7_dates)].groupby('po_name')['so_don'].mean().reset_index().rename(columns={'so_don': 'vol_created_avg_prev'})

# Merge all into PO summary
po_summary = pd.merge(ops_latest, ops_prev, on='po_name', how='left')
po_summary = pd.merge(po_summary, tao_latest, on='po_name', how='left')
po_summary = pd.merge(po_summary, tao_prev, on='po_name', how='left')

po_summary = po_summary.fillna({
    'vol_actual_avg_prev': 0, 'vol_actual_max_prev': 0, 'days_count_prev': 0,
    'vol_created_latest': 0, 'vol_created_avg_prev': 0
})

# Calculate growth & diffs
po_summary['actual_diff_vol'] = (po_summary['vol_actual_latest'] - po_summary['vol_actual_avg_prev']).round(1)
po_summary['actual_growth_pct'] = np.where(
    po_summary['vol_actual_avg_prev'] > 0,
    ((po_summary['vol_actual_latest'] - po_summary['vol_actual_avg_prev']) / po_summary['vol_actual_avg_prev'] * 100).round(1),
    np.where(po_summary['vol_actual_latest'] > 0, 100.0, 0.0)
)

po_summary['created_diff_vol'] = (po_summary['vol_created_latest'] - po_summary['vol_created_avg_prev']).round(1)
po_summary['created_growth_pct'] = np.where(
    po_summary['vol_created_avg_prev'] > 0,
    ((po_summary['vol_created_latest'] - po_summary['vol_created_avg_prev']) / po_summary['vol_created_avg_prev'] * 100).round(1),
    np.where(po_summary['vol_created_latest'] > 0, 100.0, 0.0)
)

po_summary['gtc_pct'] = np.where(
    po_summary['vol_actual_latest'] > 0,
    (po_summary['gtc_actual_latest'] / po_summary['vol_actual_latest'] * 100).round(1),
    0.0
)

def assign_spike_status(row):
    growth = row['actual_growth_pct']
    diff = row['actual_diff_vol']
    if growth >= 100 and diff >= 15:
        return 'CRITICAL', '🔴 Đột biến cực đại (+{:.0f}%)'.format(growth)
    elif (growth >= 50 and diff >= 10) or growth >= 80:
        return 'HIGH', '🟠 Đột biến cao (+{:.0f}%)'.format(growth)
    elif growth >= 25 and diff >= 5:
        return 'WARNING', '🟡 Tăng nhanh (+{:.0f}%)'.format(growth)
    elif growth <= -30:
        return 'DOWN', '📉 Giảm mạnh ({:.0f}%)'.format(growth)
    else:
        return 'NORMAL', '🟢 Bình thường'

po_summary['spike_level'], po_summary['spike_label'] = zip(*po_summary.apply(assign_spike_status, axis=1))

print("\n--- SAMPLE CRITICAL/HIGH SPIKE POS ---")
spikes = po_summary[po_summary['spike_level'].isin(['CRITICAL', 'HIGH'])].sort_values(by='actual_growth_pct', ascending=False)
print(spikes[['po_name', 'Tỉnh', 'AM', 'is_ck', 'vol_actual_latest', 'vol_actual_avg_prev', 'actual_growth_pct', 'spike_label']].head(10))

print("\n--- CK (BƯU CỤC CỒNG KỀNH) POS SUMMARY ---")
ck_summary = po_summary[po_summary['is_ck'] == True]
print(ck_summary[['po_name', 'Tỉnh', 'AM', 'vol_actual_latest', 'vol_actual_avg_prev', 'actual_growth_pct', 'gtc_pct', 'spike_label']])

