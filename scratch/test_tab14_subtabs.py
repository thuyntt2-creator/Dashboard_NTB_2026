import time
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={'width': 1600, 'height': 1000})
    errors = []
    page.on('pageerror', lambda err: errors.append(str(err)))
    page.goto('http://127.0.0.1:3000/hop')
    time.sleep(1)
    
    page.click("button.tab-item[data-tab='tab-truythu']")
    time.sleep(1)
    
    page.click('#btn-tt-loai')
    time.sleep(0.5)
    page.click('#btn-tt-amticket')
    time.sleep(0.5)
    page.click('#btn-tt-bcgiao')
    time.sleep(0.5)
    page.click('#btn-tt-bcticket')
    time.sleep(0.5)
    
    print('Tab 14 subtabs clicked cleanly! Page errors:', errors)
    browser.close()
