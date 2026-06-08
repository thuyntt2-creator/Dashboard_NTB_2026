import re

with open("google_sheet_details.txt", "r", encoding="utf-8") as f:
    content = f.read()

# Let's search for sheet name patterns
# Usually sheet names are listed like: "properties":{"sheetId":1365110988,"title":"Tổng quan",...}
# Let's search for "title":"..." or "sheetId":...
matches = re.findall(r'"title"\s*:\s*"([^"]+)"', content)
print("Titles found:", set(matches))

matches_sheet = re.findall(r'"sheetId"\s*:\s*(\d+)', content)
print("Sheet IDs found:", set(matches_sheet))

# Let's also search for gridId
grid_ids = re.findall(r'"gridId"\s*:\s*(\d+)', content)
print("gridIds found:", set(grid_ids))
