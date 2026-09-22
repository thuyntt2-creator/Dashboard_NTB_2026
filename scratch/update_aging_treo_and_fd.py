import pandas as pd
import json
import os
import sys

# 1. PROCESS FD WITH WOW COMPARISONS FOR BƯU CỤC
print("=== 1. PROCESSING FD FOR BƯU CỤC WITH WOW ===")
df_fd = pd.read_csv('sheet_FD.csv')
df_fd['date'] = pd.to_datetime(df_fd['delivery_date'])

w37_fd = df_fd[(df_fd['date'] >= '2026-09-07') & (df_fd['date'] <= '2026-09-13')]
w38_fd = df_fd[(df_fd['date'] >= '2026-09-14') & (df_fd['date'] <= '2026-09-20')]

bc_w37 = w37_fd.groupby('Tên bưu cục').agg({'Total đơn': 'sum', 'Đơn return': 'sum'}).reset_index()
bc_w37['rate_w37'] = bc_w37['Đơn return'] / bc_w37['Total đơn']
w37_rate_map = dict(zip(bc_w37['Tên bưu cục'], bc_w37['rate_w37']))

bc_w38 = w38_fd.groupby(['Tên bưu cục', 'AM']).agg({'Total đơn': 'sum', 'Đơn return': 'sum'}).reset_index()
bc_w38['rate_w38'] = bc_w38['Đơn return'] / bc_w38['Total đơn']
bc_w38['share_ret'] = bc_w38['Đơn return'] / bc_w38['Đơn return'].sum()

def get_w37_rate(bc_name):
    if bc_name in w37_rate_map:
        return float(w37_rate_map[bc_name])
    b_norm = bc_name.replace(' - ', '-').replace(' ', '')
    for k, v in w37_rate_map.items():
        if k.replace(' - ', '-').replace(' ', '') == b_norm:
            return float(v)
    return 0.0

bc_w38_sorted = bc_w38.sort_values('rate_w38', ascending=False).reset_index(drop=True)

am_name_map = {
    'AM Linh': 'Trương Quang Linh', 'AM Lợi': 'Trần Tấn Lợi', 'AM Duân': 'Huỳnh Thúc Duân',
    'AM Long': 'Nguyễn Tiến Long', 'AM Nhung': 'Trần Thị Nhung', 'AM Tiến': 'Trầm Hữu Tiến',
    'AM Duy': 'Phan Đình Duy', 'AM Phi': 'Nguyễn Hoàng Phi', 'AM Trường': 'Lê Văn Trường',
    'AM Nga': 'Hồng Bích Nga', 'AM Thư': 'Thái Thị Thanh Thư', 'AM D.Long': 'Nguyễn Duy Long',
    'AM Chi': 'Huỳnh Thị Kim Chi', 'AM Thơ': 'Nguyễn Thị Tuyết Thơ', 'AM Thủy': 'Cao Thị Thanh Thủy',
    'AM Vũ': 'Nguyễn Lê Nguyên Vũ', 'AM Nhựt': 'Lê Thanh Nhựt', 'AM Khánh': 'Nguyễn Ngọc Khánh'
}

top_bc_fd = []
for i, r in bc_w38_sorted.head(20).iterrows():
    bc = str(r['Tên bưu cục']).strip()
    am_c = str(r['AM']).strip()
    rate = float(r['rate_w38'])
    rate_prev = get_w37_rate(bc)
    diff = rate - rate_prev
    top_bc_fd.append({
        'stt': i + 1,
        'bc': bc,
        'am': am_name_map.get(am_c, am_c),
        'am_code': am_c,
        'vol': int(r['Total đơn']),
        'ret': int(r['Đơn return']),
        'rate': rate,
        'rate_prev': rate_prev,
        'diff': diff,
        'share_ret': float(r['share_ret']),
        'total_orders': int(r['Total đơn']),
        'return_orders': int(r['Đơn return']),
        'rate_fd': rate,
        'share_return': float(r['share_ret'])
    })

print(f"Top 5 BC with WoW: {[(b['bc'], round(b['rate']*100, 1), round(b['rate_prev']*100, 1), round(b['diff']*100, 2)) for b in top_bc_fd[:5]]}")

# 2. PROCESS AGING BUCKETS FROM sheet_aging.csv
print("\n=== 2. PROCESSING AGING BUCKETS FROM sheet_aging.csv ===")
df_ag = pd.read_csv('sheet_aging.csv')
total_ag = len(df_ag)
df_ag['days_num'] = pd.to_numeric(df_ag['Aging'], errors='coerce').fillna(5.0)

def classify_aging(days):
    if days > 15:
        return 'gt_15'
    elif days >= 8:
        return 'd_8_15'
    else:
        return 'd_5_8'

df_ag['bucket'] = df_ag['days_num'].apply(classify_aging)

