import time
import sys
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={'width': 1600, 'height': 900})
    page.goto('http://127.0.0.1:3000/hop', wait_until='networkidle')
    time.sleep(1)
    page.locator('button[data-tab="tab-bc-canhbao"]').click()
    time.sleep(0.5)
    page.evaluate('window.scrollTo(0, 0)')
    time.sleep(0.5)
    page.screenshot(path='scratch/top_banner_tab15_clean.png')
    browser.close()
    print("Saved scratch/top_banner_tab15_clean.png")
