import requests
import sys

sys.stdout.reconfigure(encoding='utf-8')

url = "http://127.0.0.1:5000/api/upload"
headers = {
    "Authorization": "Basic YWRtaW46YWRtaW4xMjM="
}

# The user has the Excel file. Let's upload 'Copy o NTB - BÁO CÁO VẬN HÀNH.xlsx' to the server.
file_path = r"c:\Users\lap4all\Desktop\New folder\Copy o NTB - BÁO CÁO VẬN HÀNH.xlsx"

print("Uploading file to server...")
try:
    with open(file_path, 'rb') as f:
        files = {
            'file': ('Copy o NTB - BÁO CÁO VẬN HÀNH.xlsx', f, 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        }
        data = {
            'filename': 'Copy o NTB - BÁO CÁO VẬN HÀNH.xlsx'
        }
        res = requests.post(url, headers=headers, files=files, data=data, timeout=30)
        
    print("Status code:", res.status_code)
    print("JSON Response:", res.json())
except Exception as e:
    print("Error:", e)
