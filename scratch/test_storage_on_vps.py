import sys
import paramiko

sys.stdout.reconfigure(encoding='utf-8')

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('103.82.27.107', username='root', password='T403kbek9E1r1nJy')

test_code = """
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(storage_state='/root/auto-report/cookies_ghn.json')
    page = context.new_page()
    page.goto('https://baocao.ghn.vn/dashboards/63bd175cd4435a369fade8f5', timeout=60000, wait_until='domcontentloaded')
    page.wait_for_timeout(7000)
    print('URL on VPS:', page.url)
    print('Title on VPS:', page.title())
    
    found_looker = False
    for f in page.frames:
        if 'looker' in f.url or 'datastudio' in f.url:
            print('SUCCESS! Found Looker Studio frame:', f.url[:80])
            found_looker = True
    if not found_looker:
        print('Frames:', [f.url[:50] for f in page.frames])
    browser.close()
"""

stdin, stdout, stderr = ssh.exec_command("cat << 'EOF' > /root/auto-report/test_storage_state.py\n" + test_code + "\nEOF\n")
stdout.channel.recv_exit_status()

stdin, stdout, stderr = ssh.exec_command("python3 /root/auto-report/test_storage_state.py")
print("STDOUT:", stdout.read().decode())
print("STDERR:", stderr.read().decode())
ssh.close()
