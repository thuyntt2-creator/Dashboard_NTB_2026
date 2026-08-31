import pandas as pd
import urllib.request

url = 'https://docs.google.com/spreadsheets/d/1JZ1eRerRqrpwjZ4HBevQunjd8VquM_cvPFz12TaJfMQ/export?format=csv&gid=1301452336'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
df = pd.read_csv(urllib.request.urlopen(req))

with open('scratch/ntb_sheet_info.txt', 'w', encoding='utf-8') as f:
    f.write(f"Shape: {df.shape}\n")
    f.write(f"Columns:\n")
    for i, col in enumerate(df.columns):
        f.write(f"Col {i} ({chr(65+i)}): {col}\n")
    f.write("\nFirst 10 rows:\n")
    f.write(df.head(10).to_string())
print("Done writing to scratch/ntb_sheet_info.txt")
