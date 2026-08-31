import pandas as pd
import io
import urllib.request
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
ss_id = '1DAwY-46twFrHIs77R4p4IMuIZ6JTE-e58Aj-9Kcr5Jk'

# Load sheets Data, gtc, raw
sheets_to_read = [('Data', '0'), ('gtc', '1634452132'), ('raw', '910119805')]
all_dfs = []

for name, gid in sheets_to_read:
    try:
        url = f"https://docs.google.com/spreadsheets/d/{ss_id}/export?format=csv&gid={gid}"
        df = pd.read_csv(url)
        all_dfs.append(df)
        print(f"Loaded {name}: {len(df)} rows, max date: {df['Time'].max()}")
    except Exception as e:
        print(f"Error loading {name}: {e}")

combined = pd.concat(all_dfs, ignore_index=True)
print("\n=== COMBINED SUMMARY ===")
print("Total combined rows:", len(combined))
print("Max date per category:")
print(combined.groupby('Loại Hàng')['Time'].max())

print("\n7 Latest dates for 'Hàng Mới Ca 1':")
ca1_dates = sorted(list(combined[combined['Loại Hàng'] == 'Hàng Mới Ca 1']['Time'].dropna().unique()))
print(ca1_dates[-7:])
