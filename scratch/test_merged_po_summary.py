import sys, pandas as pd, numpy as np

sys.stdout.reconfigure(encoding='utf-8')
import app

df_ops = app.safe_read_csv('ops_heavy_10kg.csv')
df_tao = app.safe_read_csv('ops_tao_don_10kg.csv')
df_co_cau = app.safe_read_csv('ops_co_cau.csv')

print(f"Loaded df_ops: {len(df_ops)}, df_tao: {len(df_tao)}")

new_in_day_col = next((c for c in df_ops.columns if c.lower() in ['hàng mới về trong ngày', 'hang moi ve trong ngay', 'hàng mới về', 'hang moi ve']), None)
print("new_in_day_col:", new_in_day_col)

df_ops['Hàng Mới Về Trong Ngày'] = app.safe_to_numeric(df_ops[new_in_day_col]) if new_in_day_col else 0.0
df_ops['Volume'] = app.safe_to_numeric(df_ops['Volume'])
df_ops['delivered_vol'] = app.safe_to_numeric(df_ops['Sản Lượng Giao Thành Công']) if 'Sản Lượng Giao Thành Công' in df_ops.columns else df_ops['Volume'] * app.normalize_pct_col(df_ops['% GTC'])
df_ops['Leadtime'] = app.safe_to_numeric(df_ops['Leadtime'])
df_ops['clean_bc'] = df_ops['Chi tiết'].astype(str).apply(app.clean_str)

df_tao['vol'] = app.safe_to_numeric(df_tao['vol'])
df_tao['kl_kg'] = app.safe_to_numeric(df_tao['kl_kg'])
df_tao['clean_bc'] = df_tao['warehouse_name'].astype(str).apply(app.clean_str)

# Group ops
ops_po = df_ops.groupby(['Chi tiết', 'clean_bc', 'mapped_am', 'mapped_prov']).agg({
    'Volume': 'sum',
    'delivered_vol': 'sum',
    'Leadtime': 'mean',
    'Hàng Mới Về Trong Ngày': 'sum'
}).reset_index()

# Group tao
tao_po = df_tao.groupby('clean_bc').agg({
    'vol': 'sum',
    'kl_kg': 'sum'
}).reset_index()

merged = pd.merge(ops_po, tao_po, on='clean_bc', how='outer')
merged['Chi tiết'] = merged['Chi tiết'].fillna(merged['clean_bc'])
merged['Volume'] = merged['Volume'].fillna(0)
merged['delivered_vol'] = merged['delivered_vol'].fillna(0)
merged['Hàng Mới Về Trong Ngày'] = merged['Hàng Mới Về Trong Ngày'].fillna(0)
merged['vol'] = merged['vol'].fillna(0)
merged['kl_kg'] = merged['kl_kg'].fillna(0)
merged['% GTC'] = (merged['delivered_vol'] / merged['Volume'] * 100).round(2).fillna(0)

merged = merged.sort_values(by='vol', ascending=False)
print("Top 10 Merged POs by Created Volume (vol):")
print(merged[['Chi tiết', 'mapped_am', 'vol', 'Hàng Mới Về Trong Ngày', 'Volume', '% GTC']].head(10).to_string())
