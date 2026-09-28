import sys
import json

sys.stdout.reconfigure(encoding='utf-8')

with open('data.json', encoding='utf-8') as f:
    d = json.load(f)

print("=== OVERVIEW CARDS ===")
for c in d['overview']['cards']:
    print(f"  {c['id']}: {c['title']} = {c['val']} {c['unit']} (diff: {c['diff']})")

print("\n=== SAN LUONG TINH FULL (W39 vs W38) ===")
for x in sorted(d['san_luong']['tinh_full'], key=lambda i: i['vol'], reverse=True):
    print(f"  {x['tinh']}: W39={x['vol']:,} (W38={x['w38']:,}, diff={x['diff']:+,})")

print("\n=== SAN LUONG TINH TTS (W39 vs W38) ===")
for x in sorted(d['san_luong']['tinh_tts'], key=lambda i: i['vol'], reverse=True):
    print(f"  {x['tinh']}: W39={x['vol']:,} (W38={x['w38']:,}, diff={x['diff']:+,})")

print("\n=== GTC TONG TINH FULL (W39 vs W38) ===")
for x in sorted(d['gtc_tong']['tinh_full'], key=lambda i: i['w39'], reverse=True):
    print(f"  {x['tinh']}: W39={x['w39']*100:.2f}% (W38={x['w38']*100:.2f}%, diff={x['diff']*100:+.2f}%p)")

print("\n=== GTC TONG TINH TTS (W39 vs W38) ===")
for x in sorted(d['gtc_tong']['tinh_tts'], key=lambda i: i['w39'], reverse=True):
    print(f"  {x['tinh']}: W39={x['w39']*100:.2f}% (W38={x['w38']*100:.2f}%, diff={x['diff']*100:+.2f}%p)")

print("\n=== ODR TINH FULL (W39 vs W38) ===")
for x in sorted(d['odr']['tinh_full'], key=lambda i: i['w39'], reverse=True):
    print(f"  {x['tinh']}: W39={x['w39']*100:.2f}% (W38={x['w38']*100:.2f}%, diff={x['diff']*100:+.2f}%p)")

print("\n=== LTC TINH FULL (W39 vs W38) ===")
for x in sorted(d['ltc']['tinh_full'], key=lambda i: i['w39'], reverse=True):
    print(f"  {x['tinh']}: W39={x['w39']*100:.2f}% (W38={x['w38']*100:.2f}%, diff={x['diff']*100:+.2f}%p)")
