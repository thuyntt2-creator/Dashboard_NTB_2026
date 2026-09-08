import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('data.json', encoding='utf-8') as f:
    d = json.load(f)

am_list = d.get('opr_tts', {}).get('am', [])
# Calculate totals
tot_vol = sum(x.get('vol_total', 0) for x in am_list)
# late orders: vol_total * (1 - w36_total)
for x in am_list:
    vol = x.get('vol_total', 0)
    w36 = x.get('w36_total', 0)
    x['late'] = round(vol * (1 - w36))
    x['vol_share'] = (vol / tot_vol * 100) if tot_vol else 0

tot_late = sum(x['late'] for x in am_list)
for x in am_list:
    x['late_share'] = (x['late'] / tot_late * 100) if tot_late else 0

# Sort by volume total descending
sorted_by_vol = sorted(am_list, key=lambda x: x.get('vol_total', 0), reverse=True)

print(f"TOTAL REGION W36: Vol={tot_vol}, Late={tot_late}, Avg OPR={(1 - tot_late/tot_vol)*100:.2f}%\n")
print(f"{'AM':<24} | {'Sản lượng':<9} | {'%SL Vùng':<8} | {'%OPR W36':<9} | {'Đạt/Rớt KPI':<11} | {'Đơn trễ':<8} | {'% Tỷ trọng lỗi':<14}")
print("-" * 95)

for r in sorted_by_vol:
    kpi_status = "ĐẠT (>=80%)" if r.get('w36_total', 0) >= 0.8 else "RỚT (<80%)"
    print(f"{r.get('am'):<24} | {r.get('vol_total', 0):<9} | {r.get('vol_share'):>7.2f}% | {r.get('w36_total', 0)*100:>8.2f}% | {kpi_status:<11} | {r['late']:<8} | {r['late_share']:>12.2f}%")
