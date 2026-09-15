# -*- coding: utf-8 -*-
import openpyxl, sys, json, pandas as pd
sys.stdout.reconfigure(encoding='utf-8')

file_path = r'C:\Users\lap4all\Downloads\report.xlsx'
df_full = pd.read_excel(file_path, sheet_name='dataODR full hàng ')
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

def get_week(time_str):
    s = str(time_str)
    if '2026-09-07' <= s[:10] <= '2026-09-13':
        return 'w37'
    elif '2026-08-31' <= s[:10] <= '2026-09-06':
        return 'w36'
    elif '2026-08-24' <= s[:10] <= '2026-08-30':
        return 'w35'
    elif '2026-08-17' <= s[:10] <= '2026-08-23':
        return 'w34'
    return 'other'

def get_am(bc_str):
    s = str(bc_str).strip()
    if s in bc_to_am:
        return bc_to_am[s]
    for k, v in bc_to_am.items():
        if k in s or s in k:
            return v
    return 'Unknown'

def get_tinh(bc_str):
    s = str(bc_str).strip()
    if s in bc_to_tinh:
        return bc_to_tinh[s]
    for k, v in bc_to_tinh.items():
        if k in s or s in k:
            return v
    return 'Unknown'

def process_df(df, is_tts=False):
    df = df.copy()
    df['ontime_rate'] = df['%Ontime'].apply(clean_pct)
    df['GTC_clean'] = pd.to_numeric(df['GTC'], errors='coerce').fillna(0)
    df['vol_ontime'] = df['GTC_clean'] * df['ontime_rate']
    df['week'] = df['Time'].apply(get_week)
    df['am'] = df['Chi tiết'].apply(get_am)
    df['tinh'] = df['Chi tiết'].apply(get_tinh)
    
    # Filter valid weeks
    df_valid = df[df['week'].isin(['w34', 'w35', 'w36', 'w37'])]
    
    # Group by AM
    am_grp = df_valid.groupby(['am', 'tinh', 'week']).agg({'GTC_clean': 'sum', 'vol_ontime': 'sum'}).reset_index()
    am_grp['odr'] = am_grp['vol_ontime'] / am_grp['GTC_clean']
    
    piv_am = am_grp.pivot(index=['am', 'tinh'], columns='week', values='odr').reset_index()
    piv_vol = am_grp.pivot(index=['am', 'tinh'], columns='week', values='GTC_clean').reset_index()
    
    am_list = []
    for idx, r in piv_am.iterrows():
        am_name = r['am']
        if am_name == 'Unknown':
            continue
        tinh_name = r['tinh']
        w34 = r.get('w34', 0.0) or 0.0
        w35 = r.get('w35', 0.0) or 0.0
        w36 = r.get('w36', 0.0) or 0.0
        w37 = r.get('w37', 0.0) or 0.0
        diff = w37 - w36
        
        # get vol in w37
        vol_r = piv_vol[(piv_vol['am'] == am_name) & (piv_vol['tinh'] == tinh_name)]
        vol_w37 = int(vol_r['w37'].values[0]) if len(vol_r) > 0 and pd.notna(vol_r['w37'].values[0]) else 0
        
        am_list.append({
            'am': am_name,
            'tinh': tinh_name,
            'vol': vol_w37,
            'diff': float(diff),
            'w34': float(w34),
            'w35': float(w35),
            'w36': float(w36),
            'w37': float(w37),
            'w32': float(w34),
            'w33': float(w34)
        })
    
    # Sort by diff descending
    am_list.sort(key=lambda x: x['diff'], reverse=True)
    
    # Group by Tỉnh
    tinh_grp = df_valid.groupby(['tinh', 'week']).agg({'GTC_clean': 'sum', 'vol_ontime': 'sum'}).reset_index()
    tinh_grp['odr'] = tinh_grp['vol_ontime'] / tinh_grp['GTC_clean']
    piv_tinh = tinh_grp.pivot(index='tinh', columns='week', values='odr').reset_index()
    piv_tinh_vol = tinh_grp.pivot(index='tinh', columns='week', values='GTC_clean').reset_index()
    
    tinh_list = []
    for idx, r in piv_tinh.iterrows():
        tinh_name = r['tinh']
        if tinh_name == 'Unknown':
            continue
        w34 = r.get('w34', 0.0) or 0.0
        w35 = r.get('w35', 0.0) or 0.0
        w36 = r.get('w36', 0.0) or 0.0
        w37 = r.get('w37', 0.0) or 0.0
        diff = w37 - w36
        vol_r = piv_tinh_vol[piv_tinh_vol['tinh'] == tinh_name]
        vol_w37 = int(vol_r['w37'].values[0]) if len(vol_r) > 0 and pd.notna(vol_r['w37'].values[0]) else 0
        
        tinh_list.append({
            'am': tinh_name,
            'tinh': tinh_name,
            'vol': vol_w37,
            'diff': float(diff),
            'w34': float(w34),
            'w35': float(w35),
            'w36': float(w36),
            'w37': float(w37),
            'w32': float(w34),
            'w33': float(w34)
        })
    tinh_list.sort(key=lambda x: x['diff'], reverse=True)
    
    # Total
    tot_grp = df_valid.groupby('week').agg({'GTC_clean': 'sum', 'vol_ontime': 'sum'})
    tot_grp['odr'] = tot_grp['vol_ontime'] / tot_grp['GTC_clean']
    tot_dict = {
        'label': 'TTS' if is_tts else 'Full hàng',
        'diff': float(tot_grp.loc['w37', 'odr'] - tot_grp.loc['w36', 'odr']),
        'w34': float(tot_grp.loc['w34', 'odr']) if 'w34' in tot_grp.index else 0.0,
        'w35': float(tot_grp.loc['w35', 'odr']) if 'w35' in tot_grp.index else 0.0,
        'w36': float(tot_grp.loc['w36', 'odr']) if 'w36' in tot_grp.index else 0.0,
        'w37': float(tot_grp.loc['w37', 'odr']) if 'w37' in tot_grp.index else 0.0,
        'w32': float(tot_grp.loc['w34', 'odr']) if 'w34' in tot_grp.index else 0.0,
        'w33': float(tot_grp.loc['w34', 'odr']) if 'w34' in tot_grp.index else 0.0
    }
    
    return am_list, tinh_list, tot_dict

am_full, tinh_full, tot_full = process_df(df_full, is_tts=False)
am_tts, tinh_tts, tot_tts = process_df(df_tts, is_tts=True)

print("=== OVERVIEW COMPARISON ===")
print("Full:", tot_full)
print("TTS:", tot_tts)

print("\n=== TOP 3 AM FULL ===")
for r in am_full[:3]:
    print(r)

print("\n=== TOP 3 AM TTS ===")
for r in am_tts[:3]:
    print(r)

# Save to scratch/odr_processed.json
with open('scratch/odr_processed.json', 'w', encoding='utf-8') as f:
    json.dump({
        'overview': [tot_full, tot_tts],
        'am_full': am_full,
        'am_tts': am_tts,
        'tinh_full': tinh_full,
        'tinh_tts': tinh_tts
    }, f, indent=2, ensure_ascii=False)

print("\nSUCCESS: Saved to scratch/odr_processed.json")
