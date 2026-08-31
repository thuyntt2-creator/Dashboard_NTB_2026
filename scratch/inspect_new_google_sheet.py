import urllib.request
import re
import pandas as pd
import io
import sys

# Set standard output encoding to utf-8 for Windows console
sys.stdout.reconfigure(encoding='utf-8')

sheet_id = "1U-vA09JQWwC6huGi95cJ19pDdrxOt_qiMjwAxM6AvbY"
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/edit"

req = urllib.request.Request(url)
req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)')

print("Fetching sheet HTML...")
try:
    with urllib.request.urlopen(req) as response:
        html = response.read().decode('utf-8')
    print("Fetched successfully. Length:", len(html))
except Exception as e:
    print("Error fetching HTML:", e)
    html = ""

# Find all sheet names and ids
# Let's inspect the HTML carefully or write it to a file
with open("scratch/raw_sheet.html", "w", encoding="utf-8") as f:
    f.write(html[:500000]) # write first 500k chars for debugging

# Another pattern for sheet names: "sheetId": (\d+), "properties": {"title": "([^"]+)"}
# Or similar. Let's find using regex.
sheet_matches = re.findall(r'"properties":\s*\{\s*"sheetId":\s*(\d+),\s*"title":\s*"([^"]+)"', html)
sheet_matches2 = re.findall(r'"title":\s*"([^"]+)",\s*"sheetId":\s*(\d+)', html)
sheet_matches3 = re.findall(r'"sheetId":\s*(\d+),\s*"title":\s*"([^"]+)"', html)

tabs = {}
for sid, title in sheet_matches:
    tabs[sid] = title
for title, sid in sheet_matches2:
    tabs[sid] = title
for sid, title in sheet_matches3:
    tabs[sid] = title

print("\nDiscovered Tabs:")
for sid, title in tabs.items():
    print(f"  sheetId (gid): {sid} -> Title: {title}")

# Try to download gid 843153285 as CSV
target_gid = "843153285"
csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={target_gid}"
print(f"\nDownloading target gid {target_gid} from {csv_url}...")
try:
    csv_req = urllib.request.Request(csv_url)
    csv_req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)')
    with urllib.request.urlopen(csv_req) as response:
        csv_data = response.read().decode('utf-8')
    print("Downloaded CSV successfully. Length:", len(csv_data))
    
    # Save CSV locally to inspect
    with open("scratch/downloaded_sheet_tab.csv", "w", encoding="utf-8") as f:
        f.write(csv_data)
    
    # Load into DataFrame and print head
    df = pd.read_csv(io.StringIO(csv_data))
    print("\nDataFrame Shape:", df.shape)
    print("Columns:", list(df.columns))
    
    # Write detailed description to a text file
    with open("scratch/sheet_inspection_results.txt", "w", encoding="utf-8") as out:
        out.write(f"DataFrame Shape: {df.shape}\n")
        out.write(f"Columns: {list(df.columns)}\n\n")
        out.write("First 50 rows:\n")
        out.write(df.head(50).to_string())
        
    print("\nFirst 10 rows:")
    print(df.head(10).to_string())
except Exception as e:
    import traceback
    print("Error downloading target CSV:")
    traceback.print_exc()
