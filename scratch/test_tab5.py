import sys
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={'width': 1600, 'height': 1000})
    
    console_logs = []
    page.on('console', lambda msg: console_logs.append(f'[{msg.type}] {msg.text}'))
    page.on('pageerror', lambda err: console_logs.append(f'[PAGE_ERROR] {err}'))

    page.goto('file:///c:/Users/lap4all/Desktop/New folder/index.html')
    page.wait_for_timeout(1000)

    # Click Tab 5
    print('Clicking Tab 5...')
    page.click('button[data-tab="tab-gan"]')
    page.wait_for_timeout(1000)

    # Click under80 filter
    print('Clicking under80 filter...')
    page.click('button[data-gan-filter="under80"]')
    page.wait_for_timeout(1000)

    page.screenshot(path='scratch/tab5_test.png', full_page=False)
    browser.close()

    print(f'Total console logs: {len(console_logs)}')
    for log in console_logs:
        if 'error' in log.lower() or 'warn' in log.lower() or 'page_error' in log.lower():
            print(log)
