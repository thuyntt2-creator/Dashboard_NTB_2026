import os
import re

workspace_dir = r"c:\Users\lap4all\Desktop\New folder"

def main():
    print("Searching python files for Google Sheets connection keys/URLs...")
    # Find all gc.open_by_key, gc.open_by_url, open_by_key, open_by_url, open_by_key
    pattern = re.compile(r'(open_by_key|open_by_url|open_by_key|open_by_url|gc\.open|sh\s*=)', re.IGNORECASE)
    
    for root, dirs, files in os.walk(workspace_dir):
        if ".git" in root or "__pycache__" in root:
            continue
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                        lines = f.readlines()
                    for idx, line in enumerate(lines):
                        if pattern.search(line):
                            rel_path = os.path.relpath(file_path, workspace_dir)
                            print(f"{rel_path}:{idx+1}: {line.strip()}")
                except Exception as e:
                    print(f"Error reading {file}: {e}")

if __name__ == '__main__':
    main()
