import json, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('data.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

print("=== GTC CA 1 THUẦN (TTS) OVERVIEW ===")
for o in d.get('gtc_ca1_thuan', {}).get('overview', []):
    lbl = o.get('label')
    w38 = o.get('w38', 0) * 100
    w39 = o.get('w39', 0) * 100
    diff = o.get('diff', 0) * 100
    print(f"- {lbl}: W39 = {w39:.2f}%, W38 = {w38:.2f}%, Diff = {diff:+.2f}%p")

print("\n=== GTC CA 1 TỒN (TTS) OVERVIEW ===")
for o in d.get('gtc_ca1_ton', {}).get('overview', []):
    lbl = o.get('label')
    w38 = o.get('w38', 0) * 100
    w39 = o.get('w39', 0) * 100
    diff = o.get('diff', 0) * 100
    print(f"- {lbl}: W39 = {w39:.2f}%, W38 = {w38:.2f}%, Diff = {diff:+.2f}%p")

print("\n=== TOP AM GTC CA 1 THUẦN TTS W39 ===")
for a in sorted(d.get('gtc_ca1_thuan', {}).get('am_tts', []), key=lambda x: x.get('w39', 0), reverse=True):
    name = a.get('am')
    w38 = a.get('w38', 0) * 100
    w39 = a.get('w39', 0) * 100
    diff = a.get('diff', 0) * 100
    print(f"- {name}: W39 = {w39:.2f}%, W38 = {w38:.2f}%, Diff = {diff:+.2f}%p")

print("\n=== TOP AM GTC CA 1 TỒN TTS W39 ===")
for a in sorted(d.get('gtc_ca1_ton', {}).get('am_tts', []), key=lambda x: x.get('w39', 0), reverse=True):
    name = a.get('am')
    w38 = a.get('w38', 0) * 100
    w39 = a.get('w39', 0) * 100
    diff = a.get('diff', 0) * 100
    print(f"- {name}: W39 = {w39:.2f}%, W38 = {w38:.2f}%, Diff = {diff:+.2f}%p")
