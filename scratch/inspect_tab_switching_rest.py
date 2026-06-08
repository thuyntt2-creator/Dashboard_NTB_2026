import os

workspace_dir = r"c:\Users\lap4all\Desktop\New folder"
file_path = os.path.join(workspace_dir, "templates", "index.html")

with open(file_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

start = 2890
end = min(len(lines), 3020)
for i in range(start, end):
    safe_line = lines[i].rstrip().encode('ascii', errors='replace').decode('ascii')
    print(f"{i + 1}: {safe_line}")
