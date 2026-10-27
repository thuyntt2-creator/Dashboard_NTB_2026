import sys
from playwright.sync_api import sync_playwright

with open('app.js', 'r', encoding='utf-8') as f:
    code = f.read()

lines = code.split('\n')
print(f"Total lines: {len(lines)}")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    
    # Binary search lines to find first syntax error
    low = 1
    high = len(lines)
    error_line = -1
    
    # Check full file first
    try:
        page.evaluate(code)
    except Exception as e:
        print(f"Full file error: {e}")
        # Get line info from error
        # In Playwright, evaluate exception might contain line info
        msg = str(e)
        print("Message details:", msg[:500])

    browser.close()
