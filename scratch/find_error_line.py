import sys
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.on('pageerror', lambda err: print(f"PAGE ERROR: {err} | message: {err.message} | name: {err.name}"))
    page.on('console', lambda msg: print(f"CONSOLE: {msg.text} ({msg.location})"))
    page.goto('http://127.0.0.1:3000/hop')
    page.wait_for_timeout(2000)
    browser.close()
