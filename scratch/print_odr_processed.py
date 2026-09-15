# -*- coding: utf-8 -*-
import json, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/odr_processed.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

print('=== OVERVIEW ===')
for r in d['overview']:
    print(r)

print('\n=== TINH FULL ===')
for r in d['tinh_full']:
    print(f"  {r['tinh']}: W37={r['w37']*100:.2f}%, W36={r['w36']*100:.2f}%, diff={r['diff']*100:+.2f}%p (Vol={r['vol']:,})")

print('\n=== TINH TTS ===')
for r in d['tinh_tts']:
    print(f"  {r['tinh']}: W37={r['w37']*100:.2f}%, W36={r['w36']*100:.2f}%, diff={r['diff']*100:+.2f}%p (Vol={r['vol']:,})")

print('\n=== AM FULL (Top 5 diff) ===')
for r in d['am_full'][:5]:
    print(f"  {r['am']}: W37={r['w37']*100:.2f}%, W36={r['w36']*100:.2f}%, diff={r['diff']*100:+.2f}%p (Vol={r['vol']:,})")

print('\n=== AM TTS (Top 5 diff) ===')
for r in d['am_tts'][:5]:
    print(f"  {r['am']}: W37={r['w37']*100:.2f}%, W36={r['w36']*100:.2f}%, diff={r['diff']*100:+.2f}%p (Vol={r['vol']:,})")
