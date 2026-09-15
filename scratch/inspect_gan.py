# -*- coding: utf-8 -*-
import json, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('data.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

print("=== GÁN VẬN HÀNH ===")
gan = d.get('gan', {})
print("gan keys:", list(gan.keys()))
print("\nOverview:")
for r in gan.get('overview', []):
    print(" ", r)

print("\nAM Full (top 5):")
for r in gan.get('am_full', [])[:5]:
    print(" ", r)

print("\nAM Full (bottom 5):")
for r in gan.get('am_full', [])[-5:]:
    print(" ", r)
