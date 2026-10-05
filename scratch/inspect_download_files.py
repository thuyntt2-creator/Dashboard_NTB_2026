import os
import sys
import glob
import pandas as pd
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

downloads = r'C:\Users\lap4all\Downloads'

# 1. Check [OE-IA] BÁO CÁO TRUY THU
tt_files = glob.glob(os.path.join(downloads, '*TRUY THU*'))
tt_files.sort(key=os.path.getmtime, reverse=True)
print("=== TRUY THU FILES IN DOWNLOADS ===")
for f in tt_files:
    mtime = datetime.fromtimestamp(os.path.getmtime(f)).strftime('%Y-%m-%d %H:%M:%S')
    print(f"File: {os.path.basename(f)} | Modified: {mtime} | Size: {os.path.getsize(f):,} bytes")
    try:
        df = pd.read_csv(f, low_memory=False)
        print(f"  Rows: {len(df):,} | Columns: {list(df.columns)[:5]}")
        col_date = [c for c in df.columns if 'ngày' in c.lower()]
        for c in col_date:
            print(f"  Col '{c}' tail dates: {df[c].dropna().unique()[-5:]}")
    except Exception as e:
        print(f"  Error reading: {e}")

# 2. Check Kinh Doanh files
print("\n=== KINH DOANH FILES IN DOWNLOADS ===")
kd_files = [
    os.path.join(downloads, '_NTB - BÁO CÁO TUẦN KINH DOANH (Looker).xlsx'),
    os.path.join(downloads, '[Vùng] TỔNG QUAN KHÁCH HÀNG_BÁO CÁO (view Ngày)_Bảng tổng hợp (13).csv'),
]
for f in kd_files:
    if os.path.exists(f):
        mtime = datetime.fromtimestamp(os.path.getmtime(f)).strftime('%Y-%m-%d %H:%M:%S')
        print(f"File: {os.path.basename(f)} | Modified: {mtime} | Size: {os.path.getsize(f):,} bytes")
        if f.endswith('.xlsx'):
            try:
                xl = pd.ExcelFile(f)
                print("  Excel sheets:", xl.sheet_names)
            except Exception as e:
                print("  Error reading excel:", e)
        else:
            try:
                df = pd.read_csv(f, low_memory=False, nrows=5)
                print("  CSV cols:", list(df.columns))
            except Exception as e:
                print("  Error reading csv:", e)
