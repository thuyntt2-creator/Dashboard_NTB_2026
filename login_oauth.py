import json
import os
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

TARGET_FILES = [
    r'c:\Users\lap4all\Desktop\Backlog_Automation\authorized_user.json',
    r'C:\Users\lap4all\Documents\Auto report\authorized_user.json',
    r'C:\Users\lap4all\Desktop\New folder\authorized_user.json'
]

def main():
    base_file = None
    for f_path in TARGET_FILES:
        if os.path.exists(f_path):
            base_file = f_path
            break

    if not base_file:
        print("❌ Không tìm thấy file authorized_user.json cũ!")
        return

    with open(base_file, 'r', encoding='utf-8') as f:
        old_data = json.load(f)

    client_config = {
        "installed": {
            "client_id": old_data["client_id"],
            "client_secret": old_data["client_secret"],
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": old_data.get("token_uri", "https://oauth2.googleapis.com/token"),
            "redirect_uris": ["http://localhost:8080/"]
        }
    }

    flow = InstalledAppFlow.from_client_config(client_config, scopes=SCOPES)
    
    print("\n" + "="*70)
    print("👉 Đang khởi chạy máy chủ xác thực...")
    print("Trình duyệt sẽ tự động mở. Nếu không thấy mở, hãy click vào đường link xuất hiện bên dưới.")
    print("="*70 + "\n")

    creds = flow.run_local_server(port=8080, prompt='consent', access_type='offline')

    auth_json = {
        "token": creds.token,
        "refresh_token": creds.refresh_token,
        "token_uri": creds.token_uri,
        "client_id": creds.client_id,
        "client_secret": creds.client_secret,
        "scopes": creds.scopes,
        "universe_domain": getattr(creds, "universe_domain", "googleapis.com"),
        "account": getattr(creds, "account", "")
    }

    for target in TARGET_FILES:
        try:
            if os.path.exists(os.path.dirname(target)):
                with open(target, 'w', encoding='utf-8') as f:
                    json.dump(auth_json, f, indent=2)
                print(f"✅ Đã lưu token mới vào: {target}")
        except Exception as e:
            print(f"⚠️ Không thể ghi {target}: {e}")

    print("\n🎉 ĐĂNG NHẬP OAUTH THÀNH CÔNG! Đã cập nhật xong token.")

if __name__ == '__main__':
    main()
