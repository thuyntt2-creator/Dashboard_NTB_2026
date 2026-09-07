import sys
import pandas as pd
import openpyxl

sys.stdout.reconfigure(encoding='utf-8')

print('=== 1. sheet_BACKLOG_KTC.csv ===')
try:
    df_backlog = pd.read_csv('sheet_BACKLOG_KTC.csv', nrows=30, header=None)
    for idx, row in df_backlog.iterrows():
        non_empty = [str(x) for x in row.values if pd.notna(x) and str(x).strip() != '']
        if non_empty:
            print(f"Row {idx}:", non_empty[:12])
except Exception as e:
    print("Error reading sheet_BACKLOG_KTC.csv:", e)

print('\n=== 2. sheet_raw.csv ===')
try:
    df_raw = pd.read_csv('sheet_raw.csv', nrows=30, header=None)
    for idx, row in df_raw.iterrows():
        non_empty = [str(x) for x in row.values if pd.notna(x) and str(x).strip() != '']
        if non_empty:
            print(f"Row {idx}:", non_empty[:12])
except Exception as e:
    print("Error reading sheet_raw.csv:", e)

print('\n=== 3. Sheet 14_NTB_Fill_Rate_Report ===')
try:
    wb = openpyxl.load_workbook('BaoCao_Tuan_NTB_W36_2026.xlsx', data_only=True)
    ws = wb['14_NTB_Fill_Rate_Report']
    for r in range(1, 35):
        row_vals = [ws.cell(r, c).value for c in range(1, 15)]
        non_empty = [str(v) for v in row_vals if v is not None]
        if non_empty:
            print(f"R{r}:", non_empty)
except Exception as e:
    print("Error reading 14_NTB_Fill_Rate_Report:", e)
