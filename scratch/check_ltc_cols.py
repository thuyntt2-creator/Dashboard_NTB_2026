import pandas as pd
import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

df = pd.read_csv('ops_ltc.csv')
print("Columns in ops_ltc.csv:", df.columns.tolist())
print("\nFirst 3 rows:\n", df.head(3).to_string())

# Apply clean_ops_df logic manually to see what happens
cols_lower = [str(c).lower().strip() for c in df.columns]
print("\nLower cols:", cols_lower)

# Check if shifted
if 'loại hàng' in cols_lower and 'time' in cols_lower and 'volume' in cols_lower and '% gán' in cols_lower:
    print("Detected shifted columns!")
else:
    print("Normal columns detected.")
