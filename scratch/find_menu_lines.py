import os

workspace_dir = r"c:\Users\lap4all\Desktop\New folder"
file_path = os.path.join(workspace_dir, "templates", "index.html")

with open(file_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

for idx, line in enumerate(lines):
    if 'switchTab(\'tab-off-spe\'' in line or 'switchTab("tab-off-spe"' in line:
        print(f"Found switchTab('tab-off-spe') on line {idx + 1}:")
        start = max(0, idx - 3)
        end = min(len(lines), idx + 8)
        for i in range(start, end):
            safe_line = lines[i].rstrip().encode('ascii', errors='replace').decode('ascii')
            print(f"{i + 1}: {safe_line}")
        break
