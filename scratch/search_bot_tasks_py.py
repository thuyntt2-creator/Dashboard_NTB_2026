import os
import re

bot_dir = r"C:\Users\lap4all\Desktop\Backlog_Automation"

def main():
    print("Searching Backlog_Automation batch/powershell files for python script executions...")
    pattern = re.compile(r'\.py', re.IGNORECASE)
    
    files = [f for f in os.listdir(bot_dir) if os.path.isfile(os.path.join(bot_dir, f)) and (f.endswith(".bat") or f.endswith(".ps1"))]
    
    for file in sorted(files):
        file_path = os.path.join(bot_dir, file)
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
