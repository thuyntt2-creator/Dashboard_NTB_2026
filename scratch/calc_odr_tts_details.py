# -*- coding: utf-8 -*-
import openpyxl, sys, pandas as pd
sys.stdout.reconfigure(encoding='utf-8')

file_path = r'C:\Users\lap4all\Downloads\report.xlsx'
df = pd.read_excel(file_path, sheet_name='dataODR TTS')
cocau = pd.read_excel(file_path, sheet_name='cocau')

print("Cocau cols:", cocau.columns.tolist())
# mapping BC -> AM, Tinh
bc_map = {}
for idx, r in cocau.iterrows():
    bc = str(r.iloc[0]).strip()
    am = str(r.iloc[1]).strip()
    tinh = str(r.iloc[2]).strip()
    bc_map[bc] = {'am': am, 'tinh': tinh}

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

df['Week'] = df['Time'].apply(get_week)
df['vol_ontime'] = df['GTC'] * df['%Ontime']

# Overall by Week
w_grp = df[df['Week'].isin(['W34', 'W35', 'W36', 'W37'])].groupby('Week').agg({'GTC': 'sum', 'vol_ontime': 'sum'})
w_grp['odr_tts'] = w_grp['vol_ontime'] / w_grp['GTC']
print("\n=== OVERALL ODR TTS BY WEEK ===")
for w in ['W34', 'W35', 'W36', 'W37']:
    if w in w_grp.index:
        print(f"  {w}: GTC={w_grp.loc[w, 'GTC']:,}, Vol_Ontime={w_grp.loc[w, 'vol_ontime']:,}, %ODR={w_grp.loc[w, 'odr_tts']*100:.2f}%")

# Map AM and Tinh
def map_bc(row):
    bc = str(row['Chi tiết']).strip()
    info = bc_map.get(bc, {})
    return pd.Series([info.get('am', 'Unknown'), info.get('tinh', 'Unknown')])

df[['AM', 'Tinh']] = df.apply(map_bc, axis=1)

# Group by Tỉnh and Week
print("\n=== ODR TTS BY TINH (W36 vs W37) ===")
tinh_w = df[df['Week'].isin(['W36', 'W37'])].groupby(['Tinh', 'Week']).agg({'GTC': 'sum', 'vol_ontime': 'sum'}).reset_index()
tinh_w['odr'] = tinh_w['vol_ontime'] / tinh_w['GTC']
piv_tinh = tinh_w.pivot(index='Tinh', columns='Week', values='odr')
piv_vol = tinh_w.pivot(index='Tinh', columns='Week', values='GTC')
for t in piv_tinh.index:
    w36 = piv_tinh.loc[t, 'W36'] if 'W36' in piv_tinh.columns else 0
    w37 = piv_tinh.loc[t, 'W37'] if 'W37' in piv_tinh.columns else 0
    diff = (w37 - w36) * 100
    vol = piv_vol.loc[t, 'W37'] if 'W37' in piv_vol.columns else 0
    print(f"  - {t}: W37 = {w37*100:.2f}% (W36 = {w36*100:.2f}%, Δ = {diff:+.2f}%p, GTC={vol:,.0f})")

# Group by AM and Week
print("\n=== TOP AM ODR TTS (W37) ===")
am_w = df[df['Week'].isin(['W36', 'W37'])].groupby(['AM', 'Week']).agg({'GTC': 'sum', 'vol_ontime': 'sum'}).reset_index()
am_w['odr'] = am_w['vol_ontime'] / am_w['GTC']
piv_am = am_w.pivot(index='AM', columns='Week', values='odr').dropna()
piv_am['diff'] = piv_am['W37'] - piv_am['W36']
piv_am_sorted = piv_am.sort_values(by='W37', ascending=False)
for am in piv_am_sorted.index[:8]:
    print(f"  Top: AM {am}: W37 = {piv_am.loc[am, 'W37']*100:.2f}% (W36 = {piv_am.loc[am, 'W36']*100:.2f}%, Δ = {piv_am.loc[am, 'diff']*100:+.2f}%p)")

print("\n=== BOTTOM AM ODR TTS (W37) ===")
for am in piv_am_sorted.index[-5:]:
    print(f"  Bottom: AM {am}: W37 = {piv_am.loc[am, 'W37']*100:.2f}% (W36 = {piv_am.loc[am, 'W36']*100:.2f}%, Δ = {piv_am.loc[am, 'diff']*100:+.2f}%p)")
