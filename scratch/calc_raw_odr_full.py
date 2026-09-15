# -*- coding: utf-8 -*-
import openpyxl, sys, pandas as pd
sys.stdout.reconfigure(encoding='utf-8')

file_path = r'C:\Users\lap4all\Downloads\report.xlsx'
df_full = pd.read_excel(file_path, sheet_name='dataODRfull hàng ')

def clean_pct(val):
    if pd.isna(val):
        return 0.0
    if isinstance(val, (int, float)):
        return float(val) if val <= 1.0 else float(val) / 100.0
    s = str(val).replace('%', '').replace(',', '.').strip()
    try:
        return float(s) / 100.0
    except:
        return 0.0

df_full['ontime_rate'] = df_full['%Ontime'].apply(clean_pct)
df_full['GTC_clean'] = pd.to_numeric(df_full['GTC'], errors='coerce').fillna(0)
df_full['vol_ontime'] = df_full['GTC_clean'] * df_full['ontime_rate']

def get_week(time_str):
    s = str(time_str)
    if '2026-09-07' <= s[:10] <= '2026-09-13':
        return 'W37'
    elif '2026-08-31' <= s[:10] <= '2026-09-06':
        return 'W36'
    elif '2026-08-24' <= s[:10] <= '2026-08-30':
        return 'W35'
    elif '2026-08-17' <= s[:10] <= '2026-08-23':
        return 'W34'
    return 'Other'

df_full['Week'] = df_full['Time'].apply(get_week)

grp = df_full[df_full['Week'].isin(['W34', 'W35', 'W36', 'W37'])].groupby('Week').agg({'GTC_clean': 'sum', 'vol_ontime': 'sum'})
grp['odr_full'] = grp['vol_ontime'] / grp['GTC_clean']

print("=== RAW dataODRfull hàng in report.xlsx ===")
for w in ['W34', 'W35', 'W36', 'W37']:
    if w in grp.index:
        gtc = grp.loc[w, 'GTC_clean']
        ontime = grp.loc[w, 'vol_ontime']
        pct = grp.loc[w, 'odr_full'] * 100
        print(f"  {w}: GTC={gtc:,.0f}, Ontime={ontime:,.1f}, %ODR={pct:.2f}%")
