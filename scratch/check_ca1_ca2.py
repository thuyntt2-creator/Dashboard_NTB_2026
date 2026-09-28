import json, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('data.json', encoding='utf-8') as f:
    d = json.load(f)

print('=== GÁN ĐƠN GIAO LÂM ĐỒNG & TOÀN VÙNG ===')
if 'gan' in d:
    for k, v in d['gan'].items():
        print(k, ':', v)

print('\n=== GTC CA 1 vs CA 2 CÁC TỈNH ===')
if 'gtc_ca1_thuan' in d:
    for p in d['gtc_ca1_thuan'].get('tinh_tts', []):
        print(p)
