import json, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('data.js', 'r', encoding='utf-8') as f:
    text = f.read()

prefix = 'window.DASHBOARD_DATA = '
data = json.loads(text[len(prefix):].rstrip(';\n '))

print("=== 18 AMs IN NAM TRUNG BỘ ===")
ams_vol = data.get('san_luong', {}).get('am_full', [])
print(f"Total AMs in san_luong: {len(ams_vol)}")
for a in sorted(ams_vol, key=lambda x: x.get('vol', 0), reverse=True):
    print(f"  {a.get('am')} ({a.get('tinh')}): Vol={a.get('vol'):,}, Diff={a.get('diff')}")

print("\n=== TOP & BOTTOM AMs FOR %GTC ===")
gtc_ams = data.get('gtc_tong', {}).get('am_full', [])
sorted_gtc = sorted([a for a in gtc_ams if a.get('w38') is not None], key=lambda x: x.get('w38', 0), reverse=True)
print("Top 3 GTC:")
for a in sorted_gtc[:3]:
    print(f"  {a.get('am')} ({a.get('tinh')}): W38={a.get('w38')*100:.1f}%, Diff={a.get('diff')*100:+.1f}%p")
print("Bottom 3 GTC:")
for a in sorted_gtc[-3:]:
    print(f"  {a.get('am')} ({a.get('tinh')}): W38={a.get('w38')*100:.1f}%, Diff={a.get('diff')*100:+.1f}%p")

print("\n=== TOP & BOTTOM AMs FOR %ODR ===")
odr_ams = data.get('odr', {}).get('am_full', [])
sorted_odr = sorted([a for a in odr_ams if a.get('w38') is not None], key=lambda x: x.get('w38', 0), reverse=True)
print("Top 3 ODR:")
for a in sorted_odr[:3]:
    print(f"  {a.get('am')} ({a.get('tinh')}): W38={a.get('w38')*100:.1f}%, Diff={a.get('diff')*100:+.1f}%p")
print("Bottom 3 ODR:")
for a in sorted_odr[-3:]:
    print(f"  {a.get('am')} ({a.get('tinh')}): W38={a.get('w38')*100:.1f}%, Diff={a.get('diff')*100:+.1f}%p")

print("\n=== TOP AMs IN AGING (>5 ngày) ===")
aging_ams = data.get('aging', {}).get('top_am', [])
for a in aging_ams[:5]:
    print(f"  {a.get('am')}: {a.get('vol')} đơn ({a.get('pct')}%)")

print("\n=== TOP AMs IN RỚT LUÂN CHUYỂN ===")
rot_ams = data.get('rot_lc', {}).get('am', [])
sorted_rot = sorted(rot_ams, key=lambda x: x.get('vol_rot_lc', 0), reverse=True)
for a in sorted_rot[:5]:
    print(f"  {a.get('am')}: Rớt {a.get('vol_rot_lc')} đơn ({a.get('pct_rot')*100:.1f}%)")

print("\n=== TOP AMs IN %FD HOÀN TRẢ ===")
fd_ams = data.get('fd', {}).get('am', [])
sorted_fd = sorted(fd_ams, key=lambda x: x.get('rate_fd', 0), reverse=True)
for a in sorted_fd[:5]:
    print(f"  {a.get('am')}: {a.get('rate_fd')*100:.1f}% ({a.get('return_orders'):,} / {a.get('total_orders'):,} đơn)")
