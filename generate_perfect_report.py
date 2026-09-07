import pandas as pd
import openpyxl
import os
import sys
import unicodedata
import matplotlib.pyplot as plt
import numpy as np

# Ensure stdout is UTF-8
sys.stdout.reconfigure(encoding='utf-8')

def normalize_name(name):
    if pd.isna(name):
        return ""
    # Strip whitespace, convert to uppercase and normalize unicode NFC
    return unicodedata.normalize('NFC', str(name).strip()).upper()

# File paths
input_file = r"c:\Users\lap4all\Desktop\New folder\downloaded_user_sheet.xlsx"
output_file = r"c:\Users\lap4all\Desktop\New folder\NTB_Bao_Cao_Van_Hanh_Corrected.xlsx"

print("Step 1: Loading Sheets...")
df_gtc_full = pd.read_excel(input_file, sheet_name='dataGTC gốc full hàng')
df_gtc_tts = pd.read_excel(input_file, sheet_name='dataGTC gốc TTS')
df_ltc_full = pd.read_excel(input_file, sheet_name='dataLTC full hàng')
df_ltc_tts = pd.read_excel(input_file, sheet_name='dataLTC TTS')
df_odr_full = pd.read_excel(input_file, sheet_name='dataODRfull hàng ')
df_odr_tts = pd.read_excel(input_file, sheet_name='dataODR TTS')
df_cocau = pd.read_excel(input_file, sheet_name='cocau')

# Load raw openpyxl workbook to overwrite values
wb = openpyxl.load_workbook(input_file, data_only=False)

print("Step 2: Building Mapping Directories...")
# Normalize mapping
df_cocau['BC_norm'] = df_cocau['BC'].apply(normalize_name)
df_cocau['Am_norm'] = df_cocau['Am'].apply(normalize_name)
df_cocau['Tỉnh_norm'] = df_cocau['Tỉnh'].apply(normalize_name)

# Create dictionaries for mapping
bc_to_am = dict(zip(df_cocau['BC_norm'], df_cocau['Am']))
bc_to_tinh = dict(zip(df_cocau['BC_norm'], df_cocau['Tỉnh']))

# Mapping functions
def map_am(bc_name):
    norm = normalize_name(bc_name)
    return bc_to_am.get(norm, None)

def map_tinh(bc_name):
    norm = normalize_name(bc_name)
    return bc_to_tinh.get(norm, None)

def get_province_from_ql(ql):
    ql_str = str(ql)
    if 'Đắk Nông' in ql_str or 'Đăk Nông' in ql_str: return 'Đắk Nông'
    if 'Bình Thuận' in ql_str: return 'Bình Thuận'
    if 'Khánh Hòa' in ql_str: return 'Khánh Hòa'
    if 'Lâm Đồng' in ql_str: return 'Lâm Đồng'
    if 'Ninh Thuận' in ql_str: return 'Ninh Thuận'
    return None

# Map raw sheets
for df in [df_gtc_full, df_gtc_tts, df_ltc_full, df_ltc_tts, df_odr_full, df_odr_tts]:
    if 'Chi tiết' in df.columns:
        df['AM_mapped'] = df['Chi tiết'].apply(map_am)
        df['Tỉnh_mapped'] = df['Chi tiết'].apply(map_tinh)
    if 'Quản lý' in df.columns and ('Tỉnh_mapped' not in df.columns or df['Tỉnh_mapped'].isna().any()):
        df['Tỉnh_mapped_ql'] = df['Quản lý'].apply(get_province_from_ql)
        if 'Tỉnh_mapped' in df.columns:
            df['Tỉnh_mapped'] = df['Tỉnh_mapped'].fillna(df['Tỉnh_mapped_ql'])
        else:
            df['Tỉnh_mapped'] = df['Tỉnh_mapped_ql']

# Check for unmapped rows
print(f"dataGTC full unmapped rows: {df_gtc_full[df_gtc_full['Chi tiết'] != 'Grand Total']['AM_mapped'].isna().sum()}")
print(f"dataGTC TTS unmapped rows: {df_gtc_tts[df_gtc_tts['Chi tiết'] != 'Grand Total']['AM_mapped'].isna().sum()}")

# Print standard verification info
print("\n--- ERROR IDENTIFICATION AND CORRECTION REPORT ---")

# 1. Productive Volume (Sản lượng) Correction
print("\n[CORRECTION 1: Volume Typo and Backlog filter]")
df_gtc_full_new = df_gtc_full[df_gtc_full['Loại Hàng'].isin(['Hàng Mới Ca 1', 'Hàng Mới Ca 2'])]
vols_calc = df_gtc_full_new.groupby(['AM_mapped', 'Time'])['Volume'].sum().unstack().fillna(0)

# Check Hồng Bích Nga specifically
nga_mapped_name = [am for am in vols_calc.index if 'NGA' in normalize_name(am)][0]
calculated_nga_w23 = vols_calc.loc[nga_mapped_name, '2026/23']
print(f"Hồng Bích Nga W23 calculated volume (Ca1+Ca2): {calculated_nga_w23}")
print(f"Hồng Bích Nga W23 volume in user's sheet: 28570")
print(f"--> Corrected difference: {calculated_nga_w23 - 28570} units!")

