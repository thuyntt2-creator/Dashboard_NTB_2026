import pickle
import pandas as pd
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open(r"c:\Users\lap4all\Desktop\New folder\scratch\raw_sheets_data.pkl", "rb") as f:
    data = pickle.load(f)

df_day = data['datatheo ngày']
print("Unique values in 'Tuan' column of 'datatheo ngày':")
unique_tuans = sorted(df_day['Tuan'].unique(), key=lambda x: str(x))
for u in unique_tuans:
    # try to convert if numeric
    try:
        val = float(u)
        dt = pd.to_datetime(val, unit='D', origin='1899-12-30')
        print(f" {u} -> {dt.strftime('%Y-%m-%d')}")
    except:
        print(f" {u} -> (string/other)")
