# -*- coding: utf-8 -*-
import json, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('data.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

print("=== OVERVIEW KPI ===")
for k, v in d.get('overview', {}).items():
    print(f"  {k}: {v}")

print("\n=== GTC CA 1 TON ===")
for r in d.get('gtc_ca1_ton', {}).get('overview', []):
    print(f"  {r}")
print("Top 5 AM GTC Ca 1:")
ca1_sorted = sorted(d.get('gtc_ca1_ton', {}).get('am', []), key=lambda x: x.get('w37', 0), reverse=True)
for r in ca1_sorted[:5]:
    print(f"  {r['am']}: W37={r['w37']*100:.1f}%, W36={r['w36']*100:.1f}%, diff={r['diff']*100:+.1f}%p")
print("Bottom 5 AM GTC Ca 1:")
for r in ca1_sorted[-5:]:
    print(f"  {r['am']}: W37={r['w37']*100:.1f}%, W36={r['w36']*100:.1f}%, diff={r['diff']*100:+.1f}%p")

print("\n=== ODR ===")
for r in d.get('odr', {}).get('overview', []):
    print(f"  {r}")
odr_sorted = sorted(d.get('odr', {}).get('am_full', []), key=lambda x: x.get('w37', 0), reverse=True)
print("Top 3 ODR:")
for r in odr_sorted[:3]:
    print(f"  {r['am']}: W37={r['w37']*100:.2f}%, W36={r['w36']*100:.2f}%")
print("Bottom 3 ODR:")
for r in odr_sorted[-3:]:
    print(f"  {r['am']}: W37={r['w37']*100:.2f}%, W36={r['w36']*100:.2f}%")

print("\n=== ROT LC ===")
for r in d.get('rot_lc', {}).get('overview', []):
    print(f"  {r}")

print("\n=== KTC (TLLD) ===")
ktc = d.get('ktc', {})
print(f"  TL lấp đầy toàn vùng: {ktc.get('tlld_toan_vung')}")
print(f"  Xe chạy rỗng (<30%): {ktc.get('xe_chay_rong')}")
print(f"  Tổng chuyến: {ktc.get('tong_chuyen')}")

print("\n=== FD ===")
for r in d.get('fd', {}).get('overview', []):
    print(f"  {r}")

print("\n=== AGING ===")
for r in d.get('aging', {}).get('overview', []):
    print(f"  {r}")
