import pandas as pd
import sys

sys.stdout.reconfigure(encoding='utf-8')
INPUT_EXCEL = r"c:\Users\lap4all\Desktop\New folder\downloaded_user_sheet.xlsx"

for sheet in ['dataGTC gốc full hàng', 'dataGTC gốc TTS', 'dataLTC full hàng', 'dataLTC TTS', 'dataODRfull hàng ', 'dataODR TTS']:
    df = pd.read_excel(INPUT_EXCEL, sheet_name=sheet)
    print(f"\n=== Sheet: {sheet} ===")
    print(f"Columns: {list(df.columns)}")
    
    # Check rows where any column contains 'grand' or 'total' (case-insensitive)
    for col in df.columns:
        matching_rows = df[df[col].astype(str).str.lower().str.contains('total|grand', na=False)]
        if not matching_rows.empty:
            print(f"Found summary rows in column '{col}':")
            print(matching_rows[[col, 'Volume' if 'Volume' in df.columns else 'GTC' if 'GTC' in df.columns else df.columns[1]]].head(5))
            
    # Check rows with empty or blank second column (Chi tiết or equivalent)
    if 'Chi tiết' in df.columns:
        blanks = df[df['Chi tiết'].isna() | (df['Chi tiết'].astype(str).str.strip() == '')]
        print(f"Blank 'Chi tiết' rows count: {len(blanks)}")
        if not blanks.empty:
            print(blanks.head(2))
    elif 'Quản lý' in df.columns:
        blanks = df[df['Quản lý'].isna() | (df['Quản lý'].astype(str).str.strip() == '')]
        print(f"Blank 'Quản lý' rows count: {len(blanks)}")
        if not blanks.empty:
            print(blanks.head(2))
