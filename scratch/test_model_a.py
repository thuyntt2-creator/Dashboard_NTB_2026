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
    # Ca 1: indexed by Col 3 (Time)
    bc1 = str(row.iloc[1]).strip()
    date1 = str(row.iloc[3]).strip()
    vol1 = clean_num(row.iloc[4])
    pct_gan1 = clean_pct(row.iloc[5])
    pct_gtc1 = clean_pct(row.iloc[6])
    gtc1 = round(vol1 * (pct_gtc1 / 100.0))
    am1 = str(row.iloc[12]).strip()
    if bc1 and bc1 not in ('nan', 'None', '', 'Cấp Quản Lý', 'Chi tiết') and date1 and date1 not in ('nan', 'None', '', 'Time'):
        records.append({
            'Bưu Cục': bc1,
            'AM': am1 if am1 not in ('nan', 'None', '') else 'Không xác định',
            'Date': date1,
            'Loại Hàng': 'Hàng Mới Ca 1',
            'Volume': vol1,
            'Sản Lượng Giao Thành Công': gtc1,
            'Assigned_Vol': vol1 * (pct_gan1 / 100.0)
        })

    # Ca 2: indexed by Col 17 (Time.1)
    bc2 = str(row.iloc[15]).strip()
    date2 = str(row.iloc[17]).strip()
    vol2 = clean_num(row.iloc[18])
    pct_gan2 = clean_pct(row.iloc[19])
    pct_gtc2 = clean_pct(row.iloc[20])
    gtc2 = round(vol2 * (pct_gtc2 / 100.0))
    am2 = str(row.iloc[26]).strip()
    if bc2 and bc2 not in ('nan', 'None', '', 'Cấp Quản Lý', 'Chi tiết') and date2 and date2 not in ('nan', 'None', '', 'Time'):
        records.append({
            'Bưu Cục': bc2,
            'AM': am2 if am2 not in ('nan', 'None', '') else 'Không xác định',
            'Date': date2,
            'Loại Hàng': 'Hàng Mới Ca 2',
            'Volume': vol2,
            'Sản Lượng Giao Thành Công': gtc2,
            'Assigned_Vol': vol2 * (pct_gan2 / 100.0)
        })

    # Hàng Tồn: indexed by Col 31 (Time.2)
    bc3 = str(row.iloc[29]).strip()
    date3 = str(row.iloc[31]).strip()
    vol3 = clean_num(row.iloc[32])
    pct_gan3 = clean_pct(row.iloc[33])
    pct_gtc3 = clean_pct(row.iloc[34])
    gtc3 = round(vol3 * (pct_gtc3 / 100.0))
    am3 = str(row.iloc[40]).strip()
    if bc3 and bc3 not in ('nan', 'None', '', 'Cấp Quản Lý', 'Chi tiết') and date3 and date3 not in ('nan', 'None', '', 'Time'):
        records.append({
            'Bưu Cục': bc3,
            'AM': am3 if am3 not in ('nan', 'None', '') else 'Không xác định',
            'Date': date3,
            'Loại Hàng': 'Hàng Tồn',
            'Volume': vol3,
            'Sản Lượng Giao Thành Công': gtc3,
            'Assigned_Vol': vol3 * (pct_gan3 / 100.0)
        })

df_parsed = pd.DataFrame(records)

print("=== MODEL A: AM NGA BY DATE ===")
nga = df_parsed[df_parsed['AM'] == 'AM Nga']
for d, sub in nga.groupby('Date'):
    v1 = sub[sub['Loại Hàng'] == 'Hàng Mới Ca 1']['Volume'].sum()
    g1 = sub[sub['Loại Hàng'] == 'Hàng Mới Ca 1']['Sản Lượng Giao Thành Công'].sum()
    v2 = sub[sub['Loại Hàng'] == 'Hàng Mới Ca 2']['Volume'].sum()
    g2 = sub[sub['Loại Hàng'] == 'Hàng Mới Ca 2']['Sản Lượng Giao Thành Công'].sum()
    v3 = sub[sub['Loại Hàng'] == 'Hàng Tồn']['Volume'].sum()
    g3 = sub[sub['Loại Hàng'] == 'Hàng Tồn']['Sản Lượng Giao Thành Công'].sum()
    
    vt = v1 + v2 + v3
    gt = g1 + g2 + g3
    pt = (gt / vt * 100) if vt > 0 else 0
    print(f"Date: {d}")
    print(f"  Ca 1: Vol {v1:,} | GTC {g1:,}")
    print(f"  Ca 2: Vol {v2:,} | GTC {g2:,}")
    print(f"  Tồn : Vol {v3:,} | GTC {g3:,}")
    print(f"  TỔNG: Vol {vt:,} | GTC {gt:,} ({pt:.2f}%)\n")
