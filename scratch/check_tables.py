# -*- coding: utf-8 -*-
import json, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('data.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

print("="*50)
print("1. SẢN LƯỢNG GIAO (Full hàng) THEO TỈNH:")
for r in d.get('san_luong', {}).get('tinh_full', []):
    pct = (r['diff'] / r['w36']) * 100 if r.get('w36') else 0
    print(f"  - {r['tinh']}: W37 = {r['w37']:,} đơn (W36 = {r['w36']:,}, Δ = +{r['diff']:,} đơn, +{pct:.1f}% WoW)")

print("\n" + "="*50)
print("2. SẢN LƯỢNG GIAO (TTS) THEO TỈNH:")
for r in d.get('san_luong', {}).get('tinh_tts', []):
    pct = (r['diff'] / r['w36']) * 100 if r.get('w36') else 0
    print(f"  - {r['tinh']}: W37 = {r['w37']:,} đơn (W36 = {r['w36']:,}, Δ = +{r['diff']:,} đơn, +{pct:.1f}% WoW)")

print("\n" + "="*50)
print("3. %GTC TỔNG OVERVIEW:")
for r in d.get('gtc_tong', {}).get('overview', []):
    print(f"  - {r['label']}: W36 = {r['w36']*100:.2f}%, W37 = {r['w37']*100:.2f}%, Δ = {r['diff']*100:+.2f}%p")

print("\n" + "="*50)
print("4. %GTC TỔNG (Full hàng) - XẾP HẠNG THEO %GTC W37 CAO NHẤT ĐẾN THẤP NHẤT:")
am_sorted_w37 = sorted(d.get('gtc_tong', {}).get('am_full', []), key=lambda x: x['w37'], reverse=True)
for idx, r in enumerate(am_sorted_w37, 1):
    print(f"  {idx}. AM {r['am']}: W37 = {r['w37']*100:.2f}% (W36 = {r['w36']*100:.2f}%, Δ = {r['diff']*100:+.2f}%p, SL = {r['vol']:,})")

print("\n" + "="*50)
print("5. %GTC TỔNG (Full hàng) - XẾP HẠNG THEO TĂNG TRƯỞNG Δ WoW TỐT NHẤT ĐẾN GIẢM MẠNH NHẤT:")
am_sorted_diff = sorted(d.get('gtc_tong', {}).get('am_full', []), key=lambda x: x['diff'], reverse=True)
for idx, r in enumerate(am_sorted_diff, 1):
    print(f"  {idx}. AM {r['am']}: Δ = {r['diff']*100:+.2f}%p (W36 = {r['w36']*100:.2f}% -> W37 = {r['w37']*100:.2f}%)")

print("\n" + "="*50)
print("6. %GTC TỔNG THEO TỈNH (nếu có):")
for r in d.get('gtc_tong', {}).get('tinh_full', []):
    print(f"  - {r.get('tinh')}: W37 = {r['w37']*100:.2f}% (W36 = {r['w36']*100:.2f}%, Δ = {r['diff']*100:+.2f}%p)")

print("\n" + "="*50)
print("7. SẢN LƯỢNG AM TOP TĂNG TRƯỞNG:")
sl_am_sorted = sorted(d.get('san_luong', {}).get('am_full', []), key=lambda x: x['diff'], reverse=True)
for idx, r in enumerate(sl_am_sorted[:6], 1):
    pct = (r['diff'] / r['w36']) * 100 if r.get('w36') else 0
    print(f"  {idx}. AM {r['am']}: W37 = {r['w37']:,} đơn (W36 = {r['w36']:,}, Δ = +{r['diff']:,} đơn, +{pct:.1f}%)")
