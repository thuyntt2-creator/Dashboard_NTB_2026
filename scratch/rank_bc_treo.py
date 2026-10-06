import pandas as pd, sys
sys.stdout.reconfigure(encoding='utf-8')
df = pd.read_csv('sheet_stuck.csv')
df.loc[df['province_name'] == '(DNO) Nhân Cơ 1', 'province_name'] = 'Đắk Nông'
df['am_clean'] = df['am_name'].astype(str).str.strip().str.replace('Hồng Bích Nga', 'Hồng Bích Nga').str.replace('Nguyễn Thanh Long', 'Nguyễn Thanh Long')

ton_col = 'Thời gian tồn đọng'
treo_cats = ['24_36', '36_48', '48_72', '72_96', '96_120', '120_192', '192']
treo36_cats = ['36_48', '48_72', '72_96', '96_120', '120_192', '192']

bc_list = []
for (bc, prov, am), g in df.groupby(['warehouse_name', 'province_name', 'am_clean']):
    tot = len(g)
    u24 = len(g[g[ton_col].isin(['0_6', '6_12', '12_24'])])
    t24 = len(g[g[ton_col].isin(treo_cats)])
    t36 = len(g[g[ton_col].isin(treo36_cats)])
    bc_list.append({'bc': bc, 'province': prov, 'am': am, 'tot': tot, 'u24': u24, 't24': t24, 't36': t36, 'rate24': t24/tot*100})

bc_list.sort(key=lambda x: (x['t24'], x['t36']), reverse=True)
for i, x in enumerate(bc_list[:15], 1):
    print(f"{i:2d}. BC {x['bc']} ({x['province']} - {x['am']}): Treo>=24h={x['t24']:2d} ({x['rate24']:4.1f}%) | Treo>=36h={x['t36']:2d} | <24h={x['u24']:3d} | Tổng={x['tot']:3d}")
