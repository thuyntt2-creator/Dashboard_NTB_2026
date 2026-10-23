import paramiko, sys
sys.stdout.reconfigure(encoding='utf-8')
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('103.82.27.107', username='root', password='T403kbek9E1r1nJy')

script = """
import sys
sys.path.append('/root/auto_report')
import report_nangsuat_direct as rpt

data = rpt.fetch_all_productivity_direct()
for am_block in data:
    for bc_name, staff in am_block['bcs']:
        low = bc_name.lower()
        if 'kiến đức' in low or 'kien duc' in low or 'tân hà' in low or 'tan ha' in low:
            total_gtc = sum(int(nv.get('tc', 0)) for nv in staff)
            total_gan = sum(int(nv.get('gan', 0)) for nv in staff)
            print(bc_name, '(AM ' + am_block['am'] + '): GTC=' + str(total_gtc) + ', Gan=' + str(total_gan))
"""

stdin, stdout, stderr = ssh.exec_command(f'python3 -c "{script}"')
print(stdout.read().decode('utf-8', errors='ignore'))
print(stderr.read().decode('utf-8', errors='ignore'))
