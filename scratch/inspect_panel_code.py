import os

workspace_dir = r"c:\Users\lap4all\Desktop\New folder"
file_path = os.path.join(workspace_dir, "templates", "index.html")

with open(file_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

# Search for the line containing id="tab-off-spe"
for idx, line in enumerate(lines):
    if 'id="tab-off-spe"' in line or "id='tab-off-spe'" in line:
        print(f"Found on line {idx + 1}:")
        # Print 50 lines before and after
        start = max(0, idx - 15)
        end = min(len(lines), idx + 50)
        for i in range(start, end):
            safe_line = lines[i].rstrip().encode('ascii', errors='replace').decode('ascii')
            print(f"{i + 1}: {safe_line}")
        break
