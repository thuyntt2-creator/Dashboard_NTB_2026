# -*- coding: utf-8 -*-
import openpyxl, sys, pandas as pd
sys.stdout.reconfigure(encoding='utf-8')

file_path = r'C:\Users\lap4all\Downloads\report.xlsx'
df_tts = pd.read_excel(file_path, sheet_name='dataODR TTS')
cocau = pd.read_excel(file_path, sheet_name='cocau')

bc_to_am = {}
bc_to_tinh = {}
for idx, r in cocau.iterrows():
    bc_name = str(r['Bưu cục']).strip()
    am_name = str(r['AM']).strip()
    tinh_name = str(r['Tỉnh']).strip()
    bc_to_am[bc_name] = am_name
    bc_to_tinh[bc_name] = tinh_name
    if 'BC' in r and pd.notna(r['BC']):
        bc_to_am[str(r['BC']).strip()] = am_name
        bc_to_tinh[str(r['BC']).strip()] = tinh_name

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

df_tts['ontime_rate'] = df_tts['%Ontime'].apply(clean_pct)
df_tts['GTC_clean'] = pd.to_numeric(df_tts['GTC'], errors='coerce').fillna(0)
df_tts['vol_ontime'] = df_tts['GTC_clean'] * df_tts['ontime_rate']

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

df_tts['Week'] = df_tts['Time'].apply(get_week)

def get_am(bc_str):
    s = str(bc_str).strip()
    if s in bc_to_am:
        return bc_to_am[s]
    for k, v in bc_to_am.items():
        if k in s or s in k:
            return v
    return 'Unknown'

df_tts['AM'] = df_tts['Chi tiết'].apply(get_am)

grp = df_tts[df_tts['Week'].isin(['W36', 'W37'])].groupby(['AM', 'Week']).agg({'GTC_clean': 'sum', 'vol_ontime': 'sum'}).reset_index()
grp['odr'] = grp['vol_ontime'] / grp['GTC_clean']
piv = grp.pivot(index='AM', columns='Week', values='odr')
piv_vol = grp.pivot(index='AM', columns='Week', values='GTC_clean')

print("\n=== REAL ODR TTS (W36 vs W37) ===")
for am in piv.index:
    w36 = piv.loc[am, 'W36'] if 'W36' in piv.columns else 0
    w37 = piv.loc[am, 'W37'] if 'W37' in piv.columns else 0
    vol = piv_vol.loc[am, 'W37'] if 'W37' in piv_vol.columns else 0
    print(f"  AM {am}: W37 = {w37*100:.2f}% (W36 = {w36*100:.2f}%, Δ = {(w37-w36)*100:+.2f}%p, SL = {vol:,.0f})")
