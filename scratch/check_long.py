import json
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('data.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

for r in d.get('gtc_tong', {}).get('am', []):
    if 'Long' in r.get('am', ''):
        print(r)
