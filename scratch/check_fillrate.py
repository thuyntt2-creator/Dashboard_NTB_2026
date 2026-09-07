import sys
sys.stdout.reconfigure(encoding='utf-8')

# Check what the ktc_processed.json has for fill rate
import os, json

if os.path.exists('scratch/ktc_processed.json'):
    with open('scratch/ktc_processed.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    print('Keys:', list(data.keys()))
    if 'fill_rate' in data:
        print('Fill rate data:', json.dumps(data['fill_rate'], ensure_ascii=False, indent=2)[:2000])
    if 'leadtime' in data:
        print('Leadtime keys:', list(data['leadtime'].keys()) if isinstance(data['leadtime'], dict) else data['leadtime'][:3])
else:
    print('No ktc_processed.json found')

# Also check the build_data_js.py for fill rate logic
with open('build_data_js.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Find lines that mention fill_rate or lap day
lines = content.split('\n')
relevant = [str(i+1) + ': ' + l for i, l in enumerate(lines) if 'fill_rate' in l.lower() or 'lap_day' in l.lower() or 'ktc' in l.lower()]
for r in relevant[:30]:
    print(r)
