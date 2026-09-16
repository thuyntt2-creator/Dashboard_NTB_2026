import sys
import pandas as pd

sys.stdout.reconfigure(encoding='utf-8')

# Check W37
excel_file = 'BaoCao_Tuan_NTB_W37_2026.xlsx'
xl = pd.ExcelFile(excel_file)
print("W37 Sheet names:", xl.sheet_names[:10])

for sname in xl.sheet_names:
    if any(k in sname.lower() for k in ['opr', 'co cau', 'danh mục', 'bc']):
        df = xl.parse(sname)
        # search for Quang Tin
        m = df.astype(str).apply(lambda row: row.str.contains('Quảng Tín|Quảng Sơn|Đức Trọng', case=False).any(), axis=1)
        if m.any():
            print(f"\nFound in sheet '{sname}':")
            print(df[m].head(5).to_string())
            break
