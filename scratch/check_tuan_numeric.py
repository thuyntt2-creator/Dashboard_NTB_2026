import pickle
import pandas as pd
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open(r"scratch\raw_sheets_data.pkl", "rb") as f:
    data = pickle.load(f)

df = data['Theo Tuần']
numeric_tuan = df[df['Tuan'].apply(lambda x: isinstance(x, (int, float)))]
print(numeric_tuan[['AM_format', 'Tuan']].head(20))
