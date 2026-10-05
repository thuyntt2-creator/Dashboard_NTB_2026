import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('data.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

meta = d.get('meta', {})
print("Meta weeks:", meta.get('weeks'))

# 1. Overview KPIs
print("\n--- OVERVIEW KPIS ---")
for k, v in d.get('overview', {}).items():
    if isinstance(v, dict):
        print(f"{k}: W40={v.get('w40')}, W39={v.get('w39')}, diff={v.get('diff')}")

# 2. San Luong
print("\n--- SẢN LƯỢNG 5 TỈNH W40 ---")
for r in d.get('san_luong', {}).get('tinh_full', []):
    print(f"Full {r.get('tinh')}: W40={r.get('w40'):,}, diff={r.get('diff', 0):,}")
for r in d.get('san_luong', {}).get('tinh_tts', []):
    print(f"TTS {r.get('tinh')}: W40={r.get('w40'):,}, diff={r.get('diff', 0):,}")

# 3. GTC Tổng
print("\n--- GTC TỔNG 5 TỈNH W40 ---")
for r in d.get('gtc_tong', {}).get('tinh', []):
    print(f"{r.get('tinh')}: W40={r.get('w40', 0):.2%}, W39={r.get('w39', 0):.2%}, diff={r.get('diff', 0):.2%}")

print("\n--- GTC TỔNG 18 AM TOP 5 & BOTTOM 5 ---")
sorted_am_gtc = sorted(d.get('gtc_tong', {}).get('am', []), key=lambda x: x.get('w40', 0), reverse=True)
print("Top 5 AM GTC:")
for i, r in enumerate(sorted_am_gtc[:5]):
    print(f"  #{i+1}: {r.get('am')} = {r.get('w40', 0):.2%} (W39: {r.get('w39', 0):.2%})")
print("Bottom 5 AM GTC:")
for i, r in enumerate(sorted_am_gtc[-5:]):
    print(f"  #{len(sorted_am_gtc)-4+i}: {r.get('am')} = {r.get('w40', 0):.2%} (W39: {r.get('w39', 0):.2%})")

# 4. GTC Ca 1 & Ca 2
print("\n--- GTC CA 1 & CA 2 TOÀN VÙNG ---")
if 'gtc_ca1_ton' in d and 'tinh' in d['gtc_ca1_ton']:
    print("GTC Ca 1 Tồn:")
    for r in d['gtc_ca1_ton']['tinh']:
        print(f"  {r.get('tinh')}: W40={r.get('w40', 0):.2%}")
if 'gtc_ca2' in d and 'tinh' in d['gtc_ca2']:
    print("GTC Ca 2:")
    for r in d['gtc_ca2']['tinh']:
        print(f"  {r.get('tinh')}: W40={r.get('w40', 0):.2%}")

# 5. ODR
print("\n--- ODR 5 TỈNH ---")
for r in d.get('odr', {}).get('tinh', []):
    print(f"  {r.get('tinh')}: W40={r.get('w40', 0):.2%}, diff={r.get('diff', 0):.2%}")

# 6. LTC
print("\n--- LTC 5 TỈNH ---")
for r in d.get('ltc', {}).get('tinh', []):
    print(f"  {r.get('tinh')}: W40={r.get('w40', 0):.2%}, diff={r.get('diff', 0):.2%}")

# 7. Gán Ca 2
print("\n--- GÁN CA 2 ---")
for r in d.get('gan', {}).get('tinh', []):
    print(f"  {r.get('tinh')}: W40={r.get('w40', 0):.2%}, diff={r.get('diff', 0):.2%}")

# 8. Rớt LC
print("\n--- RỚT LC 5 TỈNH ---")
for r in d.get('rot_lc', {}).get('tinh', []):
    print(f"  {r.get('tinh')}: W40={r.get('w40', 0):.2%}, diff={r.get('diff', 0):.2%}")
