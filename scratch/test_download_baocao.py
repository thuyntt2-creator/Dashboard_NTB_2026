import urllib.request
import io
import pandas as pd
import sys

sys.stdout.reconfigure(encoding='utf-8')

url = "https://docs.google.com/spreadsheets/d/1JZ1eRerRqrpwjZ4HBevQunjd8VquM_cvPFz12TaJfMQ/export?format=csv&gid=204876430"
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
req = urllib.request.Request(url, headers={'User-Agent': user_agent})

try:
    with urllib.request.urlopen(req, timeout=30) as response:
        content = response.read()
    
    # Read CSV with default header (first row is header)
    df = pd.read_csv(io.BytesIO(content), encoding='utf-8')
    print("Columns loaded by default:", df.columns.tolist())
    
    col_names = [str(c).strip().lower() for c in df.columns]
    if 'bưu cục' in col_names and 'mã nv' in col_names and 'nhân viên' in col_names:
        print("Headers found in columns!")
        table_df = df.iloc[:, 0:9].copy()
        table_df.columns = df.columns[0:9]
    else:
        print("Headers NOT found in columns. Searching rows...")
        header_idx = None
        for idx, row in df.iterrows():
            row_vals = [str(x).strip().lower() for x in row.values]
            if 'bưu cục' in row_vals and 'mã nv' in row_vals and 'nhân viên' in row_vals:
                header_idx = idx
                break
        if header_idx is not None:
            print("Headers found in row index:", header_idx)
            headers = df.iloc[header_idx].values
            table_df = df.iloc[header_idx + 1:, 0:9].copy()
            table_df.columns = headers[0:9]
        else:
            table_df = None
            print("Headers NOT found in rows either!")
            
    if table_df is not None:
        table_df = table_df.dropna(subset=['Bưu Cục', 'Mã NV'])
        table_df = table_df[table_df['Bưu Cục'].astype(str).str.strip() != '']
        table_df = table_df[table_df['Mã NV'].astype(str).str.strip() != '']
        print("Parsed shape:", table_df.shape)
        print("First 3 rows:")
        print(table_df.head(3))
        
except Exception as e:
    print("Error:", e)
