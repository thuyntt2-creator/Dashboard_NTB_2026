import time
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={'width': 1600, 'height': 900})
    
    # 1. Verify Tab 3 GTC Tong on dashboard
    page.goto('http://127.0.0.1:3000/hop', wait_until='networkidle')
    time.sleep(1)
    page.locator('button[data-tab="tab-gtc-tong"]').click()
    time.sleep(0.5)
    page.screenshot(path='scratch/verify_gtc_tong_banner_fixed.png')
    print("Saved scratch/verify_gtc_tong_banner_fixed.png")
    
    # 2. Verify Kich Ban HTML with OPR TTS
    page.goto('http://127.0.0.1:3000/kich-ban', wait_until='networkidle')
    time.sleep(1)
    # Scroll to Section V OPR TTS
    page.evaluate('window.scrollTo(0, 1500)')
    time.sleep(0.5)
    page.screenshot(path='scratch/verify_kich_ban_opr_tts.png')
    print("Saved scratch/verify_kich_ban_opr_tts.png")

    browser.close()
