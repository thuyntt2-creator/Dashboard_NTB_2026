import sys
import json

sys.stdout.reconfigure(encoding='utf-8')

with open('data.json', encoding='utf-8') as f:
    d = json.load(f)

print("=== 1. TỔNG QUAN ===")
print("Date range:", d['meta']['date_range'])
for c in d['overview']['cards']:
    print(f"  {c['id']}: {c['val']} {c['unit']} (diff: {c['diff']})")

print("\n=== 2. SẢN LƯỢNG ===")
print("Full by province:")
for p in sorted(d['san_luong']['tinh_full'], key=lambda x: x['vol'], reverse=True):
    print(f"  {p['tinh']}: W39={p['vol']:,}, W38={p['w38']:,}, diff={p['diff']:+,}")
print("TTS by province:")
for p in sorted(d['san_luong']['tinh_tts'], key=lambda x: x['vol'], reverse=True):
    print(f"  {p['tinh']}: W39={p['vol']:,}, W38={p['w38']:,}, diff={p['diff']:+,}")
print("Top 5 AM Full:")
for a in sorted(d['san_luong']['am_full'], key=lambda x: x['vol'], reverse=True)[:5]:
    print(f"  {a['am']}: W39={a['vol']:,}, W38={a['w38']:,}, diff={a['diff']:+,}")
print("Top 5 AM TTS:")
for a in sorted(d['san_luong']['am_tts'], key=lambda x: x['vol'], reverse=True)[:5]:
    print(f"  {a['am']}: W39={a['vol']:,}, W38={a['w38']:,}, diff={a['diff']:+,}")

print("\n=== 3. GTC TỔNG ===")
for p in sorted(d['gtc_tong']['tinh_full'], key=lambda x: x['w39'], reverse=True):
    print(f"  {p['tinh']}: Full W39={p['w39']*100:.2f}%, W38={p['w38']*100:.2f}%, diff={p['diff']*100:+.2f}%p")
for p in sorted(d['gtc_tong']['tinh_tts'], key=lambda x: x['w39'], reverse=True):
    print(f"  {p['tinh']}: TTS W39={p['w39']*100:.2f}%, W38={p['w38']*100:.2f}%, diff={p['diff']*100:+.2f}%p")

print("\n=== 4. GTC CA 1 SÁNG TTS (Target >= 76%) ===")
if 'gtc_ca1_thuan' in d:
    print("Ca 1 thuan TTS by tinh:")
    for p in sorted(d['gtc_ca1_thuan']['tinh_tts'], key=lambda x: x['w39'], reverse=True):
        print(f"  {p['tinh']}: TTS W39={p['w39']*100:.2f}%, W38={p['w38']*100:.2f}%, diff={p['diff']*100:+.2f}%p")

print("\n=== 5. GÁN ĐƠN GIAO ===")
if 'gan' in d:
    print("gan overview:", d['gan'].get('overview'))

print("\n=== 6. ODR ===")
for p in sorted(d['odr']['tinh_full'], key=lambda x: x['w39'], reverse=True):
    print(f"  {p['tinh']}: Full W39={p['w39']*100:.2f}%, W38={p['w38']*100:.2f}%, diff={p['diff']*100:+.2f}%p")
for p in sorted(d['odr']['tinh_tts'], key=lambda x: x['w39'], reverse=True):
    print(f"  {p['tinh']}: TTS W39={p['w39']*100:.2f}%, W38={p['w38']*100:.2f}%, diff={p['diff']*100:+.2f}%p")

print("\n=== 7. LTC ===")
for p in sorted(d['ltc']['tinh_full'], key=lambda x: x['w39'], reverse=True):
    print(f"  {p['tinh']}: Full W39={p['w39']*100:.2f}%, W38={p['w38']*100:.2f}%, diff={p['diff']*100:+.2f}%p")
for p in sorted(d['ltc']['tinh_tts'], key=lambda x: x['w39'], reverse=True):
    print(f"  {p['tinh']}: TTS W39={p['w39']*100:.2f}%, W38={p['w38']*100:.2f}%, diff={p['diff']*100:+.2f}%p")

print("\n=== 8. OPR TTS ===")
if 'opr_tts' in d:
    print("opr_tts tinh:", d['opr_tts'].get('tinh'))

print("\n=== 9. RỚT LUÂN CHUYỂN ===")
if 'rot_lc' in d:
    print("rot_lc overview:", d['rot_lc'].get('overview'))
    print("rot_lc tinh:", d['rot_lc'].get('tinh'))

print("\n=== 10. FD (HOÀN TRẢ) ===")
if 'fd' in d:
    print("fd overview:", d['fd'].get('overview'))

print("\n=== 11. KTC / VẬN TẢI ===")
if 'ktc' in d:
    print("ktc:", d['ktc'])

print("\n=== 12. AGING & TREO LC ===")
if 'aging' in d:
    print("aging:", d['aging'].get('total'), "total_5_8:", d['aging'].get('total_5_8'))
if 'treo_lc' in d:
    print("treo_lc:", d['treo_lc'].get('total'), "u24:", d['treo_lc'].get('total_u24'), "24_36:", d['treo_lc'].get('total_24_36'), "36_72:", d['treo_lc'].get('total_36_72'))

print("\n=== 13. COD PAYMENT ===")
if 'cod_payment' in d:
    print("cod_payment overview:", d['cod_payment'].get('overview'))

print("\n=== 14. TRUY THU ===")
if 'truy_thu_report' in d:
    print("truy_thu_report:", d['truy_thu_report'].get('summary'))

print("\n=== 15. KINH DOANH & F30 ===")
if 'kinh_doanh' in d:
    print("kinh_doanh total:", d['kinh_doanh'].get('total'))
if 'f30' in d:
    print("f30 total:", d['f30'].get('total'))
