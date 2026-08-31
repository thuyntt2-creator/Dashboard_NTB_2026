import urllib.request
import os
import sys
import pandas as pd

sys.stdout.reconfigure(encoding='utf-8')

original_url = "https://docs.google.com/spreadsheets/d/1yjXxrGH-wlAPT4c_2Y-Acg_hGgW-aKXcHWNd_zWLRkI/export?format=xlsx"
user_url = "https://docs.google.com/spreadsheets/d/1XaziS_8UB2lCwL01bxam106EdIUHtlMISDGJX1PU5A8/export?format=xlsx"

original_path = r"c:\Users\lap4all\Desktop\New folder\scratch\original_sheet.xlsx"
user_path = r"c:\Users\lap4all\Desktop\New folder\scratch\user_sheet.xlsx"

def download_file(url, path, label):
    print(f"Downloading {label} from {url}...", flush=True)
    req = urllib.request.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)')
    try:
        # 15 seconds timeout
        with urllib.request.urlopen(req, timeout=15) as response:
            print(f"Got response headers for {label}. Reading content...", flush=True)
            content = response.read()
            print(f"Read {len(content)} bytes for {label}. Writing to file...", flush=True)
            with open(path, 'wb') as out_file:
                out_file.write(content)
        print(f"Successfully downloaded {label} to {path}", flush=True)
        return True
    except Exception as e:
        print(f"Error downloading {label}: {e}", flush=True)
        return False

# Download both
download_file(original_url, original_path, "Original Sheet (Huy)")
download_file(user_url, user_path, "User's Sheet")

def inspect_xlsx(path, label):
    print(f"\n================ INSPECTING {label} ================", flush=True)
    if not os.path.exists(path):
        print("File does not exist.", flush=True)
        return
    try:
        # Check size first
        sz = os.path.getsize(path)
        print(f"File size: {sz} bytes", flush=True)
        if sz < 1000:
            print("File is too small, likely an error page. Let's read first 500 bytes as text:")
            with open(path, 'r', errors='ignore') as f:
                print(f.read(500), flush=True)
            return
        xls = pd.ExcelFile(path)
        print("Sheets:", flush=True)
        for name in xls.sheet_names:
            print(f" - {name}", flush=True)
            try:
                df = pd.read_excel(path, sheet_name=name)
                print(f"   Shape: {df.shape}", flush=True)
                print(f"   Columns: {list(df.columns)}", flush=True)
                print(f"   First row sample:\n{df.head(1).to_dict(orient='records')}", flush=True)
            except Exception as e_sheet:
                print(f"   Error reading sheet {name}: {e_sheet}", flush=True)
    except Exception as e:
        print(f"Error inspecting {path}: {e}", flush=True)

inspect_xlsx(original_path, "Original Sheet (Huy)")
inspect_xlsx(user_path, "User's Sheet")
