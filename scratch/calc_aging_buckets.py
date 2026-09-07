import pandas as pd
import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('data.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

# 1. PROCESS AGING BUCKETS FROM sheet_aging.csv
df_ag = pd.read_csv('sheet_aging.csv')
total_ag = len(df_ag)

df_ag['days_num'] = pd.to_numeric(df_ag['Aging'], errors='coerce').fillna(5.0)

def classify_bucket(days):
    if days > 15:
        return 'gt_15'
    elif days >= 8:
        return 'd_8_15'
    else:
        return 'd_5_8'

df_ag['bucket'] = df_ag['days_num'].apply(classify_bucket)

# All 18 AMs list from cocau
am_list = [
    "Lê Văn Trường", "Trương Quang Linh", "Hồng Bích Nga", "Trầm Hữu Tiến",
    "Huỳnh Thị Kim Chi", "Lê Minh Lợi", "Nguyễn Thanh Long", "Trần Thị Nhung",
    "Huỳnh Thúc Duân", "Nguyễn Duy Long", "Nguyễn Hoàng Phi", "Lê Thanh Nhựt",
    "Nguyễn Lê Nguyên Vũ", "Thái Thị Thanh Thư", "Phan Đình Duy", "Nguyễn Ngọc Khánh",
    "Cao Thị Thanh Thủy", "Nguyễn Thị Tuyết Thơ", "Lê Minh Đại", "Trần Văn Phước"
]

# Group AM
pvt_am = df_ag.pivot_table(index='am_name', columns='bucket', values='order_code', aggfunc='count', fill_value=0).reset_index()
for col in ['d_5_8', 'd_8_15', 'gt_15']:
    if col not in pvt_am.columns:
        pvt_am[col] = 0

pvt_am['vol'] = pvt_am['d_5_8'] + pvt_am['d_8_15'] + pvt_am['gt_15']
pvt_am['pct'] = (pvt_am['vol'] / total_ag * 100).round(1)

# Sort descending
pvt_am = pvt_am.sort_values('vol', ascending=False)

# Include 0-aging AMs
existing_ams = set(pvt_am['am_name'])
extra_ams = []
for am in am_list:
    clean_am = am.replace('Hồng Bích Nga', 'Hồng Bích Nga').replace('Nguyễn Thanh Long', 'Nguyễn Thanh Long')
    if am not in existing_ams and clean_am not in existing_ams:
        extra_ams.append({
            'am': am,
            'tinh': '',
            'd_5_8': 0,
            'd_8_15': 0,
            'gt_15': 0,
            'vol': 0,
            'pct': 0.0
        })

top_am_data = []
for _, r in pvt_am.iterrows():
    am_name = str(r['am_name'])
    tinh = df_ag[df_ag['am_name'] == am_name]['tinh'].mode()[0] if len(df_ag[df_ag['am_name'] == am_name]) > 0 else ''
    top_am_data.append({
        'am': am_name,
        'tinh': str(tinh),
        'd_5_8': int(r['d_5_8']),
        'd_8_15': int(r['d_8_15']),
        'gt_15': int(r['gt_15']),
        'vol': int(r['vol']),
        'pct': float(r['pct'])
    })

top_am_data.extend(extra_ams)

# Group BC
pvt_bc = df_ag.pivot_table(index=['bc', 'tinh', 'am_name'], columns='bucket', values='order_code', aggfunc='count', fill_value=0).reset_index()
for col in ['d_5_8', 'd_8_15', 'gt_15']:
    if col not in pvt_bc.columns:
        pvt_bc[col] = 0

pvt_bc['vol'] = pvt_bc['d_5_8'] + pvt_bc['d_8_15'] + pvt_bc['gt_15']
pvt_bc['pct'] = (pvt_bc['vol'] / total_ag * 100).round(1)
pvt_bc = pvt_bc.sort_values('vol', ascending=False)

top_bc_data = [
    {
        'bc': str(r['bc']),
        'tinh': str(r['tinh']),
        'am': str(r['am_name']),
        'd_5_8': int(r['d_5_8']),
        'd_8_15': int(r['d_8_15']),
        'gt_15': int(r['gt_15']),
        'vol': int(r['vol']),
        'pct': float(r['pct'])
    }
    for _, r in pvt_bc.iterrows()
]

# Total summary row
total_5_8 = int(pvt_am['d_5_8'].sum())
total_8_15 = int(pvt_am['d_8_15'].sum())
total_gt_15 = int(pvt_am['gt_15'].sum())

d['aging'] = {
    'total': int(total_ag),
    'total_5_8': total_5_8,
    'total_8_15': total_8_15,
    'total_gt_15': total_gt_15,
    'top_am': top_am_data,
    'top_bc': top_bc_data,
    'tinh': [
        {
            'tinh': str(t),
            'vol': int(c),
            'pct': float(round(c / total_ag * 100, 1))
        }
        for t, c in df_ag['tinh'].value_counts().items()
    ]
}

# 2. TREO LC BUCKETS from sheet_stuck.csv
if os.path.exists('sheet_stuck.csv'):
    try:
        df_stuck = pd.read_csv('sheet_stuck.csv', encoding='utf-8')
    except Exception:
        df_stuck = pd.read_csv('sheet_stuck.csv', encoding='latin1')
    order_col = [c for c in df_stuck.columns if 'đơn hàng' in c.lower() or 'order' in c.lower() or 'mã' in c.lower()]
    order_col = order_col[0] if order_col else df_stuck.columns[0]
    total_stuck = len(df_stuck)
    
    stuck_am = df_stuck.groupby('am_name').agg(
        vol=(order_col, 'count'),
        tinh=('province_name', lambda x: x.mode()[0] if len(x) > 0 else '')
    ).reset_index()
    stuck_am['pct'] = (stuck_am['vol'] / total_stuck * 100).round(1)
    stuck_am = stuck_am.sort_values('vol', ascending=False)

    stuck_bc = df_stuck.groupby(['warehouse_name', 'province_name', 'am_name']).agg(
        vol=(order_col, 'count')
    ).reset_index()
    stuck_bc['pct'] = (stuck_bc['vol'] / total_stuck * 100).round(1)
    stuck_bc = stuck_bc.sort_values('vol', ascending=False)

    d['treo_lc'] = {
        'total': int(total_stuck),
        'top_am': [
            {
                'am': str(r['am_name']),
                'tinh': str(r['tinh']),
                'vol': int(r['vol']),
                'pct': float(r['pct'])
            }
            for _, r in stuck_am.iterrows()
        ],
        'top_bc': [
            {
                'bc': str(r['warehouse_name']),
                'tinh': str(r['province_name']),
                'am': str(r['am_name']),
                'vol': int(r['vol']),
                'pct': float(r['pct'])
            }
            for _, r in stuck_bc.iterrows()
        ],
        'tinh': [
            {
                'tinh': str(t),
                'vol': int(c),
                'pct': float(round(c / total_stuck * 100, 1))
            }
            for t, c in df_stuck['province_name'].value_counts().items()
        ]
    }

with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(d, f, ensure_ascii=False, indent=2)

with open('data.js', 'w', encoding='utf-8') as f:
    f.write('window.DASHBOARD_DATA = ' + json.dumps(d, ensure_ascii=False, indent=2) + ';\n')

print("SUCCESSFULLY APPLIED AGING BUCKETS TO data.json & data.js!")
print(f"Total: {total_ag} | 5-8d: {total_5_8} | 8-15d: {total_8_15} | >15d: {total_gt_15}")
