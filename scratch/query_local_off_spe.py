import requests
try:
    res = requests.get("http://127.0.0.1:5000/api/off-spe", auth=('admin', 'admin123'))
    print("Status code:", res.status_code)
    print("Response json:", res.json())
except Exception as e:
    print("Error:", e)
