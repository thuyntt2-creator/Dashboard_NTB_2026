import json, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('data.json', encoding='utf-8') as f:
    d = json.load(f)

print('=== 1. TOÀN VÙNG GTC W39 ===')
card_full = next(c for c in d['overview']['cards'] if c['id'] == 'gtc_full')
card_tts = next(c for c in d['overview']['cards'] if c['id'] == 'gtc_tts')
print(f"Full: W39={card_full['val']*100:.2f}%, diff={card_full['diff']*100:+.2f}%p")
print(f"TTS: W39={card_tts['val']*100:.2f}%, diff={card_tts['diff']*100:+.2f}%p")

print('\n=== 2. GTC TINH FULL ===')
for p in sorted(d['gtc_tong']['tinh_full'], key=lambda x: x['w39'], reverse=True):
    print(f"• {p['tinh']}: W39={p['w39']*100:.2f}%, W38={p['w38']*100:.2f}%, diff={p['diff']*100:+.2f}%p")

print('\n=== 3. GTC TINH TTS ===')
for p in sorted(d['gtc_tong']['tinh_tts'], key=lambda x: x['w39'], reverse=True):
    print(f"• {p['tinh']}: W39={p['w39']*100:.2f}%, W38={p['w38']*100:.2f}%, diff={p['diff']*100:+.2f}%p")

print('\n=== 4. GTC AM FULL (Top & Bottom) ===')
sorted_am_full = sorted(d['gtc_tong']['am_full'], key=lambda x: x['w39'], reverse=True)
print("TOP 5 AM FULL:")
for a in sorted_am_full[:5]:
    print(f"• {a['am']}: W39={a['w39']*100:.2f}%, W38={a['w38']*100:.2f}%, diff={a['diff']*100:+.2f}%p")
print("BOTTOM 5 AM FULL:")
for a in sorted_am_full[-5:]:
    print(f"• {a['am']}: W39={a['w39']*100:.2f}%, W38={a['w38']*100:.2f}%, diff={a['diff']*100:+.2f}%p")

print('\n=== 5. GTC AM TTS (Top & Bottom) ===')
sorted_am_tts = sorted(d['gtc_tong']['am_tts'], key=lambda x: x['w39'], reverse=True)
print("TOP 5 AM TTS:")
for a in sorted_am_tts[:5]:
    print(f"• {a['am']}: W39={a['w39']*100:.2f}%, W38={a['w38']*100:.2f}%, diff={a['diff']*100:+.2f}%p")
print("BOTTOM 5 AM TTS:")
for a in sorted_am_tts[-5:]:
    print(f"• {a['am']}: W39={a['w39']*100:.2f}%, W38={a['w38']*100:.2f}%, diff={a['diff']*100:+.2f}%p")
