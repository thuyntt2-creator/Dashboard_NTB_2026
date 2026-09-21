from playwright.sync_api import sync_playwright
import time

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={'width': 1536, 'height': 900})
        
        logs = []
        page.on('console', lambda msg: logs.append(f'[{msg.type}] {msg.text}'))
        page.on('pageerror', lambda err: logs.append(f'[PAGE ERROR] {err}'))
        
        page.goto('http://127.0.0.1:3000/hop', wait_until='networkidle')
        time.sleep(1)
        page.click('button[data-tab="tab-truythu"]')
        time.sleep(2)
        
        print('=== ALL CONSOLE LOGS & ERRORS ===')
        for l in logs:
            print(l)
        browser.close()

if __name__ == '__main__':
    main()
