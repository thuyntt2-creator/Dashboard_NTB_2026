import sys
import time
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1440, "height": 900})
    
    errors = []
    page.on("pageerror", lambda err: errors.append(str(err)))
    
    print("Navigating to http://127.0.0.1:3000/hop...")
    page.goto("http://127.0.0.1:3000/hop", wait_until="networkidle")
    time.sleep(2)
    
    # 1. Switch to Tab 12
    page.click('button.tab-item[data-tab="tab-aging"]')
    time.sleep(1.5)
    
    # 2. Switch to Treo LC
    page.click('#btn-aging-treo')
    time.sleep(1.5)
    
    print("Errors on tab switch:", errors)
    
    # Capture Top section (Donut + Customer + Speech)
    page.screenshot(path="scratch/final_treo_lc_top.png")
    print("Captured scratch/final_treo_lc_top.png")
    
    # Scroll to AM Table
    table_am = page.locator('#table-aging-am-detailed')
    if table_am.count() > 0:
        table_am.scroll_into_view_if_needed()
        time.sleep(1)
        table_am.screenshot(path="scratch/final_treo_lc_table_am.png")
        print("Captured scratch/final_treo_lc_table_am.png")
        
    browser.close()
