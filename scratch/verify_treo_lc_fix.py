import sys
import time
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1440, "height": 900})
    
    print("Navigating to http://127.0.0.1:3000/hop...")
    page.goto("http://127.0.0.1:3000/hop", wait_until="networkidle")
    time.sleep(2)
    
    # Click Tab 12: Aging & Treo LC
    tab_aging_btn = page.locator('button[data-tab="tab-aging"]')
    if tab_aging_btn.count() > 0:
        tab_aging_btn.first.click()
        time.sleep(1.5)
        print("Clicked Tab Aging & Treo LC")
    
    # Click segment Treo Luân Chuyển
    btn_treo = page.locator('#btn-seg-treo_lc')
    if btn_treo.count() > 0:
        btn_treo.first.click()
        time.sleep(2)
        print("Switched to Treo Luân Chuyển segment")
    
    # Screenshot top area (donut chart & title & speech box)
    page.screenshot(path="scratch/verify_treo_lc_top.png")
    print("Saved scratch/verify_treo_lc_top.png")
    
    # Scroll down to table AM
    table_am = page.locator('#table-aging-am-detailed')
    if table_am.count() > 0:
        table_am.scroll_into_view_if_needed()
        time.sleep(1)
        table_am.screenshot(path="scratch/verify_treo_lc_table_am.png")
        print("Saved scratch/verify_treo_lc_table_am.png")
        
    browser.close()
