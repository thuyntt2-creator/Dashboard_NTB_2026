import time
import sys
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={'width': 1600, 'height': 1000})
    page.goto('http://127.0.0.1:3000/hop', wait_until='networkidle')
    time.sleep(1)
    page.locator('button[data-tab="tab-aging"]').click()
    time.sleep(0.5)
    page.locator('#btn-aging-treo').click()
    time.sleep(0.5)
    page.locator('#table-aging-am-detailed').scroll_into_view_if_needed()
    time.sleep(0.5)
    page.screenshot(path='scratch/treo_lc_tables_final_preview.png')
    browser.close()
    print("Saved scratch/treo_lc_tables_final_preview.png")
