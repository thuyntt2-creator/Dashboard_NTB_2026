import pandas as pd
import os
from itertools import combinations

workspace_dir = r"c:\Users\lap4all\Desktop\New folder"
file_path = os.path.join(workspace_dir, "vols_tao_don.xlsx")
output_path = os.path.join(workspace_dir, "scratch", "find_exact_filters_res.txt")

with open(output_path, "w", encoding="utf-8") as f:
    df = pd.read_excel(file_path, sheet_name="shopee_tiktok")
    df['Date'] = pd.to_datetime(df['Date'])
    
    # Filter for 2026-06-07
    df_d = df[df['Date'] == '2026-06-07'].copy()
    
    # Target values from Looker Studio for 2026-06-07
    targets = {
        'Bình Thuận': 10369,
        'Khánh Hòa': 11515,
        'Lâm Đồng': 9496,
        'Ninh Thuận': 3727,
        'Đắk Nông': 4460
    }
    
    unique_bat_on = list(df_d['bat_on'].fillna('None').unique())
    f.write(f"Unique 'bat_on' values: {unique_bat_on}\n\n")
    
    # Find combinations for each province
    for prov, target in targets.items():
        f.write(f"=== Province: {prov} (Target: {target}) ===\n")
        df_prov = df_d[df_d['Tỉnh'] == prov].copy()
        df_prov['bat_on'] = df_prov['bat_on'].fillna('None')
        
        # Group by bat_on to see values
        grouped = df_prov.groupby('bat_on')['Volume'].sum().to_dict()
        f.write(f"Sums by bat_on: {grouped}\n")
        
        # Test all possible combinations of bat_on keys
        found_any = False
        keys = list(grouped.keys())
        for r in range(1, len(keys) + 1):
            for combo in combinations(keys, r):
                combo_sum = sum(grouped[k] for k in combo)
                if abs(combo_sum - target) < 2:  # allow tiny rounding difference
                    f.write(f"  MATCH FOUND: {combo} -> Sum = {combo_sum}\n")
                    found_any = True
        if not found_any:
            f.write("  NO MATCH FOUND for combinations of bat_on\n")
            
        f.write("\n")
        
print("Done writing find_exact_filters_res.txt")
