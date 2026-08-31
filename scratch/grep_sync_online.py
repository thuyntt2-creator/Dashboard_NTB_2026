import re
import os

workspace_dir = r"c:\Users\lap4all\Desktop\New folder"
file_path = os.path.join(workspace_dir, "sync_online_direct.py")

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

lines = content.splitlines()

# Search for format, batch_update, add_chart, chart, border, color, etc.
keywords = ["format", "batch_update", "chart", "border", "color", "background", "style", "update_cells"]
found = []

for idx, line in enumerate(lines, start=1):
    for kw in keywords:
        if kw in line.lower():
            found.append(f"Line {idx}: {line.strip()}")
            break

output_file = os.path.join(workspace_dir, "scratch", "grep_sync_online_res.txt")
with open(output_file, "w", encoding="utf-8") as out:
    out.write("\n".join(found[:100]))

print("Done. Found occurrences:", len(found))
