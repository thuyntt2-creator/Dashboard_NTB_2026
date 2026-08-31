import urllib.request
import pandas as pd
import io

url = "https://docs.google.com/spreadsheets/d/1JZ1eRerRqrpwjZ4HBevQunjd8VquM_cvPFz12TaJfMQ/export?format=csv&gid=887739629"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req, timeout=30) as response:
        content = response.read()
    df = pd.read_csv(io.BytesIO(content))
    
    with open("scratch/online_sheet_check_res.txt", "w", encoding="utf-8") as f:
        f.write("Columns: " + str(list(df.columns)) + "\n")
        f.write("Shape: " + str(df.shape) + "\n\n")
        
        # Filter for Di Linh, Lam Dong
        f.write("Filtered Di Linh rows:\n")
        di_linh = df[df.astype(str).apply(lambda x: x.str.contains('Di Linh', case=False)).any(axis=1)]
        f.write(di_linh.to_string())
        
        f.write("\n\nAll rows:\n")
        f.write(df.to_string())
    print("Success: results written to scratch/online_sheet_check_res.txt")
except Exception as e:
    with open("scratch/online_sheet_check_res.txt", "w", encoding="utf-8") as f:
        f.write("Error: " + str(e))
    print("Error:", e)
