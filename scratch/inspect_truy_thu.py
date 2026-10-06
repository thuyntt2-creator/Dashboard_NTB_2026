import json, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('data.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

ttr = d.get('truy_thu_report', {})
print('=== SUMMARY ===')
print('total_can_thu_curr:', ttr.get('total_can_thu'))
print('total_can_thu_prev:', ttr.get('total_can_thu_prev'))
print('total_records_curr:', ttr.get('total_records'))

print('\n=== BY LOAI TRUY THU (sorted by can_thu_curr desc) ===')
by_loai = sorted(ttr.get('by_loai', []), key=lambda x: x.get('can_thu_curr', 0), reverse=True)
for item in by_loai:
    curr = item.get('can_thu_curr', 0)
    prev = item.get('can_thu_prev', 0)
    diff = item.get('diff_can_thu', 0)
    don = item.get('don_curr', 0)
    print(f"- {item.get('loai')}: {curr:,.0f} đ (W_prev: {prev:,.0f} đ, Δ: {diff:,.0f} đ, {don} đơn) - Đánh giá: {item.get('eval')}")

print('\n=== BY AM TRUY THU ===')
by_am = sorted(ttr.get('by_am', []), key=lambda x: x.get('can_thu_curr', 0), reverse=True)
for item in by_am:
    curr = item.get('can_thu_curr', 0)
    prev = item.get('can_thu_prev', 0)
    diff = item.get('diff_can_thu', 0)
    ticket = item.get('ticket_curr', 0)
    print(f"- AM {item.get('am')}: {curr:,.0f} đ (W_prev: {prev:,.0f} đ, Δ: {diff:,.0f} đ, {ticket} ticket, BC: {item.get('top_bc_culprit')}) - {item.get('level')}")

print('\n=== TOP 10 BUU CUC TRUY THU ===')
top_bc = sorted(ttr.get('top_bc', []), key=lambda x: x.get('can_thu_curr', 0), reverse=True)
for i, item in enumerate(top_bc[:10], 1):
    curr = item.get('can_thu_curr', 0)
    prev = item.get('can_thu_prev', 0)
    diff = item.get('diff_can_thu', 0)
    don = item.get('don_curr', 0)
    print(f"{i}. {item.get('bc')} ({item.get('tinh')} - AM {item.get('am')}): {curr:,.0f} đ (W_prev: {prev:,.0f} đ, Δ: {diff:,.0f} đ, {don} đơn)")

print('\n=== TAB 14 TRUY THU OLD IN d[\"truy_thu\"] ===')
tt = d.get('truy_thu', {})
print('keys:', list(tt.keys()))
if 'types' in tt:
    print('types in truy_thu:', json.dumps(tt['types'], indent=2, ensure_ascii=False)[:500])
if 'top_bc' in tt:
    print('top_bc in truy_thu sample:', json.dumps(tt['top_bc'][:3], indent=2, ensure_ascii=False))
