from playwright.sync_api import sync_playwright
import time

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={'width': 1536, 'height': 900})
        page.goto('http://127.0.0.1:3000/hop', wait_until='networkidle')
        time.sleep(1)
        page.click('button[data-tab="tab-truythu"]')
        time.sleep(1.5)
        page.screenshot(path='scratch/tab_truythu_current.png', full_page=False)
        print('Captured scratch/tab_truythu_current.png')
        browser.close()

if __name__ == '__main__':
    main()
