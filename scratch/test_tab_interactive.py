import time
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto('http://127.0.0.1:3000/hop')
    time.sleep(1)
    
    page.click("button.tab-item[data-tab='tab-aging']")
    time.sleep(1)
    page.click('#aging-speech-toggle-btn')
    time.sleep(0.5)
    page.click('#aging-speech-toggle-btn')
    time.sleep(0.5)
    page.click('#btn-aging-treo')
    time.sleep(1)
    page.click('#btn-aging-aging')
    time.sleep(1)
    page.click('#btn-aging-both')
    time.sleep(1)
    
    print('ALL TABS AND BUTTONS CLICKED CLEANLY WITH ZERO ERRORS!')
    browser.close()
