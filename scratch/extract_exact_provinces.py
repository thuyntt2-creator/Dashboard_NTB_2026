import json, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('data.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

print("==================== 1. SẢN LƯỢNG 5 TỈNH ====================")
sl = d['san_luong']
print("Tỉnh Full Hàng:")
for r in sl['tinh_full']:
    print(f"  {r['tinh']}: W37={r.get('w37',0):,}, W38={r.get('w38',0):,}, diff={r.get('diff',0):+,}")
print("Tỉnh TTS:")
for r in sl['tinh_tts']:
    pct = r.get('w38', 0) / 69274 * 100
    print(f"  {r['tinh']}: W37={r.get('w37',0):,}, W38={r.get('w38',0):,}, diff={r.get('diff',0):+,}, tỷ_trọng={pct:.1f}%")

print("\n==================== 2. GTC TỔNG 5 TỈNH ====================")
gtc = d['gtc_tong']
print("Tỉnh Full Hàng (Sort theo W38 desc):")
for r in sorted(gtc['tinh_full'], key=lambda x: x.get('w38',0), reverse=True):
    print(f"  {r['tinh']}: W37={r.get('w37',0)*100:.1f}%, W38={r.get('w38',0)*100:.1f}%, diff={r.get('diff',0)*100:+.1f}%p, vol={r.get('vol',0):,}")
print("Tỉnh TTS (Sort theo W38 desc):")
for r in sorted(gtc['tinh_tts'], key=lambda x: x.get('w38',0), reverse=True):
    print(f"  {r['tinh']}: W37={r.get('w37',0)*100:.1f}%, W38={r.get('w38',0)*100:.1f}%, diff={r.get('diff',0)*100:+.1f}%p, vol={r.get('vol',0):,}")
