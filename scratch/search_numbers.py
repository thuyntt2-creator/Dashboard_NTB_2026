import pandas as pd
import numpy as np
import sys

sys.stdout.reconfigure(encoding='utf-8')

# Let's inspect vols_tao_don.csv first
print("--- SEARCHING vols_tao_don.csv ---")
df = pd.read_csv("vols_tao_don.csv")
df.columns = [str(c).strip() for c in df.columns]
df['Date'] = pd.to_datetime(df['Date'])

# Find all dates in the csv
dates = sorted(df['Date'].unique())
print("Dates in vols_tao_don.csv:", [d.strftime('%Y-%m-%d') for d in dates])

# Let's search for (BTH) Phú Thủy, (BTH) Đức Linh, (BTH) Hàm Thắng
target_pos = ['(BTH) Phú Thủy', '(BTH) Đức Linh', '(BTH) Hàm Thắng', '(LDO) Lang Biang - Đà Lạt - Lâm Đồng', '(NTH) Phan Rang']

# Let's test all dates to see if there is any date where Volume_d - Volume_d7 matches the screenshot
print("\nScanning dates for D vs D-7 growth in vols_tao_don.csv:")
for d in dates:
    d7 = d - pd.Timedelta(days=7)
    if d7 in dates:
        df_d = df[df['Date'] == d]
        df_d7 = df[df['Date'] == d7]
        
        # Check without 'BC Cũ/Không thuộc ĐCL' filter
        vol_d = df_d.groupby('Bưu cục')['Volume'].sum()
        vol_d7 = df_d7.groupby('Bưu cục')['Volume'].sum()
        
        diff = vol_d - vol_d7
        
        # Check with 'BC Cũ/Không thuộc ĐCL' filter
        df_d_f = df_d[df_d['bat_on'].fillna('').str.strip() != 'BC Cũ/Không thuộc ĐCL']
        df_d7_f = df_d7[df_d7['bat_on'].fillna('').str.strip() != 'BC Cũ/Không thuộc ĐCL']
        vol_d_f = df_d_f.groupby('Bưu cục')['Volume'].sum()
        vol_d7_f = df_d7_f.groupby('Bưu cục')['Volume'].sum()
        
        diff_f = vol_d_f - vol_d7_f
        
        found = []
        for po in target_pos:
            val = diff.get(po, 0)
            val_f = diff_f.get(po, 0)
            found.append(f"{po}: Unfiltered={val:.0f}, Filtered={val_f:.0f}")
            
        print(f"Date {d7.strftime('%Y-%m-%d')} -> {d.strftime('%Y-%m-%d')}:")
        for f in found:
            print("  ", f)

# Let's look at what values are in vols_tao_don.xlsx or other columns, or check if there is another file
