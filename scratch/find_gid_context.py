with open("scratch/raw_sheet.html", "r", encoding="utf-8") as f:
    html = f.read()

target = "843153285"
idx = html.find(target)
if idx != -1:
    print(f"Found {target} at index {idx}")
    print("\nSurrounding content:")
    print(html[max(0, idx - 500): min(len(html), idx + 500)])
else:
    print(f"Could not find {target} in raw_sheet.html")
