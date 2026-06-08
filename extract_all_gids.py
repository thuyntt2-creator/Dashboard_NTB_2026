import urllib.request
import re

url = "https://docs.google.com/spreadsheets/d/1DAwY-46twFrHIs77R4p4IMuIZ6JTE-e58Aj-9Kcr5Jk/edit"
req = urllib.request.Request(url)
req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)')

output_path = "sheet_gid_search.txt"

try:
    with urllib.request.urlopen(req) as response:
        html = response.read().decode('utf-8')
        
    with open(output_path, "w", encoding="utf-8") as f:
        # Search for 1365110988
        pos = html.find("1365110988")
        if pos != -1:
            f.write(f"Found '1365110988' at index {pos}\n")
            f.write("Surrounding:\n")
            f.write(html[max(0, pos-1000):min(len(html), pos+1000)] + "\n")
        else:
            f.write("Not found '1365110988'\n")
            
except Exception as e:
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(f"Error: {e}\n")

print("Done writing sheet_gid_search.txt")
