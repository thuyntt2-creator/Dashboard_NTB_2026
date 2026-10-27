import sys
from playwright.sync_api import sync_playwright

with open('app.js', 'r', encoding='utf-8') as f:
    code = f.read()

lines = code.split('\n')

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    
    # We test functions or blocks
    # Specifically, check lines around our recent edits (7900 - 8450)
    for start in range(7850, 8450, 50):
        end = min(start + 100, len(lines))
        chunk = '\n'.join(lines[start:end])
        # test if chunk has mismatched brackets or syntax
        # Let's test eval of a wrapper function
        test_script = f"""
        try {{
            new Function(`{chunk}`);
        }} catch(e) {{
            console.log("Error in lines {start}-{end}: " + e.message);
        }}
        """
        # Alternatively, find line with ')' that causes issues
    
    # Let's inspect git diff of app.js!
    browser.close()
