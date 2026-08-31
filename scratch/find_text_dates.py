import pandas as pd
import os
import re

user_path = r"c:\Users\lap4all\Desktop\New folder\scratch\user_sheet.xlsx"

if not os.path.exists(user_path):
    print("User sheet not found.")
    exit(1)

xls = pd.ExcelFile(user_path)
for name in xls.sheet_names:
    print(f"\nSheet: {name}")
    try:
        df = pd.read_excel(user_path, sheet_name=name)
        for col in df.columns:
            # check if any string in this column has 'thg'
            has_thg = df[col].astype(str).str.contains(r'\bthg\b', regex=True, na=False)
            if has_thg.any():
                matching_samples = df[has_thg][col].unique()[:5]
                print(f"  Column '{col}' has text dates! Samples: {matching_samples}")
    except Exception as e:
        print(f"  Error: {e}")
