# -*- coding: utf-8 -*-
import os
import sys
import io
import paramiko

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

local_file = r"C:\Users\lap4all\Documents\Auto report\autonangsuat.py"
with open(local_file, "r", encoding="utf-8") as f:
    content = f.read()

# Replace _run_job_once browser initialization
old_block = """        try:
            browser = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
            print("✅ Đã kết nối với Chrome debug thành công!", flush=True)
            if len(browser.contexts) == 0:
                print("❌ Không tìm thấy Chrome context.", flush=True)
                browser.close()
                return
            context = browser.contexts[0]

            for pg in context.pages:
                if "baocao.ghn.vn" in pg.url:
                    ghn_page = pg
                    break

            if not ghn_page:
                print("ℹ️ Không tìm thấy tab baocao.ghn.vn, mở tab mới trên Chrome debug...", flush=True)
                ghn_page = context.new_page()
                ghn_page.goto(DASHBOARD_URL)
        except Exception as e:
            print(f"⚠️ Không kết nối được Chrome debug. Lỗi: {e}", flush=True)
            print("🌐 Tự động mở trình duyệt độc lập mới (Persistent Browser)...", flush=True)
            is_cdp = False
            profile_dir = os.path.join(SCRIPT_DIR, "playwright_profile")
            os.makedirs(profile_dir, exist_ok=True)

            print("🧹 Kiểm tra & dọn tiến trình msedge.exe cũ đang giữ profile (nếu có)...", flush=True)
            _kill_stale_edge_for_profile(profile_dir)

            context = p.chromium.launch_persistent_context(
                user_data_dir=profile_dir,
                channel="msedge",
                headless=False,
                accept_downloads=True,
                args=[
                    "--start-maximized",
                    "--disable-blink-features=AutomationControlled",
                    "--no-sandbox"
                ]
            )
            context.on("close", lambda: print(
                "⚠️ [DEBUG] Sự kiện 'close': context/browser vừa bị đóng.",
                flush=True
            ))
            ghn_page = context.pages[0] if len(context.pages) > 0 else context.new_page()
            print(f"👉 Mở trang báo cáo: {DASHBOARD_URL}", flush=True)
            ghn_page.goto(DASHBOARD_URL)"""

new_block = """        is_github_actions = os.environ.get("GITHUB_ACTIONS") == "true"
        cookie_file = os.path.join(SCRIPT_DIR, "cookies_ghn.json")
        if not os.path.exists(cookie_file):
            cookie_file = "/root/auto-report/cookies_ghn.json"
        cookie_env = os.environ.get("GHN_COOKIES")
        is_linux = sys.platform.startswith("linux")

        if is_github_actions or is_linux:
            print("🐧 Đang chạy ở chế độ Headless với Cookies (VPS / Cloud mode)...", flush=True)
            is_cdp = False
            browser = p.chromium.launch(
                headless=True,
                args=[
                    "--no-sandbox",
                    "--disable-setuid-sandbox",
                    "--disable-dev-shm-usage"
                ]
            )
            try:
                if cookie_env:
                    import json
                    storage_state = json.loads(cookie_env)
                    context = browser.new_context(storage_state=storage_state, accept_downloads=True)
                elif os.path.exists(cookie_file):
                    import json
                    with open(cookie_file, 'r', encoding='utf-8') as f:
                        storage_state = json.load(f)
                    context = browser.new_context(storage_state=storage_state, accept_downloads=True)
                else:
                    context = browser.new_context(accept_downloads=True)
                print("✅ Đã load cookies thành công.", flush=True)
            except Exception as e:
                print(f"❌ Lỗi load cookies: {e}", flush=True)
                context = browser.new_context(accept_downloads=True)

            ghn_page = context.new_page()
            ghn_page.goto(DASHBOARD_URL, timeout=60000, wait_until="domcontentloaded")
            ghn_page.wait_for_timeout(7000)
        else:
            try:
                browser = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
                print("✅ Đã kết nối với Chrome debug thành công!", flush=True)
                if len(browser.contexts) == 0:
                    print("❌ Không tìm thấy Chrome context.", flush=True)
                    browser.close()
                    return
                context = browser.contexts[0]

                for pg in context.pages:
                    if "baocao.ghn.vn" in pg.url:
                        ghn_page = pg
                        break

                if not ghn_page:
                    print("ℹ️ Không tìm thấy tab baocao.ghn.vn, mở tab mới trên Chrome debug...", flush=True)
                    ghn_page = context.new_page()
                    ghn_page.goto(DASHBOARD_URL)
            except Exception as e:
                print(f"⚠️ Không kết nối được Chrome debug. Lỗi: {e}", flush=True)
                print("🌐 Tự động mở trình duyệt độc lập mới (Persistent Browser)...", flush=True)
                is_cdp = False
                profile_dir = os.path.join(SCRIPT_DIR, "playwright_profile")
                os.makedirs(profile_dir, exist_ok=True)

                print("🧹 Kiểm tra & dọn tiến trình msedge.exe cũ đang giữ profile (nếu có)...", flush=True)
                _kill_stale_edge_for_profile(profile_dir)

                context = p.chromium.launch_persistent_context(
                    user_data_dir=profile_dir,
                    channel="msedge",
                    headless=False,
                    accept_downloads=True,
                    args=[
                        "--start-maximized",
                        "--disable-blink-features=AutomationControlled",
                        "--no-sandbox"
                    ]
                )
                context.on("close", lambda: print(
                    "⚠️ [DEBUG] Sự kiện 'close': context/browser vừa bị đóng.",
                    flush=True
                ))
                ghn_page = context.pages[0] if len(context.pages) > 0 else context.new_page()
                print(f"👉 Mở trang báo cáo: {DASHBOARD_URL}", flush=True)
                ghn_page.goto(DASHBOARD_URL)"""

