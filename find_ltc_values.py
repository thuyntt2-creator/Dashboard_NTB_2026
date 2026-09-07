import pandas as pd

file_path = r"c:\Users\lap4all\Desktop\New folder\downloaded_user_sheet.xlsx"
df_ltc_full = pd.read_excel(file_path, sheet_name='dataLTC full hàng')

# Find rows matching these values
row_match = df_ltc_full[(df_ltc_full['%Gán'] == 0.99) | (df_ltc_full['%LTC'] == 0.8925)]

with open(r"c:\Users\lap4all\Desktop\New folder\find_ltc_res.txt", "w", encoding="utf-8") as f:
    f.write(row_match.to_string())

print("Results written to find_ltc_res.txt")
