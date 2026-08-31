import urllib.request
import os
import pandas as pd
import sys

sys.stdout.reconfigure(encoding='utf-8')

user_url = "https://docs.google.com/spreadsheets/d/1XaziS_8UB2lCwL01bxam106EdIUHtlMISDGJX1PU5A8/export?format=xlsx"
user_path = r"c:\Users\lap4all\Desktop\New folder\scratch\user_sheet_after_fix.xlsx"

print("Downloading latest user sheet...")
req = urllib.request.Request(user_url)
req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)')
try:
    with urllib.request.urlopen(req, timeout=30) as response:
        with open(user_path, 'wb') as out_file:
            out_file.write(response.read())
    print("Downloaded successfully.")
except Exception as e:
    print(f"Error downloading: {e}")
    sys.exit(1)

xls = pd.ExcelFile(user_path)
for name in xls.sheet_names:
    print(f"\nSheet: {name}")
    try:
        df = pd.read_excel(user_path, sheet_name=name)
        print(f"  Shape: {df.shape}")
        for col in df.columns:
            if 'ngay' in col.lower() or 'date' in col.lower() or 'time' in col.lower() or col == 'Ngay':
                unique_vals = list(df[col].dropna().unique()[:10])
                print(f"    Column '{col}' unique values (first 10): {unique_vals}")
    except Exception as e:
        print(f"  Error reading: {e}")
