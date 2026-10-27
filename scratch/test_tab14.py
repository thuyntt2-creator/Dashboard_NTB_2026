import time
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={'width': 1600, 'height': 1000})
    page.goto('http://127.0.0.1:3000/hop')
    time.sleep(1)
    
    page.click("button.tab-item[data-tab='tab-truythu']")
    time.sleep(1)
    
    page.screenshot(path='scratch/tab_truythu_view.png')
    print('Captured scratch/tab_truythu_view.png')
    browser.close()
