import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('data.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

print('\nTop AM ODR (full hàng W40):')
for a in sorted(d.get('odr', {}).get('am_full', []), key=lambda x: x.get('w40', 0), reverse=True)[:5]:
    w40 = a.get('w40', 0) * 100
    w39 = a.get('w39', 0) * 100
    print(f"  {a.get('am')}: W40={w40:.1f}%, W39={w39:.1f}%")

print('\nBottom AM ODR (full hàng W40 - Cảnh báo):')
for a in sorted(d.get('odr', {}).get('am_full', []), key=lambda x: x.get('w40', 0))[:5]:
    w40 = a.get('w40', 0) * 100
    w39 = a.get('w39', 0) * 100
    print(f"  {a.get('am')}: W40={w40:.1f}%, W39={w39:.1f}%")

print('\nTop AM Aging (đơn tồn kho >5 ngày):')
for a in d.get('aging', {}).get('top_am', [])[:5]:
    print(f"  {a.get('am')}: Tổng={a.get('total')}, >15 ngày={a.get('gt_15')}")

print('\nTop AM Treo Luân Chuyển:')
for a in d.get('treo_lc', {}).get('top_am', [])[:5]:
    print(f"  {a.get('am')}: Tổng={a.get('total')}, Treo >24h={a.get('treo_24')}")
