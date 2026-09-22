import json

with open('data.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

print("=== 1. ROT LC TOP BC DETAILS ===")
rot_bc = d.get('rot_lc', {}).get('top_bc', [])
for b in rot_bc[:10]:
    print(b)

print("\n=== 1. ROT LC AM DETAILS ===")
rot_am = d.get('rot_lc', {}).get('am', [])
for a in rot_am[:10]:
    print(a.get('am'), 'Vol:', a.get('vol'), 'W37:', a.get('w37'), 'W38:', a.get('w38'), 'Diff:', a.get('diff'))

print("\n=== 2. TRUY THU BY AM ===")
tt = d.get('truy_thu_report', {})
for a in tt.get('by_am', [])[:10]:
    print(a)

print("\n=== 2. TRUY THU TOP BC ===")
for b in tt.get('top_bc', [])[:10]:
    print(b)

print("\n=== 3. KINH DOANH AM ===")
kd = d.get('kinh_doanh', {})
for a in kd.get('am', [])[:10]:
    rev_c = a.get('rev_curr', 0)
    pct = a.get('pct_rev', 0)
    diff = a.get('diff_rev', 0)
    print(f"{a.get('am')}: Rev={rev_c:,.0f} ({pct}%), Diff={diff:,.0f}")

print("\n=== 3. KINH DOANH KHÁCH HÀNG NHÓM A (TOP SHOPS) ===")
kha = kd.get('khach_hang_a', {})
for s in kha.get('shops', [])[:10]:
    print(f"{s.get('shop_name')} | AM: {s.get('am')} | BC: {s.get('bc_name')} | MTD: {s.get('mtd_rev', 0):,.0f} | % sv M-1: {s.get('pct_mtd_prev')}")
