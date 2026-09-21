from playwright.sync_api import sync_playwright
import time

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={'width': 1536, 'height': 900})
        page.goto('http://127.0.0.1:3000/hop', wait_until='networkidle')
        time.sleep(1)
        
        page.click('button[data-tab="tab-truythu"]')
        time.sleep(1)
        
        # Capture default ranking by Tiền
        page.screenshot(path='scratch/tt_rank_by_tien.png')
        print("Captured scratch/tt_rank_by_tien.png")
        
        # Click sort by Đơn
        page.click('#btn-sort-tt-don')
        time.sleep(0.5)
        page.screenshot(path='scratch/tt_rank_by_don.png')
        print("Captured scratch/tt_rank_by_don.png")
        
        browser.close()

if __name__ == '__main__':
    main()
