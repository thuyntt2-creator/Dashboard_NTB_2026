import os
import sys
import pandas as pd
import shutil

sys.stdout.reconfigure(encoding='utf-8')

downloads = r'C:\Users\lap4all\Downloads'
f1 = os.path.join(downloads, '[OE-IA] BÁO CÁO TRUY THU_Danh sách truy thu_Bảng.csv')
f2 = os.path.join(downloads, '[OE-IA] BÁO CÁO TRUY THU_Danh sách truy thu_Bảng (1).csv')
f_sheet = 'sheet_truythu.csv'

# Backup existing sheet_truythu.csv
if os.path.exists(f_sheet):
    shutil.copy(f_sheet, 'sheet_truythu_backup.csv')

dfs = []
for p in [f1, f_sheet, f2]:
    if os.path.exists(p):
        d = pd.read_csv(p, low_memory=False)
        print(f"Reading {p}: {len(d):,} rows")
        dfs.append(d)

combined = pd.concat(dfs, ignore_index=True)
# Deduplicate
combined = combined.drop_duplicates(subset=['Mã ticket', 'Mã truy thu', 'Nhân viên', 'Ngày kết luận truy thu'])
print(f"Combined deduplicated rows: {len(combined):,}")

combined.to_csv('sheet_truythu.csv', index=False, encoding='utf-8')
print("Saved combined sheet_truythu.csv!")