am_list_all = [
    "Lê Văn Trường", "Trương Quang Linh", "Hồng Bích Nga", "Trầm Hữu Tiến",
    "Huỳnh Thị Kim Chi", "Lê Minh Lợi", "Nguyễn Thanh Long", "Trần Thị Nhung",
    "Huỳnh Thúc Duân", "Nguyễn Duy Long", "Nguyễn Hoàng Phi", "Lê Thanh Nhựt",
    "Nguyễn Lê Nguyên Vũ", "Thái Thị Thanh Thư", "Phan Đình Duy", "Nguyễn Ngọc Khánh",
    "Cao Thị Thanh Thủy", "Nguyễn Thị Tuyết Thơ"
]

# Standardize am_name
df_ag['am_clean'] = df_ag['am_name'].str.strip().str.replace('Hồng Bích Nga', 'Hồng Bích Nga').str.replace('Nguyễn Thanh Long', 'Nguyễn Thanh Long')

pvt_am = df_ag.pivot_table(index='am_clean', columns='bucket', values='order_code', aggfunc='count', fill_value=0).reset_index()
for col in ['d_5_8', 'd_8_15', 'gt_15']:
    if col not in pvt_am.columns:
        pvt_am[col] = 0

pvt_am['vol'] = pvt_am['d_5_8'] + pvt_am['d_8_15'] + pvt_am['gt_15']
pvt_am['pct'] = (pvt_am['vol'] / total_ag * 100).round(1)
pvt_am = pvt_am.sort_values('vol', ascending=False)

top_am_aging = []
existing_ams = set(pvt_am['am_clean'])
for _, r in pvt_am.iterrows():
    am_name = str(r['am_clean'])
    tinh = df_ag[df_ag['am_clean'] == am_name]['tinh'].mode()[0] if len(df_ag[df_ag['am_clean'] == am_name]) > 0 else ''
    top_am_aging.append({
        'am': am_name,
        'tinh': str(tinh),
        'd_5_8': int(r['d_5_8']),
        'd_8_15': int(r['d_8_15']),
        'gt_15': int(r['gt_15']),
        'vol': int(r['vol']),
        'pct': float(r['pct'])
    })

for am in am_list_all:
    if am not in existing_ams:
        top_am_aging.append({
            'am': am,
            'tinh': '',
            'd_5_8': 0,
            'd_8_15': 0,
            'gt_15': 0,
            'vol': 0,
            'pct': 0.0
        })

# By BC
pvt_bc = df_ag.pivot_table(index=['bc', 'tinh', 'am_clean'], columns='bucket', values='order_code', aggfunc='count', fill_value=0).reset_index()
for col in ['d_5_8', 'd_8_15', 'gt_15']:
    if col not in pvt_bc.columns:
        pvt_bc[col] = 0
pvt_bc['vol'] = pvt_bc['d_5_8'] + pvt_bc['d_8_15'] + pvt_bc['gt_15']
pvt_bc['pct'] = (pvt_bc['vol'] / total_ag * 100).round(1)
pvt_bc = pvt_bc.sort_values('vol', ascending=False)

top_bc_aging = [
    {
        'bc': str(r['bc']),
        'tinh': str(r['tinh']),
        'am': str(r['am_clean']),
        'd_5_8': int(r['d_5_8']),
        'd_8_15': int(r['d_8_15']),
        'gt_15': int(r['gt_15']),
        'vol': int(r['vol']),
        'pct': float(r['pct'])
    }
    for _, r in pvt_bc.iterrows()
]

total_5_8 = int(pvt_am['d_5_8'].sum())
total_8_15 = int(pvt_am['d_8_15'].sum())
total_gt_15 = int(pvt_am['gt_15'].sum())

aging_data = {
    'total': int(total_ag),
    'total_5_8': total_5_8,
    'total_8_15': total_8_15,
    'total_gt_15': total_gt_15,
    'top_am': top_am_aging,
    'top_bc': top_bc_aging,
    'tinh': [
        {
            'tinh': str(t),
            'vol': int(c),
            'pct': float(round(c / total_ag * 100, 1))
        }
        for t, c in df_ag['tinh'].value_counts().items()
    ]
}

print(f"Aging parsed: Total {total_ag} | 5-8d: {total_5_8} | 8-15d: {total_8_15} | >15d: {total_gt_15}")

# 3. PROCESS TREO LUÂN CHUYỂN FROM sheet_stuck.csv
print("\n=== 3. PROCESSING TREO LUÂN CHUYỂN FROM sheet_stuck.csv ===")
df_stuck = pd.read_csv('sheet_stuck.csv')
total_stuck = len(df_stuck)
col_time = 'Thời gian tồn đọng' if 'Thời gian tồn đọng' in df_stuck.columns else 'Thoi gian ton dong'
df_stuck['am_clean'] = df_stuck['am_name'].astype(str).str.strip().str.replace('Hồng Bích Nga', 'Hồng Bích Nga').str.replace('Nguyễn Thanh Long', 'Nguyễn Thanh Long')

