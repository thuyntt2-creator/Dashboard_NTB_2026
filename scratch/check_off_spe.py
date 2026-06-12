import os
import pandas as pd
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

file_path = 'off_tuyen_spe.csv'
print("Exists:", os.path.exists(file_path))
if os.path.exists(file_path):
    print("File size:", os.path.getsize(file_path))
    try:
        df = pd.read_csv(file_path)
        print("Columns:", list(df.columns))
        print("Number of rows:", len(df))
        print("\nFirst 5 rows:")
        print(df.head(5).to_string())
    except Exception as e:
        print("Error reading CSV:", e)
