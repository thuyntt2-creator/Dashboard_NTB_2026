import os
import re

workspace_dir = r"c:\Users\lap4all\Desktop\New folder"

def main():
    print("Searching root python files for Google Sheets connections...")
    pattern = re.compile(r'(open_by_key|open_by_url|open_by_key|open_by_url|gc\.open|sh\s*=)', re.IGNORECASE)
    
    files = [f for f in os.listdir(workspace_dir) if os.path.isfile(os.path.join(workspace_dir, f)) and f.endswith(".py")]
    
    for file in sorted(files):
        file_path = os.path.join(workspace_dir, file)
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                lines = f.readlines()
            for idx, line in enumerate(lines):
                if pattern.search(line):
                    print(f"{file}:{idx+1}: {line.strip()}")
        except Exception as e:
            print(f"Error reading {file}: {e}")

if __name__ == '__main__':
    main()