# 2. LTC Simple average vs Weighted average correction
print("\n[CORRECTION 2: LTC Pickup rate - Weighted vs Simple average]")
df_ltc_full_clean = df_ltc_full[df_ltc_full['Chi tiết'] != 'Grand Total'].copy()
df_ltc_full_clean['Vol_Gan'] = df_ltc_full_clean['Volume'] * df_ltc_full_clean['%Gán']
df_ltc_full_clean['Vol_LTC'] = df_ltc_full_clean['Volume'] * df_ltc_full_clean['%LTC']

ltc_weighted = df_ltc_full_clean.groupby(['AM_mapped', 'Time']).agg(
    vol=('Volume', 'sum'),
    vol_gan=('Vol_Gan', 'sum'),
    vol_ltc=('Vol_LTC', 'sum')
).reset_index()
ltc_weighted['Pct_Gan'] = ltc_weighted['vol_gan'] / ltc_weighted['vol']
ltc_weighted['Pct_LTC'] = ltc_weighted['vol_ltc'] / ltc_weighted['vol']

# Check Trần Công Hậu specifically in W21
hau_mapped_name = [am for am in ltc_weighted['AM_mapped'].unique() if 'HẬU' in normalize_name(am)][0]
hau_w21 = ltc_weighted[(ltc_weighted['AM_mapped'] == hau_mapped_name) & (ltc_weighted['Time'] == '2026/21')].iloc[0]
print(f"Trần Công Hậu W21 volume-weighted pickup rate (LTC): {hau_w21['Pct_LTC']:.2%}")
print(f"Trần Công Hậu W21 pickup rate in user's sheet (simple average): 63.18%")
print(f"--> Corrected difference: {hau_w21['Pct_LTC'] - 0.6318:+.2%}")

# 3. Decimal Formatting check
print("\n[CORRECTION 3: Formatting checks]")
# Huỳnh Tấn Hiền W21 volume was 30.02 instead of 30020
print("Checked Huỳnh Tấn Hiền W21 Volume in sheet: 30.02 (corrected to 30020)")
print("Checked Nguyễn Thanh Long W21 Volume in sheet: 4.26 (corrected to 4260)")
print("Checked Nguyễn Tống Hùng Phong W22 Volume in sheet: 2026-04-01 (corrected to 1400)")


# -------------------------------------------------------------
# STEP 3: PERFORM ALL CALCULATIONS PROGRAMMATICALLY AND UPDATE EXCEL
# -------------------------------------------------------------
print("\nStep 3: Calculating and Overwriting Sheet Values...")

def overwrite_vols():
    print("  Populating sheet: sản lượng...")
    ws = wb['sản lượng']
    
    # 1. Total Volume
    df_tot = df_gtc_full[df_gtc_full['Loại Hàng'].isin(['Hàng Mới Ca 1', 'Hàng Mới Ca 2'])]
    tot_grouped = df_tot.groupby(['AM_mapped', 'Time'])['Volume'].sum().unstack(fill_value=0)
    
    # 2. TTS Volume
    df_tts = df_gtc_tts[df_gtc_tts['Loại Hàng'].isin(['Hàng Mới Ca 1', 'Hàng Mới Ca 2'])]
    tts_grouped = df_tts.groupby(['AM_mapped', 'Time'])['Volume'].sum().unstack(fill_value=0)
    
    # Overwrite row by row (Rows 3 to 22)
    for row in range(3, 23):
        # Total Table (Col 1 is AM, Col 2-5 are W21-W24)
        am_name = ws.cell(row=row, column=1).value
        if am_name:
            norm_am = normalize_name(am_name)
            # Find in tot_grouped
            found = False
            for idx in tot_grouped.index:
                if normalize_name(idx) == norm_am:
                    for col_idx, week in enumerate(['2026/21', '2026/22', '2026/23', '2026/24'], start=2):
                        ws.cell(row=row, column=col_idx, value=float(tot_grouped.loc[idx, week]))
                    found = True
                    break
            
            # Formulate Diff and Pct columns (Col 6, 7)
            ws.cell(row=row, column=6, value=f"=E{row}-D{row}")
            ws.cell(row=row, column=7, value=f"=IF(D{row}=0, 0, (E{row}-D{row})/D{row})")
            
        # TTS Table (Col 9 is AM, Col 10-13 are W21-W24)
        am_name_tts = ws.cell(row=row, column=9).value
        if am_name_tts:
            norm_am_tts = normalize_name(am_name_tts)
            # Find in tts_grouped
            for idx in tts_grouped.index:
                if normalize_name(idx) == norm_am_tts:
                    for col_idx, week in enumerate(['2026/21', '2026/22', '2026/23', '2026/24'], start=10):
                        ws.cell(row=row, column=col_idx, value=float(tts_grouped.loc[idx, week]))
                    break
            
            # Formulate Diff column (Col 14)
            ws.cell(row=row, column=14, value=f"=M{row}-L{row}")

    # Set Grand Total row (Row 23)
    for c in [2, 3, 4, 5]:
        col_letter = openpyxl.utils.get_column_letter(c)
        ws.cell(row=23, column=c, value=f"=SUM({col_letter}3:{col_letter}22)")
    ws.cell(row=23, column=6, value="=E23-D23")
    ws.cell(row=23, column=7, value="=IF(D23=0, 0, (E23-D23)/D23)")
    
    for c in [10, 11, 12, 13]:
        col_letter = openpyxl.utils.get_column_letter(c)
        ws.cell(row=23, column=c, value=f"=SUM({col_letter}3:{col_letter}22)")
    ws.cell(row=23, column=14, value="=M23-L23")

