import sys
import requests

sys.stdout.reconfigure(encoding='utf-8')

r = requests.get('https://namtrungbo.vercel.app/', timeout=15)
target = 'id="tab-off-spe"'
pos = r.text.find(target, 70000)
if pos != -1:
    print(r.text[pos:pos+2500])
else:
    print("Not found")
