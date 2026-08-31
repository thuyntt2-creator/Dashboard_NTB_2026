import pandas as pd
import numpy as np
import sys

sys.stdout.reconfigure(encoding='utf-8')

df = pd.read_csv("vols_tao_don.csv")
df.columns = [str(c).strip() for c in df.columns]
df['Date'] = pd.to_datetime(df['Date'])
df = df[df['bat_on'].fillna('').str.strip() != 'BC Cũ/Không thuộc ĐCL'].copy()

# Try with all combinations of filters
customers = [None] + list(df['Khách hàng'].dropna().unique())
dates = sorted(df['Date'].unique())

print("Scanning for Phú Thủy growth around 719:")
for d in dates:
    d7 = d - pd.Timedelta(days=7)
    if d7 not in dates:
        continue
    for cust in customers:
        sub_df = df.copy()
        if cust:
            sub_df = sub_df[sub_df['Khách hàng'] == cust]
            
        df_d = sub_df[sub_df['Date'] == d]
        df_d7 = sub_df[sub_df['Date'] == d7]
        
        vol_d = df_d.groupby('Bưu cục')['Volume'].sum()
        vol_d7 = df_d7.groupby('Bưu cục')['Volume'].sum()
        
        diff = vol_d - vol_d7
        
        pt_growth = diff.get('(BTH) Phú Thủy', 0)
        if abs(pt_growth - 719) <= 50:
            print(f"Date: {d7.strftime('%Y-%m-%d')} -> {d.strftime('%Y-%m-%d')} | Cust: {cust} | Phú Thủy Growth: {pt_growth:.1f}")
            # print top 5 on this day/filter
            top5 = diff.sort_values(ascending=False).head(5)
            print("  Top 5 on this day/filter:")
            for k, v in top5.items():
                print(f"    {k}: +{v:.0f}")