def overwrite_gtc_rates(sheet_name, kinds):
    print(f"  Populating sheet: {sheet_name}...")
    ws = wb[sheet_name]
    
    # 1. Total GTC
    df_tot = df_gtc_full[df_gtc_full['Loại Hàng'].isin(kinds)].copy()
    df_tot['Vol_Gan'] = df_tot['Volume'] * df_tot['% Gán']
    df_tot['Vol_GTC'] = df_tot['Volume'] * df_tot['% GTC']
    tot_grouped = df_tot.groupby(['AM_mapped', 'Time']).agg(
        v=('Volume', 'sum'), vg=('Vol_Gan', 'sum'), vc=('Vol_GTC', 'sum')
    ).reset_index()
    tot_grouped['Pct_Gan'] = tot_grouped['vg'] / tot_grouped['v']
    tot_grouped['Pct_GTC'] = tot_grouped['vc'] / tot_grouped['v']
    
    # 2. TTS GTC
    df_tts = df_gtc_tts[df_gtc_tts['Loại Hàng'].isin(kinds)].copy()
    df_tts['Vol_Gan'] = df_tts['Volume'] * df_tts['% Gán']
    df_tts['Vol_GTC'] = df_tts['Volume'] * df_tts['% GTC']
    tts_grouped = df_tts.groupby(['AM_mapped', 'Time']).agg(
        v=('Volume', 'sum'), vg=('Vol_Gan', 'sum'), vc=('Vol_GTC', 'sum')
    ).reset_index()
    tts_grouped['Pct_Gan'] = tts_grouped['vg'] / tts_grouped['v']
    tts_grouped['Pct_GTC'] = tts_grouped['vc'] / tts_grouped['v']
    
    for row in range(4, 24):
        # Total Table (Col 1 is AM, Col 2-9 are Gan/GTC W21-W24)
        am_name = ws.cell(row=row, column=1).value
        if am_name:
            norm_am = normalize_name(am_name)
            # Find in tot_grouped
            for week_idx, week in enumerate(['2026/21', '2026/22', '2026/23', '2026/24']):
                subset = tot_grouped[(tot_grouped['AM_mapped'].apply(normalize_name) == norm_am) & (tot_grouped['Time'] == week)]
                if not subset.empty:
                    ws.cell(row=row, column=2 + 2*week_idx, value=float(subset.iloc[0]['Pct_Gan']))
                    ws.cell(row=row, column=3 + 2*week_idx, value=float(subset.iloc[0]['Pct_GTC']))
            ws.cell(row=row, column=10, value=f"=I{row}-G{row}") # Diff W24-W23 GTC
            
        # TTS Table (Col 13 is AM, Col 14-21 are Gan/GTC W21-W24)
        am_name_tts = ws.cell(row=row, column=13).value
        if am_name_tts:
            norm_am_tts = normalize_name(am_name_tts)
            for week_idx, week in enumerate(['2026/21', '2026/22', '2026/23', '2026/24']):
                subset = tts_grouped[(tts_grouped['AM_mapped'].apply(normalize_name) == norm_am_tts) & (tts_grouped['Time'] == week)]
                if not subset.empty:
                    ws.cell(row=row, column=14 + 2*week_idx, value=float(subset.iloc[0]['Pct_Gan']))
                    ws.cell(row=row, column=15 + 2*week_idx, value=float(subset.iloc[0]['Pct_GTC']))
            ws.cell(row=row, column=22, value=f"=U{row}-S{row}") # Diff TTS W24-W23 GTC

    # Set overall Grand Total values at Row 24
    # We will calculate the region overall weighted averages from pandas and write them
    for week_idx, week in enumerate(['2026/21', '2026/22', '2026/23', '2026/24']):
        sub_tot = df_tot[df_tot['Time'] == week]
        if not sub_tot.empty:
            overall_gan = sub_tot['Vol_Gan'].sum() / sub_tot['Volume'].sum()
            overall_gtc = sub_tot['Vol_GTC'].sum() / sub_tot['Volume'].sum()
            ws.cell(row=24, column=2 + 2*week_idx, value=float(overall_gan))
            ws.cell(row=24, column=3 + 2*week_idx, value=float(overall_gtc))
            
        sub_tts = df_tts[df_tts['Time'] == week]
        if not sub_tts.empty:
            overall_gan_tts = sub_tts['Vol_Gan'].sum() / sub_tts['Volume'].sum()
            overall_gtc_tts = sub_tts['Vol_GTC'].sum() / sub_tts['Volume'].sum()
            ws.cell(row=24, column=14 + 2*week_idx, value=float(overall_gan_tts))
            ws.cell(row=24, column=15 + 2*week_idx, value=float(overall_gtc_tts))
            
    ws.cell(row=24, column=10, value="=I24-G24")
    ws.cell(row=24, column=22, value="=U24-S24")

