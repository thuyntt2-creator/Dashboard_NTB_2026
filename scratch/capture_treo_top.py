import time
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={'width': 1600, 'height': 850})
    page.goto('http://127.0.0.1:3000/hop', wait_until='networkidle')
    time.sleep(1)
    page.locator('button[data-tab="tab-aging"]').click()
    time.sleep(0.5)
    page.locator('#btn-aging-treo').click()
    time.sleep(0.5)
    # Scroll slightly to show headers and rows 1 to 10
    page.evaluate('window.scrollTo(0, 680)')
    time.sleep(0.5)
    page.screenshot(path='scratch/treo_lc_top_rows.png')
    browser.close()
    print("Done")
