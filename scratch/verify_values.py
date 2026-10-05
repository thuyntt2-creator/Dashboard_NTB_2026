import json
import sys
sys.stdout.reconfigure(encoding='utf-8')

d = json.load(open('data.json', encoding='utf-8'))

print("=== CHECKING ACCURACY OF ALL VALUES ===")
# Overview
print("Latest week:", d['meta']['latest_week'])
print("Prev week:", d['meta']['prev_week'])
print("Weeks:", d['meta']['weeks'])
print("Date range:", d['meta']['date_range'])

# San Luong
print("\n--- San Luong Tinh ---")
for t in d['san_luong'].get('tinh', []):
    print(t.get('tinh'), "W40 Full:", t.get('w40_full', t.get('w40')), "TTS:", t.get('w40_tts'))

# GTC Tinh
print("\n--- GTC Tinh ---")
for t in d['gtc_tong'].get('tinh', []):
    print(t.get('tinh'), "W40 Full:", t.get('w40_full', t.get('w40')), "TTS:", t.get('w40_tts'))

# ODR Tinh
print("\n--- ODR Tinh ---")
for t in d['odr'].get('tinh', []):
    print(t.get('tinh'), "W40 Full:", t.get('w40_full', t.get('w40')), "TTS:", t.get('w40_tts'))

# Rot LC
print("\n--- Rot LC ---")
print(d['rot_lc'].get('overview'))

# FD
print("\n--- FD ---")
print("overview:", d['fd'].get('overview'))
print("summary:", d['fd'].get('summary'))

# COD
print("\n--- COD ---")
for m in d['cod_report'].get('metrics', []):
    print(m['chi_so'], "Prev:", m['prev'], "Curr:", m['curr'], "Diff:", m['diff_val'], m['diff_pct'])

# Kinh Doanh
print("\n--- Kinh Doanh ---")
print(d.get('kinh_doanh', {}).get('total'))
