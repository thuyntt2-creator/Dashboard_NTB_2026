import pandas as pd
import glob
import os

csv_files = glob.glob(r"c:\Users\lap4all\Desktop\New folder\*.csv")

output = []
for file in csv_files:
    basename = os.path.basename(file)
    output.append(f"\n=========================================\nCSV: {basename}\n=========================================")
    try:
        df = pd.read_csv(file, nrows=5)
        output.append(f"Columns: {list(df.columns)}")
        output.append(df.to_string())
    except Exception as e:
        output.append(f"Error reading: {e}")

with open(r"c:\Users\lap4all\Desktop\New folder\local_csv_preview.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(output))

print("Local CSV preview written to local_csv_preview.txt")
