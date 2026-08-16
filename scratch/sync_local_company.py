import os
import sys
import json
import urllib.request
import urllib.parse
import requests
import re
import unicodedata
import pandas as pd
from dotenv import load_dotenv

load_dotenv(override=True)

# 1. Get OAuth token using local authorized_user.json
token_path = 'authorized_user.json'
if not os.path.exists(token_path):
    print("Error: authorized_user.json not found!", flush=True)
    sys.exit(1)

with open(token_path, 'r', encoding='utf-8') as f:
    token_data = json.load(f)

data = urllib.parse.urlencode({
    'grant_type': 'refresh_token',
    'client_id': token_data['client_id'],
    'client_secret': token_data['client_secret'],
    'refresh_token': token_data['refresh_token']
}).encode('utf-8')

req = urllib.request.Request(token_data['token_uri'], data=data, headers={'Content-Type': 'application/x-www-form-urlencoded'})

access_token = None
try:
    with urllib.request.urlopen(req, timeout=10) as resp:
        res = json.loads(resp.read().decode('utf-8'))
        access_token = res.get("access_token")
        print("Success! Acquired OAuth access_token from authorized_user.json.", flush=True)
except Exception as e:
    print(f"Error getting access token: {e}", flush=True)
    sys.exit(1)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)',
    'Authorization': f'Bearer {access_token}'
}

url = os.getenv('CONSOLIDATED_URL', 'https://docs.google.com/spreadsheets/d/1JZ1eRerRqrpwjZ4HBevQunjd8VquM_cvPFz12TaJfMQ/edit')
print(f"Connecting to company Google Sheet: {url}", flush=True)

match = re.search(r'/spreadsheets/d/([a-zA-Z0-9-_]+)', url)
if not match:
    print("Invalid Google Sheet URL!", flush=True)
    sys.exit(1)
spreadsheet_id = match.group(1)

edit_url = f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}/edit"
r_edit = requests.get(edit_url, headers=headers, timeout=20)
if r_edit.status_code != 200:
    print(f"Failed to access Google Sheet: HTTP {r_edit.status_code}", flush=True)
    sys.exit(1)

html = r_edit.text
pattern = r'\[\s*\d+\s*,\s*0\s*,\s*\\"?(\d+)\\"?\s*,\s*\[\s*\{\s*\\"?1\\"?\s*:\s*\[\s*\[\s*0\s*,\s*0\s*,\s*\\"?([^\\"\(\]]+)\\"?'
matches = re.findall(pattern, html)
print(f"Extracted {len(matches)} tabs/sheets from company Google Sheet.", flush=True)

gid_map = {}
for gid, name in matches:
    norm_name = unicodedata.normalize('NFC', name.strip().lower())
    gid_map[norm_name] = gid

sheet_mappings = [
    (["data"], "ops_gtc.csv"),
    (["dataltc", "rawltc", "data ltc"], "ops_ltc.csv"),
    (["cocauvung", "cơ cấu", "co_cau", "co cau"], "ops_co_cau.csv"),
    (["cocauvung", "cơ cấu", "co_cau", "co cau"], "co_cau_ntb.csv"),
    (["tts"], "ops_tts.csv"),
    (["opr"], "opr_opr.csv"),
    (["raw n-1", "oe_madh", "raw_n-1", "raw n - 1", "oe madh"], "opr_oe.csv"),
    (["rawopr"], "opr_raw.csv"),
    (["aging trên 5 ngày", "aging tren 5 ngay", "đơn giao aging trên 5 ngày", "don giao aging tren 5 ngay"], "aging_raw.csv"),
    (["treo lc", "stuck", "treo luân chuyển", "treo luan chuyen"], "treo_stuck.csv"),
    (["ntb", "bất ổn", "bat_on", "cảnh báo"], "buu_cuc_bat_on.csv"),
    (["đang off", "dang off", "off", "off_tuyen", "off tuyến"], "off_tuyen_spe.csv"),
    (["shopee_tiktok", "tao_don", "tạo đơn"], "vols_tao_don.csv"),
    (["odr tts", "odr_tts"], "ODR TTS.csv"),
    (["fd"], "ops_fd.csv"),
    (["baocao", "báo cáo"], "ops_productivity_realtime.csv"),
    (["nhân sự", "nhan su"], "ops_nhan_su.csv"),
    (["trên10kg", "tren10kg", "trên 10kg", "tren 10kg", "10kg", "hàng 10kg"], "raw_tren10kg.csv")
]

downloaded_count = 0
for candidates, target_csv in sheet_mappings:
    matched_gid = None
    for cand in candidates:
        cand_clean = unicodedata.normalize('NFC', cand.strip().lower())
        if cand_clean in gid_map:
            matched_gid = gid_map[cand_clean]
            break
    if matched_gid:
        csv_url = f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}/export?format=csv&gid={matched_gid}"
        r_csv = requests.get(csv_url, headers=headers, timeout=30)
        if r_csv.status_code == 200 and len(r_csv.content) > 10:
            with open(target_csv, 'wb') as f_out:
                f_out.write(r_csv.content)
            downloaded_count += 1
            print(f"Downloaded {target_csv} ({len(r_csv.content)} bytes)", flush=True)

print(f"\nCOMPLETED LOCAL SYNC! Downloaded {downloaded_count} CSV files.", flush=True)
