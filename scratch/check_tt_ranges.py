import os
import sys
import pandas as pd

sys.stdout.reconfigure(encoding='utf-8')

downloads = r'C:\Users\lap4all\Downloads'

for fname in ['[OE-IA] BÁO CÁO TRUY THU_Danh sách truy thu_Bảng.csv', '[OE-IA] BÁO CÁO TRUY THU_Danh sách truy thu_Bảng (1).csv', 'sheet_truythu.csv']:
    fpath = os.path.join(downloads, fname) if fname.startswith('[') else fname
    if os.path.exists(fpath):
        df = pd.read_csv(fpath, low_memory=False)
        print(f"File {fname}: {len(df)} rows")
        if 'Ngày kết luận truy thu' in df.columns:
            dates = df['Ngày kết luận truy thu'].dropna().unique()
            print(f"  Dates: first 3={dates[:3]}, last 5={dates[-5:]}")
