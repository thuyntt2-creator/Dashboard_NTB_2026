import urllib.request
import pandas as pd
import io
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

url = 'https://docs.google.com/spreadsheets/d/1JZ1eRerRqrpwjZ4HBevQunjd8VquM_cvPFz12TaJfMQ/export?format=csv&gid=260711009'
df = pd.read_csv(url, header=1)

def clean_num(x):
    try:
        if pd.isna(x) or str(x).strip() == '': return 0
        s = str(x).replace('.','').replace(',','').strip()
        return int(s)
    except:
        return 0

def clean_pct(x):
    try:
        if pd.isna(x) or str(x).strip() == '': return 0.0
        val_str = str(x).strip()
        has_percent = '%' in val_str
        val_str = val_str.replace('%', '').replace(',', '.')
        val = float(val_str)
        if not has_percent and 0 < val <= 1.0:
            val = val * 100
        return val
    except:
        return 0.0

records = []
for idx, row in df.iterrows():
    date1 = str(row.iloc[3]).strip()
    date2 = str(row.iloc[17]).strip()
    date3 = str(row.iloc[31]).strip()
    
    row_date = date1 if (date1 and date1 not in ('nan', 'None', '')) else (date2 if (date2 and date2 not in ('nan', 'None', '')) else date3)
    if not row_date or row_date in ('nan', 'None', '', 'Time'):
        continue

    # Ca 1
    bc1 = str(row.iloc[1]).strip()
    vol1 = clean_num(row.iloc[4])
    pct_gan1 = clean_pct(row.iloc[5])
    pct_gtc1 = clean_pct(row.iloc[6])
    gtc1 = round(vol1 * (pct_gtc1 / 100.0))
    am1 = str(row.iloc[12]).strip()
    if bc1 and bc1 not in ('nan', 'None', '', 'Cấp Quản Lý', 'Chi tiết'):
        records.append({
            'Bưu Cục': bc1,
            'AM': am1 if am1 not in ('nan', 'None', '') else 'Không xác định',
            'Date': row_date,
            'Loại Hàng': 'Hàng Mới Ca 1',
            'Volume': vol1,
            'Sản Lượng Giao Thành Công': gtc1,
            'Assigned_Vol': vol1 * (pct_gan1 / 100.0)
        })

    # Ca 2
    bc2 = str(row.iloc[15]).strip()
    vol2 = clean_num(row.iloc[18])
    pct_gan2 = clean_pct(row.iloc[19])
    pct_gtc2 = clean_pct(row.iloc[20])
    gtc2 = round(vol2 * (pct_gtc2 / 100.0))
    am2 = str(row.iloc[26]).strip()
    if bc2 and bc2 not in ('nan', 'None', '', 'Cấp Quản Lý', 'Chi tiết'):
        records.append({
            'Bưu Cục': bc2,
            'AM': am2 if am2 not in ('nan', 'None', '') else 'Không xác định',
            'Date': row_date,
            'Loại Hàng': 'Hàng Mới Ca 2',
            'Volume': vol2,
            'Sản Lượng Giao Thành Công': gtc2,
            'Assigned_Vol': vol2 * (pct_gan2 / 100.0)
        })

    # Hàng Tồn
    bc3 = str(row.iloc[29]).strip()
    vol3 = clean_num(row.iloc[32])
    pct_gan3 = clean_pct(row.iloc[33])
    pct_gtc3 = clean_pct(row.iloc[34])
    gtc3 = round(vol3 * (pct_gtc3 / 100.0))
    am3 = str(row.iloc[40]).strip()
    if bc3 and bc3 not in ('nan', 'None', '', 'Cấp Quản Lý', 'Chi tiết'):
        records.append({
            'Bưu Cục': bc3,
            'AM': am3 if am3 not in ('nan', 'None', '') else 'Không xác định',
            'Date': row_date,
            'Loại Hàng': 'Hàng Tồn',
            'Volume': vol3,
            'Sản Lượng Giao Thành Công': gtc3,
            'Assigned_Vol': vol3 * (pct_gan3 / 100.0)
        })

df_parsed = pd.DataFrame(records)
nga_23 = df_parsed[(df_parsed['AM'] == 'AM Nga') & (df_parsed['Date'] == '2026-07-23 - Thứ 5')]

print("=== RECALCULATED TABLE FOR AM NGA (2026-07-23) ===")
print(nga_23[['Bưu Cục', 'Loại Hàng', 'Volume', 'Sản Lượng Giao Thành Công']])

piv = nga_23.pivot_table(index='Bưu Cục', columns='Loại Hàng', values=['Volume', 'Sản Lượng Giao Thành Công'], aggfunc='sum', fill_value=0)
print("\n=== PIVOT TABLE ===")
print(piv)