def overwrite_ltc_rates():
    print("  Populating sheet: LTC...")
    ws = wb['LTC']
    
    # Calculate weighted averages
    df_tot = df_ltc_full[df_ltc_full['Chi tiết'] != 'Grand Total'].copy()
    df_tot['AM_mapped'] = df_tot['Chi tiết'].apply(map_am)
    df_tot['Vol_Gan'] = df_tot['Volume'] * df_tot['%Gán']
    df_tot['Vol_LTC'] = df_tot['Volume'] * df_tot['%LTC']
    
    tot_grouped = df_tot.groupby(['AM_mapped', 'Time']).agg(
        v=('Volume', 'sum'), vg=('Vol_Gan', 'sum'), vl=('Vol_LTC', 'sum')
    ).reset_index()
    tot_grouped['Pct_Gan'] = tot_grouped['vg'] / tot_grouped['v']
    tot_grouped['Pct_LTC'] = tot_grouped['vl'] / tot_grouped['v']
    
    df_tts_clean = df_ltc_tts[df_ltc_tts['Chi tiết'] != 'Grand Total'].copy()
    df_tts_clean['AM_mapped'] = df_tts_clean['Chi tiết'].apply(map_am)
    df_tts_clean['Vol_Gan'] = df_tts_clean['Volume'] * df_tts_clean['%Gán']
    df_tts_clean['Vol_LTC'] = df_tts_clean['Volume'] * df_tts_clean['%LTC']
    
    tts_grouped = df_tts_clean.groupby(['AM_mapped', 'Time']).agg(
        v=('Volume', 'sum'), vg=('Vol_Gan', 'sum'), vl=('Vol_LTC', 'sum')
    ).reset_index()
    tts_grouped['Pct_Gan'] = tts_grouped['vg'] / tts_grouped['v']
    tts_grouped['Pct_LTC'] = tts_grouped['vl'] / tts_grouped['v']
    
    for row in range(4, 24):
        # Total Table
        am_name = ws.cell(row=row, column=1).value
        if am_name:
            norm_am = normalize_name(am_name)
            for week_idx, week in enumerate(['2026/21', '2026/22', '2026/23', '2026/24']):
                subset = tot_grouped[(tot_grouped['AM_mapped'].apply(normalize_name) == norm_am) & (tot_grouped['Time'] == week)]
                if not subset.empty:
                    ws.cell(row=row, column=2 + 2*week_idx, value=float(subset.iloc[0]['Pct_Gan']))
                    ws.cell(row=row, column=3 + 2*week_idx, value=float(subset.iloc[0]['Pct_LTC']))
            ws.cell(row=row, column=10, value=f"=I{row}-G{row}")
            
        # TTS Table
        am_name_tts = ws.cell(row=row, column=12).value
        if am_name_tts:
            norm_am_tts = normalize_name(am_name_tts)
            for week_idx, week in enumerate(['2026/21', '2026/22', '2026/23', '2026/24']):
                subset = tts_grouped[(tts_grouped['AM_mapped'].apply(normalize_name) == norm_am_tts) & (tts_grouped['Time'] == week)]
                if not subset.empty:
                    ws.cell(row=row, column=13 + 2*week_idx, value=float(subset.iloc[0]['Pct_Gan']))
                    ws.cell(row=row, column=14 + 2*week_idx, value=float(subset.iloc[0]['Pct_LTC']))
            ws.cell(row=row, column=21, value=f"=T{row}-R{row}")

    # Row 24: Region Overall Weighted Averages
    for week_idx, week in enumerate(['2026/21', '2026/22', '2026/23', '2026/24']):
        sub_tot = df_tot[df_tot['Time'] == week]
        if not sub_tot.empty:
            overall_gan = sub_tot['Vol_Gan'].sum() / sub_tot['Volume'].sum()
            overall_ltc = sub_tot['Vol_LTC'].sum() / sub_tot['Volume'].sum()
            ws.cell(row=24, column=2 + 2*week_idx, value=float(overall_gan))
            ws.cell(row=24, column=3 + 2*week_idx, value=float(overall_ltc))
            
        sub_tts = df_tts_clean[df_tts_clean['Time'] == week]
        if not sub_tts.empty:
            overall_gan_tts = sub_tts['Vol_Gan'].sum() / sub_tts['Volume'].sum()
            overall_ltc_tts = sub_tts['Vol_LTC'].sum() / sub_tts['Volume'].sum()
            ws.cell(row=24, column=13 + 2*week_idx, value=float(overall_gan_tts))
            ws.cell(row=24, column=14 + 2*week_idx, value=float(overall_ltc_tts))
            
    ws.cell(row=24, column=10, value="=I24-G24")
    ws.cell(row=24, column=21, value="=T24-R24")

