# -*- coding: utf-8 -*-
import sys, json
sys.stdout.reconfigure(encoding='utf-8')

with open('data.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

fd = d.get('fd', {})
print("=== OVERVIEW ===")
print(fd.get('overview'))

print("\n=== ALL AMs IN FD ===")
for a in sorted(fd.get('am', []), key=lambda k: k.get('rate_full', 0), reverse=True):
    name = a.get('am')
    rf = a.get('rate_full', 0) * 100
    rtts = a.get('rate_tts', 0) * 100
    ret_f = a.get('ret_full', 0)
    vol_f = a.get('vol_full', 0)
    ret_tts = a.get('ret_tts', 0)
    vol_tts = a.get('vol_tts', 0)
    share = a.get('share_ret', 0) * 100
    diff_f = a.get('diff_full', 0) * 100
    print(f"{name:25s} | Full: {rf:6.2f}% ({diff_f:+5.2f}%p) | Ret/Vol: {ret_f:5d}/{vol_f:6d} | TTS: {rtts:5.2f}% ({ret_tts:4d}/{vol_tts:5d}) | Share: {share:5.2f}%")

print("\n=== TOP BC IN FD ===")
for bc in fd.get('top_bc', []):
    name = bc.get('bc')
    am = bc.get('am')
    rate = bc.get('rate', 0) * 100
    ret = bc.get('ret', 0)
    vol = bc.get('vol', 0)
    share = bc.get('share_ret', 0) * 100
    diff = bc.get('diff', 0) * 100
    print(f"{name:28s} | {am:22s} | Rate: {rate:6.2f}% ({diff:+5.2f}%p) | Ret/Vol: {ret:4d}/{vol:5d} | Share: {share:5.2f}%")
