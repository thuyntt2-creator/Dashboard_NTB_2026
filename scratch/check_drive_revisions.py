import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

creds = Credentials.from_authorized_user_file('authorized_user.json', ['https://www.googleapis.com/auth/drive'])
drive_service = build('drive', 'v3', credentials=creds)

source_id = "15Z-aMM6OFfiWUXd2Zwz6BFNq_Y0KWwHiVDqxkioHufM"
file_meta = drive_service.files().get(fileId=source_id, fields="id, name, modifiedTime, lastModifyingUser, owners").execute()
print("File metadata:", file_meta)

revs = drive_service.revisions().list(fileId=source_id, fields="revisions(id, modifiedTime, lastModifyingUser)").execute()
print("\nRevisions count:", len(revs.get('revisions', [])))
for r in revs.get('revisions', [])[-10:]:
    print(r)
