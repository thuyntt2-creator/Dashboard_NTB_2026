import json, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('data.json', encoding='utf-8') as f:
    d = json.load(f)

ams = d.get('opr_tts', {}).get('am', [])
print(f"Tổng số AM trong OPR TTS: {len(ams)} AM")

dat_kpi = []
khong_dat = []

for a in ams:
    name = a['am']
    tot = a['w39_total'] * 100
    day = a['w39_day'] * 100
    night = a['w39_night'] * 100
    vol = a['vol_total']
    diff = a['diff_total'] * 100
    
    info = {
        'name': name,
        'tot': tot,
        'day': day,
        'night': night,
        'vol': vol,
        'diff': diff
    }
    if tot >= 80.0:
        dat_kpi.append(info)
    else:
        khong_dat.append(info)

print(f"\n=== 1. NHÓM ĐẠT KPI OPR TỔNG (>= 80.0%) [{len(dat_kpi)} AM] ===")
for a in sorted(dat_kpi, key=lambda x: x['tot'], reverse=True):
    print(f"• {a['name']}: OPR Tổng = {a['tot']:.2f}% (Ca ngày: {a['day']:.1f}% | Ca đêm: {a['night']:.1f}% | diff: {a['diff']:+.2f}%p | Vol: {a['vol']:,})")

print(f"\n=== 2. NHÓM KHÔNG ĐẠT KPI OPR TỔNG (< 80.0%) [{len(khong_dat)} AM] ===")
for a in sorted(khong_dat, key=lambda x: x['tot'], reverse=True):
    print(f"• {a['name']}: OPR Tổng = {a['tot']:.2f}% (Ca ngày: {a['day']:.1f}% | Ca đêm: {a['night']:.1f}% | diff: {a['diff']:+.2f}%p | Vol: {a['vol']:,})")
