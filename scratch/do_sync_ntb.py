import urllib.request
import os

url = 'https://docs.google.com/spreadsheets/d/1JZ1eRerRqrpwjZ4HBevQunjd8VquM_cvPFz12TaJfMQ/export?format=csv&gid=1301452336'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
content = urllib.request.urlopen(req).read()

with open('buu_cuc_bat_on.csv', 'wb') as f:
    f.write(content)

print("Downloaded latest buu_cuc_bat_on.csv, size:", len(content))
