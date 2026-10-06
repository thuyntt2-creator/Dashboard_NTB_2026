import pandas as pd
import json, sys
sys.stdout.reconfigure(encoding='utf-8')

df = pd.read_csv('sheet_stuck.csv')
print("=== SHEET_STUCK.CSV OVERVIEW ===")
print("Total rows:", len(df))
print("Distinct 'Loại đơn':", df['Loại đơn'].value_counts().to_dict())
print("Distinct 'Trạng thái':", df['Trạng thái'].value_counts().to_dict())
print("Distinct 'Thời gian tồn đọng':", df['Thời gian tồn đọng'].value_counts().to_dict())
if 'BL' in df.columns:
    print("Distinct 'BL':", df['BL'].value_counts().to_dict())

print("\nDistinct province_name:", df['province_name'].value_counts().to_dict())
