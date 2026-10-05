import json
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('data.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

for k in ['gtc_ca1', 'gtc_ca2', 'gtc_tts', 'gtc_tong']:
    if k in d:
        for r in d[k].get('am', []):
            if r.get('am') == 'Nguyễn Duy Long':
                print(f"{k}: W40={r.get('w40', 0):.2%}, W39={r.get('w39', 0):.2%}, vol={r.get('vol', 0)}")
