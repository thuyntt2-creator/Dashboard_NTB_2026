import urllib.request
import re

url = "https://docs.google.com/spreadsheets/d/1DAwY-46twFrHIs77R4p4IMuIZ6JTE-e58Aj-9Kcr5Jk/edit"
req = urllib.request.Request(url)
req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)')

output_path = "sheet_tab_html.txt"

try:
    with urllib.request.urlopen(req) as response:
        html = response.read().decode('utf-8')
        
    with open(output_path, "w", encoding="utf-8") as f:
        # Find all sheet tab HTML blocks
        # Let's search using a regex that captures docs-sheet-tab class and its surrounding text
        matches = re.finditer(r'<div class="[^"]*docs-sheet-tab[^"]*".+?<\/div><\/div><\/div><\/div>', html)
        f.write("Matches found:\n")
        for idx, m in enumerate(matches):
            f.write(f"\nMatch {idx}:\n")
            f.write(m.group(0) + "\n")
            
        # Also print the javascript variables that contain the sheet name to GID map
        # Let's search for sheetId and title in script tags
        # Sometimes sheets look like {"id":1365110988,"name":"Tổng quan"}
        # Let's search for any json lists containing sheet properties
        js_arrays = re.findall(r'(\[[^\]]*?"Tổng quan"[^\[]*?\])', html)
        f.write(f"\nJS Arrays found: {len(js_arrays)}\n")
        for idx, arr in enumerate(js_arrays):
            f.write(f"Array {idx}: {arr[:500]}\n")
            
except Exception as e:
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(f"Error: {e}\n")

print("Done writing sheet_tab_html.txt")
