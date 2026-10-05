import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('data.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

print('=== GTC TỔNG AM W40 ===')
gtc_am = d.get('gtc_tong', {}).get('am', [])
for r in sorted(gtc_am, key=lambda x: x.get('w40', 0), reverse=True):
    print(f"{r.get('am')}: GTC W40 = {r.get('w40'):.1%}, Vol = {r.get('vol'):,}")

print('\n=== SẢN LƯỢNG FULL HÀNG AM W40 ===')
sl_am = d.get('san_luong', {}).get('am_full', [])
for r in sorted(sl_am, key=lambda x: x.get('w40', 0), reverse=True):
    print(f"{r.get('am')}: Vol W40 = {r.get('w40'):,}, diff = {r.get('diff', 0):,}")
