import json, sys
sys.stdout.reconfigure(encoding='utf-8')
d = json.load(open('data.json', encoding='utf-8'))
gtc = d.get('gtc_tong', {})

print('OVERVIEW:')
for ov in gtc.get('overview', []):
    print(ov)

print('\nAM FULL (sorted by w37 desc):')
ams_full = sorted(gtc.get('am_full', []), key=lambda x: x.get('w37', 0), reverse=True)
for a in ams_full:
    w36 = a.get('w36', 0) * 100
    w37 = a.get('w37', 0) * 100
    diff = a.get('diff', 0) * 100
    print(f"{a['am']}: w36={w36:.1f}%, w37={w37:.1f}%, diff={diff:+.1f}%")

print('\nAM TTS (sorted by w37 desc):')
ams_tts = sorted(gtc.get('am_tts', []), key=lambda x: x.get('w37', 0), reverse=True)
for a in ams_tts:
    w36 = a.get('w36', 0) * 100
    w37 = a.get('w37', 0) * 100
    diff = a.get('diff', 0) * 100
    print(f"{a['am']}: w36={w36:.1f}%, w37={w37:.1f}%, diff={diff:+.1f}%")

print('\nTINH FULL:')
for t in gtc.get('tinh_full', []):
    print(t)
