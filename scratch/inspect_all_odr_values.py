import json, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('data.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

print("TTS ODR values:")
for a in d.get('odr', {}).get('am_tts', []):
    w38 = a.get('w38', 0) * 100
    w39 = a.get('w39', 0) * 100
    diff = a.get('diff', 0) * 100
    print(f"- {a.get('am')}: W38={w38:.1f}%, W39={w39:.1f}%, Diff={diff:+.1f}%p")

print("\nFULL ODR values:")
for a in d.get('odr', {}).get('am_full', []):
    w38 = a.get('w38', 0) * 100
    w39 = a.get('w39', 0) * 100
    diff = a.get('diff', 0) * 100
    print(f"- {a.get('am')}: W38={w38:.1f}%, W39={w39:.1f}%, Diff={diff:+.1f}%p")
