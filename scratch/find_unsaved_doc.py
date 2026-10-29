import os
import glob
import datetime
import subprocess

print("=== SEARCHING FOR UNSAVED / RECENT DOCUMENTS ===")

user_profile = os.environ.get("USERPROFILE", "C:\\Users\\lap4all")
appdata = os.environ.get("APPDATA", os.path.join(user_profile, "AppData", "Roaming"))
localappdata = os.environ.get("LOCALAPPDATA", os.path.join(user_profile, "AppData", "Local"))
temp_dir = os.environ.get("TEMP", os.path.join(localappdata, "Temp"))

search_dirs = [
    # Office Unsaved & AutoRecover
    os.path.join(appdata, "Microsoft", "Word"),
    os.path.join(localappdata, "Microsoft", "Office", "UnsavedFiles"),
    os.path.join(appdata, "Microsoft", "Excel"),
    os.path.join(appdata, "Microsoft", "PowerPoint"),
    # Notepad++ & Editors
    os.path.join(appdata, "Notepad++", "backup"),
    # VS Code / Antigravity Backups
    os.path.join(appdata, "Code", "Backups"),
    os.path.join(appdata, "Antigravity", "Backups"),
    # Recent
    os.path.join(appdata, "Microsoft", "Windows", "Recent"),
    # Workspace
    r"c:\Users\lap4all\Desktop\New folder",
    # Desktop
    os.path.join(user_profile, "Desktop"),
    # Documents
    os.path.join(user_profile, "Documents"),
    # Downloads
    os.path.join(user_profile, "Downloads"),
]

# 1. Search for .asd, .wbk, .tmp, .docx, .doc, .txt, .md, .xlsx modified in last 48 hours
extensions = [".asd", ".wbk", ".tmp", ".docx", ".doc", ".xlsx", ".csv", ".txt", ".md", ".json"]
now = datetime.datetime.now()

print("\n--- 1. Office AutoRecover & UnsavedFiles Check ---")
office_paths = [
    os.path.join(appdata, "Microsoft", "Word"),
    os.path.join(localappdata, "Microsoft", "Office", "UnsavedFiles"),
    os.path.join(appdata, "Microsoft", "Excel"),
]
found_office = []
for p in office_paths:
    if os.path.exists(p):
        print(f"Checking {p}...")
        for root, dirs, files in os.walk(p):
            for f in files:
                full_p = os.path.join(root, f)
                try:
                    mtime = datetime.datetime.fromtimestamp(os.path.getmtime(full_p))
                    size = os.path.getsize(full_p)
                    found_office.append((mtime, size, full_p))
                except Exception as e:
                    pass
    else:
        print(f"Path does not exist: {p}")

found_office.sort(key=lambda x: x[0], reverse=True)
for mtime, size, fp in found_office[:15]:
    print(f"[{mtime.strftime('%Y-%m-%d %H:%M:%S')}] ({size} bytes) {fp}")

print("\n--- 2. Recent Files in Windows Recent ---")
recent_dir = os.path.join(appdata, "Microsoft", "Windows", "Recent")
if os.path.exists(recent_dir):
    recent_files = []
    for f in os.listdir(recent_dir):
        full_p = os.path.join(recent_dir, f)
        try:
            mtime = datetime.datetime.fromtimestamp(os.path.getmtime(full_p))
            recent_files.append((mtime, f, full_p))
        except:
            pass
    recent_files.sort(key=lambda x: x[0], reverse=True)
    for mtime, f, fp in recent_files[:20]:
        print(f"[{mtime.strftime('%Y-%m-%d %H:%M:%S')}] {f}")

print("\n--- 3. Workspace Recently Modified (Last 24h) ---")
ws_files = []
ws_dir = r"c:\Users\lap4all\Desktop\New folder"
for root, dirs, files in os.walk(ws_dir):
    # skip .git and __pycache__
    if ".git" in root or "__pycache__" in root or ".gemini" in root or "node_modules" in root:
        continue
    for f in files:
        full_p = os.path.join(root, f)
        try:
            mtime = datetime.datetime.fromtimestamp(os.path.getmtime(full_p))
            diff_hours = (now - mtime).total_seconds() / 3600
            if diff_hours <= 36:
                size = os.path.getsize(full_p)
                ws_files.append((mtime, size, full_p))
        except:
            pass
ws_files.sort(key=lambda x: x[0], reverse=True)
for mtime, size, fp in ws_files[:20]:
    rel = os.path.relpath(fp, ws_dir)
    print(f"[{mtime.strftime('%Y-%m-%d %H:%M:%S')}] ({size} bytes) {rel}")

print("\n--- 4. Temp Word / Office Files (~*.* or *.tmp in Temp) ---")
temp_found = []
if os.path.exists(temp_dir):
    try:
        for f in os.listdir(temp_dir):
            if f.startswith("~") or f.endswith(".asd") or f.endswith(".tmp") or f.endswith(".docx"):
                fp = os.path.join(temp_dir, f)
                try:
                    mtime = datetime.datetime.fromtimestamp(os.path.getmtime(fp))
                    diff_hours = (now - mtime).total_seconds() / 3600
                    if diff_hours <= 36:
                        temp_found.append((mtime, os.path.getsize(fp), fp))
                except:
                    pass
    except Exception as e:
        print("Error reading temp:", e)

temp_found.sort(key=lambda x: x[0], reverse=True)
for mtime, size, fp in temp_found[:15]:
    print(f"[{mtime.strftime('%Y-%m-%d %H:%M:%S')}] ({size} bytes) {fp}")

print("\n--- 5. Running Processes ---")
try:
    cmd = 'tasklist /v /fo csv'
    output = subprocess.check_output(cmd, shell=True, text=True, errors='ignore')
    lines = output.strip().split('\n')
    header = lines[0]
    for line in lines[1:]:
        if any(app in line.lower() for app in ['word', 'excel', 'notepad', 'code', 'chrome', 'msedge', 'wps', 'powerpnt']):
            print(line.strip())
except Exception as e:
    print("Process check error:", e)
