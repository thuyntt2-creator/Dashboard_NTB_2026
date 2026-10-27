import sys, time
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={'width': 1600, 'height': 1000})
    page.goto('http://127.0.0.1:3000/hop')
    time.sleep(1)
    
    page.click("button.tab-item[data-tab='tab-control']")
    time.sleep(1)
    
    val = page.locator('#kpi-cod-total-val').inner_text()
    meta = page.locator('#kpi-cod-total-meta').inner_text()
    cash = page.locator('#kpi-cod-cash-val').inner_text()
    bank = page.locator('#kpi-cod-bank-val').inner_text()
    rate = page.locator('#kpi-cod-rate-val').inner_text()
    
    print('Total COD:', val, '|', meta)
    print('Cash:', cash)
    print('Bank:', bank)
    print('Rate TM:', rate)
    
    # Also click Subtab 2 (AM So Sánh 2 Tuần) as shown in user's screenshot
    page.click('#btn-cod-am')
    time.sleep(1)
    page.screenshot(path='scratch/tab13_subtab2_am.png')
    print('Captured scratch/tab13_subtab2_am.png')
    
    browser.close()
