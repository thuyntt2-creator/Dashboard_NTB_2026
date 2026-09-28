import json, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('data.json', encoding='utf-8') as f:
    d = json.load(f)

print('=== 1. TOÀN VÙNG GTC CA 1 TTS W39 ===')
for k in d['overview']['kpis_trend']:
    if 'Ca1 thuần' in k['indicator'] and 'TTS' in k['indicator']:
        print(f"Indicator: {k['indicator']} | W39: {k['w39']*100:.2f}% | W38: {k['w38']*100:.2f}% | diff: {k['diff']*100:+.2f}%p")
    if 'Ca1+Tồn' in k['indicator'] and 'TTS' in k['indicator']:
        print(f"Indicator: {k['indicator']} | W39: {k['w39']*100:.2f}% | W38: {k['w38']*100:.2f}% | diff: {k['diff']*100:+.2f}%p")
    if 'Ca2' in k['indicator'] and 'TTS' in k['indicator']:
        print(f"Indicator: {k['indicator']} | W39: {k['w39']*100:.2f}% | W38: {k['w38']*100:.2f}% | diff: {k['diff']*100:+.2f}%p")

print('\n=== 2. TỈNH GTC CA 1 TTS W39 ===')
if 'gtc_ca1_thuan' in d:
    for p in sorted(d['gtc_ca1_thuan']['tinh_tts'], key=lambda x: x['w39'], reverse=True):
        print(f"• {p['tinh']}: W39={p['w39']*100:.2f}% | W38={p['w38']*100:.2f}% | diff={p['diff']*100:+.2f}%p | Vol={p['vol']:,}")

print('\n=== 3. TOP AM GTC CA 1 TTS W39 ===')
if 'gtc_ca1_thuan' in d:
    sorted_am = sorted(d['gtc_ca1_thuan']['am_tts'], key=lambda x: x['w39'], reverse=True)
    print("TOP 5 AM:")
    for a in sorted_am[:5]:
        print(f"• {a['am']}: W39={a['w39']*100:.2f}% | W38={a['w38']*100:.2f}% | diff={a['diff']*100:+.2f}%p | Vol={a['vol']:,}")
    print("\nBOTTOM 5 AM:")
    for a in sorted_am[-5:]:
        print(f"• {a['am']}: W39={a['w39']*100:.2f}% | W38={a['w38']*100:.2f}% | diff={a['diff']*100:+.2f}%p | Vol={a['vol']:,}")
