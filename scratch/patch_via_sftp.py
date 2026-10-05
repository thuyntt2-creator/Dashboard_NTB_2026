import sys
import os
import re
import paramiko

sys.stdout.reconfigure(encoding='utf-8')

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('103.82.27.107', username='root', password='T403kbek9E1r1nJy')

sftp = ssh.open_sftp()
with sftp.open('/root/auto-report/calculate_and_render_report.py', 'r') as f:
    content = f.read().decode('utf-8')

pattern = r'oauth_file\s*=\s*"credentials_oauth\.json"\s*auth_user_file\s*=\s*"authorized_user\.json"'
replacement = '''script_dir = os.path.dirname(os.path.abspath(__file__))
    oauth_file = os.path.join(script_dir, "credentials_oauth.json")
    auth_user_file = os.path.join(script_dir, "authorized_user.json")'''

new_content, count = re.subn(pattern, replacement, content)
print(f"Patched calculate_and_render_report.py matches: {count}")

if count > 0:
    with sftp.open('/root/auto-report/calculate_and_render_report.py', 'w') as f:
        f.write(new_content.encode('utf-8'))
    print("File saved successfully via SFTP!")
else:
    print("Pattern did not match!")

sftp.close()
ssh.close()
