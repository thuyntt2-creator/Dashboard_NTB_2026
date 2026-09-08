import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('data.json', encoding='utf-8') as f:
    d = json.load(f)

cod = d.get('cod_report', {})
print('summary_text:', cod.get('summary_text'))
print('metrics count:', len(cod.get('metrics', [])))
for m in cod.get('metrics', []):
    print('  ', m)

print('\nAM count:', len(cod.get('am_comparison', [])))
for a in cod.get('am_comparison', []):
    print('  ', a)

print('\nActions count:', len(cod.get('actions', [])))
