import pandas as pd
import numpy as np

# Load test data from local file previously saved or from url
import urllib.request, io
url = 'https://docs.google.com/spreadsheets/d/1JZ1eRerRqrpwjZ4HBevQunjd8VquM_cvPFz12TaJfMQ/export?format=csv&gid=432631208'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req, timeout=30) as resp:
    content = resp.read()
df = pd.read_csv(io.BytesIO(content), encoding='utf-8')

import app
name_to_am = {}
df_cc = app.safe_read_csv(app.resolve_path('co_cau_ntb.csv', write=False))
for _, r in df_cc.iterrows():
    bc_name = str(r.get('Bưu cục', '')).strip()
    am_val = str(r.get('AM', '')).strip()
    if bc_name:
        name_clean = app.clean_po_name(bc_name)
        name_to_am[name_clean] = am_val

def clean_num(x):
    try:
        if pd.isna(x) or x == '': return 0
        return int(str(x).replace('.','').replace(',',''))
    except:
        return 0

records = []
for idx, row in df.iterrows():
    bc1 = str(row.get(' Chi tiết.2', '')).strip()
    vol1 = clean_num(row.get(' Volume.2', 0))
    gtc1 = clean_num(row.get(' GTC.2', 0))
    if bc1 and bc1 != 'nan' and bc1 != 'None':
        am1 = name_to_am.get(app.clean_po_name(bc1), 'Không xác định')
        records.append({'Bưu Cục': bc1, 'AM': am1, 'Loại Hàng': 'Hàng Mới Ca 1', 'Volume': vol1, 'Sản Lượng Giao Thành Công': gtc1})

    bc2 = str(row.get(' Chi tiết.3', '')).strip()
    vol2 = clean_num(row.get(' Volume.3', 0))
    gtc2 = clean_num(row.get(' GTC.3', 0))
    if bc2 and bc2 != 'nan' and bc2 != 'None':
        am2 = name_to_am.get(app.clean_po_name(bc2), 'Không xác định')
        records.append({'Bưu Cục': bc2, 'AM': am2, 'Loại Hàng': 'Hàng Mới Ca 2', 'Volume': vol2, 'Sản Lượng Giao Thành Công': gtc2})

    bc3 = str(row.get(' Chi tiết.1', '')).strip()
    vol3 = clean_num(row.get(' Volume.1', 0))
    gtc3 = clean_num(row.get(' GTC.1', 0))
    if bc3 and bc3 != 'nan' and bc3 != 'None':
        am3 = name_to_am.get(app.clean_po_name(bc3), 'Không xác định')
        records.append({'Bưu Cục': bc3, 'AM': am3, 'Loại Hàng': 'Hàng Tồn', 'Volume': vol3, 'Sản Lượng Giao Thành Công': gtc3})

df_parsed = pd.DataFrame(records)

pt_bc = df_parsed.pivot_table(index=['AM', 'Bưu Cục'], columns='Loại Hàng', values=['Volume', 'Sản Lượng Giao Thành Công'], aggfunc='sum', fill_value=0)
pt_bc.columns = [f"{c[1]}_{c[0]}" for c in pt_bc.columns]
pt_bc = pt_bc.reset_index()

pt_am = df_parsed.pivot_table(index=['AM'], columns='Loại Hàng', values=['Volume', 'Sản Lượng Giao Thành Công'], aggfunc='sum', fill_value=0)
pt_am.columns = [f"{c[1]}_{c[0]}" for c in pt_am.columns]
pt_am = pt_am.reset_index()

print("AM pivot:")
print(pt_am.head())
