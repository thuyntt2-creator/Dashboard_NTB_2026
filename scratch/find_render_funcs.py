import os

workspace_dir = r"c:\Users\lap4all\Desktop\New folder"
file_path = os.path.join(workspace_dir, "templates", "index.html")

with open(file_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

for idx, line in enumerate(lines):
    if 'function renderOffSpe(' in line:
        print(f"Found renderOffSpe on line {idx + 1}:")
        start = idx
        end = min(len(lines), idx + 60)
        for i in range(start, end):
            safe_line = lines[i].rstrip().encode('ascii', errors='replace').decode('ascii')
            print(f"{i + 1}: {safe_line}")
        break
