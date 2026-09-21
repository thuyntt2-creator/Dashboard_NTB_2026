from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={'width': 1200, 'height': 800})
    page.goto('http://127.0.0.1:3000/kich-ban', wait_until='networkidle')
    page.wait_for_timeout(1000)
    page.screenshot(path='scratch/kich_ban_w38_preview.png')
    print("Captured scratch/kich_ban_w38_preview.png")
    browser.close()
