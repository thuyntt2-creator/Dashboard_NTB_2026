import re
import os

workspace_dir = r"c:\Users\lap4all\Desktop\New folder"
file_path = os.path.join(workspace_dir, "templates", "index.html")
output_path = os.path.join(workspace_dir, "scratch", "inspect_menu_res.txt")

with open(file_path, "r", encoding="utf-8") as f:
    html = f.read()

with open(output_path, "w", encoding="utf-8") as out:
    # 1. Print menu items sidebar
    out.write("=== SIDEBAR MENU ITEMS ===\n")
    menu_match = re.search(r'<ul[^>]*class="[^"]*menu[^"]*"[^>]*>(.*?)</ul>', html, re.DOTALL | re.IGNORECASE)
    if menu_match:
        out.write(menu_match.group(1).strip() + "\n\n")
    else:
        # search for sidebar container
        sidebar_match = re.search(r'<div[^>]*class="[^"]*sidebar[^"]*"[^>]*>(.*?)</div>\s*<div[^>]*class="[^"]*main-content[^"]*"', html, re.DOTALL | re.IGNORECASE)
        if sidebar_match:
            out.write(sidebar_match.group(1).strip() + "\n\n")
            
    # 2. Print overview KPI cards container
    out.write("=== KPI CARDS ON OVERVIEW ===\n")
    # Search for kpi-cards-grid or container containing kpi-card
    grid_matches = re.findall(r'<div[^>]*class="[^"]*kpi-grid[^"]*"[^>]*>.*?</div>\s*</div>', html, re.DOTALL | re.IGNORECASE)
    for idx, grid in enumerate(grid_matches):
        out.write(f"Grid {idx} (length {len(grid)}):\n{grid.strip()[:1000]}...\n\n")
        
    # Also find all elements containing kpi-card
    cards = re.findall(r'<div[^>]*class="kpi-card[^"]*"[^>]*>.*?</div>\s*</div>', html, re.DOTALL | re.IGNORECASE)
    out.write(f"Found {len(cards)} elements matching kpi-card class.\n")
    for idx, card in enumerate(cards[:10]):
        out.write(f"Card {idx}:\n{card.strip()[:500]}...\n\n")

    # 3. Print the structure of the last tab panel (tab-off-spe or tab-sync)
    out.write("=== STRUCTURE OF tab-off-spe PANEL ===\n")
    panel_match = re.search(r'<div id="tab-off-spe"[^>]*>(.*?)</div>\s*<!--\s*tab-off-spe\s*-->', html, re.DOTALL | re.IGNORECASE)
    if not panel_match:
        panel_match = re.search(r'<div id="tab-off-spe"[^>]*>(.*?)</div>\s*<div id="tab-sync"', html, re.DOTALL | re.IGNORECASE)
    if panel_match:
        out.write(panel_match.group(0).strip()[:1000] + "\n\n")
    else:
        out.write("Could not find tab-off-spe panel text.\n")
        
print("Done writing inspect_menu_res.txt")
