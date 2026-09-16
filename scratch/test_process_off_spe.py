import sys
import json
from app import process_off_spe

sys.stdout.reconfigure(encoding='utf-8')

res = process_off_spe()
print("Total off:", res.get("total_off"))
print("Total pending:", res.get("total_pending"))
print("Records count:", len(res.get("records", [])))
if res.get("records"):
    print("Sample record 0:", json.dumps(res["records"][0], ensure_ascii=False, indent=2))
    print("Sample record 1:", json.dumps(res["records"][1], ensure_ascii=False, indent=2))
    # Check AM values across all records
    ams = set(r.get('am') for r in res.get("records", []))
    print("Unique AMs found in records:", ams)
    # Check status values
    statuses = set(r.get('status') for r in res.get("records", []))
    print("Statuses:", statuses)
    # Check off_time, on_time
    print("Sample times:", [(r.get('post_office'), r.get('off_time'), r.get('on_time'), r.get('pct_cap_down')) for r in res.get("records", [])[:5]])