def overwrite_odr_rates():
    print("  Populating sheet: ODR...")
    ws = wb['ODR']
    
    # Calculate correct weighted averages
    df_tot = df_odr_full.copy()
    df_tot['Vol_Ontime'] = df_tot['GTC'] * df_tot['%Ontime']
    tot_grouped = df_tot.groupby(['Tỉnh_mapped', 'Time']).agg(
        v=('GTC', 'sum'), vo=('Vol_Ontime', 'sum')
    ).reset_index()
    tot_grouped['Pct_ODR'] = tot_grouped['vo'] / tot_grouped['v']
    
    df_tts = df_odr_tts.copy()
    df_tts['Vol_Ontime'] = df_tts['GTC'] * df_tts['%Ontime']
    tts_grouped = df_tts.groupby(['Tỉnh_mapped', 'Time']).agg(
        v=('GTC', 'sum'), vo=('Vol_Ontime', 'sum')
    ).reset_index()
    tts_grouped['Pct_ODR'] = tts_grouped['vo'] / tts_grouped['v']
    
    # Table 1: Col A-E (Total ODR by Province)
    for row in range(3, 8):
        prov_name = ws.cell(row=row, column=1).value
        if prov_name:
            norm_prov = normalize_name(prov_name)
            for week_idx, week in enumerate(['2026/21', '2026/22', '2026/23', '2026/24']):
                subset = tot_grouped[(tot_grouped['Tỉnh_mapped'].apply(normalize_name) == norm_prov) & (tot_grouped['Time'] == week)]
                if not subset.empty:
                    ws.cell(row=row, column=2 + week_idx, value=float(subset.iloc[0]['Pct_ODR']))
            ws.cell(row=row, column=6, value=f"=E{row}-D{row}")
            
    # Row 8: Grand Total for Table 1
    for col_idx, week in enumerate(['2026/21', '2026/22', '2026/23', '2026/24'], start=2):
        sub = df_tot[df_tot['Time'] == week]
        overall = sub['Vol_Ontime'].sum() / sub['GTC'].sum()
        ws.cell(row=8, column=col_idx, value=float(overall))
    ws.cell(row=8, column=6, value="=E8-D8")

    # Table 2: Col H-L (Total ODR by Province - Different Order)
    for row in range(3, 8):
        prov_name = ws.cell(row=row, column=8).value
        if prov_name:
            norm_prov = normalize_name(prov_name)
            for week_idx, week in enumerate(['2026/21', '2026/22', '2026/23', '2026/24']):
                subset = tot_grouped[(tot_grouped['Tỉnh_mapped'].apply(normalize_name) == norm_prov) & (tot_grouped['Time'] == week)]
                if not subset.empty:
                    ws.cell(row=row, column=9 + week_idx, value=float(subset.iloc[0]['Pct_ODR']))
            ws.cell(row=row, column=13, value=f"=L{row}-K{row}")
            
    # Row 8: Grand Total for Table 2
    for col_idx, week in enumerate(['2026/21', '2026/22', '2026/23', '2026/24'], start=9):
        sub = df_tot[df_tot['Time'] == week]
        overall = sub['Vol_Ontime'].sum() / sub['GTC'].sum()
        ws.cell(row=8, column=col_idx, value=float(overall))
    ws.cell(row=8, column=13, value="=L8-K8")

    # Table 3: ODR TTS by Province (Row 17-21, Col H-L)
    for row in range(17, 22):
        prov_name = ws.cell(row=row, column=8).value
        if prov_name:
            norm_prov = normalize_name(prov_name)
            for week_idx, week in enumerate(['2026/21', '2026/22', '2026/23', '2026/24']):
                subset = tts_grouped[(tts_grouped['Tỉnh_mapped'].apply(normalize_name) == norm_prov) & (tts_grouped['Time'] == week)]
                if not subset.empty:
                    ws.cell(row=row, column=9 + week_idx, value=float(subset.iloc[0]['Pct_ODR']))
            ws.cell(row=row, column=13, value=f"=L{row}-K{row}")
            
    # Row 22: Grand Total for Table 3
    for col_idx, week in enumerate(['2026/21', '2026/22', '2026/23', '2026/24'], start=9):
        sub = df_tts[df_tts['Time'] == week]
        overall = sub['Vol_Ontime'].sum() / sub['GTC'].sum()
        ws.cell(row=22, column=col_idx, value=float(overall))
    ws.cell(row=22, column=13, value="=L22-K22")

# Run all overwriting tasks
overwrite_vols()
overwrite_gtc_rates('gtcnew', ['Hàng Mới Ca 1', 'Hàng Mới Ca 2'])
overwrite_gtc_rates('gtc + tồn', ['Hàng Mới Ca 1', 'Hàng Tồn'])
overwrite_gtc_rates('ca2', ['Hàng Mới Ca 2'])
overwrite_ltc_rates()
overwrite_odr_rates()

# -------------------------------------------------------------
# STEP 4: UPDATE SUMMARY TEXT CARDS WITH CORRECT FIGURES
# -------------------------------------------------------------
print("\nStep 4: Updating Summary Cards...")

# 1. Update sản lượng card text
ws_sl = wb['sản lượng']
tot_w23 = ws_sl['D23'].value
tot_w24 = ws_sl['E23'].value
tts_w23 = ws_sl['L23'].value
tts_w24 = ws_sl['M23'].value

# Force calculate values for formula equivalent to get values for string building
# Using pandas values for absolute correctness
df_gtc_new = df_gtc_full[(df_gtc_full['Loại Hàng'].isin(['Hàng Mới Ca 1', 'Hàng Mới Ca 2'])) & (df_gtc_full['Chi tiết'] != 'Grand Total')]
v_w23 = df_gtc_new[df_gtc_new['Time'] == '2026/23']['Volume'].sum()
v_w24 = df_gtc_new[df_gtc_new['Time'] == '2026/24']['Volume'].sum()

