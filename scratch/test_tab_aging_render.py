import sys
import time
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1440, "height": 950})
    
    print("Navigating to http://127.0.0.1:3000/hop...")
    page.goto("http://127.0.0.1:3000/hop", wait_until="networkidle")
    page.wait_for_timeout(2000)
    
    # Click Tab 12
    page.evaluate("""
        const tab = document.querySelector('.tab-item[data-tab="tab-aging"]');
        if (tab) tab.click();
    """)
    page.wait_for_timeout(1000)
    
    # Switch to Treo LC
    page.evaluate("""
        if (typeof window.setAgingSegment === 'function') {
            window.setAgingSegment('treo_lc');
        } else {
            const btn = document.querySelector('#btn-aging-treo');
            if (btn) btn.click();
        }
    """)
    page.wait_for_timeout(1500)
    
    # Check Active Tab ID
    active_tab = page.evaluate("document.querySelector('.tab-view.active')?.id")
    print(f"Active Tab ID: {active_tab}")
    
    donut_title = page.evaluate("document.getElementById('aging-donut-title')?.textContent")
    donut_badge = page.evaluate("document.getElementById('aging-donut-total-badge')?.textContent")
    print(f"Donut Title: {donut_title}")
    print(f"Donut Badge: {donut_badge}")
    
    # Headers of table AM
    headers = page.evaluate("""
        Array.from(document.querySelectorAll('#table-aging-am-detailed thead th')).map(th => th.innerText.trim())
    """)
    print("\nHeaders of Table AM:", headers)
    
    # Row 1 of table AM
    row1 = page.evaluate("""
        Array.from(document.querySelectorAll('#table-aging-am-detailed tbody tr:first-child td')).map(td => td.innerText.trim().replace(/\\n/g, ' '))
    """)
    print("Row 1 of Table AM:", row1)
    
    # Total row of table AM
    total_row = page.evaluate("""
        Array.from(document.querySelectorAll('#table-aging-am-detailed tbody tr:last-child td')).map(td => td.innerText.trim().replace(/\\n/g, ' '))
    """)
    print("Total Row of Table AM:", total_row)
    
    page.screenshot(path="scratch/check_final_treo_lc_top.png")
    
    page.evaluate("document.getElementById('table-aging-am-detailed')?.scrollIntoView()")
    page.wait_for_timeout(500)
    page.screenshot(path="scratch/check_final_treo_lc_table.png")
    
    print("Screenshots saved!")
    browser.close()
