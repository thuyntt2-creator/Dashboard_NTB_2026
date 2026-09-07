import pandas as pd
import json
import re
import unicodedata

# 1. Load co_cau
co_cau = pd.read_csv('co_cau_ntb.csv')
co_cau['bc_norm'] = co_cau['Bưu cục'].apply(lambda s: unicodedata.normalize('NFC', re.sub(r'\s+', ' ', re.sub(r'[\s\-_]+', '', str(s).lower()))))
bc_am_map = dict(zip(co_cau['bc_norm'], co_cau['AM'].apply(lambda s: unicodedata.normalize('NFC', str(s).strip()))))

def find_am_for_bc(bc_name):
    norm = unicodedata.normalize('NFC', re.sub(r'\s+', ' ', re.sub(r'[\s\-_]+', '', str(bc_name).lower())))
    return bc_am_map.get(norm, '---')

# AM mapping
am_name_map = {
    'AM Vũ': 'Nguyễn Lê Nguyên Vũ',
    'AM Nga': 'Hồng Bích Nga',
    'AM Long': 'Nguyễn Thanh Long',
    'AM Khánh': 'Nguyễn Ngọc Khánh',
    'AM Linh': 'Trương Quang Linh',
    'AM Thủy': 'Cao Thị Thanh Thủy',
    'AM Lợi': 'Lê Minh Lợi',
    'AM Tiến': 'Trầm Hữu Tiến',
    'AM Duân': 'Huỳnh Thúc Duân',
    'AM Thơ': 'Nguyễn Thị Tuyết Thơ',
    'AM Phi': 'Nguyễn Hoàng Phi',
    'AM Nhựt': 'Lê Thanh Nhựt',
    'AM Thư': 'Thái Thị Thanh Thư',
    'AM Chi': 'Huỳnh Thị Kim Chi',
    'AM D.Long': 'Nguyễn Duy Long',
    'AM Nhung': 'Trần Thị Nhung',
    'AM Duy': 'Phan Đình Duy',
    'AM Trường': 'Lê Văn Trường'
}

# 2. Load sheet_FD.csv
df = pd.read_csv('sheet_FD.csv')
df_w36 = df[df['delivery_date'] != '8/30/2026'].copy()
df_prev = df[df['delivery_date'] == '8/30/2026'].copy()

# Filter valid AM
df_w36 = df_w36[df_w36['AM'].notna() & (df_w36['AM'] != '')].copy()

# Full calculation W36
full_w36 = df_w36.groupby('AM').agg({'Total đơn': 'sum', 'Đơn return': 'sum'}).reset_index()
tot_ret_full = full_w36['Đơn return'].sum()
tot_vol_full = full_w36['Total đơn'].sum()

# TTS calculation W36
df_tts_w36 = df_w36[df_w36['client_type'].isin(['TTS', 'TTS Bulky'])].copy()
tts_w36 = df_tts_w36.groupby('AM').agg({'Total đơn': 'sum', 'Đơn return': 'sum'}).reset_index()
tot_ret_tts = tts_w36['Đơn return'].sum()
tot_vol_tts = tts_w36['Total đơn'].sum()

# Load fd_history baseline for Full prev
with open('fd_history.json', 'r', encoding='utf-8') as f:
    hist = json.load(f)[0]
am_hist = hist.get('am_map', {})

# TTS prev from 8/30
df_tts_prev = df_prev[df_prev['client_type'].isin(['TTS', 'TTS Bulky'])].copy()
tts_prev_agg = df_tts_prev.groupby('AM').agg({'Total đơn': 'sum', 'Đơn return': 'sum'}).reset_index()
tts_prev_agg['rate'] = tts_prev_agg['Đơn return'] / tts_prev_agg['Total đơn']
tts_prev_map = dict(zip(tts_prev_agg['AM'], tts_prev_agg['rate']))