# Also ensure finally cleans up browser when not is_cdp
old_finally = """        finally:
            try:
                if is_cdp:
                    if browser:
                        browser.close()
                else:
                    if context:
                        context.close()
            except Exception:
                pass"""

new_finally = """        finally:
            try:
                if is_cdp:
                    if browser:
                        browser.close()
                else:
                    if context:
                        context.close()
                    if browser:
                        browser.close()
            except Exception:
                pass"""

# Check iframe timeout and looker frame loop
old_iframe = """        try:
            print("⏳ Đang kiểm tra trạng thái đăng nhập...", flush=True)
            ghn_page.wait_for_selector("iframe", timeout=10000)
        except Exception:
            print("🔑 Vui lòng thực hiện đăng nhập tài khoản GHN trên cửa sổ trình duyệt vừa mở...", flush=True)
            try:
                ghn_page.wait_for_selector("iframe", timeout=120000)
                print("✅ Đăng nhập thành công!", flush=True)
            except Exception as err:
                print(f"❌ Chi tiết lỗi khi chờ đăng nhập: {err}", flush=True)
                print("❌ Hết thời gian chờ đăng nhập (3 phút). Vui lòng chạy lại script.", flush=True)
                if is_cdp:
                    browser.close()
                else:
                    context.close()
                return"""

new_iframe = """        try:
            print("⏳ Đang kiểm tra trạng thái đăng nhập...", flush=True)
            ghn_page.wait_for_selector("iframe", timeout=30000)
        except Exception:
            if is_linux:
                print("❌ Không tìm thấy iframe báo cáo (có thể cookies đã hết hạn).", flush=True)
                if browser:
                    browser.close()
                return
            print("🔑 Vui lòng thực hiện đăng nhập tài khoản GHN trên cửa sổ trình duyệt vừa mở...", flush=True)
            try:
                ghn_page.wait_for_selector("iframe", timeout=120000)
                print("✅ Đăng nhập thành công!", flush=True)
            except Exception as err:
                print(f"❌ Chi tiết lỗi khi chờ đăng nhập: {err}", flush=True)
                print("❌ Hết thời gian chờ đăng nhập (3 phút). Vui lòng chạy lại script.", flush=True)
                if is_cdp:
                    browser.close()
                else:
                    context.close()
                return"""

if old_block not in content:
    print("❌ Cannot find old_block in autonangsuat.py")
    sys.exit(1)

content = content.replace(old_block, new_block)
content = content.replace(old_finally, new_finally)
content = content.replace(old_iframe, new_iframe)

# Save updated local file
with open(local_file, "w", encoding="utf-8") as f:
    f.write(content)
print("✅ Đã cập nhật file local:", local_file)

# Upload to VPS
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('103.82.27.107', username='root', password='T403kbek9E1r1nJy', timeout=10)

sftp = ssh.open_sftp()
with sftp.file('/root/auto-report/autonangsuat.py', 'w') as remote_f:
    remote_f.write(content)
sftp.close()
print("✅ Đã tải file autonangsuat.py lên VPS /root/auto-report/autonangsuat.py!")
ssh.close()
