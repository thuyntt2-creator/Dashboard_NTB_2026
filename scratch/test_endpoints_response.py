import requests

def test_endpoints():
    endpoints = [
        "/api/operational",
        "/api/opr",
        "/api/backlog",
        "/api/unstable-po",
        "/api/off-spe",
        "/api/volume-creation",
        "/api/user-role"
    ]
    
    base_url = "http://127.0.0.1:5000"
    auth = ("admin", "admin123")
    
    for ep in endpoints:
        url = base_url + ep
        print(f"\nCalling: {url}")
        try:
            res = requests.get(url, auth=auth, timeout=10)
            print(f"Status: {res.status_code}")
            if res.status_code == 200:
                data = res.json()
                print(f"Success! Keys: {list(data.keys()) if isinstance(data, dict) else 'list length ' + str(len(data))}")
            else:
                print(f"Error Body: {res.text}")
        except Exception as e:
            print(f"Request failed: {e}")

if __name__ == '__main__':
    test_endpoints()
