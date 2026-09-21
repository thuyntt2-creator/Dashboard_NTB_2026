import sys
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={'width': 1600, 'height': 1200})
    page.goto('http://127.0.0.1:3000/hop', wait_until='networkidle')
    page.wait_for_timeout(2000)

    # 1. Switch to tab-volume
    page.click('button[data-tab="tab-volume"]')
    page.wait_for_timeout(1000)
    page.screenshot(path='scratch/redesign_tab_volume.png')
    print("Captured scratch/redesign_tab_volume.png")

    # 2. Switch to tab-gtc-tong
    page.click('button[data-tab="tab-gtc-tong"]')
    page.wait_for_timeout(1000)
    page.screenshot(path='scratch/redesign_tab_gtc_tong.png')
    print("Captured scratch/redesign_tab_gtc_tong.png")

    # 3. Switch to tab-odr
    page.click('button[data-tab="tab-odr"]')
    page.wait_for_timeout(1000)
    page.screenshot(path='scratch/redesign_tab_odr.png')
    print("Captured scratch/redesign_tab_odr.png")

    browser.close()
