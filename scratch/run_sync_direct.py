import sys
import os
import pandas as pd
from dotenv import load_dotenv

# Ensure we can load app modules
sys.path.append(os.getcwd())
load_dotenv()

from app import sync_sheets_directly_as_csv, update_all_caches

url = os.environ.get("CONSOLIDATED_URL")
print("Using CONSOLIDATED_URL:", url)

success, msg = sync_sheets_directly_as_csv(url)
print("Sync success:", success)
print("Sync message:", msg)

if success:
    print("Updating caches...")
    update_all_caches()
    print("Caches updated successfully.")
