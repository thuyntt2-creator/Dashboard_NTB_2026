import sys, json
sys.stdout.reconfigure(encoding='utf-8')
with open('data.json', 'r', encoding='utf-8') as f:
    D = json.load(f)

# Extract key numbers for W36 script
print('=== VOLUME ===')
ov = D.get('overview', {})
for card in ov.get('cards', []):
    val = card['val']
    diff = card.get('diff', 0)
    if card['unit'] == '%':
        print(f"{card['title']}: {val*100:.1f}% (diff: {diff*100:+.1f}%)")
    elif card['unit'] == 'VNĐ':
        print(f"{card['title']}: {val:,.0f} VNĐ (diff: {diff/1e6:+.1f}M)")
    else:
        print(f"{card['title']}: {val:,.0f} {card['unit']} (diff: {diff:+,.0f})")

print('\n=== GTC THEO AM (W35 vs W36) ===')
gtc = D.get('gtc_tong', {})
for am in gtc.get('am', [])[:20]:
    w35 = am.get('w35', 0) or 0
    w36 = am.get('w36', 0) or 0
    diff = am.get('diff', w36-w35)
    print(f"  {am['am']}: W35={w35*100:.1f}% W36={w36*100:.1f}% diff={diff*100:+.1f}%")

print('\n=== ODR THEO TINH ===')
odr = D.get('odr', {})
for t in odr.get('tinh', []):
    w35 = t.get('w35', 0) or 0
    w36 = t.get('w36', 0) or 0
    print(f"  {t.get('tinh','')}: W35={w35*100:.1f}% W36={w36*100:.1f}% diff={(w36-w35)*100:+.1f}%")

print('\n=== LTC ===')
ltc = D.get('ltc', {})
print('LTC full:', ltc.get('summary_full', {}))
print('LTC TTS:', ltc.get('summary_tts', {}))

print('\n=== ROT LC TOP AM ===')
rot = D.get('rot_lc', {})
for am in sorted(rot.get('am', []), key=lambda x: x.get('w36',0) or 0, reverse=True)[:5]:
    print(f"  {am['am']}: W36={am.get('w36',0)*100:.2f}%")

print('\n=== COMMERCIAL ===')
comm = D.get('commercial', {})
f30 = comm.get('f30', {})
print('F30:', f30)
truy_thu = comm.get('truy_thu_report', {})
print('Truy thu overview:', list(truy_thu.keys())[:5] if truy_thu else 'N/A')
