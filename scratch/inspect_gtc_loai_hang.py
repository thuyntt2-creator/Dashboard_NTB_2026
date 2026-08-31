import pandas as pd
import sys
sys.stdout.reconfigure(encoding='utf-8')
excel_path = r"c:\Users\lap4all\Desktop\New folder\downloaded_user_sheet.xlsx"
df = pd.read_excel(excel_path, sheet_name='dataGTC gốc full hàng')
print("Loại Hàng unique values:")
print(df['Loại Hàng'].unique())
