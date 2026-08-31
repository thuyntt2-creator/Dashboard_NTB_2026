import os
import re

workspace_dir = r"c:\Users\lap4all\Desktop\New folder"

def main():
    print("Searching python files in workspace root for raw/upload references...")
    pattern = re.compile(r'(rawtts|raw_tts|rawGTCTTS|\.update\(|batch_update|to_excel|to_csv|raw)', re.IGNORECASE)
    
    # Just list files in workspace_dir (not walking into subdirectories like scratch)
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
