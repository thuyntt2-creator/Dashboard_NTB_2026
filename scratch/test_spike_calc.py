import os, sys
import pandas as pd
import numpy as np

sys.stdout.reconfigure(encoding='utf-8')

df_ops = pd.read_csv("scratch/sheet_sl_10kg_raw.csv")
df_tao = pd.read_csv("scratch/sheet_tren10kg_raw.csv")

print("=== Check dates in df_ops ===")
# Parse date from Time: '2026-08-29 - Thứ 7' -> '2026-08-29'
df_ops['date_str'] = df_ops['Time'].astype(str).apply(lambda x: x.split(' - ')[0].strip() if ' - ' in str(x) else str(x).strip())
print(df_ops['date_str'].value_counts().sort_index())

print("\n=== Check dates in df_tao ===")
df_tao['date_str'] = df_tao['ngay_tao_don'].astype(str).str.strip()
print(df_tao['date_str'].value_counts().sort_index())

# Let's see PO names in df_ops vs df_tao
ops_pos = set(df_ops['Chi tiết'].dropna().unique())
tao_pos = set(df_tao['warehouse_name'].dropna().unique())
print(f"\nUnique POs in df_ops: {len(ops_pos)}")
print(f"Unique POs in df_tao: {len(tao_pos)}")
common_pos = ops_pos.intersection(tao_pos)
print(f"Common POs exact match: {len(common_pos)}")

# Check clean matching
def clean_po(s):
    if not s or pd.isna(s): return ""
    import unicodedata
    s = unicodedata.normalize('NFC', str(s).strip().lower())
    for prefix in ['bưu cục', 'kho', 'bc', 'đpxl', 'dpxl', 'hub', 'ghn']:
        if s.startswith(prefix):
            s = s[len(prefix):].strip()
    return s.strip()

ops_pos_clean = {clean_po(p): p for p in ops_pos}
tao_pos_clean = {clean_po(p): p for p in tao_pos}
matched_clean = set(ops_pos_clean.keys()).intersection(set(tao_pos_clean.keys()))
print(f"Clean matched POs: {len(matched_clean)} / {len(ops_pos_clean)}")

# Let's test Surge calculation on latest date: 2026-08-29
latest_date_ops = sorted(df_ops['date_str'].unique())[-1]
prev_dates_ops = [d for d in sorted(df_ops['date_str'].unique()) if d < latest_date_ops]
print(f"\nLatest date ops: {latest_date_ops}, Previous dates: {prev_dates_ops[-5:]}")

# PO level volume by date in df_ops
po_date_ops = df_ops.groupby(['Chi tiết', 'date_str', 'Tỉnh', 'AM'])['Volume'].sum().reset_index()

# Latest day volume vs previous days average
po_latest = po_date_ops[po_date_ops['date_str'] == latest_date_ops].rename(columns={'Volume': 'vol_latest'})
po_prev = po_date_ops[po_date_ops['date_str'].isin(prev_dates_ops[-7:])].groupby('Chi tiết')['Volume'].agg(['mean', 'max', 'count']).reset_index()
po_prev.columns = ['Chi tiết', 'vol_avg_prev', 'vol_max_prev', 'days_count']

surge_df = pd.merge(po_latest, po_prev, on='Chi tiết', how='left').fillna({'vol_avg_prev': 0, 'vol_max_prev': 0, 'days_count': 0})
surge_df['vol_diff'] = surge_df['vol_latest'] - surge_df['vol_avg_prev']
surge_df['growth_pct'] = np.where(surge_df['vol_avg_prev'] > 0, ((surge_df['vol_latest'] - surge_df['vol_avg_prev']) / surge_df['vol_avg_prev'] * 100).round(1), np.where(surge_df['vol_latest'] > 0, 100.0, 0.0))

print("\n--- TOP 10 POs with highest surge on latest date (SL > 10kg) ---")
print(surge_df.sort_values(by='growth_pct', ascending=False)[['Chi tiết', 'Tỉnh', 'AM', 'vol_latest', 'vol_avg_prev', 'vol_diff', 'growth_pct']].head(10))

