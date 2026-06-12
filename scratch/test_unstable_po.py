import os
import sys
sys.path.insert(0, os.getcwd())

from app import process_unstable_po
import json

res = process_unstable_po()
print("Result fields:", list(res.keys()))
if "error" in res:
    print("Error:", res["error"])
else:
    print("Total warning:", res["total_warning"])
    print("Update time:", res["update_time"])
    print("Number of records:", len(res["records"]))
    if len(res["records"]) > 0:
        print("First record:", res["records"][0])
        print("Unique statuses:", set(r["status"] for r in res["records"]))
        print("AM deepdive:", res["am_deepdive"])
