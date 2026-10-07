# -*- coding: utf-8 -*-
import sys
import paramiko

sys.stdout.reconfigure(encoding='utf-8')

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('103.82.27.107', username='root', password='T403kbek9E1r1nJy', timeout=10)

test_code = """
import json
from playwright.sync_api import sync_playwright

with open('/root/auto-report/cookies_ghn.json', 'r', encoding='utf-8') as f:
    state = json.load(f)

print('Số lượng cookie:', len(state.get('cookies', [])))
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(storage_state=state)
    page = context.new_page()
    page.goto('https://baocao.ghn.vn/dashboards/63bd175cd4435a369fade8f5')
    page.wait_for_timeout(8000)
    print('Tiêu đề trang:', page.title())
    iframe_count = page.locator('iframe').count()
    print('Số lượng iframe tìm thấy:', iframe_count)
    if iframe_count > 0:
        print('🎉 XÁC NHẬN: COOKIE MỚI HOẠT ĐỘNG HOÀN HẢO! ĐÃ VÀO TRỰC TIẾP TRANG BÁO CÁO!')
    else:
        print('URL hiện tại:', page.url)
    browser.close()
"""

sftp = ssh.open_sftp()
with sftp.file('/root/auto-report/check_cookie.py', 'w') as f:
    f.write(test_code)
sftp.close()

_, stdout, _ = ssh.exec_command('python3 /root/auto-report/check_cookie.py')
print(stdout.read().decode())

ssh.close()
