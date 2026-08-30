import os
import sys
import subprocess
import datetime

cwd = r"c:\Users\lap4all\Desktop\New folder"
log_path = os.path.join(cwd, "auto_sync.log")

def log(msg):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{now}] {msg}\n"
    print(line, end="")
    try:
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(line)
    except Exception:
        pass

def show_windows_alert(title, message):
    try:
        ps_cmd = f'[System.Reflection.Assembly]::LoadWithPartialName("System.Windows.Forms"); [System.Windows.Forms.MessageBox]::Show("{message}", "{title}", 0, 48)'
        subprocess.Popen(["powershell", "-NoProfile", "-Command", ps_cmd], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception:
        pass

log("=== Starting Auto Sync Pipeline ===")

# Step 1: Run local company sync script
step1_success = False
try:
    log("Step 1: Downloading latest company Google Sheets...")
    p1 = subprocess.run([sys.executable, r"scratch\sync_local_company.py"], cwd=cwd, capture_output=True, text=True, timeout=120)
    log(f"Step 1 Return Code: {p1.returncode}")
    if p1.stdout:
        log(f"Output: {p1.stdout.strip()}")
    if p1.returncode == 0:
        step1_success = True
    else:
        log("❌ Step 1 Failed! Google Sheets could not be downloaded.")
        show_windows_alert(
            "CẢNH BÁO ĐỒNG BỘ DỮ LIỆU NTB", 
            "Đồng bộ Google Sheets bị lỗi (Có thể do Token Google OAuth hết hạn).\\nVui lòng chạy file DANG_NHAP_LAI_GOOGLE.bat trên Desktop/thư mục dự án để làm mới đăng nhập!"
        )
except Exception as e:
    log(f"Step 1 Exception: {e}")

if not step1_success:
    log("⚠️ Aborting Step 2 and Step 3 because Step 1 (Download Data) failed.")
    log("=== Auto Sync Pipeline Finished With Errors ===")
    sys.exit(1)

# Step 2: Bootstrap/Update Neon DB
try:
    log("Step 2: Updating Neon PostgreSQL Database...")
    p2 = subprocess.run([sys.executable, r"scratch\bootstrap_new_db.py"], cwd=cwd, capture_output=True, text=True, timeout=180)
    log(f"Step 2 Return Code: {p2.returncode}")
    if p2.stdout:
        log(f"Output: {p2.stdout.strip()}")
except Exception as e:
    log(f"Step 2 Exception: {e}")

# Step 3: Git add, commit, and push
try:
    log("Step 3: Git add and commit...")
    subprocess.run(["git", "add", "*.csv", "app.py"], cwd=cwd, capture_output=True)
    subprocess.run(["git", "commit", "-m", "Auto update data and DB"], cwd=cwd, capture_output=True)
    log("Step 3: Git push to GitHub...")
    p3 = subprocess.run(["git", "push", "origin", "main"], cwd=cwd, capture_output=True, text=True, timeout=120)
    log(f"Step 3 Return Code: {p3.returncode}")
    if p3.stdout:
        log(f"Output: {p3.stdout.strip()}")
    if p3.stderr:
        log(f"Stderr: {p3.stderr.strip()}")
except Exception as e:
    log(f"Step 3 Exception: {e}")

log("=== Auto Sync Pipeline Finished ===")
