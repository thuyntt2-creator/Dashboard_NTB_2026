import pandas as pd

local_file = r"c:\Users\lap4all\Desktop\New folder\Copy o NTB - BÁO CÁO VẬN HÀNH.xlsx"
df_local_ltc = pd.read_excel(local_file, sheet_name='DataLTC')

# Let's filter for W21 (Time == '2026/21') and check Trần Công Hậu rows
df_local_w21 = df_local_ltc[df_local_ltc['Time'] == '2026/21'].copy()

# Filter for Trần Công Hậu rows in local W21
df_local_hau = df_local_w21[df_local_w21['AM'].str.contains('Hậu', na=False, case=False)]

# Filter for Hồng Bích Nga rows in local W21
df_local_nga = df_local_w21[df_local_w21['AM'].str.contains('Nga', na=False, case=False)]

# Save to file
with open(r"c:\Users\lap4all\Desktop\New folder\local_dataltc_check.txt", "w", encoding="utf-8") as f:
    f.write("=== COLUMNS ===\n")
    f.write(str(df_local_ltc.columns.tolist()) + "\n\n")
    f.write("=== UNIQUE AM IN LOCAL W21 ===\n")
    f.write(str(df_local_w21['AM'].dropna().unique().tolist()) + "\n\n")
    f.write("=== TRẦN CÔNG HẬU W21 ROWS ===\n")
    f.write(df_local_hau[['Chi tiết', 'Volume', '%Gán', '%LTC', 'AM']].to_string() + "\n\n")
    f.write("=== HỒNG BÍCH NGA W21 ROWS ===\n")
    f.write(df_local_nga[['Chi tiết', 'Volume', '%Gán', '%LTC', 'AM']].to_string() + "\n")

print("Saved to local_dataltc_check.txt successfully.")
