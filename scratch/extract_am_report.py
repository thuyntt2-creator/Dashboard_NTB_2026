import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('data.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

# 1. AM Business (KD)
kd_ams = d.get('kinh_doanh', {}).get('am', [])
print('=== TOP AM KINH DOANH (Doanh thu & Diff) ===')
for a in kd_ams[:10]:
    r_c = a.get('rev_curr', 0) / 1e6
    pct = a.get('pct_diff_rev', 0)
    v_c = a.get('vol_curr', 0)
    v_diff = a.get('diff_vol', 0)
    print(f"  {a.get('am')}: Rev={r_c:,.1f} Tr ({pct:+.1f}%), Vol={v_c:,} ({v_diff:+,})")

# Bottom AM KD (Drops)
print('\n=== BOTTOM AM KINH DOANH (Sụt giảm mạnh nhất) ===')
sorted_drop = sorted(kd_ams, key=lambda x: x.get('diff_rev', 0))
for a in sorted_drop[:7]:
    r_diff = a.get('diff_rev', 0) / 1e6
    pct = a.get('pct_diff_rev', 0)
    v_diff = a.get('diff_vol', 0)
    print(f"  {a.get('am')}: Diff Rev={r_diff:+,.1f} Tr ({pct:+.1f}%), Diff Vol={v_diff:+,}")

# 2. AM F30
f30_ams = d.get('f30', {}).get('am', [])
print('\n=== TOP AM F30 (Shop mới) ===')
for a in f30_ams[:10]:
    k_c = a.get('kh_curr', 0)
    d_k = a.get('diff_kh', 0)
    r_c = a.get('rev_curr', 0) / 1e6
    print(f"  {a.get('am')}: KH={k_c} (diff={d_k:+d}), Rev={r_c:,.2f} Tr")

# 3. AM Truy Thu
tt_ams = d.get('truy_thu_report', {}).get('by_am', [])
print('\n=== TOP AM TRUY THU (Tiền cần thu W40) ===')
for a in tt_ams[:10]:
    c_c = a.get('can_thu_curr', 0) / 1e6
    c_p = a.get('can_thu_prev', 0) / 1e6
    d_c = a.get('diff_can_thu', 0) / 1e6
    tk = a.get('ticket_curr', 0)
    lvl = a.get('level', '')
    top_bc = a.get('top_bc_culprit', '')
    print(f"  {a.get('am')}: Cần thu={c_c:,.1f} Tr (W39={c_p:,.1f} Tr, diff={d_c:+,.1f} Tr), Ticket={tk} | {lvl} | Điểm nóng: {top_bc}")

# 4. AM Quality / Ops (ODR, Aging, Backlog)
ams_ops = d.get('ams', [])
print('\n=== AM OPS METRICS (ODR, Backlog...) ===')
for a in ams_ops[:10]:
    name = a.get('name')
    odr = a.get('odr')
    gtc = a.get('gtc')
    vol = a.get('vol_w40') or a.get('vol')
    print(f"  {name}: ODR={odr}, GTC={gtc}, Vol={vol}")

# Check bc_canh_bao
bc_cb = d.get('bc_canh_bao', [])
print('\n=== BƯU CỤC CẢNH BÁO / BẤT ỔN ===')
print(f"Total bưu cục cảnh báo: {len(bc_cb)}")
for b in bc_cb[:8]:
    print(f"  {b.get('bc') or b.get('name')} (AM: {b.get('am')}): Lý do: {b.get('ly_do') or b.get('reason') or b.get('risk')}")
