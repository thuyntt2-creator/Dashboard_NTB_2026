import pandas as pd
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

df = pd.read_csv('ops_fd.csv', header=None)

print(f"Total rows: {len(df)}, Columns: {df.shape[1]}")

# Let's inspect rows around the tables
print("\n--- Rows 0-10 ---")
for i in range(10):
    print(f"Row {i}: {df.iloc[i].tolist()}")

# Let's find table sections
print("\n--- Searching for Section Headers ---")
for i, val in enumerate(df[0]):
    val_str = str(val).strip()
    if '🏪' in val_str or '👤' in val_str or '🗺️' in val_str or 'AM' in val_str or 'Tỉnh' in val_str or 'Bưu Cục' in val_str:
        print(f"Row {i}: {df.iloc[i].tolist()}")

print("\n--- Row 80-114 ---")
for i in range(80, 115):
    print(f"Row {i}: {df.iloc[i].tolist()}")
