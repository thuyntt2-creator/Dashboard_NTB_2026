import pandas as pd
import traceback
import sys
import os

sys.path.insert(0, os.getcwd())
from app import get_dataframes, process_treo_backlog, update_all_caches

try:
    print("Running update_all_caches() directly in main thread...")
    update_all_caches()
    
    import app
    print("DF_TREO_CACHE shape:", app.DF_TREO_CACHE.shape if app.DF_TREO_CACHE is not None else "None")
    if app.DF_TREO_CACHE is not None:
        print("DF_TREO_CACHE columns:", app.DF_TREO_CACHE.columns.tolist())
        
    print("Calling process_treo_backlog(df_raw=app.DF_TREO_CACHE)...")
    res = process_treo_backlog(df_raw=app.DF_TREO_CACHE, df_co_cau=None)
    print("Result:", res if "error" in res else f"Success with {len(res.get('raw_records', []))} records")
except Exception as e:
    print("Caught Exception:")
    traceback.print_exc()
