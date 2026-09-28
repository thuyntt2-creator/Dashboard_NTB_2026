import json, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('data.json', encoding='utf-8') as f:
    d = json.load(f)

print('=== 1. XẾP HẠNG GTC FULL 18 AM THEO MỨC SỤT GIẢM (DIFF TỪ GIẢM NHIỀU NHẤT ĐẾN TĂNG) ===')
for a in sorted(d['gtc_tong']['am_full'], key=lambda x: x['diff']):
    print(f"• {a['am']}: W39 = {a['w39']*100:.2f}% | W38 = {a['w38']*100:.2f}% | Biến động = {a['diff']*100:+.2f}%p")

print('\n=== 2. KIỂM TRA BƯU CỤC CỦA AM TRƯỜNG & LÂM VIÊN 2 ===')
import pandas as pd
df = pd.read_csv('buu_cuc_bat_on.csv', skiprows=4)
for _, r in df.iterrows():
    name = str(r.iloc[3]).strip()
    if 'Lâm Viên' in name or 'Xuân Hương' in name or 'Đơn Dương' in name:
        print(f"BC: {name} | GTC W39: {r.iloc[4]} | Best: {r.iloc[5]} | Days warn: {r.iloc[19] if len(r)>19 else 'N/A'}")
