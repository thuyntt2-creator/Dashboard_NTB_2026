import sys
sys.stdout.reconfigure(encoding='utf-8')
import time
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1600, "height": 1000})
    page.goto('http://127.0.0.1:3000/hop', wait_until='networkidle')
    time.sleep(1)

    # 1. Check Tab 1 Overview has warning table
    print("Checking Tab 1 Overview...")
    ov_tbl = page.locator('#table-bc-canh-bao-overview')
    print("Tab 1 Warning Table count:", ov_tbl.count())
    if ov_tbl.count() > 0:
        ov_tbl.scroll_into_view_if_needed()
        time.sleep(0.5)
        print("Tab 1 Warning Rows:", page.locator('#table-bc-canh-bao-overview tbody tr').count())
        page.screenshot(path='scratch/tab1_warning_table.png')
        print("Saved scratch/tab1_warning_table.png")

    # 2. Check Top Nav Bar for Tab 15
    nav_tab15 = page.locator('button[data-tab="tab-bc-canhbao"]')
    print("Nav Tab 15 count:", nav_tab15.count())
    print("Nav Tab 15 text:", nav_tab15.inner_text())

    # 3. Click Nav Tab 15
    nav_tab15.click()
    time.sleep(1)
    print("Switched to Tab 15! Title:", page.locator('#tab-bc-canhbao .report-card-title').first.inner_text())
    print("Tab 15 Warning Rows:", page.locator('#table-bc-canhbao-tab tbody tr').count())
    page.screenshot(path='scratch/tab15_warning_dedicated.png')
    print("Saved scratch/tab15_warning_dedicated.png")

    # 4. Check Tab 12 button
    page.locator('button[data-tab="tab-aging"]').click()
    time.sleep(0.5)
    btn_canhbao_12 = page.locator('#btn-aging-canhbao')
    print("Tab 12 Canh Bao button count:", btn_canhbao_12.count())
    page.screenshot(path='scratch/tab12_with_canhbao_btn.png')
    print("Saved scratch/tab12_with_canhbao_btn.png")

    browser.close()
    print("All checks completed successfully!")
