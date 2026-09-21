import json, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('data.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

print(f"Total {len(d['gtc_tong']['am_full'])} AMs in GTC TỔNG:")
for i, r in enumerate(sorted(d['gtc_tong']['am_full'], key=lambda x: x.get('w38', 0), reverse=True)):
    w38 = r.get('w38', 0) * 100
    w37 = r.get('w37', 0) * 100
    diff = r.get('diff', 0) * 100
    vol = r.get('vol', 0)
    am_name = r['am']
    print(f"  {i+1:2d}. AM {am_name:24} | W38: {w38:5.1f}% | W37: {w37:5.1f}% | Δ: {diff:+5.1f}%p | Vol: {vol:6,}")
