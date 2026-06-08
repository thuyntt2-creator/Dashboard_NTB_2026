import urllib.request
import re

url = "https://docs.google.com/spreadsheets/d/1DAwY-46twFrHIs77R4p4IMuIZ6JTE-e58Aj-9Kcr5Jk/edit"
req = urllib.request.Request(url)
req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)')

output_path = "google_sheet_details.txt"

try:
    with urllib.request.urlopen(req) as response:
        html = response.read().decode('utf-8')
        
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("Searching in raw HTML...\n")
        
        # Look for sheet titles and ids
        # Google sheets JSON has: "properties":{"sheetId":0,"title":"Sheet1",...}
        # Or: {"sheetId": 123, "title": "abc"}
        sheet_properties = re.findall(r'{"sheetId":\s*(\d+),\s*"title":\s*"([^"]+)"', html)
        f.write(f"Properties found via sheetId/title: {len(sheet_properties)}\n")
        for sid, title in sheet_properties:
            f.write(f"  sheetId: {sid} -> title: {title}\n")
            
        # Another pattern: "title":"Tổng quan","sheetId":1365110988
        sheet_properties_reverse = re.findall(r'"title":\s*"([^"]+)",\s*"sheetId":\s*(\d+)', html)
        f.write(f"Properties found via title/sheetId: {len(sheet_properties_reverse)}\n")
        for title, sid in sheet_properties_reverse:
            f.write(f"  title: {title} -> sheetId: {sid}\n")
            
        # Generic find for gids
        gids = re.findall(r'"gid":\s*(\d+)', html)
        f.write(f"Generic gids: {list(set(gids))}\n")
            
except Exception as e:
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(f"Error: {e}\n")

print("Done writing google_sheet_details.txt")
