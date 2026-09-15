# -*- coding: utf-8 -*-
import json, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('data.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

am_gan = sorted(d['gan']['am_full'], key=lambda x: x.get('tong_curr', 0), reverse=True)
print('Ranked Gan Tong W37:')
for idx, r in enumerate(am_gan, 1):
    curr = r.get('tong_curr', 0) * 100
    prev = r.get('tong_prev', 0) * 100
    diff = r.get('tong_diff', 0) * 100
    print(f"  {idx}. AM {r['am']}: {curr:.1f}% (W36: {prev:.1f}%, Δ = {diff:+.1f}%p)")
