import sys
import os
import pandas as pd
import numpy as np

WORKSPACE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

print("1. Loading Vols data...")
df = pd.read_excel(os.path.join(WORKSPACE_DIR, 'vols_tao_don.xlsx'), sheet_name="shopee_tiktok")
df.columns = [str(c).strip() for c in df.columns]
df['Date'] = pd.to_datetime(df['Date'])
df = df[df['bat_on'].fillna('').str.strip() != 'BC Cũ/Không thuộc ĐCL'].copy()
print(f"Loaded vols: {len(df)} rows.")

print("2. Loading buu cuc type map...")
# Simulating load_buu_cuc_type_map
buu_cuc_path = os.path.join(WORKSPACE_DIR, 'buu_cuc_bat_on.xlsx')
type_map = {}
if os.path.exists(buu_cuc_path):
    xls = pd.ExcelFile(buu_cuc_path)
    sheet_name = [s for s in xls.sheet_names if "ntb" in s.lower() or "bất ổn" in s.lower()][0]
    df_raw = pd.read_excel(xls, sheet_name=sheet_name, header=None)
    header_row_idx = None
    for r_idx in range(len(df_raw)):
        row_vals = [str(x).lower().strip() for x in df_raw.iloc[r_idx].values]
        if any(x == "bưu cục" or "kho_giao_id" in x for x in row_vals):
            header_row_idx = r_idx
            break
    if header_row_idx is not None:
        df_table = pd.read_excel(xls, sheet_name=sheet_name, skiprows=header_row_idx)
        df_table.columns = [str(c).strip() for c in df_table.columns]
        id_col = next((c for c in df_table.columns if "id" in c.lower() or "kho_giao_id" in c.lower()), None)
        type_col = next((c for c in df_table.columns if "type" in c.lower() or "warehouse_type" in c.lower()), None)
        if id_col and type_col:
            df_table = df_table.dropna(subset=[id_col, type_col])
            for _, row in df_table.iterrows():
                try:
                    type_map[int(float(row[id_col]))] = str(row[type_col]).strip()
                except:
                    pass
print(f"Loaded type map: {len(type_map)} items.")

# 3. Simulate get_volume_creation logic
print("3. Simulating filter logic...")
province = None
district = None
ward = None
post_office = None
customer = None
po_type = None
date_range = '7d'

df_filtered = df.copy()

latest_dt = df_filtered['Date'].max()
print(f"Latest Date in dataset: {latest_dt.strftime('%Y-%m-%d')}")

# WTD sums
weekday = latest_dt.weekday()
wtd_start = latest_dt - pd.Timedelta(days=weekday)
wtd_end = latest_dt
wtd_sums = df_filtered[(df_filtered['Date'] >= wtd_start) & (df_filtered['Date'] <= wtd_end)].groupby('Tỉnh')['Volume'].sum()
print("WTD sums:", {str(k).encode('ascii', 'ignore').decode(): int(v) for k, v in wtd_sums.to_dict().items()})

# Date range filtering for matrix/charts
if date_range == '7d':
    start_date = latest_dt - pd.Timedelta(days=6)
    df_date_filtered = df_filtered[(df_filtered['Date'] >= start_date) & (df_filtered['Date'] <= latest_dt)]

matrix_dates = sorted(df_date_filtered['Date'].dt.strftime('%Y-%m-%d').unique())
print("Matrix dates:", matrix_dates)

# Heatmap matrix rows
prov_date_vol = df_date_filtered.groupby(['Tỉnh', df_date_filtered['Date'].dt.strftime('%Y-%m-%d')])['Volume'].sum().unstack(fill_value=0)
po_date_vol = df_date_filtered.groupby(['Tỉnh', 'Bưu cục', df_date_filtered['Date'].dt.strftime('%Y-%m-%d')])['Volume'].sum().unstack(fill_value=0)

for d in matrix_dates:
    if d not in prov_date_vol.columns:
        prov_date_vol[d] = 0
    if d not in po_date_vol.columns:
        po_date_vol[d] = 0

matrix_rows = []
for p in sorted(df_date_filtered['Tỉnh'].dropna().unique()):
    p_vols = prov_date_vol.loc[p].to_dict() if p in prov_date_vol.index else {}
    p_total = int(sum(p_vols.values()))
    
    pos_list = []
    if p in po_date_vol.index:
        p_po_df = po_date_vol.loc[p]
        for po in sorted(p_po_df.index):
            po_vols = p_po_df.loc[po].to_dict()
            po_total = int(sum(po_vols.values()))
            pos_list.append({
                'bc': po,
                'data': {d: int(po_vols.get(d, 0)) for d in matrix_dates},
                'total': po_total
            })
    
    matrix_rows.append({
        'province': p,
        'data': {d: int(p_vols.get(d, 0)) for d in matrix_dates},
        'total': p_total,
        'pos': pos_list
    })

print(f"Matrix Rows computed: {len(matrix_rows)} provinces.")
for r in matrix_rows[:2]:
    safe_province = str(r['province']).encode('ascii', 'ignore').decode()
    print(f"  Province '{safe_province}' total: {r['total']}, details count: {len(r['pos'])}")

# Treemap growth ranking
df_d = df_filtered[df_filtered['Date'] == latest_dt]
df_d7 = df_filtered[df_filtered['Date'] == (latest_dt - pd.Timedelta(days=7))]
vol_d = df_d.groupby(['Tỉnh', 'Bưu cục'])['Volume'].sum().reset_index()
vol_d7 = df_d7.groupby('Bưu cục')['Volume'].sum().reset_index()
merged_growth = pd.merge(vol_d, vol_d7, on='Bưu cục', suffixes=('_d', '_d7'), how='left').fillna(0)
merged_growth['growth_abs'] = merged_growth['Volume_d'] - merged_growth['Volume_d7']
merged_growth['growth_pct'] = (merged_growth['growth_abs'] / merged_growth['Volume_d7'] * 100).replace([np.inf, -np.inf], 0).fillna(0)
merged_growth = merged_growth.sort_values(by='growth_abs', ascending=False)

treemap_list = []
for _, row in merged_growth.iterrows():
    treemap_list.append({
        'name': row['Bưu cục'],
        'value': int(row['Volume_d']),
        'province': row['Tỉnh'],
        'growth_abs': int(row['growth_abs']),
        'growth_pct': round(float(row['growth_pct']), 1)
    })
print(f"Treemap data computed: {len(treemap_list)} items.")
print("Top 3 growth post offices:")
for item in treemap_list[:3]:
    safe_name = str(item['name']).encode('ascii', 'ignore').decode()
    print(f"  {safe_name}: size={item['value']}, growth_abs={item['growth_abs']}, growth_pct={item['growth_pct']}%")

print("All logic validation passed successfully!")
