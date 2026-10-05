import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('data.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

am_gtc = d.get('gtc_tong', {}).get('am', [])
# Calculate diff WoW = w40 - w39
analyzed = []
for r in am_gtc:
    am = r.get('am')
    w39 = r.get('w39', 0)
    w40 = r.get('w40', 0)
    diff = w40 - w39
    vol = r.get('vol', 0)
    analyzed.append({
        'am': am,
        'tinh': r.get('tinh', ''),
        'w39': w39,
        'w40': w40,
        'diff': diff,
        'vol': vol
    })

analyzed.sort(key=lambda x: x['diff'], reverse=True)

print("=== BẢNG XẾP HẠNG 18 AM THEO MỨC ĐỘ TĂNG TRƯỞNG %GTC (W40 vs W39) ===")
for i, r in enumerate(analyzed):
    print(f"#{i+1:2d}: {r['am']:<25} | W39: {r['w39']:.2%} -> W40: {r['w40']:.2%} | Δ: {r['diff']*100:+.2f}%p | Vol: {r['vol']:,}")
