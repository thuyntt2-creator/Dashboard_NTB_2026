import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('data.json', encoding='utf-8') as f:
    d = json.load(f)

opr = d.get('opr_tts', {})
print("opr_tts.am type:", type(opr.get('am')))
if isinstance(opr.get('am'), list):
    print("Sample row:", opr['am'][0] if opr['am'] else "Empty")
    rows = opr['am']
elif isinstance(opr.get('am'), dict):
    print("Keys in opr.am:", list(opr['am'].keys()))
    rows = opr['am'].get('rows', opr['am'].get('table_data', []))
    if not rows:
        # let's see structure
        print("dict items sample:", list(opr['am'].items())[:3])

print("\n--- Let's print out what is in opr['am'] ---")
import pprint
pprint.pprint(opr['am'][:5] if isinstance(opr['am'], list) else list(opr['am'].items())[:5])
