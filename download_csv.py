import urllib.request

url = "https://docs.google.com/spreadsheets/d/1DAwY-46twFrHIs77R4p4IMuIZ6JTE-e58Aj-9Kcr5Jk/export?format=csv&gid=1400910659"
req = urllib.request.Request(url)
req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)')

output_path = "thu_cung_ky.csv"

try:
    with urllib.request.urlopen(req) as response:
        content = response.read()
    with open(output_path, "wb") as f:
        f.write(content)
    print("Success downloading CSV! Characters written:", len(content))
except Exception as e:
    print("Error downloading CSV:", e)
