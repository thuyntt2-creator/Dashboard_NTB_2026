import sys
import paramiko

sys.stdout.reconfigure(encoding='utf-8')

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('103.82.27.107', username='root', password='T403kbek9E1r1nJy')

fix_cmd = """python3 -c '
import re

with open("/root/auto-report/calculate_and_render_report.py", "r", encoding="utf-8") as f:
    text = f.read()

pattern = r"oauth_file\s*=\s*\"credentials_oauth\.json\"\s*auth_user_file\s*=\s*\"authorized_user\.json\""
replacement = "script_dir = os.path.dirname(os.path.abspath(__file__))\\n    oauth_file = os.path.join(script_dir, \\"credentials_oauth.json\\")\\n    auth_user_file = os.path.join(script_dir, \\"authorized_user.json\\")"

new_text, count = re.subn(pattern, replacement, text)
print(f"Substituted count: {count}")
if count > 0:
    with open("/root/auto-report/calculate_and_render_report.py", "w", encoding="utf-8") as f:
        f.write(new_text)
' """

stdin, stdout, stderr = ssh.exec_command(fix_cmd)
print(stdout.read().decode('utf-8', errors='replace'))
print(stderr.read().decode('utf-8', errors='replace'))

ssh.close()
