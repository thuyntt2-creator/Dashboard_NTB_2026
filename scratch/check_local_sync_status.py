import requests
import json
try:
    res = requests.get("http://127.0.0.1:5000/api/sync/status", auth=('admin', 'admin123'))
    with open("scratch/local_sync_status.txt", "w", encoding="utf-8") as f:
        f.write(f"Status code: {res.status_code}\n")
        f.write(f"Response JSON: {res.json()}\n")
    print("Done")
except Exception as e:
    with open("scratch/local_sync_status.txt", "w", encoding="utf-8") as f:
        f.write(f"Error: {e}\n")
    print("Error written")
