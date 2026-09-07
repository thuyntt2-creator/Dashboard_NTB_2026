import pandas as pd
import re
import json
import unicodedata

csv_name = 'sheet_Danh_sách_KH_không_lên_đơn_sv_ngày_hôm_qua_hoặc_giảm_đơn_sv_cùng_kỳ_tuần_trước.csv'
df = pd.read_csv(csv_name).dropna(how='all')

def parse_date(d_str):
    if not isinstance(d_str, str): return None
    m = re.match(r'(\d+)\s+thg\s+(\d+),\s+(\d+)', d_str.strip())
    if m:
        day, month, year = m.groups()
        return pd.Timestamp(f'{year}-{int(month):02d}-{int(day):02d}')
    return pd.to_datetime(d_str, errors='coerce')

df['dt_date'] = df['Ngaynext'].apply(parse_date)

# Exact Kinh doanh cycle: 23-29/8 vs 30/8-5/9
prev_df = df[(df['dt_date'] >= '2026-08-23') & (df['dt_date'] <= '2026-08-29')]
curr_df = df[(df['dt_date'] >= '2026-08-30') & (df['dt_date'] <= '2026-09-05')]

p_agg = prev_df.groupby(['MaKH', 'TenKH', 'AM', 'Bưu cục'])['DT'].sum().reset_index().rename(columns={'DT': 'vol_prev'})
c_agg = curr_df.groupby(['MaKH', 'TenKH', 'AM', 'Bưu cục'])['DT'].sum().reset_index().rename(columns={'DT': 'vol_curr'})

m = pd.merge(p_agg, c_agg, on=['MaKH', 'TenKH', 'AM', 'Bưu cục'], how='outer').fillna(0)
m['diff'] = m['vol_curr'] - m['vol_prev']
m['pct_diff'] = (m['diff'] / m['vol_prev']).replace([float('inf'), -float('inf')], 0) * 100

top10 = m.sort_values(by='diff', ascending=True).head(10)
churn_list = []
for i, (_, r) in enumerate(top10.iterrows(), 1):
    pct = round(float(r['pct_diff']), 1)
    status = 'Rời Bỏ (Về 0)' if r['vol_curr'] == 0 else f'Giảm Mạnh ({pct}%)'
    am_clean = unicodedata.normalize('NFC', str(r['AM'])).strip()
    churn_list.append({
        'stt': i,
        'makh': int(r['MaKH']),
        'tenkh': unicodedata.normalize('NFC', str(r['TenKH'])).strip(),
        'am': am_clean,
        'bc': unicodedata.normalize('NFC', str(r['Bưu cục'])).strip(),
        'vol_prev': int(r['vol_prev']),
        'vol_curr': int(r['vol_curr']),
        'diff': int(r['diff']),
        'pct_diff': pct,
        'status': status
    })

# Also find shops that dropped to 0 completely
zero_df = m[m['vol_curr'] == 0].sort_values(by='diff', ascending=True).head(5)
zero_list = []
for i, (_, r) in enumerate(zero_df.iterrows(), 1):
    pct = round(float(r['pct_diff']), 1)
    am_clean = unicodedata.normalize('NFC', str(r['AM'])).strip()
    zero_list.append({
        'stt': i,
        'makh': int(r['MaKH']),
        'tenkh': unicodedata.normalize('NFC', str(r['TenKH'])).strip(),
        'am': am_clean,
        'bc': unicodedata.normalize('NFC', str(r['Bưu cục'])).strip(),
        'vol_prev': int(r['vol_prev']),
        'vol_curr': 0,
        'diff': int(r['diff']),
        'pct_diff': -100.0,
        'status': '🔴 Rời Bỏ (Về 0 đơn)'
    })

payload = {
    'top10_drop': churn_list,
    'top_zero': zero_list
}

with open('scratch/top10_churn.json', 'w', encoding='utf-8') as f:
    json.dump(payload, f, ensure_ascii=False, indent=2)

print("Saved scratch/top10_churn.json with clean NFC strings!")
