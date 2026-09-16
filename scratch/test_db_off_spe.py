import sys
sys.path.insert(0, '.')
from app import load_df_from_db, process_off_spe
import json

df_db = load_df_from_db('off_tuyen_spe.csv')
print("Loaded from DB rows:", len(df_db) if df_db is not None else "None")
if df_db is not None:
    print("DB columns:", list(df_db.columns))

# Now test process_off_spe
res = process_off_spe()
print("\nprocess_off_spe result:")
print("Total off:", res.get("total_off"))
print("Total pending:", res.get("total_pending"))
print("Total records:", len(res.get("records", [])))
print("Sample record 0:")
print(json.dumps(res.get("records", [])[0], ensure_ascii=False, indent=2))
print("Sample record -1:")
print(json.dumps(res.get("records", [])[-1], ensure_ascii=False, indent=2))
