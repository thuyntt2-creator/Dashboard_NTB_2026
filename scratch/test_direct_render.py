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
    
    # Force switch tab & call renderAgingTab directly
    page.evaluate("""
        document.querySelectorAll('.tab-item').forEach(t => t.classList.remove('active'));
        document.querySelectorAll('.tab-view').forEach(v => v.classList.remove('active'));
        const btn = document.querySelector('.tab-item[data-tab="tab-aging"]');
        if (btn) btn.classList.add('active');
        const view = document.getElementById('tab-aging');
        if (view) view.classList.add('active');
        
        // Set segment to treo_lc
        setAgingSegment('treo_lc');
    """)
    time.sleep(1.5)
    
    # Scroll and Screenshot table AM
    page.evaluate("document.getElementById('table-aging-am-detailed')?.scrollIntoView()")
    time.sleep(0.5)
    page.screenshot(path="scratch/verified_treo_lc_table_rendered.png")
    
    # Scroll to top to capture Donut & script
    page.evaluate("window.scrollTo(0, 0)")
    time.sleep(0.5)
    page.screenshot(path="scratch/verified_treo_lc_top_rendered.png")
    
    print("Screenshots taken successfully!")
    browser.close()
