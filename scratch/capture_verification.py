import sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1440, "height": 900})
    page.goto("http://127.0.0.1:3000/hop", wait_until="networkidle")
    page.wait_for_timeout(1000)

    # 1. Capture Tab 3: GTC TTS table (Screenshot 1 fix)
    page.click('[data-tab="tab-gtc-tong"]')
    page.wait_for_timeout(500)
    page.locator("#table-gtc-tts-detailed").scroll_into_view_if_needed()
    page.screenshot(path="scratch/verified_tab3_gtc_tts.png")

    # 2. Capture Tab 5: Gan Overview Chart (Screenshot 2 fix)
    page.click('[data-tab="tab-gan"]')
    page.wait_for_timeout(500)
    page.locator("#chart-gan-overview-bar").scroll_into_view_if_needed()
    page.screenshot(path="scratch/verified_tab5_gan_chart.png")

    # 3. Capture Tab 6: ODR TTS table (Screenshot 3 & 4 fix)
    page.click('[data-tab="tab-odr"]')
    page.wait_for_timeout(500)
    page.locator("#table-odr-tts-detailed").scroll_into_view_if_needed()
    page.screenshot(path="scratch/verified_tab6_odr_tts.png")

    print("✓ All screenshots captured successfully!")
    browser.close()
