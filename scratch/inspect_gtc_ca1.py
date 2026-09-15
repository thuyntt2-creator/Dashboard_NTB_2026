# -*- coding: utf-8 -*-
import json, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('data.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

print("=== 1. GTC CA 1 THUẦN ===")
c1_thuan = d.get('gtc_ca1_thuan', {})
for r in c1_thuan.get('overview', []):
    print("  Overview:", r)

print("\n  Top AM W37 (GTC Ca 1 Thuần):")
am_w37 = sorted(c1_thuan.get('am', []), key=lambda x: x.get('w37', 0), reverse=True)
for r in am_w37:
    pass_sla = "Đạt SLA" if r['w37'] >= 0.76 else "Chưa đạt"
    print(f"    - AM {r['am']}: W37 = {r['w37']*100:.2f}% (W36 = {r['w36']*100:.2f}%, Δ = {r['diff']*100:+.2f}%p) [{pass_sla}]")

print("\n  Top AM bứt phá Δ WoW (GTC Ca 1 Thuần):")
am_diff = sorted(c1_thuan.get('am', []), key=lambda x: x.get('diff', 0), reverse=True)
for r in am_diff[:5]:
    print(f"    - AM {r['am']}: Δ = {r['diff']*100:+.2f}%p (W36 = {r['w36']*100:.2f}% -> W37 = {r['w37']*100:.2f}%)")

print("\n  Top AM sụt giảm mạnh nhất Δ WoW (GTC Ca 1 Thuần):")
for r in am_diff[-5:]:
    print(f"    - AM {r['am']}: Δ = {r['diff']*100:+.2f}%p (W36 = {r['w36']*100:.2f}% -> W37 = {r['w37']*100:.2f}%)")

print("\n" + "="*50)
print("=== 2. GTC CA 1 + TỒN ===")
c1_ton = d.get('gtc_ca1_ton', {})
for r in c1_ton.get('overview', []):
    print("  Overview:", r)
