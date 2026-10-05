from playwright.sync_api import sync_playwright
import os, sys

sys.stdout.reconfigure(encoding='utf-8')

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={'width': 1600, 'height': 1200})
    file_path = os.path.abspath('index.html').replace('\\', '/')
    page.goto('file:///' + file_path)
    page.wait_for_timeout(1000)
    
    # Click on Tab 2: Sản Lượng Giao
    page.locator('button[data-tab="tab-volume"]').click()
    page.wait_for_timeout(1500)
    
    # Check rows in Bang 3A
    rows_3a = page.locator('#table-volume-tinh-full tbody tr').all()
    print(f"Bang 3A (Full) rows: {len(rows_3a)}")
    for r in rows_3a:
        print("  3A:", " | ".join(r.inner_text().split()))
        
    # Check rows in Bang 3B
    rows_3b = page.locator('#table-volume-tinh-tts tbody tr').all()
    print(f"Bang 3B (TTS) rows: {len(rows_3b)}")
    for r in rows_3b:
        print("  3B:", " | ".join(r.inner_text().split()))
        
    # Screenshot Tab 2 top section
    page.screenshot(path='verify_tab2_5_provinces.png', clip={'x': 0, 'y': 150, 'width': 1600, 'height': 750})
    print("Screenshot saved: verify_tab2_5_provinces.png")
    browser.close()
