import sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    def handle_pageerror(err):
        print(f"PAGE ERROR STACK:\n{err.stack if hasattr(err, 'stack') else err}")

    page.on('pageerror', handle_pageerror)
    page.on('console', lambda msg: print(f"CONSOLE: {msg.text}"))

    page.goto('http://127.0.0.1:3000/hop', wait_until='networkidle')
    page.click('button[data-tab="tab-truythu"]')
    page.wait_for_timeout(1000)

    browser.close()
