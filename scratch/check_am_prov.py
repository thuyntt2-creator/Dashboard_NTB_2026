import json
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('data.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

print(d.get('meta', {}).get('am_province_map', {}))
if not d.get('meta', {}).get('am_province_map'):
    # Search am list
    for k in ['san_luong', 'gtc_tong', 'odr']:
        if k in d:
            for r in d[k].get('am', []):
                print(r.get('am'), ':', r.get('tinh', ''))
            break
