import os
from google_auth_oauthlib.flow import InstalledAppFlow

scopes = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

oauth_file = r'C:\Users\lap4all\Documents\Auto report\credentials_oauth.json'
out_targets = [
    r'C:\Users\lap4all\Documents\Auto report\authorized_user.json',
    r'c:\Users\lap4all\Desktop\New folder\authorized_user.json',
    r'C:\Users\lap4all\Desktop\Backlog_Automation\authorized_user.json'
]

print("🌐 Đang mở trình duyệt để đăng nhập OAuth Google...")
flow = InstalledAppFlow.from_client_secrets_file(oauth_file, scopes=scopes)
creds = flow.run_local_server(port=0)

for target in out_targets:
    target_dir = os.path.dirname(target)
    if os.path.exists(target_dir):
        with open(target, 'w', encoding='utf-8') as f:
            f.write(creds.to_json())
        print(f"✅ Đã lưu token mới vào: {target}")

print("🎉 Đăng nhập OAuth thành công!")
