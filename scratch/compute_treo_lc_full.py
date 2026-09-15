import pandas as pd
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

df = pd.read_csv('sheet_stuck.csv')

# Regional Totals
vc_all = df['Thoi gian ton dong'].value_counts().to_dict()
tot_u24 = vc_all.get('0_6', 0) + vc_all.get('6_12', 0) + vc_all.get('12_24', 0)
tot_24_36 = vc_all.get('24_36', 0)
tot_36_72 = vc_all.get('36_48', 0) + vc_all.get('48_72', 0)
tot_72_120 = vc_all.get('72_96', 0) + vc_all.get('96_120', 0)
tot_120_plus = vc_all.get('120_192', 0) + vc_all.get('192', 0)
tot_treo_24 = tot_24_36 + tot_36_72 + tot_72_120 + tot_120_plus
tot_treo_36 = tot_36_72 + tot_72_120 + tot_120_plus

print(f"REGIONAL TOTALS: Total={len(df)}, <24h={tot_u24}, 24-36h={tot_24_36}, 36-72h={tot_36_72}, 72-120h={tot_72_120}, >120h={tot_120_plus}, Treo>=24h={tot_treo_24}, Treo>=36h={tot_treo_36}")

# By AM
am_stats = []
for am, g in df.groupby('am_name'):
    vc = g['Thoi gian ton dong'].value_counts().to_dict()
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
        'pct': round(vol / len(df) * 100, 1),
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

# Sort by total vol descending
am_stats = sorted(am_stats, key=lambda x: x['vol'], reverse=True)

# By BC
bc_stats = []
for (bc, tinh, am), g in df.groupby(['warehouse_name', 'province_name', 'am_name']):
    vc = g['Thoi gian ton dong'].value_counts().to_dict()
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
        'pct': round(vol / len(df) * 100, 1),
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
for tinh, g in df.groupby('province_name'):
    vol = len(g)
    tinh_stats.append({
        'tinh': tinh,
        'vol': vol,
        'pct': round(vol / len(df) * 100, 1)
    })
tinh_stats = sorted(tinh_stats, key=lambda x: x['vol'], reverse=True)

res = {
    'total': len(df),
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

with open('scratch/treo_lc_calculated.json', 'w', encoding='utf-8') as f:
    json.dump(res, f, ensure_ascii=False, indent=2)

print("Saved scratch/treo_lc_calculated.json with full bucket breakdowns!")
