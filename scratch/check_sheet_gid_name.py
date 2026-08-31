import sys, urllib.request, re, unicodedata

sys.stdout.reconfigure(encoding='utf-8')

spreadsheet_id = "1JZ1eRerRqrpwjZ4HBevQunjd8VquM_cvPFz12TaJfMQ"
edit_url = f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}/edit"
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'

print(f"Fetching edit HTML to extract GIDs from: {edit_url}")
req = urllib.request.Request(edit_url, headers={'User-Agent': user_agent})

try:
    with urllib.request.urlopen(req, timeout=20) as r:
        html = r.read().decode('utf-8')

    pattern = r'\[\s*\d+\s*,\s*0\s*,\s*\\"?(\d+)\\"?\s*,\s*\[\s*\{\s*\\"?1\\"?\s*:\s*\[\s*\[\s*0\s*,\s*0\s*,\s*\\"?([^\\"\(\]]+)\\"?'
    matches = re.findall(pattern, html)
    print(f"Extracted {len(matches)} matches:")
    for gid, name in matches:
        norm_name = unicodedata.normalize('NFC', name.strip().lower())
        print(f"GID: {gid} -> Raw Name: '{name}' | Norm Name: '{norm_name}'")

        if gid == "1203902008":
            print(f"  *** MATCH FOR GID 1203902008! Raw: '{name}', Norm: '{norm_name}' ***")
except Exception as e:
    print(f"Error fetching HTML: {e}")
