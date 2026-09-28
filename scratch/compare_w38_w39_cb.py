import json
import sys
import pandas as pd
sys.stdout.reconfigure(encoding='utf-8')

with open('data.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

old_list = d.get('bc_canh_bao', [])
old_map = {r['bc']: r for r in old_list}

df = pd.read_csv('buu_cuc_bat_on.csv', skiprows=4)
new_list = []
for _, row in df.iterrows():
    name = row.iloc[3]
    if pd.notna(name) and str(name).strip() and str(name).strip() != 'nan':
        bname = str(name).strip()
        tinh = str(row.iloc[1]).strip()
        gtc7 = str(row.iloc[4]).strip()
        gtc_best = str(row.iloc[5]).strip()
        days = str(row.iloc[19]).strip() if len(row) > 19 else 'N/A'
        new_list.append({
            'bc': bname,
            'tinh': tinh,
            'gtc_w39': gtc7,
            'gtc_best': gtc_best,
            'days': days
        })

new_map = {r['bc']: r for r in new_list}

print(f"Tổng BC cảnh báo kỳ trước (W38): {len(old_map)} bưu cục")
print(f"Tổng BC cảnh báo kỳ này (W39): {len(new_map)} bưu cục")

escaped = set(old_map.keys()) - set(new_map.keys())
new_born = set(new_map.keys()) - set(old_map.keys())
persistent = set(old_map.keys()).intersection(set(new_map.keys()))

print(f"\n1. Bưu cục ĐÃ THOÁT cảnh báo thành công ({len(escaped)} BC):")
for bc in escaped:
    print(f"  🟢 {bc} (AM: {old_map[bc].get('am')})")

print(f"\n2. Bưu cục MỚI LỌT VÀO cảnh báo W39 ({len(new_born)} BC):")
for bc in new_born:
    print(f"  🚨 {bc} ({new_map[bc]['tinh']}) - %GTC: {new_map[bc]['gtc_w39']} | Số ngày cảnh báo: {new_map[bc]['days']} ngày")

print(f"\n3. Bưu cục TỒN TẠI LIÊN TỤC cả 2 tuần ({len(persistent)} BC):")
for bc in persistent:
    print(f"  ⚠️ {bc} - W38: {old_map[bc].get('gtc_w37')}% -> W39: {new_map[bc]['gtc_w39']}")
