import requests

r = requests.get('https://namtrungbo.vercel.app/', timeout=15)
print("Status code:", r.status_code)
print("Length:", len(r.text))
print("First 300 chars:")
print(r.text[:300])

# Check for specific strings
for term in ['custom-table', 'tab-off-spe', 'off_tuyen', 'BÁO CÁO VẬN HÀNH', 'Outfit']:
    print(f"Contains '{term}':", term in r.text)
