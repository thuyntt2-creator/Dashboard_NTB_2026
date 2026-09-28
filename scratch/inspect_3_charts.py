import sys
import json

sys.stdout.reconfigure(encoding='utf-8')

with open('data.json', encoding='utf-8') as f:
    d = json.load(f)

am_full = {x['am']: x for x in d['san_luong']['am_full']}
am_tts = {x['am']: x for x in d['san_luong']['am_tts']}

print("=== CHART 1: FULL HÀNG (Sort by diff) ===")
list_full = sorted(d['san_luong']['am_full'], key=lambda x: x['diff'], reverse=True)
for x in list_full:
    print(f"  {x['am']}: W39={x['vol']:,}, W38={x['w38']:,}, diff={x['diff']:+,}")

print("\n=== CHART 2: TIKTOK SHOP (Sort by diff) ===")
list_tts = sorted(d['san_luong']['am_tts'], key=lambda x: x['diff'], reverse=True)
for x in list_tts:
    print(f"  {x['am']}: W39={x['vol']:,}, W38={x['w38']:,}, diff={x['diff']:+,}")

print("\n=== CHART 3: SO SÁNH FULL vs TTS & TỶ TRỌNG (Sort by vol full) ===")
for x in sorted(d['san_luong']['am_full'], key=lambda x: x['vol'], reverse=True):
    am = x['am']
    f_vol = x['vol']
    t_vol = am_tts.get(am, {}).get('vol', 0)
    pct = (t_vol / f_vol * 100) if f_vol > 0 else 0
    print(f"  {am}: Full={f_vol:,}, TTS={t_vol:,}, %TTS={pct:.1f}%")
