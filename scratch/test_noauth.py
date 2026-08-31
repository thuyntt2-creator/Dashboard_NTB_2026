import os
import requests
import re
from dotenv import load_dotenv

load_dotenv(override=True)

url = os.getenv('CONSOLIDATED_URL', 'https://docs.google.com/spreadsheets/d/1JZ1eRerRqrpwjZ4HBevQunjd8VquM_cvPFz12TaJfMQ/edit')

headers_noauth = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
}

print(f"Testing url without auth header: {url}", flush=True)
try:
    r = requests.get(url, headers=headers_noauth, timeout=10)
    print(f"Status Code: {r.status_code}", flush=True)
    print(f"Content Length: {len(r.content)}", flush=True)
    
    match = re.search(r'/spreadsheets/d/([a-zA-Z0-9-_]+)', url)
    if match:
        ssid = match.group(1)
        export_url = f"https://docs.google.com/spreadsheets/d/{ssid}/export?format=xlsx"
        print(f"Testing export_url without auth header: {export_url}", flush=True)
        r_exp = requests.get(export_url, headers=headers_noauth, timeout=10)
        print(f"Export Status Code: {r_exp.status_code}", flush=True)
        print(f"Export Content Length: {len(r_exp.content)}", flush=True)
except Exception as e:
    print(f"Error: {e}", flush=True)
