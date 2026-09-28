import json, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('data.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

rot = d.get('rot_lc', {})
print("=== OVERVIEW ===")
ov = rot.get('overview', {})
print(f"Toan vung W39: {ov.get('rate_curr', 0)*100:.2f}% (W38: {ov.get('rate_prev', 0)*100:.2f}%, Diff: {ov.get('diff', 0)*100:+.2f}%p)")
print(f"Tong don can LC: {ov.get('tot_can')}, Tong don rot: {ov.get('tot_rot')}")

print("\n=== 5 TINH THÀNH ===")
for t in rot.get('tinh', []):
    t_name = t['tinh']
    vol = t.get('vol')
    w_curr = t.get('w_curr', 0) * 100
    w_prev = t.get('w_prev', 0) * 100
    diff = t.get('diff', 0) * 100
    print(f"- {t_name}: Vol={vol}, W39={w_curr:.2f}%, W38={w_prev:.2f}%, Diff={diff:+.2f}%p")

print("\n=== CÁC AM (SẮP XẾP THEO TỶ LỆ RỚT W39 GIẢM DẦN) ===")
for a in sorted(rot.get('am', []), key=lambda x: x.get('w_curr', 0), reverse=True):
    am_name = a['am']
    vol = a.get('vol')
    w_curr = a.get('w_curr', 0) * 100
    w_prev = a.get('w_prev', 0) * 100
    diff = a.get('diff', 0) * 100
    # calculate absolute dropped orders if possible: vol * w_curr / 100
    rot_est = round(vol * a.get('w_curr', 0)) if vol else 0
    print(f"- AM {am_name}: Vol={vol}, Rớt={rot_est} đơn ({w_curr:.2f}%), W38={w_prev:.2f}%, Diff={diff:+.2f}%p")

print("\n=== TOP 10 BƯU CỤC RỚT CAO NHẤT ===")
for b in rot.get('top_bc', [])[:10]:
    bc_name = b.get('bc')
    am = b.get('am')
    vol_can = b.get('vol_can_lc')
    vol_rot = b.get('vol_rot_lc')
    pct = b.get('pct_rot', 0) * 100
    print(f"{b.get('stt')}. {bc_name} (AM {am}): {vol_rot}/{vol_can} đơn ({pct:.1f}%)")
