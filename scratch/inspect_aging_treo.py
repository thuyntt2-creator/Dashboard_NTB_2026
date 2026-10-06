# -*- coding: utf-8 -*-
import sys, json
sys.stdout.reconfigure(encoding='utf-8')

with open('data.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

ag = d.get('aging', {})
tr = d.get('treo_lc', {})

print("=== AGING TỒN ĐỌNG ===")
print(f"Tổng tồn Aging: {ag.get('total')} đơn")
print(f"  5-8 ngày: {ag.get('total_5_8')} đơn")
print(f"  8-15 ngày: {ag.get('total_8_15')} đơn")
print(f"  >15 ngày: {ag.get('total_gt_15')} đơn")

print("\n--- TOP AM AGING ---")
for x in ag.get('top_am', [])[:8]:
    print(f"- {x['am']} ({x['tinh']}): {x['vol']} đơn ({x['pct']}%) [5-8N: {x['d_5_8']}, 8-15N: {x['d_8_15']}, >15N: {x['gt_15']}, TB: {x['avg_days']} ngày]")

print("\n--- TOP BC AGING ---")
for x in ag.get('top_bc', [])[:8]:
    print(f"- {x['bc']} ({x['tinh']} - AM: {x['am']}): {x['vol']} đơn [5-8N: {x['d_5_8']}, 8-15N: {x['d_8_15']}, >15N: {x['gt_15']}]")

print("\n=== TREO LUÂN CHUYỂN ===")
print(f"Tổng đơn luân chuyển: {tr.get('total')} đơn")
print(f"  Đúng hạn (<24h): {tr.get('total_u24')} đơn ({round(tr.get('total_u24',0)/tr.get('total',1)*100, 1)}%)")
print(f"  Treo >=24h: {tr.get('total_treo_24')} đơn ({tr.get('pct_treo_24')}%)")
print(f"    24-36h: {tr.get('total_24_36')} đơn")
print(f"    36-72h: {tr.get('total_36_72')} đơn")
print(f"    72-120h: {tr.get('total_72_120')} đơn")
print(f"    >120h: {tr.get('total_120_plus')} đơn")
print(f"  Treo >=36h (trễ nặng): {tr.get('total_treo_36')} đơn ({tr.get('pct_treo_36')}%)")

print("\n--- THEO TỈNH TREO LC ---")
for x in tr.get('tinh', []):
    print(x)

print("\n--- TOP AM TREO LC ---")
for x in tr.get('top_am', [])[:8]:
    print(f"- {x['am']} ({x.get('tinh')}): Tổng {x.get('vol')} đơn | Treo>=24h: {x.get('treo_24')} ({x.get('rate_treo_24')}%) | Treo>=36h: {x.get('treo_36')} [<24h: {x.get('u_24')}, 24-36h: {x.get('h_24_36')}, 36-72h: {x.get('h_36_72')}, 72-120h: {x.get('h_72_120')}, >120h: {x.get('h_120_plus')}]")

print("\n--- TOP BC TREO LC ---")
for x in tr.get('top_bc', [])[:8]:
    print(f"- {x['bc']} ({x.get('tinh')} - AM: {x.get('am')}): Tổng {x.get('vol')} đơn | Treo>=24h: {x.get('treo_24')} ({x.get('rate_treo_24')}%) | Treo>=36h: {x.get('treo_36')} [24-36h: {x.get('h_24_36')}, 36-72h: {x.get('h_36_72')}, 72-120h: {x.get('h_72_120')}, >120h: {x.get('h_120_plus')}]")

