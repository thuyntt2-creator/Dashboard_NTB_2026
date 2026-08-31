import urllib.request, sys
import pandas as pd

sys.stdout.reconfigure(encoding='utf-8')

# Download online DataLTC directly to ops_ltc.csv
url_ltc = 'https://docs.google.com/spreadsheets/d/1DAwY-46twFrHIs77R4p4IMuIZ6JTE-e58Aj-9Kcr5Jk/export?format=csv&gid=1365110988'
req = urllib.request.Request(url_ltc, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req, timeout=30) as resp:
    content = resp.read()

with open('ops_ltc.csv', 'wb') as f:
    f.write(content)

print("Downloaded latest DataLTC to ops_ltc.csv")

# Now load app and update clean_ops_df logic mentally / test
import sys, os
sys.path.insert(0, os.path.abspath('.'))
from app import clean_ops_df, get_dataframes, process_operational_report

# Monkeypatch clean_ops_df to test the fix
def patch_clean_ops_df(df, sheet_type):
    if df is None:
        return None
    df = df.copy()
    df.columns = [str(c).strip() for c in df.columns]
    cols_lower = {c.lower(): c for c in df.columns}
    
    if sheet_type == "ltc":
        rename_map = {}
        is_idbuucuc_shifted = False
        if 'idbuucuc' in cols_lower and 'time' in cols_lower and 'volume' in cols_lower:
            first_id_val = str(df[cols_lower['idbuucuc']].dropna().iloc[0]) if len(df) > 0 else ''
            if ' - ' in first_id_val or '-' in first_id_val or '/' in first_id_val:
                is_idbuucuc_shifted = True
                
        if is_idbuucuc_shifted:
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
        elif 'loại hàng' in cols_lower and 'time' in cols_lower and 'volume' in cols_lower and '% gán' in cols_lower:
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
    import app
    return app.clean_ops_df(df, sheet_type)

import app
app.clean_ops_df = patch_clean_ops_df

df_gtc, df_ltc, df_co_cau, df_aging, df_treo, df_tts = get_dataframes(force=True)
ops = process_operational_report(df_gtc=df_gtc, df_ltc=df_ltc, df_tts=df_tts)

print("\n--- OPERATIONAL REPORT LTC RESULTS ---")
print("overall_ltc:", ops.get('overall_ltc'))
print("top_10_ltc:", ops.get('top_10_ltc'))
print("worst_10_ltc:", ops.get('worst_10_ltc'))
print("Latest 3 days of trend_ltc:", ops.get('trend_ltc')[-3:] if ops.get('trend_ltc') else None)
