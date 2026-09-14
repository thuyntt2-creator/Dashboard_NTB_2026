import sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

with sync_playwright() as p:
    b = p.chromium.launch(headless=True)
    page = b.new_page()
    page.goto('http://127.0.0.1:3000/hop')
    page.wait_for_timeout(1000)

    page.click('[data-tab="tab-gtc-tong"]')
    page.wait_for_timeout(500)
    print('GTC Full thead:', page.locator('#table-gtc-full-detailed thead tr').inner_text().replace('\n', ' | '))
    print('GTC TTS thead:', page.locator('#table-gtc-tts-detailed thead tr').inner_text().replace('\n', ' | '))

    page.click('[data-tab="tab-odr"]')
    page.wait_for_timeout(500)
    print('ODR Full thead:', page.locator('#table-odr-full-detailed thead tr').inner_text().replace('\n', ' | '))
    print('ODR TTS thead:', page.locator('#table-odr-tts-detailed thead tr').inner_text().replace('\n', ' | '))

    b.close()
