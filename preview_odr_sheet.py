import pandas as pd

file_path = r"c:\Users\lap4all\Desktop\New folder\downloaded_user_sheet.xlsx"
df_odr = pd.read_excel(file_path, sheet_name='ODR', header=None)

with open(r"c:\Users\lap4all\Desktop\New folder\odr_sheet_preview.txt", "w", encoding="utf-8") as f:
    f.write(df_odr.iloc[:25, :15].to_string())

print("ODR sheet preview written.")