full_map = dict(zip(full_w36['AM'], zip(full_w36['Total đơn'], full_w36['Đơn return'])))
tts_map = dict(zip(tts_w36['AM'], zip(tts_w36['Total đơn'], tts_w36['Đơn return'])))

am_list = []
for am_code, am_full_name in am_name_map.items():
    v_full, r_full = full_map.get(am_code, (0, 0))
    rate_full = (r_full / v_full) if v_full > 0 else 0
    prev_full_pct = am_hist.get(am_code, {}).get('fd_rate', (rate_full * 100)) / 100.0
    diff_full = rate_full - prev_full_pct

    v_tts, r_tts = tts_map.get(am_code, (0, 0))
    rate_tts = (r_tts / v_tts) if v_tts > 0 else 0
    prev_tts_rate = tts_prev_map.get(am_code, rate_tts)
    diff_tts = rate_tts - prev_tts_rate

    share_ret = (r_full / tot_ret_full) if tot_ret_full > 0 else 0
    share_vol = (v_full / tot_vol_full) if tot_vol_full > 0 else 0

    am_list.append({
        'am': am_full_name,
        'am_code': am_code,
        'vol_full': int(v_full),
        'ret_full': int(r_full),
        'rate_full': round(rate_full, 4),
        'rate_full_prev': round(prev_full_pct, 4),
        'diff_full': round(diff_full, 4),
        'vol_tts': int(v_tts),
        'ret_tts': int(r_tts),
        'rate_tts': round(rate_tts, 4),
        'rate_tts_prev': round(prev_tts_rate, 4),
        'diff_tts': round(diff_tts, 4),
        'share_ret': round(share_ret, 4),
        'share_vol': round(share_vol, 4)
    })

# Sort by %FD full descending
am_list = sorted(am_list, key=lambda x: x['rate_full'], reverse=True)

# 3. Top Bưu Cục
bc_df = df_w36.groupby(['ID bưu cục', 'Tên bưu cục', 'AM']).agg({
    'Total đơn': 'sum',
    'Đơn return': 'sum'
}).reset_index()

bc_df['rate'] = bc_df['Đơn return'] / bc_df['Total đơn']
bc_df['share_ret'] = bc_df['Đơn return'] / tot_ret_full

top10_bc_raw = bc_df.sort_values(by='rate', ascending=False).head(15)
top_bc_list = []
for i, (_, r) in enumerate(top10_bc_raw.iterrows(), 1):
    bc_name = unicodedata.normalize('NFC', str(r['Tên bưu cục']).strip())
    am_raw = am_name_map.get(str(r['AM']).strip(), find_am_for_bc(bc_name))
    top_bc_list.append({
        'stt': i,
        'id_bc': int(r['ID bưu cục']),
        'bc': bc_name,
        'am': am_raw,
        'vol': int(r['Total đơn']),
        'ret': int(r['Đơn return']),
        'rate': round(float(r['rate']), 4),
        'share_ret': round(float(r['share_ret']), 4)
    })

fd_payload = {
    'summary': {
        'vol_full': int(tot_vol_full),
        'ret_full': int(tot_ret_full),
        'rate_full': round(tot_ret_full / tot_vol_full, 4),
        'vol_tts': int(tot_vol_tts),
        'ret_tts': int(tot_ret_tts),
        'rate_tts': round(tot_ret_tts / tot_vol_tts, 4),
        'bc_count': len(bc_df),
        'am_count': len(am_list)
    },
    'am': am_list,
    'top_bc': top_bc_list
}

with open('scratch/fd_processed.json', 'w', encoding='utf-8') as f:
    json.dump(fd_payload, f, ensure_ascii=False, indent=2)

print("Saved scratch/fd_processed.json successfully!")
print("Summary:", fd_payload['summary'])
print("Top 3 AM Full:", [(a['am'], a['rate_full'], a['diff_full']) for a in am_list[:3]])
print("Top 3 BC:", [(b['bc'], b['am'], b['rate']) for b in top_bc_list[:3]])
