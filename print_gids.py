import urllib.request
import re

url = "https://docs.google.com/spreadsheets/d/1DAwY-46twFrHIs77R4p4IMuIZ6JTE-e58Aj-9Kcr5Jk/edit"
req = urllib.request.Request(url)
req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)')

output_path = "sheet_gids_mapped.txt"

try:
    with urllib.request.urlopen(req) as response:
        html = response.read().decode('utf-8')
        
    with open(output_path, "w", encoding="utf-8") as f:
        # Search for GID patterns
        # The pattern is: [index, 0, "gid_str", [{"1":[[0,0,"sheet_name"]]
        matches = re.finditer(r'\[\d+,\s*0,\s*"([^"]+)",\s*\[\s*\{\s*"1"\s*:\s*\[\s*\[\s*0,\s*0,\s*"([^"]+)"', html)
        f.write("Matches found:\n")
        for m in matches:
            f.write(f"Sheet Name: '{m.group(2)}' -> GID: '{m.group(1)}'\n")
            
        # Also print any matches with different spacings
        matches_v2 = re.findall(r'"([^"]+)"\s*,\s*\[\s*\{\s*"1"\s*:\s*\[\s*\[\s*0,\s*0,\s*"([^"]+)"', html)
        f.write(f"\nMatches V2 ({len(matches_v2)}):\n")
        for gid, name in matches_v2:
            f.write(f"Sheet Name: '{name}' -> GID: '{gid}'\n")

except Exception as e:
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(f"Error: {e}\n")

print("Done writing sheet_gids_mapped.txt")
