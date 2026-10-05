import os
import sys
import pandas as pd

sys.stdout.reconfigure(encoding='utf-8')

downloads = r'C:\Users\lap4all\Downloads'

# 1. Inspect _NTB - BÁO CÁO TUẦN KINH DOANH (Looker).xlsx
xl_path = os.path.join(downloads, '_NTB - BÁO CÁO TUẦN KINH DOANH (Looker).xlsx')
print(f"=== Inspecting {xl_path} ===")
xl = pd.ExcelFile(xl_path)
print("Sheets:", xl.sheet_names)
for s in ['tong_quan', 'f30', 'KH A']:
    if s in xl.sheet_names:
        df = pd.read_excel(xl_path, sheet_name=s)
        print(f"Sheet '{s}': {len(df)} rows, columns: {list(df.columns)}")
        if 'Ngay' in df.columns:
            print(f"  Max date in 'Ngay': {df['Ngay'].dropna().unique()[-5:]}")
        elif any('ngày' in c.lower() for c in df.columns):
            c_date = [c for c in df.columns if 'ngày' in c.lower()][0]
            print(f"  Col '{c_date}': {df[c_date].dropna().unique()[-5:]}")

# 2. Inspect Truy Thu files
print("\n=== Inspecting Truy Thu files ===")
for fname in ['[OE-IA] BÁO CÁO TRUY THU_Danh sách truy thu_Bảng (1).csv', '[OE-IA] BÁO CÁO TRUY THU_Danh sách truy thu_Bảng (2).csv']:
    fpath = os.path.join(downloads, fname)
    if os.path.exists(fpath):
        df = pd.read_csv(fpath, low_memory=False)
        print(f"\nFile: {fname} | Rows: {len(df)} | Cols: {list(df.columns)}")
        col_date = [c for c in df.columns if 'ngày' in c.lower()]
        for c in col_date:
            print(f"  Col '{c}' range: min={df[c].dropna().min()} max={df[c].dropna().max()}")
