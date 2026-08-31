import pandas as pd
import os

path = "Copy o NTB - BÁO CÁO VẬN HÀNH.xlsx"
out_path = "scratch/latest_dates.txt"

with open(out_path, "w", encoding="utf-8") as f:
    f.write("=== LATEST DATES IN FILES ===\n")
    
    # Check Excel sheets
    if os.path.exists(path):
        xls = pd.ExcelFile(path, engine='openpyxl', engine_kwargs={'read_only': True})
        for sname in ['Data', 'raw', 'TTS', 'DataLTC', 'ODR TTS']:
            if sname in xls.sheet_names:
                df = pd.read_excel(xls, sheet_name=sname)
                # Find date column
                date_col = None
                for c in df.columns:
                    if 'time' in c.lower() or 'ngay' in c.lower():
                        date_col = c
                        break
                if date_col:
                    unique_dates = df[date_col].dropna().unique().tolist()
                    # sort them if possible
                    try:
                        sorted_dates = sorted(unique_dates)
                        f.write(f"Sheet '{sname}' max date: {sorted_dates[-1]} (total unique: {len(sorted_dates)})\n")
                        f.write(f"Latest 5 dates in '{sname}': {sorted_dates[-5:]}\n")
                    except Exception as e:
                        f.write(f"Sheet '{sname}' unique dates (first 5): {unique_dates[:5]} (error sorting: {e})\n")
    
    # Check CSV files
    for csv_file in ['ops_gtc.csv', 'ops_ltc.csv', 'ops_fd.csv', 'ODR TTS.csv', 'buu_cuc_bat_on.csv', 'opr_raw.csv']:
        if os.path.exists(csv_file):
            try:
                df = pd.read_csv(csv_file)
                date_col = None
                for c in df.columns:
                    if 'time' in c.lower() or 'ngay' in c.lower() or 'date' in c.lower() or 'snapshot' in c.lower():
                        date_col = c
                        break
                if date_col:
                    unique_dates = df[date_col].dropna().unique().tolist()
                    try:
                        sorted_dates = sorted(unique_dates)
                        f.write(f"CSV '{csv_file}' max date: {sorted_dates[-1]} (total unique: {len(sorted_dates)})\n")
                        f.write(f"Latest 5 dates in '{csv_file}': {sorted_dates[-5:]}\n")
                    except Exception as e:
                        f.write(f"CSV '{csv_file}' unique dates (first 5): {unique_dates[:5]} (error sorting: {e})\n")
                else:
                    # just print headers or something
                    f.write(f"CSV '{csv_file}' columns: {df.columns.tolist()[:3]}\n")
            except Exception as e:
                f.write(f"CSV '{csv_file}' error: {e}\n")
                
print("Done checking latest dates!")
