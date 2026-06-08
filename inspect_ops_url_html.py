import urllib.request

url = "https://docs.google.com/spreadsheets/d/1DAwY-46twFrHIs77R4p4IMuIZ6JTE-e58Aj-9Kcr5Jk/edit"
req = urllib.request.Request(url)
req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)')

output_path = "google_sheet_html_head.txt"

try:
    with urllib.request.urlopen(req) as response:
        html = response.read().decode('utf-8')
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html[:1000])
except Exception as e:
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(f"Error: {e}\n")

print("Done writing google_sheet_html_head.txt")
