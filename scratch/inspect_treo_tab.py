import sys
import urllib.request
import pandas as pd
import io

sys.stdout.reconfigure(encoding='utf-8')

user_agent = 'Mozilla/5.0'
gid = '213061164' # Treo LC
print(f"Downloading tab 'Treo LC' (GID: {gid})...")
csv_url = f"https://docs.google.com/spreadsheets/d/1JZ1eRerRqrpwjZ4HBevQunjd8VquM_cvPFz12TaJfMQ/export?format=csv&gid={gid}"
req_csv = urllib.request.Request(csv_url, headers={'User-Agent': user_agent})
try:
    with urllib.request.urlopen(req_csv, timeout=30) as response:
        content = response.read()
    df = pd.read_csv(io.BytesIO(content))
    print("Columns:")
    print(df.columns.tolist())
    print("First row:")
    print(df.iloc[0].to_dict() if len(df) > 0 else "Empty")
except Exception as e:
    print(f"Error: {e}")
