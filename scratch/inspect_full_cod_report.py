import json, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('data.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

cr = d.get('cod_report', {})
print("=== METRICS ===")
for m in cr.get('metrics', []):
    print(m)

print("\n=== AM COMPARISON ===")
for a in cr.get('am_comparison', []):
    print(f"{a.get('stt')}. {a.get('am')}: W38={a.get('prev_tm')} -> W39={a.get('curr_tm')} ({a.get('diff')}) -- {a.get('level')}")

print("\n=== TOP BC TIỀN MẶT ===")
for b in cr.get('bc_details', [])[:10]:
    print(f"- {b.get('bc')} (AM {b.get('am')}): W38={b.get('prev_tm')} -> W39={b.get('curr_tm')} ({b.get('diff')}), TM={b.get('cash_m')} Tr -- {b.get('level')}")
