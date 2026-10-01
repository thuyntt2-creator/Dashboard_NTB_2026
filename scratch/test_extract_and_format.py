import os
import sys
import unicodedata
from collections import defaultdict
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

sys.stdout.reconfigure(encoding='utf-8')

sheet_id = '1JSbLo353RgRCTuGyyMmPH7jiB48tNIRMXR6KMze39jg'
creds = Credentials.from_authorized_user_file('authorized_user.json', ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive'])
service = build('sheets', 'v4', credentials=creds)

res1 = service.spreadsheets().values().get(spreadsheetId=sheet_id, range='Sheet1').execute()
sheet1_vals = res1.get('values', [])

res3 = service.spreadsheets().values().get(spreadsheetId=sheet_id, range='Sheet3').execute()
sheet3_vals = res3.get('values', [])

def norm(text):
    if not text:
        return ""
    return unicodedata.normalize('NFC', str(text)).strip()

token = None
am_to_group = {}
for r in sheet3_vals:
    if len(r) >= 2:
        k = norm(r[0])
        v = norm(r[1])
        if k == 'TOKEN':
            token = v
        elif k and v:
            am_to_group[k] = v

print(f"Token: {token}")
print("Sheet3 AM count:", len(am_to_group))

# Parse orders from Sheet1
orders_by_am = defaultdict(list)
all_orders = []

for idx, r in enumerate(sheet1_vals[1:], start=2):
    vung = norm(r[0]) if len(r) > 0 else ''
    tinh = norm(r[1]) if len(r) > 1 else ''
    bc = norm(r[2]) if len(r) > 2 else ''
    madh = norm(r[3]) if len(r) > 3 else ''
    am = norm(r[4]) if len(r) > 4 else ''
    
    if madh:
        item = {'row': idx, 'vung': vung, 'tinh': tinh, 'bc': bc, 'madh': madh, 'am': am}
        all_orders.append(item)
        orders_by_am[am].append(item)

print(f"Total orders: {len(all_orders)}")
print(f"Unique AMs in orders: {len(orders_by_am)}")

for am, items in orders_by_am.items():
    gid = am_to_group.get(am)
    print(f"\nAM: '{am}' -> {len(items)} đơn | Group ID: {gid}")
    # Group by bưu cục
    by_bc = defaultdict(list)
    for it in items:
        by_bc[it['bc']].append(it['madh'])
    for bc, mads in by_bc.items():
        print(f"   * Bưu cục: {bc} ({len(mads)} đơn): {', '.join(mads)}")
