import pandas as pd
import openpyxl
import unicodedata
import sys

sys.stdout.reconfigure(encoding='utf-8')
INPUT_EXCEL = r"c:\Users\lap4all\Desktop\New folder\downloaded_user_sheet.xlsx"

df_cocau = pd.read_excel(INPUT_EXCEL, sheet_name='cocau')
wb = openpyxl.load_workbook(INPUT_EXCEL, data_only=True)

def normalize_name(name):
    if pd.isna(name):
        return ""
    return unicodedata.normalize('NFC', str(name).strip()).upper()

cocau_ams = set(df_cocau['Am'].dropna().unique())
cocau_ams_norm = {normalize_name(name): name for name in cocau_ams}

print("=== Unique AM names in 'cocau' sheet ===")
for name in sorted(cocau_ams):
    print(f" - '{name}' (Normalized: '{normalize_name(name)}')")

# Let's inspect 'sản lượng' sheet AM names
ws_sl = wb['sản lượng']
sl_ams = []
for r in range(3, 23):
    val = ws_sl.cell(row=r, column=1).value
    if val:
        sl_ams.append(val)

print("\n=== AM names in 'sản lượng' sheet (Column A) ===")
for name in sl_ams:
    norm = normalize_name(name)
    matched = norm in cocau_ams_norm
    status = "MATCHED" if matched else "❌ MISMATCHED"
    print(f" - '{name}' (Normalized: '{norm}') -> {status}")
    if not matched:
        # Check closest match
        closest = []
        for c_norm in cocau_ams_norm:
            if c_norm.replace(' ', '')[:5] == norm.replace(' ', '')[:5]:
                closest.append(cocau_ams_norm[c_norm])
        print(f"   Closest in cocau: {closest}")
