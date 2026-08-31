import os, sys, json, urllib.request, urllib.parse

possible_paths = [
    r'authorized_user.json',
    r'C:\Users\lap4all\Documents\Auto report\authorized_user.json',
    r'C:\Users\lap4all\Desktop\Backlog_Automation\authorized_user.json',
]

access_token = None
for token_path in possible_paths:
    if not os.path.exists(token_path):
        continue
    try:
        with open(token_path, 'r', encoding='utf-8') as f:
            token_data = json.load(f)
        data = urllib.parse.urlencode({
            'grant_type': 'refresh_token',
            'client_id': token_data['client_id'],
            'client_secret': token_data['client_secret'],
            'refresh_token': token_data['refresh_token']
        }).encode('utf-8')
        req = urllib.request.Request(token_data['token_uri'], data=data, headers={'Content-Type': 'application/x-www-form-urlencoded'})
        with urllib.request.urlopen(req, timeout=10) as resp:
            res = json.loads(resp.read().decode('utf-8'))
            access_token = res.get("access_token")
            if access_token:
                break
    except Exception as e:
        pass

sheet_id = "1JZ1eRerRqrpwjZ4HBevQunjd8VquM_cvPFz12TaJfMQ"
api_url = f"https://sheets.googleapis.com/v4/spreadsheets/{sheet_id}?fields=sheets.properties"
headers = {'Authorization': f'Bearer {access_token}'}

req = urllib.request.Request(api_url, headers=headers)
with urllib.request.urlopen(req, timeout=15) as resp:
    data = json.loads(resp.read().decode('utf-8'))
    for s in data.get('sheets', []):
        props = s.get('properties', {})
        title = props.get('title')
        gid = props.get('sheetId')
        sys.stdout.buffer.write(f"GID: {gid:<12} | Title: {title}\n".encode('utf-8'))
