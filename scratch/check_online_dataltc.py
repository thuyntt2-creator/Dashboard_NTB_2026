import urllib.request, io, sys
import pandas as pd
sys.stdout.reconfigure(encoding='utf-8')

# GID 1365110988 is DataLTC
url_ltc = 'https://docs.google.com/spreadsheets/d/1DAwY-46twFrHIs77R4p4IMuIZ6JTE-e58Aj-9Kcr5Jk/export?format=csv&gid=1365110988'
req = urllib.request.Request(url_ltc, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req, timeout=30) as resp:
        content = resp.read()
    
    df = pd.read_csv(io.BytesIO(content))
    print(f"DataLTC downloaded successfully: {len(df)} rows, {len(df.columns)} columns")
    print("Columns:", list(df.columns))
    print("\nHead:")
    print(df.head(5))
    print("\nTail:")
    print(df.tail(5))
    print("\nUnique dates in DataLTC:")
    if 'Time' in df.columns:
        print(df['Time'].unique())
    elif 'time' in df.columns:
        print(df['time'].unique())
    else:
        for c in df.columns:
            if 'time' in c.lower() or 'ngày' in c.lower() or 'date' in c.lower():
                print(c, df[c].unique())
except Exception as e:
    print(f"Error downloading DataLTC: {e}")
