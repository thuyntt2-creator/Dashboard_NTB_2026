import sys
import time
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1440, "height": 950})
    
    print("Navigating to http://127.0.0.1:3000/hop...")
    page.goto("http://127.0.0.1:3000/hop", wait_until="networkidle")
    time.sleep(2)
    
    # Click Tab 12 via DOM click
    page.evaluate("document.querySelector('button.tab-item[data-tab=\"tab-aging\"]').click()")
    time.sleep(1.5)
    
    # Click Treo LC button via DOM click
    page.evaluate("document.querySelector('#btn-aging-treo').click()")
    time.sleep(1.5)
    
    # Print titles and texts
    donut_title = page.inner_text('#aging-donut-title')
    donut_badge = page.inner_text('#aging-donut-total-badge')
    print("Donut Title:", donut_title)
    print("Donut Badge:", donut_badge)
    
    # Print Table AM Header
    th_am = [th.inner_text().strip() for th in page.query_selector_all('#table-aging-am-detailed thead th')]
    print("\nTable AM Headers (count = {}):".format(len(th_am)))
    for idx, h in enumerate(th_am):
        print(f"  Col {idx+1}: {h}")
    
    # Print Table AM First Row
    td_r1 = [td.inner_text().strip().replace('\n', ' ') for td in page.query_selector_all('#table-aging-am-detailed tbody tr:first-child td')]
    print("\nTable AM Row 1 (count = {}):".format(len(td_r1)))
    for idx, d in enumerate(td_r1):
        print(f"  Col {idx+1}: {d}")
    
    # Print Table AM Total Row
    td_total = [td.inner_text().strip().replace('\n', ' ') for td in page.query_selector_all('#table-aging-am-detailed tbody tr:last-child td')]
    print("\nTable AM Total Row (count = {}):".format(len(td_total)))
    for idx, d in enumerate(td_total):
        print(f"  Col {idx+1}: {d}")
    
    # Screenshot full page of tab aging
    page.screenshot(path="scratch/treo_lc_fixed_top.png")
    print("\nSaved scratch/treo_lc_fixed_top.png")
    
    # Scroll and Screenshot table AM
    page.evaluate("document.querySelector('#table-aging-am-detailed').scrollIntoView()")
    time.sleep(1)
    page.screenshot(path="scratch/treo_lc_fixed_table_am.png")
    print("Captured scratch/treo_lc_fixed_table_am.png")
        
    browser.close()
