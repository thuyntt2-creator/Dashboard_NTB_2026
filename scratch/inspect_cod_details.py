import json, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('data.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

print("=== COD_REPORT SUMMARY ===")
cr = d.get('cod_report', {})
print("overview:", cr.get('overview'))
print("am_comparison (len):", len(cr.get('am_comparison', [])))
for a in cr.get('am_comparison', [])[:6]:
    print("  AM:", a)

print("\n=== TOP BC TIỀN MẶT CAO NHẤT ===")
for b in cr.get('bc_details', [])[:8]:
    print("  BC:", b)

print("\n=== COD_PAYMENT ===")
cp = d.get('cod_payment', {})
if isinstance(cp, dict):
    print("cod_payment keys:", cp.keys())
    for k in cp:
        print(f"  {k}:", str(cp[k])[:300])
