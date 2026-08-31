import pandas as pd
import numpy as np
import sys

sys.stdout.reconfigure(encoding='utf-8')

# Replicate load_vols_tao_don_df
df = pd.read_csv("vols_tao_don.csv")
df.columns = [str(c).strip() for c in df.columns]
df['Date'] = pd.to_datetime(df['Date'])
df = df[df['bat_on'].fillna('').str.strip() != 'BC Cũ/Không thuộc ĐCL'].copy()

# Replicate get_volume_creation filtering
# Vùng is filtered inside get_volume_creation or in apply_filters?
# In get_volume_creation: df = apply_filters(df, am=am, province=None, post_office=None)
# Wait, let's see: what province list is used?
# provinces_list = ['Bình Thuận', 'Khánh Hòa', 'Lâm Đồng', 'Ninh Thuận', 'Đắk Nông']
# Wait, df_filtered is df.copy() (before any province/district filters if we are talking about the main dropdowns)
# Wait, does df itself only contain NTB?
# Yes, Vols_tao_don.csv might only contain NTB or has Vùng. Let's print df['Vùng'].unique()
print("Vùng unique values:", df['Vùng'].unique())

# Let's run the exact growth code:
latest_dt = df['Date'].max()
print(f"Latest Date: {latest_dt.strftime('%Y-%m-%d')}")

df_d = df[df['Date'] == latest_dt]
df_d7 = df[df['Date'] == (latest_dt - pd.Timedelta(days=7))]

print(f"df_d length: {len(df_d)}, df_d7 length: {len(df_d7)}")

if len(df_d) > 0:
    vol_d = df_d.groupby(['Tỉnh', 'Bưu cục'])['Volume'].sum().reset_index()
    vol_d7 = df_d7.groupby('Bưu cục')['Volume'].sum().reset_index()
    
    merged_growth = pd.merge(vol_d, vol_d7, on='Bưu cục', suffixes=('_d', '_d7'), how='left').fillna(0)
    merged_growth['growth_abs'] = merged_growth['Volume_d'] - merged_growth['Volume_d7']
    merged_growth['growth_pct'] = (merged_growth['growth_abs'] / merged_growth['Volume_d7'] * 100).replace(np.inf, 100.0).replace(-np.inf, -100.0).fillna(0)
    
    merged_growth = merged_growth.sort_values(by='growth_abs', ascending=False)
    
    print("\n=== Top 10 Bưu cục tăng trưởng tốt nhất (7D tuyệt đối) ===")
    print(merged_growth.head(10).to_string(index=False))

    print("\n=== Growth for (BTH) Phú Thủy ===")
    print(merged_growth[merged_growth['Bưu cục'].str.contains("Phú Thủy", na=False)].to_string(index=False))
