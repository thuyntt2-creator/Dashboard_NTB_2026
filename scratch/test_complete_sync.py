import sys
import os
sys.path.insert(0, os.getcwd())
from dotenv import load_dotenv

sys.stdout.reconfigure(encoding='utf-8')
load_dotenv(override=True)

# Set is_vercel simulation or just run normal
from app import sync_sheets_directly_as_csv, get_dataframes

url = "https://docs.google.com/spreadsheets/d/1JZ1eRerRqrpwjZ4HBevQunjd8VquM_cvPFz12TaJfMQ/edit"

print("1. Running sync_sheets_directly_as_csv...")
success, msg = sync_sheets_directly_as_csv(url)
print(f"Sync success: {success}, msg: {msg}")

if not success:
    print("Sync failed! Exiting.")
    sys.exit(1)

print("\n2. Building dataframes cache (get_dataframes)...")
try:
    dfs = get_dataframes(force=True)
    print("Success! Dataframes loaded successfully.")
    print("GTC columns:", dfs[0].columns.tolist() if dfs[0] is not None else "None")
    print("LTC columns:", dfs[1].columns.tolist() if dfs[1] is not None else "None")
    print("Aging columns:", dfs[2].columns.tolist() if dfs[2] is not None else "None")
except Exception as e:
    import traceback
    print(f"Error occurred: {e}")
    traceback.print_exc()
