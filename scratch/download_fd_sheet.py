import urllib.request
import pandas as pd
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

spreadsheet_id = "1JZ1eRerRqrpwjZ4HBevQunjd8VquM_cvPFz12TaJfMQ"
gid = "626823626" # FD sheet GID from URL
csv_url = f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}/export?format=csv&gid={gid}"
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'

req = urllib.request.Request(csv_url, headers={'User-Agent': user_agent})
try:
    print(f"Downloading from {csv_url}...")
    with urllib.request.urlopen(req, timeout=30) as response:
        content = response.read()
    
    output_path = 'ops_fd.csv'
    with open(output_path, 'wb') as f:
        f.write(content)
        
    print(f"File downloaded successfully to {output_path}. Size: {os.path.getsize(output_path)} bytes.")
    
    # Read and print details
    df = pd.read_csv(output_path, header=None)
    print("\nShape of df:", df.shape)
    print("\nFirst 15 rows of CSV:")
    for idx, row in df.head(15).iterrows():
        print(f"Row {idx}: {row.dropna().tolist()}")
        
    # Find "Tổng NTB" row
    print("\nSearching for 'Tổng NTB' in column 0:")
    tong_ntb_rows = df[df[0].astype(str).str.strip() == 'Tổng NTB']
    for idx, row in tong_ntb_rows.iterrows():
        print(f"Row {idx}: {row.tolist()}")
        
except Exception as e:
    print("Error:", e)
