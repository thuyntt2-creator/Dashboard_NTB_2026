import sys, json
sys.stdout.reconfigure(encoding='utf-8')
with open('data.json', 'r', encoding='utf-8') as f:
    D = json.load(f)

print('=== FD CHI TIET ===')
fd = D.get('fd', {})
print('Summary:', fd.get('summary'))
print('AM list:')
for am in fd.get('am', [])[:20]:
    r35 = am.get('rate_w35_full', am.get('rate_w35', 0)) or 0
    r36 = am.get('rate_w36_full', am.get('rate_w36', 0)) or 0
    print(f"  {am.get('am','')}: FD Full W35={r35*100:.1f}% W36={r36*100:.1f}% diff={(r36-r35)*100:+.1f}%")

print('\nTop BC FD:')
for bc in fd.get('top_bc', [])[:10]:
    print(f"  {bc}")

print('\n=== LTC AM FULL ===')
ltc = D.get('ltc', {})
for am in ltc.get('am_full', [])[:20]:
    w35 = am.get('w35', 0) or 0
    w36 = am.get('w36', 0) or 0
    print(f"  {am.get('am','')}: W35={w35*100:.1f}% W36={w36*100:.1f}% diff={(w36-w35)*100:+.1f}%")

print('\n=== LTC TINH FULL ===')
for t in ltc.get('tinh_full', [])[:10]:
    w35 = t.get('w35', 0) or 0
    w36 = t.get('w36', 0) or 0
    print(f"  {t.get('tinh','')}: W35={w35*100:.1f}% W36={w36*100:.1f}% diff={(w36-w35)*100:+.1f}%")

print('\n=== GTC TONG CA2 ===')
gtc = D.get('gtc_tong', {})
print('Summary ca2:', gtc.get('summary_ca2', {}))
for am in gtc.get('am', [])[:10]:
    r35 = am.get('w35_ca2', am.get('w35', 0)) or 0
    r36 = am.get('w36_ca2', am.get('w36', 0)) or 0

print('\n=== GAN SUMMARY ===')
gan = D.get('gan', {})
print('Keys:', list(gan.keys())[:10])
for k in list(gan.keys())[:5]:
    v = gan[k]
    if isinstance(v, list):
        print(f'  {k}: [{len(v)} items] sample:', str(v[0])[:200] if v else '')
    else:
        print(f'  {k}:', str(v)[:200])

print('\n=== GAN TONG SUMMARY ===')
gan_ov = gan.get('overview', {})
print(gan_ov)
gan_sum = gan.get('summary', {})
print(gan_sum)
