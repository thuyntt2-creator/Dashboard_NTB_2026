from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1440, "height": 900})
    page.goto("http://127.0.0.1:3000/hop", wait_until="networkidle")
    page.wait_for_timeout(1000)

    # 1. Capture Tab 3 table headers
    page.click('[data-tab="tab-gtc-tong"]')
    page.wait_for_timeout(500)
    page.locator("#gtctong-tables-split-grid").scroll_into_view_if_needed()
    page.screenshot(path="scratch/header_tab3_gtc.png")

    # 2. Capture Tab 6 table headers
    page.click('[data-tab="tab-odr"]')
    page.wait_for_timeout(500)
    page.locator("#odr-tables-split-grid").scroll_into_view_if_needed()
    page.screenshot(path="scratch/header_tab6_odr.png")

    browser.close()
