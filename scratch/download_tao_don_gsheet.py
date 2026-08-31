import urllib.request
import os
import sys
import pandas as pd
import numpy as np

sys.stdout.reconfigure(encoding='utf-8')

# The spreadsheet ID from config.json (tao_don_url)
sheet_id = "1OygEPTn6Qu8okwAqpbx_RBiYQr1cfpO5hiaxqu4AMNE"
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=xlsx"
output_file = r"scratch/vols_tao_don_live.xlsx"

print("Downloading live 'tao_don' spreadsheet...")
req = urllib.request.Request(url)
req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)')

try:
    with urllib.request.urlopen(req, timeout=30) as response:
        with open(output_file, 'wb') as out_file:
            out_file.write(response.read())
    print("Download successful!")
    
    # Load the sheet. The name candidates are 'shopee_tiktok', 'tao_don', 'tạo đơn'
    xls = pd.ExcelFile(output_file)
    print("Sheets in live file:", xls.sheet_names)
    
    # Let's find the correct sheet name
    matched_sheet = None
    for s in xls.sheet_names:
        if s.strip().lower() in ['shopee_tiktok', 'tao_don', 'tạo đơn']:
            matched_sheet = s
            break
            
    if not matched_sheet:
        matched_sheet = xls.sheet_names[0]
        
    print(f"Reading sheet: {matched_sheet}")
    df = pd.read_excel(output_file, sheet_name=matched_sheet)
    df.columns = [str(c).strip() for c in df.columns]
    
    # Process
    if 'Date' in df.columns:
        df['Date'] = pd.to_datetime(df['Date'])
        # Filter bat_on
        df_filtered = df[df['bat_on'].fillna('').str.strip() != 'BC Cũ/Không thuộc ĐCL'].copy()
        
        latest_dt = df_filtered['Date'].max()
        print(f"Latest date in live sheet: {latest_dt.strftime('%Y-%m-%d')}")
        
        # Calculate D vs D-7
        df_d = df_filtered[df_filtered['Date'] == latest_dt]
        df_d7 = df_filtered[df_filtered['Date'] == (latest_dt - pd.Timedelta(days=7))]
        
        print(f"Rows on latest date: {len(df_d)}, Rows on latest-7 date: {len(df_d7)}")
        
        vol_d = df_d.groupby('Bưu cục')['Volume'].sum().reset_index()
        vol_d7 = df_d7.groupby('Bưu cục')['Volume'].sum().reset_index()
        
        merged_growth = pd.merge(vol_d, vol_d7, on='Bưu cục', suffixes=('_d', '_d7'), how='left').fillna(0)
        merged_growth['growth_abs'] = merged_growth['Volume_d'] - merged_growth['Volume_d7']
        merged_growth['growth_pct'] = (merged_growth['growth_abs'] / merged_growth['Volume_d7'] * 100).replace(np.inf, 100.0).replace(-np.inf, -100.0).fillna(0)
        
        merged_growth = merged_growth.sort_values(by='growth_abs', ascending=False)
        print("\n=== LIVE TOP 10 Growth ===")
        print(merged_growth.head(10).to_string(index=False))
        
        # Scan other date pairs in the live sheet
        print("\nScanning other date pairs in the live sheet:")
        dates = sorted(df_filtered['Date'].unique())
        for d in dates:
            d7 = d - pd.Timedelta(days=7)
            if d7 in dates:
                df_d_sub = df_filtered[df_filtered['Date'] == d]
                df_d7_sub = df_filtered[df_filtered['Date'] == d7]
                
                v_d = df_d_sub.groupby('Bưu cục')['Volume'].sum()
                v_d7 = df_d7_sub.groupby('Bưu cục')['Volume'].sum()
                
                diff = v_d - v_d7
                pt_grow = diff.get('(BTH) Phú Thủy', 0)
                dl_grow = diff.get('(BTH) Đức Linh', 0)
                ht_grow = diff.get('(BTH) Hàm Thắng', 0)
                
                # Check if this matches our targets
                if abs(pt_grow - 719) <= 5:
                    print(f"Found match on date: {d7.strftime('%Y-%m-%d')} -> {d.strftime('%Y-%m-%d')}")
                    print(f"  Phú Thủy: {pt_grow:.1f}, Đức Linh: {dl_grow:.1f}, Hàm Thắng: {ht_grow:.1f}")
                    
except Exception as e:
    print("Error:", e)
