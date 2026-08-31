import os
import re

bot_dir = r"C:\Users\lap4all\Desktop\Backlog_Automation"

def main():
    print("Searching Backlog_Automation python files for raw / rawtts / sheet references...")
    pattern = re.compile(r'(raw|rawtts|raw_tts|rawGTCTTS|1DAwY-46twFrHIs77R4p4IMuIZ6JTE-e58Aj-9Kcr5Jk)', re.IGNORECASE)
    
    files = [f for f in os.listdir(bot_dir) if os.path.isfile(os.path.join(bot_dir, f)) and f.endswith(".py")]
    
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
