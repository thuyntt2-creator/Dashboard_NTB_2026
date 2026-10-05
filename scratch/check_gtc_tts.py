import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('data.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

print("=== CHECK GTC TTS IN DATA.JSON ===")
# Check where TTS GTC is located
found_keys = [k for k in d.keys() if 'tts' in k.lower()]
print("Keys with TTS:", found_keys)

if 'gtc_tts' in d:
    print("\n--- GTC TTS TINH ---")
    for r in d['gtc_tts'].get('tinh', []):
        print(f"{r.get('tinh')}: W40={r.get('w40', 0):.2%}, W39={r.get('w39', 0):.2%}, diff={r.get('diff', 0):.2%}")
    print("\n--- GTC TTS AM ---")
    for r in d['gtc_tts'].get('am', []):
        w39 = r.get('w39', 0)
        w40 = r.get('w40', 0)
        diff = w40 - w39
        vol = r.get('vol', 0)
        print(f"{r.get('am')}: W39={w39:.2%}, W40={w40:.2%}, diff={diff*100:+.2f}%p, vol={vol}")
else:
    # Check overview or other sections
    print("gtc_tts not a top-level key. Checking other keys...")
    for k in ['overview', 'san_luong', 'opr_tts']:
        if k in d:
            print(k, ":", list(d[k].keys()) if isinstance(d[k], dict) else len(d[k]))
