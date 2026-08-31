import os, sys
sys.path.insert(0, os.path.abspath('.'))
sys.stdout.reconfigure(encoding='utf-8')

import app

print("Testing sync mapping...")
config = app.load_config()
url = config.get("consolidated_url", "https://docs.google.com/spreadsheets/d/1JZ1eRerRqrpwjZ4HBevQunjd8VquM_cvPFz12TaJfMQ/edit")

print("Url:", url)
success, msg = app.sync_sheets_directly_as_csv(url)
print("Sync result:", success, msg)
