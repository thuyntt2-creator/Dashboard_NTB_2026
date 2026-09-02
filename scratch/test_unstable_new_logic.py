import sys
import os
import json
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.abspath('.'))

from app import process_unstable_po

res = process_unstable_po()
print("Error:", res.get("error"))
print("Update time:", res.get("update_time"))
print("Total warning count:", res.get("total_warning"))
print("Records count:", len(res.get("records", [])))

print("\n--- Unstable POs List ---")
for r in res.get("records", []):
    if r.get("status") == "Bất ổn":
        print(f"[{r.get('id')}] {r.get('name')} ({r.get('province')}, AM: {r.get('am')}) - %GTC 7D: {r.get('pct_gtc_7d')}% (Best: {r.get('pct_gtc_best')}%) -> {r.get('reason')}")
