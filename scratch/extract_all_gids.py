import urllib.request
import re
import json
import os

workspace_dir = r"c:\Users\lap4all\Desktop\New folder"
url = "https://docs.google.com/spreadsheets/d/1DAwY-46twFrHIs77R4p4IMuIZ6JTE-e58Aj-9Kcr5Jk/edit"
output_path = os.path.join(workspace_dir, "scratch", "sheet_gids_extracted.txt")

os.makedirs(os.path.dirname(output_path), exist_ok=True)

req = urllib.request.Request(url)
req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)')

try:
    with urllib.request.urlopen(req) as response:
        html = response.read().decode('utf-8')
        
    with open(output_path, "w", encoding="utf-8") as f:
        # Save HTML snippet to check structure if needed
        # Search for sheetName, sheetId, gid, etc.
        # Often it is: {"sheetId":1400910659,"title":"Thứ cùng kỳ",...} or "title":"Thứ cùng kỳ","sheetId":1400910659
        
        # Let's search for sheetId and title
        pairs = []
        
        # Find all occurrences of "title" and "sheetId" or "sheetId" and "title"
        # We can extract all {"sheetId": X, "title": "Y"} patterns
        matches1 = re.findall(r'\"sheetId\"\s*:\s*(\d+)\s*,\s*\"title\"\s*:\s*\"([^\"]+)\"', html)
        matches2 = re.findall(r'\"title\"\s*:\s*\"([^\"]+)\"\s*,\s*\"sheetId\"\s*:\s*(\d+)', html)
        
        for sid, title in matches1:
            pairs.append((title, sid))
        for title, sid in matches2:
            pairs.append((title, sid))
            
        # Also look for properties block containing title and sheetId:
        # e.g., properties: {title: "...", sheetId: ...}
        properties = re.findall(r'properties\s*:\s*\{[^\}]+title\s*:\s*\"([^\"]+)\"[^\}]+sheetId\s*:\s*(\d+)', html)
        for title, sid in properties:
            pairs.append((title, sid))
            
        pairs = list(set(pairs))
        f.write(f"Found {len(pairs)} sheets:\n")
        for title, sid in sorted(pairs):
            f.write(f"Sheet Name: '{title}' -> GID: {sid}\n")
            
        # If no sheets found, write a block of HTML for debugging
        if len(pairs) == 0:
            f.write("No pairs found. Showing re.findall on title/gid...\n")
            titles = re.findall(r'\"title\"\s*:\s*\"([^\"]+)\"', html)
            gids = re.findall(r'\"sheetId\"\s*:\s*(\d+)', html)
            f.write(f"Titles found: {set(titles)}\n")
            f.write(f"Sheet IDs found: {set(gids)}\n")
            
except Exception as e:
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(f"Error: {e}\n")

print("GIDs extraction completed.")
