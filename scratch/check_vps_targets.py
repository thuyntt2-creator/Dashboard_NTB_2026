import paramiko, sys
sys.stdout.reconfigure(encoding='utf-8')
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('103.82.27.107', username='root', password='T403kbek9E1r1nJy')

script = '''
import sys
sys.path.append("/root/auto_report")
import report_nangsuat_direct as rpt
m = rpt.load_alert_hubs_map()
seen = set()
for k, v in m.items():
    if isinstance(v, dict) and "bc_name" in v and v["bc_name"] not in seen:
        seen.add(v["bc_name"])
        print(v["bc_name"] + " | Target: " + str(v.get("target")) + " | Vol: " + str(v.get("vol_today")))
'''

stdin, stdout, stderr = ssh.exec_command(f"python3 -c '{script}'")
print(stdout.read().decode('utf-8', errors='ignore'))
print(stderr.read().decode('utf-8', errors='ignore'))
