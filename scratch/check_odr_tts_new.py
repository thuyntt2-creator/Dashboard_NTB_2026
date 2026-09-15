# -*- coding: utf-8 -*-
import openpyxl, sys, pandas as pd
sys.stdout.reconfigure(encoding='utf-8')

file_path = r'C:\Users\lap4all\Downloads\report.xlsx'
df = pd.read_excel(file_path, sheet_name='dataODR TTS')
print("dataODR TTS columns:", df.columns.tolist())
print("Time values:", df['Time'].unique().tolist() if 'Time' in df.columns else "No Time col")
print("Sample rows:")
print(df.head(10))

# Group by Time to see overall ODR TTS
if 'GTC' in df.columns and '%Ontime' in df.columns and 'Time' in df.columns:
    df['vol_ontime'] = df['GTC'] * df['%Ontime']
    grp = df.groupby('Time').agg({'GTC': 'sum', 'vol_ontime': 'sum'})
    grp['odr_tts'] = grp['vol_ontime'] / grp['GTC']
    print("\nOverall ODR TTS by Time:")
    print(grp[['GTC', 'odr_tts']])
