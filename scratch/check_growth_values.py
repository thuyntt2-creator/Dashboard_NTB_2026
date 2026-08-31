import pandas as pd
import numpy as np

# Load data
df = pd.read_csv("vols_tao_don.csv")
df['Date'] = pd.to_datetime(df['Date'])

latest_dt = df['Date'].max()
print("Latest Date:", latest_dt)

df_d = df[df['Date'] == latest_dt]
df_d7 = df[df['Date'] == (latest_dt - pd.Timedelta(days=7))]

if len(df_d) > 0:
    vol_d = df_d.groupby(['Tỉnh', 'Bưu cục'])['Volume'].sum().reset_index()
    vol_d7 = df_d7.groupby('Bưu cục')['Volume'].sum().reset_index()
    
    merged_growth = pd.merge(vol_d, vol_d7, on='Bưu cục', suffixes=('_d', '_d7'), how='left').fillna(0)
    merged_growth['growth_abs'] = merged_growth['Volume_d'] - merged_growth['Volume_d7']
    merged_growth['growth_pct'] = (merged_growth['growth_abs'] / merged_growth['Volume_d7'] * 100).replace(np.inf, 100.0).replace(-np.inf, -100.0).fillna(0)
    
    # Sort by absolute growth ascending (worst first)
    merged_growth = merged_growth.sort_values(by='growth_abs', ascending=True)
    
    print("\nWorst 10 growth post offices:")
    print(merged_growth[['Bưu cục', 'Tỉnh', 'Volume_d7', 'Volume_d', 'growth_abs', 'growth_pct']].head(10).to_string())
