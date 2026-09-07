import pandas as pd

file_path = r"c:\Users\lap4all\Desktop\New folder\downloaded_user_sheet.xlsx"
df_cocau = pd.read_excel(file_path, sheet_name='cocau')

df_nga = df_cocau[df_cocau['Am'].str.contains('Nga', na=False, case=False)]

with open(r"c:\Users\lap4all\Desktop\New folder\nga_cocau_rows.txt", "w", encoding="utf-8") as f:
    f.write(df_nga.to_string())

print("Nga cocau rows written to nga_cocau_rows.txt")