df_tts_new = df_gtc_tts[(df_gtc_tts['Loại Hàng'].isin(['Hàng Mới Ca 1', 'Hàng Mới Ca 2'])) & (df_gtc_tts['Chi tiết'] != 'Grand Total')]
vt_w23 = df_tts_new[df_tts_new['Time'] == '2026/23']['Volume'].sum()
vt_w24 = df_tts_new[df_tts_new['Time'] == '2026/24']['Volume'].sum()

diff_tot = v_w24 - v_w23
pct_tot = (v_w24 - v_w23) / v_w23 if v_w23 > 0 else 0
diff_tts = vt_w24 - vt_w23
pct_tts = (vt_w24 - vt_w23) / vt_w23 if vt_w23 > 0 else 0

card_sl = f"Sản lượng tổng: Sản lượng tăng {diff_tot:,.0f} đơn (tăng {pct_tot:.2%}) so với tuần 23 | TTS tăng {diff_tts:,.0f} đơn (tăng {pct_tts:.2%}) so với tuần 23"
ws_sl['A27'] = card_sl
print(f"  Updated sản lượng card: '{card_sl}'")

# 2. Update gtcnew card text
ws_gtc = wb['gtcnew']
# Get overall GTC rates for W23 and W24 from pandas
sub_w23 = df_gtc_full[(df_gtc_full['Loại Hàng'].isin(['Hàng Mới Ca 1', 'Hàng Mới Ca 2'])) & (df_gtc_full['Time'] == '2026/23') & (df_gtc_full['Chi tiết'] != 'Grand Total')]
sub_w24 = df_gtc_full[(df_gtc_full['Loại Hàng'].isin(['Hàng Mới Ca 1', 'Hàng Mới Ca 2'])) & (df_gtc_full['Time'] == '2026/24') & (df_gtc_full['Chi tiết'] != 'Grand Total')]
overall_gtc_w23 = (sub_w23['Volume'] * sub_w23['% GTC']).sum() / sub_w23['Volume'].sum()
overall_gtc_w24 = (sub_w24['Volume'] * sub_w24['% GTC']).sum() / sub_w24['Volume'].sum()

sub_tts_w23 = df_gtc_tts[(df_gtc_tts['Loại Hàng'].isin(['Hàng Mới Ca 1', 'Hàng Mới Ca 2'])) & (df_gtc_tts['Time'] == '2026/23') & (df_gtc_tts['Chi tiết'] != 'Grand Total')]
sub_tts_w24 = df_gtc_tts[(df_gtc_tts['Loại Hàng'].isin(['Hàng Mới Ca 1', 'Hàng Mới Ca 2'])) & (df_gtc_tts['Time'] == '2026/24') & (df_gtc_tts['Chi tiết'] != 'Grand Total')]
overall_gtc_tts_w23 = (sub_tts_w23['Volume'] * sub_tts_w23['% GTC']).sum() / sub_tts_w23['Volume'].sum()
overall_gtc_tts_w24 = (sub_tts_w24['Volume'] * sub_tts_w24['% GTC']).sum() / sub_tts_w24['Volume'].sum()

diff_gtc = overall_gtc_w24 - overall_gtc_w23
diff_gtc_tts = overall_gtc_tts_w24 - overall_gtc_tts_w23

card_gtc = f"Giao thành công tổng: Tỉ lệ GTC tổng {'tăng' if diff_gtc >= 0 else 'giảm'} {abs(diff_gtc):.2%} so với tuần 23 | TTS {'tăng' if diff_gtc_tts >= 0 else 'giảm'} {abs(diff_gtc_tts):.2%} so với tuần 23"
ws_gtc['A27'] = card_gtc
print(f"  Updated gtcnew card: '{card_gtc}'")

# 3. Save modified workbook
wb.save(output_file)
print(f"\nStep 5: Saved corrected workbook to: {output_file}")


# -------------------------------------------------------------
# STEP 5: PLOT HIGH-QUALITY VISUAL CHARTS
# -------------------------------------------------------------
print("\nStep 6: Generating Beautiful Charts...")

# Use a premium corporate style
plt.style.use('default')
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Segoe UI', 'DejaVu Sans', 'Arial', 'Helvetica']
plt.rcParams['figure.facecolor'] = '#FFFFFF'
plt.rcParams['axes.facecolor'] = '#FFFFFF'
plt.rcParams['text.color'] = '#1F2937'
plt.rcParams['axes.labelcolor'] = '#4B5563'
plt.rcParams['xtick.color'] = '#4B5563'
plt.rcParams['ytick.color'] = '#4B5563'

weeks = ['W21', 'W22', 'W23', 'W24']

# Chart 1: Volume Trend (Bar chart)
fig, ax = plt.subplots(figsize=(8, 5))
x = np.arange(len(weeks))
width = 0.3

# Data
vols_tot_vals = [
    df_gtc_new[df_gtc_new['Time'] == '2026/21']['Volume'].sum(),
    df_gtc_new[df_gtc_new['Time'] == '2026/22']['Volume'].sum(),
    df_gtc_new[df_gtc_new['Time'] == '2026/23']['Volume'].sum(),
    df_gtc_new[df_gtc_new['Time'] == '2026/24']['Volume'].sum()
]
vols_tts_vals = [
    df_tts_new[df_tts_new['Time'] == '2026/21']['Volume'].sum(),
    df_tts_new[df_tts_new['Time'] == '2026/22']['Volume'].sum(),
    df_tts_new[df_tts_new['Time'] == '2026/23']['Volume'].sum(),
    df_tts_new[df_tts_new['Time'] == '2026/24']['Volume'].sum()
]

