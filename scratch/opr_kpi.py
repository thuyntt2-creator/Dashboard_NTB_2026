import sys, json
sys.stdout.reconfigure(encoding='utf-8')
with open('data.json', 'r', encoding='utf-8') as f:
    D = json.load(f)

opr = D.get('opr_tts', {})
KPI = 0.80

ams = opr.get('am', [])

# Tính tổng vùng (weighted)
total_vol_day = sum(r.get('vol_day', 0) for r in ams)
total_vol_night = sum(r.get('vol_night', 0) for r in ams)
wtd_day = sum(r.get('vol_day', 0) * r.get('w36_day', 0) for r in ams)
wtd_night = sum(r.get('vol_night', 0) * r.get('w36_night', 0) for r in ams)
vung_day = wtd_day / total_vol_day if total_vol_day else 0
vung_night = wtd_night / total_vol_night if total_vol_night else 0

# W35 vung
wtd_day35 = sum(r.get('vol_day', 0) * r.get('w35_day', 0) for r in ams)
wtd_night35 = sum(r.get('vol_night', 0) * r.get('w35_night', 0) for r in ams)
vung_day35 = wtd_day35 / total_vol_day if total_vol_day else 0
vung_night35 = wtd_night35 / total_vol_night if total_vol_night else 0

print('=== OPR TTS TOAN VUNG W36 ===')
print(f'Ca Ngay:  W35={vung_day35*100:.1f}% -> W36={vung_day*100:.1f}%  ({(vung_day-vung_day35)*100:+.1f}%p)')
print(f'Ca Dem:   W35={vung_night35*100:.1f}% -> W36={vung_night*100:.1f}%  ({(vung_night-vung_night35)*100:+.1f}%p)')
print()

# Phân loại AM theo KPI
ok_day = []
fail_day = []
ok_night = []
fail_night = []

for r in sorted(ams, key=lambda x: x.get('w36_day', 0)):
    am = r['am']
    vd = r.get('w36_day', 0)
    vn = r.get('w36_night', 0)
    dd = r.get('diff_day', 0)
    dn = r.get('diff_night', 0)
    vold = r.get('vol_day', 0)

    if vd >= KPI:
        ok_day.append((am, vd, dd))
    else:
        fail_day.append((am, vd, dd, vold))

    if vn >= KPI:
        ok_night.append((am, vn, dn))
    else:
        fail_night.append((am, vn, dn))

print(f'=== CA NGAY (KPI >= {KPI*100:.0f}%) ===')
print(f'CHUA DAT ({len(fail_day)} AM):')
for am, v, d, vol in sorted(fail_day, key=lambda x: x[1]):
    gap = (KPI - v) * 100
    print(f'  ❌ {am}: {v*100:.1f}%  ({d*100:+.1f}%p WoW)  | Cach KPI: -{gap:.1f}%p')

print()
print(f'DA DAT ({len(ok_day)} AM):')
for am, v, d in sorted(ok_day, key=lambda x: -x[1]):
    print(f'  ✅ {am}: {v*100:.1f}%  ({d*100:+.1f}%p WoW)')

print()
print(f'=== CA DEM (KPI >= {KPI*100:.0f}%) ===')
print(f'CHUA DAT ({len(fail_night)} AM):')
for am, v, d in sorted(fail_night, key=lambda x: x[1]):
    gap = (KPI - v) * 100
    print(f'  ❌ {am}: {v*100:.1f}%  ({d*100:+.1f}%p WoW)  | Cach KPI: -{gap:.1f}%p')

print()
print(f'DA DAT ({len(ok_night)} AM):')
for am, v, d in sorted(ok_night, key=lambda x: -x[1]):
    print(f'  ✅ {am}: {v*100:.1f}%  ({d*100:+.1f}%p WoW)')
