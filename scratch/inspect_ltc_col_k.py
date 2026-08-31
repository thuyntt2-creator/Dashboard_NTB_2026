import sys, os
import pandas as pd

sys.path.insert(0, os.path.abspath('.'))
sys.stdout.reconfigure(encoding='utf-8')
from app import safe_to_numeric, safe_read_csv, clean_ops_df

df_raw = safe_read_csv('ops_ltc.csv')
df = clean_ops_df(df_raw, 'ltc')
print('Columns after clean_ops_df:', list(df.columns))
if 'Sản Lượng Lấy Thành Công' in df.columns:
    print('Sản Lượng Lấy Thành Công sample values:', df['Sản Lượng Lấy Thành Công'].head(10).tolist())
    s = safe_to_numeric(df['Sản Lượng Lấy Thành Công'])
    print('safe_to_numeric result sum:', s.sum(), 'nan count:', s.isna().sum())

print('\nCheck %LTC * Volume vs Sản Lượng Lấy Thành Công:')
df['Volume'] = safe_to_numeric(df['Volume'])
from app import normalize_pct_col
df['%LTC'] = normalize_pct_col(df['%LTC'])
vol_pct = df['Volume'] * df['%LTC']
print('Volume * %LTC sum:', vol_pct.sum())
