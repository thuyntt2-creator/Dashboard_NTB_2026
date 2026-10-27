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
    
    # Force switch tab & segment via JS
    page.evaluate("""
        document.querySelectorAll('.tab-item').forEach(t => t.classList.remove('active'));
        document.querySelectorAll('.tab-view').forEach(v => v.classList.remove('active'));
        const btn = document.querySelector('.tab-item[data-tab="tab-aging"]');
        if (btn) btn.classList.add('active');
        const view = document.getElementById('tab-aging');
        if (view) view.classList.add('active');
        if (typeof window.setAgingSegment === 'function') {
            window.setAgingSegment('treo_lc');
        }
    """)
    time.sleep(1.5)
    
    # Check text
    donut_title = page.evaluate("document.getElementById('aging-donut-title')?.textContent")
    donut_badge = page.evaluate("document.getElementById('aging-donut-total-badge')?.textContent")
    print(f"Donut Title: {donut_title}")
    print(f"Donut Badge: {donut_badge}")
    
    # Check headers
    headers = page.evaluate("""
        Array.from(document.querySelectorAll('#table-aging-am-detailed thead th')).map(th => th.innerText.trim())
    """)
    print("\nHeaders of Table AM (count = {}): {}".format(len(headers), headers))
    
    # Check row 1
    row1 = page.evaluate("""
        Array.from(document.querySelectorAll('#table-aging-am-detailed tbody tr:first-child td')).map(td => td.innerText.trim().replace(/\\n/g, ' '))
    """)
    print("Row 1 of Table AM:", row1)
    
    # Check total row
    total_row = page.evaluate("""
        Array.from(document.querySelectorAll('#table-aging-am-detailed tbody tr:last-child td')).map(td => td.innerText.trim().replace(/\\n/g, ' '))
    """)
    print("Total Row of Table AM:", total_row)
    
    page.screenshot(path="scratch/final_verified_treo_lc_top.png")
    
    page.evaluate("document.getElementById('table-aging-am-detailed')?.scrollIntoView()")
    time.sleep(0.5)
    page.screenshot(path="scratch/final_verified_treo_lc_table.png")
    
    print("\nSUCCESS! Saved both screenshots.")
    browser.close()
