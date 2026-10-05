import json
import sys

sys.stdout.reconfigure(encoding='utf-8')
with open('data.json', encoding='utf-8') as f:
    d = json.load(f)

print("=== GTC TONG TINH ===")
for t in d['gtc_tong'].get('tinh_full', []):
    print(t['tinh'], f"W40: {t.get('w40', 0)*100:.2f}%", f"W39: {t.get('w39', 0)*100:.2f}%")

print("\n=== ODR TINH ===")
for t in d['odr'].get('tinh_full', []):
    print(t['tinh'], f"W40: {t.get('w40', 0)*100:.2f}%", f"W39: {t.get('w39', 0)*100:.2f}%")

print("\n=== LTC TINH ===")
for t in d['ltc'].get('tinh_full', []):
    print(t['tinh'], f"W40: {t.get('w40', 0)*100:.2f}%", f"W39: {t.get('w39', 0)*100:.2f}%")

print("\n=== OPR TTS TINH ===")
for t in d.get('opr_tts', {}).get('tinh', []):
    print(t)

print("\n=== ROT LC TINH ===")
for t in d.get('rot_lc', {}).get('tinh', []):
    print(t)

print("\n=== COD PAYMENT PROVINCES ===")
for t in d.get('cod_payment', {}).get('provinces', []):
    print(t)

print("\n=== TRUY THU BY PROVINCE ===")
for t in d.get('truy_thu_report', {}).get('by_province', []):
    print(t)
