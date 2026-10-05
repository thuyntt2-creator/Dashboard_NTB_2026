import json, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('data.json', encoding='utf-8') as f:
    d = json.load(f)

print("=== 1. GAN ===")
print("Overview:", d['gan'].get('overview'))
print("AM Full (first 5):", d['gan'].get('am_full', [])[:5])
print("AM TTS (first 5):", d['gan'].get('am_tts', [])[:5])

print("\n=== 2. ODR ===")
print("Overview:", d['odr'].get('overview'))
print("AM Full (first 5):", d['odr'].get('am_full', [])[:5])
print("AM TTS (first 5):", d['odr'].get('am_tts', [])[:5])
print("Tinh Full:", d['odr'].get('tinh_full', []))

print("\n=== 3. OPR TTS ===")
print("AM (first 5):", d['opr_tts'].get('am', [])[:5])
print("Tinh:", d['opr_tts'].get('tinh', []))

print("\n=== 4. ROT LC ===")
print("Overview:", d['rot_lc'].get('overview'))
print("AM (first 5):", d['rot_lc'].get('am', [])[:5])
print("Top BC:", d['rot_lc'].get('top_bc', [])[:5])

print("\n=== 5. FD ===")
print("Overview:", d['fd'].get('overview'))
print("AM (first 5):", d['fd'].get('am', [])[:5])
print("Top BC (first 5):", d['fd'].get('top_bc', [])[:5])

print("\n=== 6. COD REPORT ===")
print("Summary Text:", d.get('cod_report', {}).get('summary_text'))
print("AM (all):", d.get('cod_report', {}).get('am', []))
print("Top BC (first 5):", d.get('cod_report', {}).get('top_bc', [])[:5])

print("\n=== 7. TRUY THU REPORT ===")
print("Summary:", d.get('truy_thu_report', {}).get('summary'))
print("By AM (first 8):", d.get('truy_thu_report', {}).get('by_am', [])[:8])
print("Top BC Culprit (first 5):", d.get('truy_thu_report', {}).get('top_bc', [])[:5])
