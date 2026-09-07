import pandas as pd
import unicodedata
import sys

sys.stdout.reconfigure(encoding='utf-8')

INPUT_EXCEL = r"c:\Users\lap4all\Desktop\New folder\downloaded_user_sheet.xlsx"

print("Reading raw data sheets and 'cocau' sheet...")
df_gtc_full = pd.read_excel(INPUT_EXCEL, sheet_name='dataGTC gốc full hàng')
df_gtc_tts = pd.read_excel(INPUT_EXCEL, sheet_name='dataGTC gốc TTS')
df_ltc_full = pd.read_excel(INPUT_EXCEL, sheet_name='dataLTC full hàng')
df_ltc_tts = pd.read_excel(INPUT_EXCEL, sheet_name='dataLTC TTS')
df_odr_full = pd.read_excel(INPUT_EXCEL, sheet_name='dataODRfull hàng ')
df_odr_tts = pd.read_excel(INPUT_EXCEL, sheet_name='dataODR TTS')
df_cocau = pd.read_excel(INPUT_EXCEL, sheet_name='cocau')

def normalize_name(name):
    if pd.isna(name):
        return ""
    return unicodedata.normalize('NFC', str(name).strip()).upper()

# Normalize cocau mappings
df_cocau['BC_norm'] = df_cocau['BC'].apply(normalize_name)
bc_to_am = dict(zip(df_cocau['BC_norm'], df_cocau['Am']))
bc_to_tinh = dict(zip(df_cocau['BC_norm'], df_cocau['Tỉnh']))

# Let's inspect GTC full sheet
print("\n=== Inspecting 'dataGTC gốc full hàng' ===")
unique_bcs = df_gtc_full['Chi tiết'].dropna().unique()
missing_bcs = []
for bc in unique_bcs:
    bc_norm = normalize_name(bc)
    if bc_norm not in bc_to_am:
        # Calculate volume
        vol = df_gtc_full[df_gtc_full['Chi tiết'] == bc]['Volume'].sum()
        missing_bcs.append((bc, vol))

missing_bcs = sorted(missing_bcs, key=lambda x: x[1], reverse=True)
print(f"Total unique post offices in raw GTC: {len(unique_bcs)}")
print(f"Post offices missing from 'cocau' mapping sheet ({len(missing_bcs)}):")
for bc, vol in missing_bcs[:30]:
    print(f" - '{bc}': volume = {vol:,.0f}")

# Let's check LTC full sheet
print("\n=== Inspecting 'dataLTC full hàng' ===")
unique_bcs_ltc = df_ltc_full['Chi tiết'].dropna().unique()
missing_bcs_ltc = []
for bc in unique_bcs_ltc:
    if bc == 'Grand Total': continue
    bc_norm = normalize_name(bc)
    if bc_norm not in bc_to_am:
        vol = df_ltc_full[df_ltc_full['Chi tiết'] == bc]['Volume'].sum()
        missing_bcs_ltc.append((bc, vol))

missing_bcs_ltc = sorted(missing_bcs_ltc, key=lambda x: x[1], reverse=True)
for bc, vol in missing_bcs_ltc[:20]:
    print(f" - '{bc}': volume = {vol:,.0f}")
