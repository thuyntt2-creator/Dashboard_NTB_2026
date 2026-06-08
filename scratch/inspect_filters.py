import pandas as pd
import os

workspace_dir = r"c:\Users\lap4all\Desktop\New folder"
file_path = os.path.join(workspace_dir, "vols_tao_don.xlsx")
output_path = os.path.join(workspace_dir, "scratch", "inspect_filters_res.txt")

with open(output_path, "w", encoding="utf-8") as f:
    df = pd.read_excel(file_path, sheet_name="shopee_tiktok")
    df['Date'] = pd.to_datetime(df['Date'])
    
    # Filter for 2026-06-07
    df_d = df[df['Date'] == '2026-06-07'].copy()
    
    f.write("Unique values of 'bat_on':\n")
    f.write(str(df_d['bat_on'].value_counts()) + "\n\n")
    
    f.write("Unique values of 'Khách hàng':\n")
    f.write(str(df_d['Khách hàng'].value_counts()) + "\n\n")
    
    # Try different filters
    f.write("--- Sum of Volume by Province for different filters on 2026-06-07 ---\n")
    
    # Filter 1: No filter (All)
    f.write("\n1. All data (no filter):\n")
    f.write(df_d.groupby('Tỉnh')['Volume'].sum().to_string() + "\n")
    
    # Filter 2: bat_on == 'Bình thường'
    f.write("\n2. Filter: bat_on == 'Bình thường':\n")
    df_f2 = df_d[df_d['bat_on'] == 'Bình thường']
    f.write(df_f2.groupby('Tỉnh')['Volume'].sum().to_string() + "\n")
    
    # Filter 3: bat_on != 'Cấp cảnh báo'
    f.write("\n3. Filter: bat_on != 'Cấp cảnh báo':\n")
    df_f3 = df_d[df_d['bat_on'] != 'Cấp cảnh báo']
    f.write(df_f3.groupby('Tỉnh')['Volume'].sum().to_string() + "\n")
    
    # Filter 4: Filter out some customer or something
    f.write("\n4. Filter by customer (Khách hàng):\n")
    for cust in df_d['Khách hàng'].unique():
        f.write(f"\n   Khách hàng == '{cust}':\n")
        f.write(df_d[df_d['Khách hàng'] == cust].groupby('Tỉnh')['Volume'].sum().to_string() + "\n")
        
print("Done writing inspect_filters_res.txt")
