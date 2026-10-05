# -*- coding: utf-8 -*-
import sys, json
sys.stdout.reconfigure(encoding='utf-8')

with open('data.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

fd_am = d.get('fd', {}).get('am', [])
print(f"{'STT':3s} | {'AM Phụ Trách':22s} | {'Vol Full':8s} | {'%FD Full':8s} | {'Vol TTS':7s} | {'%FD TTS':8s} | {'Chênh lệch':10s}")
print("-" * 80)
for a in sorted(fd_am, key=lambda k: k.get('rate_full', 0), reverse=True):
    name = a['am']
    vf = a['vol_full']
    rf = a['rate_full'] * 100
    vt = a['vol_tts']
    rt = a['rate_tts'] * 100
    diff = rt - rf
    print(f"{a['stt']:2d}  | {name:22s} | {vf:8d} | {rf:7.2f}% | {vt:7d} | {rt:7.2f}% | {diff:+7.2f}%p")
