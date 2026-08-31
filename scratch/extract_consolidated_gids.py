import urllib.request
import re

url = "https://docs.google.com/spreadsheets/d/1JZ1eRerRqrpwjZ4HBevQunjd8VquM_cvPFz12TaJfMQ/edit"
req = urllib.request.Request(url)
req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)')

try:
    with urllib.request.urlopen(req) as response:
        html = response.read().decode('utf-8')
        
    pattern = r'\[\s*\d+\s*,\s*0\s*,\s*\\"?(\d+)\\"?\s*,\s*\[\s*\{\s*\\"?1\\"?\s*:\s*\[\s*\[\s*0\s*,\s*0\s*,\s*\\"?([^\\"\(\]]+)\\"?'
    matches = re.findall(pattern, html)
    
    with open("scratch/consolidated_gids.txt", "w", encoding="utf-8") as f:
        if matches:
            for gid, name in matches:
                f.write(f"GID: {gid} -> Name: {name}\n")
            print(f"Success: extracted {len(matches)} sheets to scratch/consolidated_gids.txt")
        else:
            f.write("No sheet matches found in HTML edit response.\n")
            # Let's dump a small portion of HTML around bootstrap data or raw list of strings
            f.write("Searching for bootstrap data...\n")
            pos = html.find("bootstrap_data")
            if pos != -1:
                f.write(html[pos:pos+5000])
            print("Warning: no GID pattern matches found.")
            
except Exception as e:
    print("Error:", e)
