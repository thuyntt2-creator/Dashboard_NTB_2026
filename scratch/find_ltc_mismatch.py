import pandas as pd
import sys
import os

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# Read local CSV directly to check the raw numbers
csv_path = 'ops_ltc.csv'
if os.path.exists(csv_path):
    df = pd.read_csv(csv_path)
    df = df[df['Time'] == '2026-06-10 - Thứ 4'].copy()
    
    # Clean up columns
    df['Volume'] = pd.to_numeric(df['Volume'].astype(str).str.replace(',', ''), errors='coerce').fillna(0)
    df['Sản Lượng Lấy Thành Công'] = pd.to_numeric(df['Sản Lượng Lấy Thành Công'], errors='coerce').fillna(0)
    
    # Filter out Grand Total
    df_details = df[df['Cấp quản lý'] != 'Grand Total'].copy()
    
    print("Total rows:", len(df_details))
    print("Sum of Volume (details):", df_details['Volume'].sum())
    print("Sum of Sản Lượng Lấy Thành Công (details):", df_details['Sản Lượng Lấy Thành Công'].sum())
    
    # Find rows where Sản Lượng Lấy Thành Công > Volume
    mismatch = df_details[df_details['Sản Lượng Lấy Thành Công'] > df_details['Volume']]
    print("\nRows where Sản Lượng Lấy Thành Công > Volume:")
    print(mismatch[['Chi tiết', 'Ca', 'Volume', 'Sản Lượng Lấy Thành Công', '%LTC', '%LC', 'AM']].to_string())
    
    # Print the sum of GTC details for the same day to compare GTC volume and LTC volume
    gtc_path = 'ops_gtc.csv'
    if os.path.exists(gtc_path):
        df_gtc = pd.read_csv(gtc_path)
        df_gtc = df_gtc[(df_gtc['Time'] == '2026-06-10 - Thứ 4') & (df_gtc['Cấp Quản Lý'] != 'Grand Total')].copy()
        df_gtc['Volume'] = pd.to_numeric(df_gtc['Volume'].astype(str).str.replace(',', ''), errors='coerce').fillna(0)
        print("\nSum of GTC Volume (details):", df_gtc['Volume'].sum())
else:
    print("ops_ltc.csv not found!")
