import pandas as pd
import sys

sys.stdout.reconfigure(encoding='utf-8')
df = pd.read_csv('sheet_stuck.csv')

print(f"TOTAL ROWS: {len(df)}")
print("Distribution of Thoi gian ton dong:")
print(df['Thoi gian ton dong'].value_counts())
print("\n" + "="*80)

for am, g in df.groupby('am_name'):
    vc = g['Thoi gian ton dong'].value_counts().to_dict()
    under_24 = vc.get("0_6", 0) + vc.get("6_12", 0) + vc.get("12_24", 0)
    h_24_36 = vc.get("24_36", 0)
    h_36_72 = vc.get("36_48", 0) + vc.get("48_72", 0)
    h_72_120 = vc.get("72_96", 0) + vc.get("96_120", 0)
    h_120_192 = vc.get("120_192", 0)
    h_192 = vc.get("192", 0)
    treo_24 = h_24_36 + h_36_72 + h_72_120 + h_120_192 + h_192
    treo_36 = h_36_72 + h_72_120 + h_120_192 + h_192
    print(f"{am:22s} | Total={len(g):4d} | <24h={under_24:4d} | 24-36h={h_24_36:3d} | 36-72h={h_36_72:3d} | 72-120h={h_72_120:2d} | 120-192h={h_120_192:2d} | >192h={h_192:2d} | Treo>=24h={treo_24:3d} | Treo>=36h={treo_36:3d}")
