# -*- coding: utf-8 -*-
import sys
import os
import time
import paramiko

sys.stdout.reconfigure(encoding='utf-8')

VPS_IP = '103.82.27.107'
VPS_USER = 'root'
VPS_PASS = 'T403kbek9E1r1nJy'
REMOTE_DIR = '/root/auto-report'

def run_cmd(ssh, cmd):
    print(f"\n👉 [VPS RUN]: {cmd}")
    stdin, stdout, stderr = ssh.exec_command(cmd)
    while True:
        line = stdout.readline()
        if not line:
            break
        print(line, end='', flush=True)
    err = stderr.read().decode()
    if err and "warning" not in err.lower() and "notice" not in err.lower():
        print(f"⚠️ [STDERR]: {err}", flush=True)
    return stdout.channel.recv_exit_status()

def main():
    print("🚀 Bắt đầu kết nối và thiết lập VPS CloudFly...")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(VPS_IP, username=VPS_USER, password=VPS_PASS, timeout=15)
    print("✅ Đã kết nối SSH thành công!")

    # 1. Cài đặt múi giờ Việt Nam
    run_cmd(ssh, "timedatectl set-timezone Asia/Ho_Chi_Minh && date")

    # 2. Cập nhật apt & font chữ tiếng Việt
    print("\n📦 Đang cập nhật gói hệ điều hành và font tiếng Việt...")
    run_cmd(ssh, "export DEBIAN_FRONTEND=noninteractive && apt-get update -y && apt-get install -y python3-pip python3-dev fonts-dejavu-core fonts-liberation fonts-noto-color-emoji curl git")

    # 3. Cài đặt thư viện Python
    print("\n🐍 Đang cài đặt thư viện Python...")
    run_cmd(ssh, "pip install --upgrade pip")
    run_cmd(ssh, "pip install requests urllib3 gspread google-auth pillow pandas playwright")
    
    print("\n🌐 Cài đặt Playwright Chromium...")
    run_cmd(ssh, "playwright install --with-deps chromium")

    # 4. Tạo thư mục làm việc và upload code qua SFTP
    print(f"\n📂 Tạo thư mục {REMOTE_DIR} trên VPS...")
    run_cmd(ssh, f"mkdir -p {REMOTE_DIR}")

    sftp = ssh.open_sftp()
    local_dir = r"c:\Users\lap4all\Desktop\New folder"
    files_to_upload = [
        "fetch_lastmile_productivity.py",
        "send_realtime_and_target_gtalk.py",
        "ghn_config.json",
        "authorized_user.json",
        "credentials.json"
    ]

    for fname in files_to_upload:
        lpath = os.path.join(local_dir, fname)
        rpath = f"{REMOTE_DIR}/{fname}"
        if os.path.exists(lpath):
            print(f"⬆️ Đang tải lên: {fname} -> {rpath}")
            sftp.put(lpath, rpath)
        else:
            print(f"⚠️ Không tìm thấy file cục bộ: {fname}")

    sftp.close()
    print("✅ Đã tải lên toàn bộ file thành công!")

    # 5. Chạy thử nghiệm cào dữ liệu ngay trên VPS
    print("\n=======================================================")
    print("🧪 CHẠY THỬ NGHIỆM CÀO DỮ LIỆU TRỰC TIẾP TRÊN VPS VIỆT NAM...")
    print("=======================================================")
    exit_code = run_cmd(ssh, f"cd {REMOTE_DIR} && python3 fetch_lastmile_productivity.py")
    print(f"\n🏁 Kết quả chạy thử: Exit code = {exit_code}")

    ssh.close()
    print("🎉 HOÀN TẤT THIẾT LẬP VPS!")

if __name__ == '__main__':
    main()
