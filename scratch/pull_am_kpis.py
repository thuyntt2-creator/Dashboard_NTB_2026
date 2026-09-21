import json, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('data.js', 'r', encoding='utf-8') as f:
    text = f.read()

prefix = 'window.DASHBOARD_DATA = '
data = json.loads(text[len(prefix):].rstrip(';\n '))

print("=== ODR BY AM ===")
for a in data.get('odr', {}).get('am_full', [])[:6]:
    print(" ", a.get('am'), a.get('w38'), a.get('diff'))

print("\n=== LTC BY AM ===")
for a in data.get('ltc', {}).get('am_full', [])[:6]:
    print(" ", a.get('am'), a.get('w38'), a.get('diff'))

print("\n=== GTC CA 1 BY AM ===")
for a in data.get('gtc_ca1_thuan', {}).get('am_full', [])[:6]:
    print(" ", a.get('am'), a.get('w38'), a.get('diff'))

print("\n=== KINH DOANH BY AM ===")
for a in data.get('kinh_doanh', {}).get('am', [])[:6]:
    print(" ", a.get('am'), a.get('rev_curr'), a.get('pct_diff_rev'))