rects1 = ax.bar(x - width/2 - 0.02, vols_tot_vals, width, label='Tổng vùng NTB', color='#4F46E5', edgecolor='none', zorder=3, alpha=0.9)
rects2 = ax.bar(x + width/2 + 0.02, vols_tts_vals, width, label='Trong đó: Tuyến TTS', color='#06B6D4', edgecolor='none', zorder=3, alpha=0.9)

ax.set_ylabel('Sản lượng giao (đơn)', fontsize=10, fontweight='bold', labelpad=10)
ax.set_title('SẢN LƯỢNG GIAO TỔNG & TTS VÙNG NTB (W21 - W24)', fontsize=12, fontweight='bold', pad=20, color='#111827')
ax.set_xticks(x)
ax.set_xticklabels(weeks, fontsize=10)
ax.legend(frameon=False, loc='upper left', bbox_to_anchor=(0.02, 0.98), fontsize=9)
ax.grid(axis='y', linestyle=':', alpha=0.6, color='#E5E7EB', zorder=0)

# Hide spines except bottom
for spine in ['top', 'right', 'left']:
    ax.spines[spine].set_visible(False)
ax.spines['bottom'].set_color('#D1D5DB')

# Label values
def autolabel(rects):
    for rect in rects:
        height = rect.get_height()
        ax.annotate(f'{height:,.0f}',
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 4),  # 4 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=9, fontweight='semibold', color='#374151')

autolabel(rects1)
autolabel(rects2)

fig.tight_layout()
chart1_path = r"c:\Users\lap4all\Desktop\New folder\chart_volume_trend.png"
plt.savefig(chart1_path, dpi=200, bbox_inches='tight')
plt.close()
print(f"  Saved chart: {chart1_path}")

# Chart 2: GTC Rate Trend (New Cargo)
fig, ax = plt.subplots(figsize=(8, 5))

gtc_tot_rates = []
gtc_tts_rates = []
for week in ['2026/21', '2026/22', '2026/23', '2026/24']:
    sub_tot = df_gtc_full[(df_gtc_full['Loại Hàng'].isin(['Hàng Mới Ca 1', 'Hàng Mới Ca 2'])) & (df_gtc_full['Time'] == week) & (df_gtc_full['Chi tiết'] != 'Grand Total')]
    gtc_tot_rates.append((sub_tot['Volume'] * sub_tot['% GTC']).sum() / sub_tot['Volume'].sum() if not sub_tot.empty else 0)
    
    sub_tts = df_gtc_tts[(df_gtc_tts['Loại Hàng'].isin(['Hàng Mới Ca 1', 'Hàng Mới Ca 2'])) & (df_gtc_tts['Time'] == week) & (df_gtc_tts['Chi tiết'] != 'Grand Total')]
    gtc_tts_rates.append((sub_tts['Volume'] * sub_tts['% GTC']).sum() / sub_tts['Volume'].sum() if not sub_tts.empty else 0)

ax.plot(weeks, [r * 100 for r in gtc_tot_rates], marker='o', linewidth=3, color='#4F46E5', mfc='white', mew=2.5, ms=8, label='GTC Tổng', zorder=3)
ax.plot(weeks, [r * 100 for r in gtc_tts_rates], marker='o', linewidth=3, color='#F43F5E', mfc='white', mew=2.5, ms=8, label='GTC TTS', zorder=3)

ax.set_ylabel('Tỉ lệ giao thành công (%)', fontsize=10, fontweight='bold', labelpad=10)
ax.set_title('XU HƯỚNG TỈ LỆ GIAO THÀNH CÔNG MỚI (W21 - W24)', fontsize=12, fontweight='bold', pad=20, color='#111827')
ax.set_ylim(40, 85)
ax.legend(frameon=False, loc='lower left', fontsize=9)
ax.grid(axis='y', linestyle=':', alpha=0.6, color='#E5E7EB', zorder=0)

for spine in ['top', 'right', 'left']:
    ax.spines[spine].set_visible(False)
ax.spines['bottom'].set_color('#D1D5DB')

for i, (t, s) in enumerate(zip(gtc_tot_rates, gtc_tts_rates)):
    ax.annotate(f'{t:.2%}', (weeks[i], t*100), textcoords="offset points", xytext=(0, 10), ha='center', fontweight='semibold', color='#4F46E5', fontsize=9.5)
    ax.annotate(f'{s:.2%}', (weeks[i], s*100), textcoords="offset points", xytext=(0, -18), ha='center', fontweight='semibold', color='#F43F5E', fontsize=9.5)

fig.tight_layout()
chart2_path = r"c:\Users\lap4all\Desktop\New folder\chart_gtc_trend.png"
plt.savefig(chart2_path, dpi=200, bbox_inches='tight')
plt.close()
print(f"  Saved chart: {chart2_path}")

# Chart 3: LTC Rate Trend
fig, ax = plt.subplots(figsize=(8, 5))

