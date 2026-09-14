import pandas as pd
import json

df = pd.read_csv('sheet_stuck.csv', encoding='utf-8')

# Check columns
print("Total rows:", len(df))

# Bucket mapping
# 36-72h: 36_48, 48_72
# 72-120h: 72_96, 96_120
# 120-192h: 120_192
# 192h+: 192

# Let's check total for regional buckets:
c_all = df['Thoi gian ton dong'].value_counts().to_dict()
tot_36_72 = c_all.get('36_48', 0) + c_all.get('48_72', 0)
tot_72_120 = c_all.get('72_96', 0) + c_all.get('96_120', 0)
tot_120_192 = c_all.get('120_192', 0)
tot_192_plus = c_all.get('192', 0)

print(f"Regional Totals: 36-72h={tot_36_72}, 72-120h={tot_72_120}, 120-192h={tot_120_192}, 192+={tot_192_plus}")

# By AM
am_stats = []
for am, g in df.groupby('am_name'):
    counts = g['Thoi gian ton dong'].value_counts().to_dict()
    h36 = counts.get('36_48', 0) + counts.get('48_72', 0)
    h72 = counts.get('72_96', 0) + counts.get('96_120', 0)
    h120 = counts.get('120_192', 0)
    h192 = counts.get('192', 0)
    tinh = g['province_name'].mode()[0] if len(g['province_name']) > 0 else ''
    vol = len(g)
    am_stats.append({
        'am': am,
        'tinh': tinh,
        'vol': vol,
        'pct': round(vol / len(df) * 100, 1),
        'h_36_72': h36,
        'h_72_120': h72,
        'h_120_192': h120,
        'h_192_plus': h192
    })

am_stats = sorted(am_stats, key=lambda x: x['vol'], reverse=True)

# By BC
bc_stats = []
for (bc, tinh, am), g in df.groupby(['warehouse_name', 'province_name', 'am_name']):
    counts = g['Thoi gian ton dong'].value_counts().to_dict()
    h36 = counts.get('36_48', 0) + counts.get('48_72', 0)
    h72 = counts.get('72_96', 0) + counts.get('96_120', 0)
    h120 = counts.get('120_192', 0)
    h192 = counts.get('192', 0)
    vol = len(g)
    bc_stats.append({
        'bc': bc,
        'tinh': tinh,
        'am': am,
        'vol': vol,
        'pct': round(vol / len(df) * 100, 1),
        'h_36_72': h36,
        'h_72_120': h72,
        'h_120_192': h120,
        'h_192_plus': h192
    })

bc_stats = sorted(bc_stats, key=lambda x: x['vol'], reverse=True)

# Also by Tinh
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
    'total_36_72': tot_36_72,
    'total_72_120': tot_72_120,
    'total_120_192': tot_120_192,
    'total_192_plus': tot_192_plus,
    'top_am': am_stats,
    'top_bc': bc_stats[:30],
    'tinh': tinh_stats
}

with open('scratch/treo_lc_calculated.json', 'w', encoding='utf-8') as f:
    json.dump(res, f, ensure_ascii=False, indent=2)

print("Saved scratch/treo_lc_calculated.json successfully!")
