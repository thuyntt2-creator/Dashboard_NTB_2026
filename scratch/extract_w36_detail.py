import sys, json
sys.stdout.reconfigure(encoding='utf-8')
with open('data.json', 'r', encoding='utf-8') as f:
    D = json.load(f)

# More detailed extraction
print('=== GTC CA1 TTS THEO AM ===')
gtc_ca1 = D.get('gtc_tts_ca1', {})
for am in gtc_ca1.get('am', [])[:20]:
    w35 = am.get('w35', 0) or 0
    w36 = am.get('w36', 0) or 0
    diff = w36 - w35
    print(f"  {am.get('am','')}: W35={w35*100:.1f}% W36={w36*100:.1f}% diff={diff*100:+.1f}%")

print('\n=== GAN THEO AM ===')
gan = D.get('gan', {})
for am in gan.get('am', [])[:10]:
    w35 = am.get('w35', 0) or 0
    w36 = am.get('w36', 0) or 0
    print(f"  {am.get('am','')}: W35={w35*100:.1f}% W36={w36*100:.1f}% diff={(w36-w35)*100:+.1f}%")
if gan.get('summary'):
    print('  Summary:', gan['summary'])

print('\n=== ODR BY AM ===')
odr = D.get('odr', {})
for am in odr.get('am', [])[:20]:
    w35 = am.get('w35', 0) or 0
    w36 = am.get('w36', 0) or 0
    print(f"  {am.get('am','')}: W35={w35*100:.1f}% W36={w36*100:.1f}% diff={(w36-w35)*100:+.1f}%")

print('\n=== VOL BY AM ===')
vol = D.get('volume', {})
for am in vol.get('am', [])[:10]:
    w35 = am.get('w35', 0) or 0
    w36 = am.get('w36', 0) or 0
    print(f"  {am.get('am','')}: W35={w35:,.0f} W36={w36:,.0f} diff={(w36-w35):+,.0f}")

print('\n=== LTC ===')
ltc = D.get('ltc', {})
for k in list(ltc.keys())[:5]:
    print(f'  {k}:', str(ltc[k])[:200])

print('\n=== ROT LC BY BUUCUC ===')
rot = D.get('rot_lc', {})
top_bc = sorted(rot.get('buu_cuc', []), key=lambda x: x.get('w36',0) or 0, reverse=True)[:5]
for bc in top_bc:
    print(f"  {bc.get('buu_cuc','')}: {bc.get('w36',0)*100:.2f}%")

print('\n=== FD DATA ===')
fd = D.get('fd', {})
for k in list(fd.keys())[:8]:
    val = fd[k]
    if isinstance(val, dict):
        print(f'  {k}:', list(val.keys())[:5])
    elif isinstance(val, list):
        print(f'  {k}: list({len(val)})')
    else:
        print(f'  {k}:', str(val)[:100])

print('\n=== KTC DATA ===')
ktc = D.get('ktc', {})
if ktc:
    bl = ktc.get('backlog', {})
    tot = bl.get('total_am', {})
    print('Backlog total:', tot)
    fr = ktc.get('fill_rate', {})
    wtot = fr.get('weekly', {}).get('total', {})
    print('Fill rate W36 total:', wtot)

print('\n=== COMMERCIAL ===')
comm = D.get('commercial', {})
print('Keys:', list(comm.keys())[:10])
for k in list(comm.keys())[:10]:
    v = comm[k]
    if isinstance(v, list):
        print(f'  {k}: {len(v)} items')
        if v:
            print('    sample:', str(v[0])[:150])
    elif isinstance(v, dict):
        print(f'  {k}: dict with keys', list(v.keys())[:5])
    else:
        print(f'  {k}:', str(v)[:100])
