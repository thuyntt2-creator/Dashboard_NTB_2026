import re
import os

workspace_dir = r"c:\Users\lap4all\Desktop\New folder"
file_path = os.path.join(workspace_dir, "templates", "index.html")
output_path = os.path.join(workspace_dir, "scratch", "inspect_index_html_res.txt")

with open(file_path, "r", encoding="utf-8") as f:
    html = f.read()

with open(output_path, "w", encoding="utf-8") as out:
    out.write(f"index.html length: {len(html)} characters\n\n")
    
    # Find all tab buttons or navigation tabs
    out.write("--- Tab Buttons / Navigation ---\n")
    tabs = re.findall(r'<button\s+[^>]*class="[^"]*tab[^"]*"[^>]*>.*?</button>', html, re.IGNORECASE | re.DOTALL)
    for idx, tab in enumerate(tabs[:15]):
        out.write(f"Tab {idx}: {tab.strip()}\n")
        
    out.write("\n--- Tab Content Containers ---\n")
    containers = re.findall(r'<div\s+[^>]*id="[^"]*tab[^"]*"[^>]*>', html, re.IGNORECASE)
    for idx, c in enumerate(containers):
        out.write(f"Container {idx}: {c}\n")
        
    # Let's search for "OFF Tuyến SPE" card or tab to find exactly where it was inserted
    out.write("\n--- Occurrences of SPE ---\n")
    spe_matches = [m.start() for m in re.finditer(r'spe', html, re.IGNORECASE)]
    out.write(f"Found {len(spe_matches)} matches for 'spe'.\n")
    for pos in spe_matches[:5]:
        start = max(0, pos - 100)
        end = min(len(html), pos + 100)
        out.write(f"Match at {pos}: ... {html[start:end].strip()} ...\n")
        
    # Let's search for the script section where data fetching and API calls are defined
    out.write("\n--- Fetch API Calls in Scripts ---\n")
    fetches = re.findall(r'fetch\([^\)]*\)', html, re.IGNORECASE)
    for idx, f_call in enumerate(fetches[:15]):
        out.write(f"Fetch {idx}: {f_call}\n")

print("Done writing inspect_index_html_res.txt")
