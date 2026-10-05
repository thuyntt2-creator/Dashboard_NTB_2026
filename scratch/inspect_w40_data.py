import json
import sys
sys.stdout.reconfigure(encoding='utf-8')

d = json.load(open('data.json', encoding='utf-8'))

print('=== 1. OVERVIEW ===')
print('Latest:', d['meta']['latest_week'], 'Date:', d['meta']['date_range'])
for c in d['overview']['cards']:
    print(f"  {c['title']}: {c['val']} {c['unit']} (diff: {c['diff']})")

print('\n=== 2. SAN LUONG ===')
if 'tinh' in d['san_luong']:
    for r in d['san_luong']['tinh']:
        print(f"  {r.get('tinh')}: {r}")

print('\n=== 3. GTC TONG ===')
print('  GTC Overview:', d['gtc_tong'].get('overview'))
if 'tinh' in d['gtc_tong']:
    for r in d['gtc_tong']['tinh']:
        print(f"  {r.get('tinh')}: {r}")

print('\n=== 4. GTC CA 1 ===')
print('  GTC CA 1 Thuan:', d['gtc_ca1_thuan'].get('overview'))
print('  GTC CA 1 Ton:', d['gtc_ca1_ton'].get('overview'))

print('\n=== 5. GAN ===')
print('  Gan overview:', d['gan'].get('overview'))

print('\n=== 6. ODR ===')
print('  ODR overview:', d['odr'].get('overview'))

print('\n=== 7. LTC ===')
print('  LTC overview:', d['ltc'].get('overview'))

print('\n=== 8. OPR TTS ===')
if 'opr_tts' in d:
    print('  OPR TTS keys:', d['opr_tts'].keys())
    if 'tinh' in d['opr_tts']:
        for r in d['opr_tts']['tinh']:
            print('   ', r)

print('\n=== 9. ROT LC ===')
print('  Rot LC overview:', d['rot_lc'].get('overview'))

print('\n=== 10. FD ===')
print('  FD overview:', d['fd'].get('overview'))
print('  FD summary:', d['fd'].get('summary'))

print('\n=== 11. KTC ===')
print('  KTC:', d.get('ktc'))

print('\n=== 12. AGING & TREO ===')
print('  Aging:', d.get('aging', {}).get('total'))
print('  Treo LC:', d.get('treo_lc', {}).get('total'))

print('\n=== 13. COD ===')
print('  COD:', d.get('cod_report', {}).get('metrics'))

print('\n=== 14. TRUY THU ===')
print('  Truy thu:', d.get('truy_thu_report', {}).get('summary'))

print('\n=== 15. KINH DOANH ===')
print('  Kinh doanh:', d.get('kinh_doanh', {}).get('total'))
