# -*- coding: utf-8 -*-
"""
Script mở trình duyệt để người dùng đăng nhập GHN,
tự động lưu cookies mới và upload thẳng lên VPS CloudFly.
"""
import os
import sys
import json
import time
from playwright.sync_api import sync_playwright
import paramiko

sys.stdout.reconfigure(encoding='utf-8')

VPS_IP = '103.82.27.107'
VPS_USER = 'root'
VPS_PASS = 'T403kbek9E1r1nJy'
REMOTE_COOKIE_PATH = '/root/auto-report/cookies_ghn.json'

LOCAL_COOKIE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cookies_ghn.json")
DASHBOARD_URL = "https://baocao.ghn.vn/dashboards/63bd175cd4435a369fade8f5"

def sync_cookie_to_vps(local_file):
    print(f"\n📡 Đang đẩy file cookie lên VPS ({VPS_IP})...")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(VPS_IP, username=VPS_USER, password=VPS_PASS, timeout=10)
    
    sftp = ssh.open_sftp()
    sftp.put(local_file, REMOTE_COOKIE_PATH)
    sftp.close()
    
    # Đồng bộ sang cả thư mục Auto report trên máy nếu có
    docs_cookie = r"c:\Users\lap4all\Documents\Auto report\cookies_ghn.json"
    try:
        import shutil
        shutil.copy(local_file, docs_cookie)
        print(f"✅ Đã cập nhật cookie cục bộ: {docs_cookie}")
    except Exception:
        pass

    ssh.close()
    print(f"🎉 ĐÃ ĐỒNG BỘ COOKIE MỚI LÊN VPS THÀNH CÔNG: {REMOTE_COOKIE_PATH}!")

def main():
    print("=" * 60)
    print("🌐 ĐANG MỞ TRÌNH DUYỆT ĐỂ BẠN ĐĂNG NHẬP GHN...")
    print("=" * 60)
    print("👉 Cửa sổ trình duyệt đang mở lên trên màn hình máy tính của bạn.")
    print("👉 Hãy đăng nhập tài khoản GHN của bạn trên cửa sổ đó.")
    print("👉 Sau khi đăng nhập thành công vào báo cáo, hệ thống sẽ tự động lưu cookie!")

    profile_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "browser_profile")
    os.makedirs(profile_dir, exist_ok=True)

    with sync_playwright() as p:
        # Ưu tiên mở Edge hoặc Chrome có sẵn trên Windows
        browser_channel = "msedge"
        try:
            context = p.chromium.launch_persistent_context(
                user_data_dir=profile_dir,
                channel=browser_channel,
                headless=False,
                args=["--start-maximized"]
            )
        except Exception:
            context = p.chromium.launch_persistent_context(
                user_data_dir=profile_dir,
                headless=False,
                args=["--start-maximized"]
            )

        page = context.pages[0] if context.pages else context.new_page()
        page.goto(DASHBOARD_URL)

        # Chờ người dùng đăng nhập xong và trang báo cáo (có iframe hoặc url baocao) xuất hiện
        print("⏳ Đang chờ bạn đăng nhập trên trình duyệt (thời gian tối đa 5 phút)...")
        logged_in = False
        t_start = time.time()
        while time.time() - t_start < 300:
            try:
                # Kiểm tra xem iframe của Looker Studio đã xuất hiện chưa
                iframe = page.locator("iframe").first
                if iframe.count() > 0 and iframe.is_visible():
                    logged_in = True
                    break
            except Exception:
                pass
            time.sleep(2)

        if logged_in:
            print("✅ Phát hiện đã đăng nhập thành công vào trang báo cáo!")
            time.sleep(3) # Chờ 3s để cookie ghi đầy đủ
            
            storage = context.storage_state()
            with open(LOCAL_COOKIE_FILE, "w", encoding="utf-8") as f:
                json.dump(storage, f, ensure_ascii=False, indent=2)
            print(f"💾 Đã lưu cookie mới vào: {LOCAL_COOKIE_FILE}")
            
            context.close()
            
            # Tự động đẩy lên VPS
            sync_cookie_to_vps(LOCAL_COOKIE_FILE)
            print("🎉 HOÀN TẤT LẤY VÀ CẬP NHẬT COOKIE MỚI!")
        else:
            print("❌ Hết thời gian chờ đăng nhập (5 phút).")
            context.close()

if __name__ == '__main__':
    main()