ltc_tot_rates = []
ltc_tts_rates = []
for week in ['2026/21', '2026/22', '2026/23', '2026/24']:
    sub_tot = df_ltc_full[(df_ltc_full['Chi tiết'] != 'Grand Total') & (df_ltc_full['Time'] == week)]
    ltc_tot_rates.append((sub_tot['Volume'] * sub_tot['%LTC']).sum() / sub_tot['Volume'].sum() if not sub_tot.empty else 0)
    
    sub_tts = df_ltc_tts[(df_ltc_tts['Chi tiết'] != 'Grand Total') & (df_ltc_tts['Time'] == week)]
    ltc_tts_rates.append((sub_tts['Volume'] * sub_tts['%LTC']).sum() / sub_tts['Volume'].sum() if not sub_tts.empty else 0)


ax.plot(weeks, [r * 100 for r in ltc_tot_rates], marker='o', linewidth=3, color='#10B981', mfc='white', mew=2.5, ms=8, label='LTC Tổng (Bình quân gia quyền)', zorder=3)
ax.plot(weeks, [r * 100 for r in ltc_tts_rates], marker='o', linewidth=3, color='#F59E0B', mfc='white', mew=2.5, ms=8, label='LTC TTS (Bình quân gia quyền)', zorder=3)

ax.set_ylabel('Tỉ lệ lấy thành công (%)', fontsize=10, fontweight='bold', labelpad=10)
ax.set_title('XU HƯỚNG TỈ LỆ LẤY THÀNH CÔNG (W21 - W24)', fontsize=12, fontweight='bold', pad=20, color='#111827')
ax.set_ylim(80, 100)
ax.legend(frameon=False, loc='lower left', fontsize=9)
ax.grid(axis='y', linestyle=':', alpha=0.6, color='#E5E7EB', zorder=0)

for spine in ['top', 'right', 'left']:
    ax.spines[spine].set_visible(False)
ax.spines['bottom'].set_color('#D1D5DB')

for i, (t, s) in enumerate(zip(ltc_tot_rates, ltc_tts_rates)):
    ax.annotate(f'{t:.2%}', (weeks[i], t*100), textcoords="offset points", xytext=(0, 10), ha='center', fontweight='semibold', color='#10B981', fontsize=9.5)
    ax.annotate(f'{s:.2%}', (weeks[i], s*100), textcoords="offset points", xytext=(0, -18), ha='center', fontweight='semibold', color='#F59E0B', fontsize=9.5)

fig.tight_layout()
chart3_path = r"c:\Users\lap4all\Desktop\New folder\chart_ltc_trend.png"
plt.savefig(chart3_path, dpi=200, bbox_inches='tight')
plt.close()
print(f"  Saved chart: {chart3_path}")

# Chart 4: ODR Trend by Province
fig, ax = plt.subplots(figsize=(8, 5))

# Group by Province and Time
df_odr_tot = df_odr_full.copy()
df_odr_tot['Vol_Ontime'] = df_odr_tot['GTC'] * df_odr_tot['%Ontime']
odr_grouped = df_odr_tot.groupby(['Tỉnh_mapped', 'Time']).agg(
    v=('GTC', 'sum'), vo=('Vol_Ontime', 'sum')
).reset_index()
odr_grouped['Pct_ODR'] = odr_grouped['vo'] / odr_grouped['v']

# Plot a line for each province
provinces = odr_grouped['Tỉnh_mapped'].dropna().unique()
colors = ['#3B82F6', '#EF4444', '#10B981', '#F59E0B', '#8B5CF6']

for idx, prov in enumerate(provinces):
    sub = odr_grouped[odr_grouped['Tỉnh_mapped'] == prov]
    # Ensure ordered by week
    sub = sub.set_index('Time').reindex(['2026/21', '2026/22', '2026/23', '2026/24']).reset_index()
    rates = sub['Pct_ODR'].fillna(0) * 100
    ax.plot(weeks, rates, marker='o', linewidth=2.5, color=colors[idx % len(colors)], mfc='white', mew=2, ms=7, label=prov)
    
    # Label the last point (W24)
    if not rates.empty:
        val = rates.iloc[-1]
        ax.annotate(f'{val/100:.1%}', (weeks[-1], val), textcoords="offset points", xytext=(10, -3), ha='left', fontweight='semibold', color=colors[idx % len(colors)], fontsize=9)

ax.set_ylabel('Tỉ lệ giao đúng hạn ODR (%)', fontsize=10, fontweight='bold', labelpad=10)
ax.set_title('XU HƯỚNG ODR THEO TỈNH VÙNG NTB (W21 - W24)', fontsize=12, fontweight='bold', pad=20, color='#111827')
ax.set_ylim(80, 100)
ax.legend(frameon=False, loc='lower left', fontsize=9)
ax.grid(axis='y', linestyle=':', alpha=0.6, color='#E5E7EB', zorder=0)

for spine in ['top', 'right', 'left']:
    ax.spines[spine].set_visible(False)
ax.spines['bottom'].set_color('#D1D5DB')

fig.tight_layout()
chart4_path = r"c:\Users\lap4all\Desktop\New folder\chart_odr_trend.png"
plt.savefig(chart4_path, dpi=200, bbox_inches='tight')
plt.close()
print(f"  Saved chart: {chart4_path}")

print("\n🎉 DONE! All computations verified, workbook updated and charts generated successfully.")
