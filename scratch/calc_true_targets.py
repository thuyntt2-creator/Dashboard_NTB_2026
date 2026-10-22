# -*- coding: utf-8 -*-
import sys
import math
import gspread
import pandas as pd
from google.oauth2.credentials import Credentials

sys.stdout.reconfigure(encoding='utf-8')

creds = Credentials.from_authorized_user_file('authorized_user.json', scopes=['https://www.googleapis.com/auth/spreadsheets'])
gc = gspread.authorize(creds)
sh = gc.open_by_key('14cN4YAf01NqKtREtmhBngRP58OCdgby-PjVoixVlpZo')

# 1. Tab Data NTB
ws_data = sh.worksheet('Data NTB')
data_rows = ws_data.get_all_values()
df_data = pd.DataFrame(data_rows[1:], columns=data_rows[0])
df_data['Volume_num'] = pd.to_numeric(df_data['Volume'].astype(str).str.replace(',', '').str.replace('.', ''), errors='coerce').fillna(0)
df_data['GTC_num'] = pd.to_numeric(df_data['Sản Lượng Giao Thành Công'].astype(str).str.replace(',', '').str.replace('.', ''), errors='coerce').fillna(0)

sorted_dates = sorted([d for d in df_data['Time'].unique() if d], reverse=True)
last_6_dates = sorted_dates[:6]
print('6 dates from Data NTB:', last_6_dates)

df_6d = df_data[df_data['Time'].isin(last_6_dates)]
agg_6d = df_6d.groupby('Chi tiết')[['Volume_num', 'GTC_num']].sum().reset_index()
map_6d = {}
for _, r in agg_6d.iterrows():
    map_6d[r['Chi tiết'].strip()] = {'vol_6d': int(r['Volume_num']), 'gtc_6d': int(r['GTC_num'])}

# 2. Tab Bất ổn
ws_bo = sh.worksheet('Bất ổn')
bo_rows = ws_bo.get_all_values()
best_map = {}
for r in bo_rows[5:]:
    if len(r) >= 6 and r[3].strip():
        bc = r[3].strip()
        val_str = r[5].strip().replace('%', '')
        try:
            best_map[bc] = float(val_str) / 100.0
        except:
            pass

# 3. Tab hàng về
ws_hv = sh.worksheet('hàng về')
hv_rows = ws_hv.get_all_values()
vol_today_map = {}
for r in hv_rows[1:]:
    if len(r) >= 2:
        k = r[0].strip()
        v = r[1].strip().replace(',', '').replace('.', '')
        if v.isdigit():
            vol_today_map[k] = int(v)

ws_cocau = sh.worksheet('cocau')
hub_id_map = {}
for r in ws_cocau.get_all_values()[1:]:
    if len(r) >= 2:
        hub_id_map[r[1].strip()] = r[0].strip()

alert_hubs = [
    '(LDO) Đức Trọng 1',
    '(KHO) Tây Nha Trang',
    '(LDO) Hòa Ninh',
    '(DNO) Quảng Khê',
    "(LDO) D'Ran",
    '(LDO) Tân Hà Lâm Hà',
    '(DNO) Đông Gia Nghĩa',
    '(LDO) Lang Biang - Đà Lạt 1',
    '(LDO) Lang Biang - Đà Lạt 2',
    '(DNO) Đức An'
]

print('\n' + '='*85)
print('🎯 CHUẨN XÁC TARGET THEO CÔNG THỨC CHỊ THỦY (F11):')
print('='*85)
results = {}
for bc in alert_hubs:
    d6 = map_6d.get(bc, {'vol_6d': 0, 'gtc_6d': 0})
    vol_6d = d6['vol_6d']
    gtc_6d = d6['gtc_6d']
    
    hid = hub_id_map.get(bc, '')
    vol_today = vol_today_map.get(hid, vol_today_map.get(bc, 0))
    gtc_best = best_map.get(bc, 0.45)
    
    c1 = (vol_6d + vol_today) * 0.7 * gtc_best - gtc_6d
    c2 = (vol_6d + vol_today) * 0.45 - gtc_6d
    c3 = vol_today * 0.2
    target = math.ceil(max(c1, c2, c3)) if vol_today > 0 else 0
    target = max(target, 0)
    results[bc] = {
        'vol_today': vol_today,
        'target': target,
        'vol_6d': vol_6d,
        'gtc_6d': gtc_6d,
        'gtc_best': round(gtc_best * 100, 1)
    }
    print(f"{bc:27} | Vol: {vol_today:5} | Vol6d: {vol_6d:5} | GTC6d: {gtc_6d:5} | Best: {gtc_best*100:.1f}% => TARGET: {target}")

import json
with open('true_targets_today.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
