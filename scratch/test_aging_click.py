import sys
import time
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1440, "height": 950})
    
    page.goto("http://127.0.0.1:3000/hop", wait_until="networkidle")
    time.sleep(2)
    
    # Click Tab 12
    btn_tab = page.locator('button.tab-item[data-tab="tab-aging"]')
    print("Found tab button:", btn_tab.count())
    btn_tab.click()
    time.sleep(2)
    
    # Click Treo LC
    btn_treo = page.locator('#btn-aging-treo')
    print("Found treo button:", btn_treo.count())
    btn_treo.click()
    time.sleep(2)
    
    # Screenshot top
    page.screenshot(path="scratch/shot_treo_top.png")
    
    # Screenshot table AM
    page.locator('#table-aging-am-detailed').scroll_into_view_if_needed()
    time.sleep(1)
    page.screenshot(path="scratch/shot_treo_table.png")
    
    print("Done screenshots!")
    browser.close()
