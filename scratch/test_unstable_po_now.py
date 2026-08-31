import sys
sys.path.append('.')
from app import process_unstable_po

res = process_unstable_po()
print("Keys:", res.keys() if isinstance(res, dict) else type(res))
if isinstance(res, dict) and "records" in res:
    print("Total records:", len(res["records"]))
    if len(res["records"]) > 0:
        print("Sample record 0:", res["records"][0])
        print("Sample record 1:", res["records"][1])
