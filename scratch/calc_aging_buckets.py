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
    
    total_stuck = len(df_stuck)
    
    # Regional Totals
    vc_all = df_stuck['Thoi gian ton dong'].value_counts().to_dict() if 'Thoi gian ton dong' in df_stuck.columns else {}
    tot_u24 = vc_all.get('0_6', 0) + vc_all.get('6_12', 0) + vc_all.get('12_24', 0)
    tot_24_36 = vc_all.get('24_36', 0)
    tot_36_72 = vc_all.get('36_48', 0) + vc_all.get('48_72', 0)
    tot_72_120 = vc_all.get('72_96', 0) + vc_all.get('96_120', 0)
    tot_120_plus = vc_all.get('120_192', 0) + vc_all.get('192', 0)
    tot_treo_24 = tot_24_36 + tot_36_72 + tot_72_120 + tot_120_plus
    tot_treo_36 = tot_36_72 + tot_72_120 + tot_120_plus

    # By AM
    am_stats = []
    for am, g in df_stuck.groupby('am_name'):
        vc = g['Thoi gian ton dong'].value_counts().to_dict() if 'Thoi gian ton dong' in g.columns else {}
        u24 = vc.get('0_6', 0) + vc.get('6_12', 0) + vc.get('12_24', 0)
        h24 = vc.get('24_36', 0)
        h36 = vc.get('36_48', 0) + vc.get('48_72', 0)
        h72 = vc.get('72_96', 0) + vc.get('96_120', 0)
        h120 = vc.get('120_192', 0) + vc.get('192', 0)
        treo24 = h24 + h36 + h72 + h120
        treo36 = h36 + h72 + h120
        tinh = g['province_name'].mode()[0] if len(g['province_name']) > 0 else ''
        vol = len(g)
        am_stats.append({
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
    am_stats = sorted(am_stats, key=lambda x: x['vol'], reverse=True)

    # By BC
    bc_stats = []
    for (bc, tinh, am), g in df_stuck.groupby(['warehouse_name', 'province_name', 'am_name']):
        vc = g['Thoi gian ton dong'].value_counts().to_dict() if 'Thoi gian ton dong' in g.columns else {}
        u24 = vc.get('0_6', 0) + vc.get('6_12', 0) + vc.get('12_24', 0)
        h24 = vc.get('24_36', 0)
        h36 = vc.get('36_48', 0) + vc.get('48_72', 0)
        h72 = vc.get('72_96', 0) + vc.get('96_120', 0)
        h120 = vc.get('120_192', 0) + vc.get('192', 0)
        treo24 = h24 + h36 + h72 + h120
        treo36 = h36 + h72 + h120
        vol = len(g)
        bc_stats.append({
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
    bc_stats = sorted(bc_stats, key=lambda x: x['vol'], reverse=True)

    # By Tinh
    tinh_stats = []
    for tinh, g in df_stuck.groupby('province_name'):
        vol = len(g)
        tinh_stats.append({
            'tinh': tinh,
            'vol': vol,
            'pct': round(vol / total_stuck * 100, 1) if total_stuck else 0
        })
    tinh_stats = sorted(tinh_stats, key=lambda x: x['vol'], reverse=True)

    d['treo_lc'] = {
        'total': total_stuck,
        'total_u24': tot_u24,
        'total_24_36': tot_24_36,
        'total_36_72': tot_36_72,
        'total_72_120': tot_72_120,
        'total_120_plus': tot_120_plus,
        'total_treo_24': tot_treo_24,
        'total_treo_36': tot_treo_36,
        'top_am': am_stats,
        'top_bc': bc_stats,
        'tinh': tinh_stats
    }

    os.makedirs('scratch', exist_ok=True)
    with open('scratch/treo_lc_calculated.json', 'w', encoding='utf-8') as f_calc:
        json.dump(d['treo_lc'], f_calc, ensure_ascii=False, indent=2)

with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(d, f, ensure_ascii=False, indent=2)

with open('data.js', 'w', encoding='utf-8') as f:
    f.write('window.DASHBOARD_DATA = ' + json.dumps(d, ensure_ascii=False, indent=2) + ';\n')

print("SUCCESSFULLY APPLIED AGING BUCKETS TO data.json & data.js!")
print(f"Total: {total_ag} | 5-8d: {total_5_8} | 8-15d: {total_8_15} | >15d: {total_gt_15}")
