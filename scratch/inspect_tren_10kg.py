import sys, requests, io
import pandas as pd

sys.stdout.reconfigure(encoding='utf-8')

sheet_id = "1JZ1eRerRqrpwjZ4HBevQunjd8VquM_cvPFz12TaJfMQ"
gid = "1203902008"

csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid}"
print(f"Fetching CSV from: {csv_url}")

res = requests.get(csv_url)
print(f"Status code: {res.status_code}")

if res.status_code == 200:
    df = pd.read_csv(io.BytesIO(res.content), header=None)
    print(f"Total shape: {df.shape}")
    print("\nFirst 15 rows preview:")
    for idx, row in df.head(15).iterrows():
        non_empty = [f"Col{i}: {val}" for i, val in enumerate(row) if pd.notnull(val) and str(val).strip() != '']
        print(f"Row {idx}: {non_empty[:10]}")
    
    # Save raw csv for inspection
    with open("scratch/raw_tren10kg.csv", "wb") as f:
        f.write(res.content)
    print("\nSaved scratch/raw_tren10kg.csv")
else:
    print(f"Failed to fetch CSV: {res.text[:200]}")
