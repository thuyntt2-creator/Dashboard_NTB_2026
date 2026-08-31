import pickle
import pandas as pd
import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

with open(r"c:\Users\lap4all\Desktop\New folder\scratch\raw_sheets_data.pkl", "rb") as f:
    data = pickle.load(f)

df_week = data['data theo tuần']
df_cocau = data['Cocauvung']

# Map of AM name to Tỉnh from Cocauvung
# An AM might manage multiple warehouses/bưu cục, potentially across multiple Tỉnh? Let's check if each AM is unique to one Tỉnh.
am_to_province = {}
for am, group in df_cocau.groupby('AM'):
    provinces = group['Tỉnh'].unique()
    am_to_province[am] = list(provinces)

print("=== AM to Provinces in Cocauvung ===")
for am, provs in am_to_province.items():
    print(f" {am} -> {provs}")

# Let's write a function to extract name from raw AM field in raw data
def extract_am_name(raw_am):
    if not raw_am:
        return ""
    parts = str(raw_am).split('-')
    if len(parts) > 1:
        return parts[1].strip()
    return str(raw_am).strip()

raw_ams = df_week['AM'].unique()
print("\n=== Mapping Raw AMs to Cocauvung ===")
for raw_am in raw_ams:
    clean_name = extract_am_name(raw_am)
    mapped_provs = am_to_province.get(clean_name, None)
    print(f"Raw: '{raw_am}' -> Clean: '{clean_name}' -> Mapped Provinces: {mapped_provs}")