vc_all = df_stuck[col_time].value_counts().to_dict()
tot_u24 = vc_all.get('0_6', 0) + vc_all.get('6_12', 0) + vc_all.get('12_24', 0)
tot_24_36 = vc_all.get('24_36', 0)
tot_36_72 = vc_all.get('36_48', 0) + vc_all.get('48_72', 0)
tot_72_120 = vc_all.get('72_96', 0) + vc_all.get('96_120', 0)
tot_120_plus = vc_all.get('120_192', 0) + vc_all.get('192', 0)
tot_treo_24 = tot_24_36 + tot_36_72 + tot_72_120 + tot_120_plus
tot_treo_36 = tot_36_72 + tot_72_120 + tot_120_plus

am_stuck = []
for am, g in df_stuck.groupby('am_clean'):
    vc = g[col_time].value_counts().to_dict()
    u24 = vc.get('0_6', 0) + vc.get('6_12', 0) + vc.get('12_24', 0)
    h24 = vc.get('24_36', 0)
    h36 = vc.get('36_48', 0) + vc.get('48_72', 0)
    h72 = vc.get('72_96', 0) + vc.get('96_120', 0)
    h120 = vc.get('120_192', 0) + vc.get('192', 0)
    treo24 = h24 + h36 + h72 + h120
    treo36 = h36 + h72 + h120
    tinh = g['province_name'].mode()[0] if len(g['province_name']) > 0 else ''
    vol = len(g)
    am_stuck.append({
        'am': am,
        'tinh': tinh,
        'vol': vol,
        'pct': round(vol / total_stuck * 100, 1) if total_stuck else 0,
        'u_24': u24,
        'h_24_36': h24,
        'h_36_72': h36,
        'h_72_120': h72,
        'h_120_plus': h120,
        'h_120_192': vc.get('120_192', 0),
        'h_192_plus': vc.get('192', 0),
        'treo_24': treo24,
        'treo_36': treo36
    })

am_stuck = sorted(am_stuck, key=lambda x: x['vol'], reverse=True)

bc_stuck = []
for (bc, tinh, am), g in df_stuck.groupby(['warehouse_name', 'province_name', 'am_clean']):
    vc = g[col_time].value_counts().to_dict()
    u24 = vc.get('0_6', 0) + vc.get('6_12', 0) + vc.get('12_24', 0)
    h24 = vc.get('24_36', 0)
    h36 = vc.get('36_48', 0) + vc.get('48_72', 0)
    h72 = vc.get('72_96', 0) + vc.get('96_120', 0)
    h120 = vc.get('120_192', 0) + vc.get('192', 0)
    treo24 = h24 + h36 + h72 + h120
    treo36 = h36 + h72 + h120
    vol = len(g)
    bc_stuck.append({
        'bc': bc,
        'tinh': tinh,
        'am': am,
        'vol': vol,
        'pct': round(vol / total_stuck * 100, 1) if total_stuck else 0,
        'u_24': u24,
        'h_24_36': h24,
        'h_36_72': h36,
        'h_72_120': h72,
        'h_120_plus': h120,
        'h_120_192': vc.get('120_192', 0),
        'h_192_plus': vc.get('192', 0),
        'treo_24': treo24,
        'treo_36': treo36
    })

bc_stuck = sorted(bc_stuck, key=lambda x: x['vol'], reverse=True)

tinh_stuck = []
for tinh, g in df_stuck.groupby('province_name'):
    vol = len(g)
    tinh_stuck.append({
        'tinh': tinh,
        'vol': vol,
        'pct': round(vol / total_stuck * 100, 1) if total_stuck else 0
    })
tinh_stuck = sorted(tinh_stuck, key=lambda x: x['vol'], reverse=True)

treo_data = {
    'total': total_stuck,
    'total_u24': tot_u24,
    'total_24_36': tot_24_36,
    'total_36_72': tot_36_72,
    'total_72_120': tot_72_120,
    'total_120_plus': tot_120_plus,
    'total_treo_24': tot_treo_24,
    'total_treo_36': tot_treo_36,
    'top_am': am_stuck,
    'top_bc': bc_stuck,
    'tinh': tinh_stuck
}

print(f"Stuck parsed: Total {total_stuck} | <24h: {tot_u24} | Treo >24h: {tot_treo_24} | Treo >36h: {tot_treo_36}")

# 4. SAVE TO JSON & JS FILES
with open('scratch/treo_lc_calculated.json', 'w', encoding='utf-8') as f:
    json.dump(treo_data, f, ensure_ascii=False, indent=2)

with open('data.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

d['aging'] = aging_data
d['treo_lc'] = treo_data
if 'fd' in d:
    d['fd']['top_bc'] = top_bc_fd

with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(d, f, ensure_ascii=False, indent=2)

with open('data.js', 'w', encoding='utf-8') as f:
    f.write('window.DASHBOARD_DATA = ' + json.dumps(d, ensure_ascii=False, indent=2) + ';\n')

print("🎉 Successfully updated data.json and data.js with fresh Aging, Treo LC, and FD Bưu Cục WoW!")
