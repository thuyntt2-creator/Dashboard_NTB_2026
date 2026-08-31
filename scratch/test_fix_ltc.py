import urllib.request, io, sys
import pandas as pd
import numpy as np

sys.stdout.reconfigure(encoding='utf-8')

# Download online DataLTC
url_ltc = 'https://docs.google.com/spreadsheets/d/1DAwY-46twFrHIs77R4p4IMuIZ6JTE-e58Aj-9Kcr5Jk/export?format=csv&gid=1365110988'
req = urllib.request.Request(url_ltc, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req, timeout=30) as resp:
    df_raw = pd.read_csv(io.BytesIO(resp.read()))

def fix_ltc_df(df):
    df = df.copy()
    df.columns = [str(c).strip() for c in df.columns]
    cols_lower = {c.lower(): c for c in df.columns}
    
    rename_map = {}
    if 'idbuucuc' in cols_lower and 'time' in cols_lower and 'volume' in cols_lower:
        # Check if IDBuuCuc contains dates (shifted column layout)
        first_id_val = str(df[cols_lower['idbuucuc']].dropna().iloc[0]) if len(df) > 0 else ''
        if ' - ' in first_id_val or '-' in first_id_val or '/' in first_id_val:
            print("Detected shifted DataLTC layout with 'IDBuuCuc' containing date strings!")
            rename_map[cols_lower['idbuucuc']] = 'Time'
            rename_map[cols_lower['time']] = 'Volume'
            rename_map[cols_lower['volume']] = '%Gán'
            rename_map[cols_lower['%gán']] = '%LTC'
            if '%ltc' in cols_lower:
                rename_map[cols_lower['%ltc']] = '%Đóng kiện'
            if '%đóng kiện' in cols_lower:
                rename_map[cols_lower['%đóng kiện']] = '%LC'
            if '%lc' in cols_lower:
                rename_map[cols_lower['%lc']] = 'Leadtime'
                
    if rename_map:
        df = df.rename(columns=rename_map)
    return df

df_fixed = fix_ltc_df(df_raw)
print("Fixed columns:", list(df_fixed.columns))
print("\nFirst 3 rows of fixed DataLTC:")
print(df_fixed[['Chi tiết', 'Ca', 'Time', 'Volume', '%LTC', 'Sản Lượng Lấy Thành Công']].head(3))
