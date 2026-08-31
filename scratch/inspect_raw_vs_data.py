import pandas as pd
import io
import urllib.request
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
ss_id = '1DAwY-46twFrHIs77R4p4IMuIZ6JTE-e58Aj-9Kcr5Jk'

for name, gid in [('Data', '0'), ('raw', '910119805'), ('gtc', '1634452132'), ('rawGTCTTS', '1006637898')]:
    url = f"https://docs.google.com/spreadsheets/d/{ss_id}/export?format=csv&gid={gid}"
    try:
        df = pd.read_csv(url)
        print(f"=== Sheet '{name}' (GID {gid}) ===")
        print(f"  Rows: {len(df)}, Cols: {len(df.columns)}")
        print(f"  Columns: {list(df.columns)}")
        if 'Loại Hàng' in df.columns:
            print(f"  Loại Hàng value counts:\n{df['Loại Hàng'].value_counts()}")
    except Exception as e:
        print(f"Error reading {name}: {e}")
