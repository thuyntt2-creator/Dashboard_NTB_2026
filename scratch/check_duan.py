import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('data.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

print("=== CHECK D.gtc_ca1_thuan.am_tts ===")
am_tts = d.get('gtc_ca1_thuan', {}).get('am_tts', [])
print("Length of am_tts:", len(am_tts))
for i, r in enumerate(am_tts):
    print(f"#{i+1:2d}: {r.get('am')}")

has_duan = any('Duân' in r.get('am', '') or 'Duan' in r.get('am', '') for r in am_tts)
print("Has Huỳnh Thúc Duân in am_tts?", has_duan)
