import sys
sys.stdout.reconfigure(encoding='utf-8')
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

creds = Credentials.from_authorized_user_file('authorized_user.json', ['https://www.googleapis.com/auth/spreadsheets'])
service = build('sheets', 'v4', credentials=creds)

for sid, sname in [('15Z-aMM6OFfiWUXd2Zwz6BFNq_Y0KWwHiVDqxkioHufM', 'Working Sheet'), ('1odUPX5mWpUYUUQOrhX_k8kXWV7drMUdQ58DRwgSQNS8', 'Master FD')]:
    print(f"Checking {sname}...")
    meta = service.spreadsheets().get(spreadsheetId=sid).execute()
    for s in meta['sheets']:
        title = s['properties']['title']
        try:
            res = service.spreadsheets().values().get(spreadsheetId=sid, range=f"'{title}'!A1:B30").execute()
            rows = res.get('values', [])
            found = False
            for r in rows:
                for c in r:
                    if '21/09' in str(c) or '9/21' in str(c):
                        print(f"  Found 21/09 in {title}: {r}")
                        found = True
                        break
                if found: break
        except Exception:
            pass
print("Done checking.")
