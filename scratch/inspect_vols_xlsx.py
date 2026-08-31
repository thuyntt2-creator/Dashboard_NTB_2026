import openpyxl
import pandas as pd
import sys

sys.stdout.reconfigure(encoding='utf-8')

excel_file = "vols_tao_don.xlsx"
wb = openpyxl.load_workbook(excel_file, read_only=True)
print("Sheet names in vols_tao_don.xlsx:", wb.sheetnames)

# Read the first sheet
df = pd.read_excel(excel_file)
df.columns = [str(c).strip() for c in df.columns]
print("\nExcel columns:", df.columns.tolist())
print("Excel rows count:", len(df))
if 'Date' in df.columns:
    df['Date'] = pd.to_datetime(df['Date'])
    print("Min date in Excel:", df['Date'].min())
    print("Max date in Excel:", df['Date'].max())
    
    # Calculate D vs D-7 growth for the max date in Excel
    latest_dt = df['Date'].max()
    df_d = df[df['Date'] == latest_dt]
    df_d7 = df[df['Date'] == (latest_dt - pd.Timedelta(days=7))]
    
    # Check without 'BC Cũ/Không thuộc ĐCL' filter
    vol_d = df_d.groupby('Bưu cục')['Volume'].sum()
    vol_d7 = df_d7.groupby('Bưu cục')['Volume'].sum()
    diff = vol_d - vol_d7
    print(f"\nCalculated growth (Excel max date {latest_dt.strftime('%Y-%m-%d')}):")
    print(diff.sort_values(ascending=False).head(10))
