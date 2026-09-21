import json, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('data.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

gtc = d['gtc_tong']
print("=== GTC TONG OVERVIEW ===")
print(json.dumps(gtc['overview'], indent=2, ensure_ascii=False))

print("\n=== GTC TONG TINH FULL ===")
for r in gtc['tinh_full']:
    print(r)

print("\n=== GTC TONG TINH TTS ===")
for r in gtc['tinh_tts']:
    print(r)

print("\n=== GTC TONG AM FULL (TOP 5 & BOTTOM 5) ===")
for r in gtc['am_full'][:5]:
    print(r)
print("...")
for r in gtc['am_full'][-5:]:
    print(r)
