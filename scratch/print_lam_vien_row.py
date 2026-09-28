import pandas as pd, sys
sys.stdout.reconfigure(encoding='utf-8')

df = pd.read_csv('buu_cuc_bat_on.csv', skiprows=4)
row_lv2 = df[df['Tên Bưu cục'].astype(str).str.contains('Lâm Viên.*2', regex=True, na=False)]

for col in df.columns:
    val = row_lv2[col].values[0] if len(row_lv2) > 0 else 'N/A'
    print(f"{col} ---> {val}")
