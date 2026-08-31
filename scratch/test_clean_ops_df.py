import urllib.request, io, sys
import pandas as pd
import numpy as np

sys.stdout.reconfigure(encoding='utf-8')

def clean_ops_df(df, sheet_type):
    if df is None:
        return None
    df = df.copy()
    
    # Strip column names
    df.columns = [str(c).strip() for c in df.columns]
    cols_lower = {c.lower(): c for c in df.columns}
    
    if sheet_type == "ltc":
        rename_map = {}
        # Case A: Shifted dataltc layout with 'IDBuuCuc' containing date strings
        is_idbuucuc_shifted = False
        if 'idbuucuc' in cols_lower and 'time' in cols_lower and 'volume' in cols_lower:
            first_id_val = str(df[cols_lower['idbuucuc']].dropna().iloc[0]) if len(df) > 0 else ''
            if ' - ' in first_id_val or '-' in first_id_val or '/' in first_id_val:
                is_idbuucuc_shifted = True
                
        if is_idbuucuc_shifted:
            print("Cleaning LTC: Detected shifted layout with IDBuuCuc column!")
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
                
            other_cols = {
                'cấp quản lý': 'Cấp quản lý',
                'chi tiết': 'Chi tiết',
                'ca': 'Ca',
                'tỉnh': 'Tỉnh',
                'vùng': 'Vùng',
                'am': 'AM'
            }
            for k, standard_name in other_cols.items():
                if k in cols_lower and cols_lower[k] != standard_name:
                    rename_map[cols_lower[k]] = standard_name
                    
        # Case B: Shifted dataltc layout with 'loại hàng' containing date strings
        elif 'loại hàng' in cols_lower and 'time' in cols_lower and 'volume' in cols_lower and '% gán' in cols_lower:
            print("Cleaning LTC: Detected shifted layout with loại hàng column!")
            rename_map[cols_lower['loại hàng']] = 'Time'
            rename_map[cols_lower['time']] = 'Volume'
            rename_map[cols_lower['volume']] = '% Gán'
            rename_map[cols_lower['% gán']] = '%LTC'
            if '% ltc' in cols_lower:
                rename_map[cols_lower['% ltc']] = '%LC'
            elif '%ltc' in cols_lower:
                rename_map[cols_lower['%ltc']] = '%LC'
            
            other_cols = {
                'cấp quản lý': 'Cấp quản lý',
                'chi tiết': 'Chi tiết',
                'leadtime': 'Leadtime',
                'lead time': 'Leadtime',
                'leadtime (h)': 'Leadtime',
                'leadtime giao': 'Leadtime',
                'lead time (h)': 'Leadtime'
            }
            for k, standard_name in other_cols.items():
                if k in cols_lower and cols_lower[k] != standard_name:
                    rename_map[cols_lower[k]] = standard_name
        else:
            print("Cleaning LTC: Standard layout")
            core_ltc_cols = {
                'cấp quản lý': 'Cấp quản lý',
                'chi tiết': 'Chi tiết',
                'ca': 'Ca',
                'time': 'Time',
                'volume': 'Volume',
                'leadtime': 'Leadtime',
                'lead time': 'Leadtime',
                'leadtime (h)': 'Leadtime',
                'leadtime giao': 'Leadtime',
                'lead time (h)': 'Leadtime'
            }
            for k, standard_name in core_ltc_cols.items():
                if k in cols_lower and cols_lower[k] != standard_name:
                    rename_map[cols_lower[k]] = standard_name
                    
            if '%ltc' not in cols_lower:
                if '% ltc' in cols_lower:
                    rename_map[cols_lower['% ltc']] = '%LTC'
                elif '% gtc' in cols_lower:
                    rename_map[cols_lower['% gtc']] = '%LTC'
            else:
                rename_map[cols_lower['%ltc']] = '%LTC'
                
            if '%lc' not in cols_lower:
                if '% lc' in cols_lower:
                    rename_map[cols_lower['% lc']] = '%LC'
                elif '% chuyển trả' in cols_lower:
                    rename_map[cols_lower['% chuyển trả']] = '%LC'
            else:
                rename_map[cols_lower['%lc']] = '%LC'
                
            if '%gán' not in cols_lower:
                if '% gán' in cols_lower:
                    rename_map[cols_lower['% gán']] = '%Gán'
            else:
                rename_map[cols_lower['%gán']] = '%Gán'
            
        if rename_map:
            df = df.rename(columns=rename_map)
        return df

# Test 1: Online DataLTC
url_ltc = 'https://docs.google.com/spreadsheets/d/1DAwY-46twFrHIs77R4p4IMuIZ6JTE-e58Aj-9Kcr5Jk/export?format=csv&gid=1365110988'
req = urllib.request.Request(url_ltc, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req, timeout=30) as resp:
    df_online = pd.read_csv(io.BytesIO(resp.read()))

df_clean = clean_ops_df(df_online, "ltc")
print("\nCleaned online DataLTC:")
print("Columns:", list(df_clean.columns))
print(df_clean[['Chi tiết', 'Time', 'Volume', '%LTC', 'Sản Lượng Lấy Thành Công']].head(3))

# Test 2: Local ops_ltc.csv
df_local = pd.read_csv('ops_ltc.csv')
df_clean_local = clean_ops_df(df_local, "ltc")
print("\nCleaned local ops_ltc.csv:")
print("Columns:", list(df_clean_local.columns))
print(df_clean_local[['Chi tiết', 'Time', 'Volume', '%LTC', 'Sản Lượng Lấy Thành Công']].head(3))
