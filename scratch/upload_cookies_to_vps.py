# -*- coding: utf-8 -*-
import sys
import os
import paramiko

sys.stdout.reconfigure(encoding='utf-8')

VPS_IP = '103.82.27.107'
VPS_USER = 'root'
VPS_PASS = 'T403kbek9E1r1nJy'
REMOTE_DIR = '/root/auto-report'

LOCAL_COOKIE_FILE = os.path.join(os.path.dirname(__file__), "cookies_ghn.json")

def main():
    print(f"Connecting to VPS {VPS_IP}...")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(VPS_IP, username=VPS_USER, password=VPS_PASS, timeout=15)
    print("SSH connected.")

    sftp = ssh.open_sftp()
    remote_cookie_file = f"{REMOTE_DIR}/cookies_ghn.json"
    print(f"Uploading {LOCAL_COOKIE_FILE} to {remote_cookie_file}...")
    sftp.put(LOCAL_COOKIE_FILE, remote_cookie_file)
    print("Upload complete!")
    sftp.close()

    # Test accessing baocao.ghn.vn on VPS using python script
    test_script = """
import json
from playwright.sync_api import sync_playwright

with open('/root/auto-report/cookies_ghn.json', 'r', encoding='utf-8') as f:
    storage = json.load(f)

cookies = storage.get('cookies', [])
print(f'Loaded {len(cookies)} cookies.')

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context()
    context.add_cookies(cookies)
    page = context.new_page()
    page.goto('https://baocao.ghn.vn/dashboards/63bd175cd4435a369fade8f5', timeout=60000, wait_until='domcontentloaded')
    page.wait_for_timeout(7000)
    print('URL on VPS:', page.url)
    print('Title on VPS:', page.title())
    
    # Check if iframe exists
    iframes = page.frames
    print(f'Total frames found: {len(iframes)}')
    for f in iframes:
        if 'looker' in f.url or 'datastudio' in f.url or 'google' in f.url:
            print('Found Looker Studio frame:', f.url[:80])
    
    browser.close()
"""
    # Write test script to VPS
    stdin, stdout, stderr = ssh.exec_command("cat << 'EOF' > /root/auto-report/test_cookie_access.py\n" + test_script + "\nEOF\n")
    stdout.channel.recv_exit_status()

    # Run test script
    print("\nRunning test on VPS...")
    stdin, stdout, stderr = ssh.exec_command("python3 /root/auto-report/test_cookie_access.py")
    out = stdout.read().decode('utf-8', errors='replace')
    err = stderr.read().decode('utf-8', errors='replace')
    print("--- Output from VPS ---")
    print(out)
    if err:
        print("--- Error from VPS ---")
        print(err)

    ssh.close()

if __name__ == "__main__":
    main()
