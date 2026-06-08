import os

workspace_dir = r"c:\Users\lap4all\Desktop\New folder"
file_path = os.path.join(workspace_dir, "templates", "index.html")

with open(file_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

# Search for the start of main <script> tag (or near the end of the file)
script_idx = -1
for idx, line in enumerate(lines):
    if '<script>' in line or '<script ' in line:
        if idx > 2500:  # looking for the main script block
            script_idx = idx
            break

if script_idx != -1:
    print(f"Found main script block starting on line {script_idx + 1}:")
    start = script_idx
    end = min(len(lines), script_idx + 100)
    for i in range(start, end):
        safe_line = lines[i].rstrip().encode('ascii', errors='replace').decode('ascii')
        print(f"{i + 1}: {safe_line}")
else:
    print("Main script block not found after line 2500.")
