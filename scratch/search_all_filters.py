import pandas as pd
import numpy as np
import sys

sys.stdout.reconfigure(encoding='utf-8')

# Replicate load_vols_tao_don_df
df = pd.read_csv("vols_tao_don.csv")
df.columns = [str(c).strip() for c in df.columns]
df['Date'] = pd.to_datetime(df['Date'])
df = df[df['bat_on'].fillna('').str.strip() != 'BC Cũ/Không thuộc ĐCL'].copy()

# Load type map if exists
type_map = {}
import os
if os.path.exists("ops_co_cau.csv"):
    try:
        df_cc = pd.read_csv("ops_co_cau.csv")
        df_cc.columns = [c.strip() for c in df_cc.columns]
        for _, r in df_cc.iterrows():
            wh_id = r.get('warehouse_id')
            bc_type = r.get('Loại bưu cục', 'BC')
            if pd.notna(wh_id):
                try:
                    wh_id_clean = int(float(wh_id))
                    type_map[wh_id_clean] = str(bc_type).strip()
                except:
                    type_map[str(wh_id).strip()] = str(bc_type).strip()
    except Exception as e:
        print("Error loading ops_co_cau.csv:", e)

# Apply type map
def clean_id(x):
    try:
        return int(float(x))
    except:
        return str(x).strip()

df['warehouse_id_clean'] = df['warehouse_id'].apply(clean_id)
df['po_type_mapped'] = df['warehouse_id_clean'].map(type_map).fillna('BC')

customers = [None] + list(df['Khách hàng'].dropna().unique())
po_types = [None, 'BC', 'GXT']
dates = sorted(df['Date'].unique())

print("Unique customers in dataset:", customers)
print("Unique po_types in dataset:", po_types)
print("Number of dates in dataset:", len(dates))

found_combinations = []

# Scan
for d in dates:
    d7 = d - pd.Timedelta(days=7)
    if d7 not in dates:
        continue
    
    for cust in customers:
        for pt in po_types:
            # Apply filters
            sub_df = df.copy()
            if cust:
                sub_df = sub_df[sub_df['Khách hàng'] == cust]
            if pt:
                sub_df = sub_df[sub_df['po_type_mapped'] == pt]
                
            df_d = sub_df[sub_df['Date'] == d]
            df_d7 = sub_df[sub_df['Date'] == d7]
            
            if len(df_d) == 0:
                continue
                
            vol_d = df_d.groupby('Bưu cục')['Volume'].sum()
            vol_d7 = df_d7.groupby('Bưu cục')['Volume'].sum()
            
            diff = vol_d - vol_d7
            
            # Check targets
            pt_growth = diff.get('(BTH) Phú Thủy', 0)
            dl_growth = diff.get('(BTH) Đức Linh', 0)
            ht_growth = diff.get('(BTH) Hàm Thắng', 0)
            lb_growth = diff.get('(LDO) Lang Biang - Đà Lạt - Lâm Đồng', 0)
            
            # Let's check if the growth of Phu Thuy is close to 719, and Duc Linh is close to 707
            if abs(pt_growth - 719) <= 20 and abs(dl_growth - 707) <= 20:
                found_combinations.append({
                    'date': d.strftime('%Y-%m-%d'),
                    'customer': cust,
                    'po_type': pt,
                    'Phú Thủy': pt_growth,
                    'Đức Linh': dl_growth,
                    'Hàm Thắng': ht_growth,
                    'Lang Biang': lb_growth
                })

print(f"\nFound {len(found_combinations)} potential combinations:")
for combo in found_combinations:
    print(combo)
