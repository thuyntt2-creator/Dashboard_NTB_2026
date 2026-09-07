import pandas as pd
import openpyxl
import unicodedata
import sys

sys.stdout.reconfigure(encoding='utf-8')
INPUT_EXCEL = r"c:\Users\lap4all\Desktop\New folder\downloaded_user_sheet.xlsx"

df_cocau = pd.read_excel(INPUT_EXCEL, sheet_name='cocau')
wb = openpyxl.load_workbook(INPUT_EXCEL, data_only=True)

def normalize_name(name):
    if pd.isna(name): return ""
    return unicodedata.normalize('NFC', str(name).strip()).upper()

cocau_ams = set(df_cocau['Am'].dropna().unique())
cocau_ams_norm = {normalize_name(name): name for name in cocau_ams}

for sheet_name in ['gtcnew', 'gtc + tồn', 'ca2', 'LTC']:
    ws = wb[sheet_name]
    sheet_ams = []
    # In these sheets, row ranges might be different. Let's find AM names in column A
    for r in range(1, 100):
        val = ws.cell(row=r, column=1).value
        # If it's a string and looks like an AM name (exclude header or empty)
        if val and isinstance(val, str) and not any(keyword in val.lower() for keyword in ['tên', 'am', 'nhân viên', 'bình quân', 'tổng cộng', 'trung bình', 'kpi']):
            # Exclude very short names or headers
            if len(val.strip()) > 3:
                sheet_ams.append((r, val))
                
    print(f"\n=== Sheet: {sheet_name} ===")
    for row, name in sheet_ams:
        norm = normalize_name(name)
        matched = norm in cocau_ams_norm
        status = "MATCHED" if matched else "❌ MISMATCHED"
        print(f"Row {row}: '{name}' -> {status}")
        if not matched:
            # Check closest match
            closest = []
            for c_norm in cocau_ams_norm:
                if c_norm.replace(' ', '')[:5] == norm.replace(' ', '')[:5]:
                    closest.append(cocau_ams_norm[c_norm])
            print(f"   Closest in cocau: {closest}")
