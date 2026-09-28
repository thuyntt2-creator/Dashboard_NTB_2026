import json, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('data.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

ttr = d.get('truy_thu_report', {})
print("ALL AMs TRUY THU:")
for a in ttr.get('by_am', []):
    print(f"- {a.get('am')}: Tickets={a.get('ticket_curr')} ({a.get('pct_ticket_diff')}), Cần thu={a.get('can_thu_curr'):,.0f} đ ({a.get('pct_can_thu_diff')}), Level={a.get('level')}, Top BC={a.get('top_bc_culprit')}")

print("\nALL BƯU CỤC CẢNH BÁO:")
for i, b in enumerate(d.get('bc_canh_bao', [])):
    print(f"{i+1}. {b.get('bc')} ({b.get('tinh')} - AM {b.get('am')}): GTC={b.get('gtc_w37')}%, Backlog={b.get('backlog')}, 5d={b.get('backlog_5d')}, Warn={b.get('warn_type')}")
