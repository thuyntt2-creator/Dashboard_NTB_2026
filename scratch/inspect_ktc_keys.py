# -*- coding: utf-8 -*-
import sys, json
sys.stdout.reconfigure(encoding='utf-8')

with open('data.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

ktc = d.get('ktc', {})
print("KTC keys:", list(ktc.keys()))
for k in ktc.keys():
    v = ktc[k]
    if isinstance(v, dict):
        print(f"Key {k} (dict keys):", list(v.keys()))
    elif isinstance(v, list):
        print(f"Key {k} (list len {len(v)}):", v[:2])

print("\n--- CHECK FILL RATE ---")
print(ktc.get('fill_rate'))

print("\n--- CHECK LEADTIME ---")
print(ktc.get('leadtime'))

print("\n--- CHECK BACKLOG ---")
print(ktc.get('backlog'))
