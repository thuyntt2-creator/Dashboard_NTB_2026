from playwright.sync_api import sync_playwright
import time

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={'width': 1536, 'height': 900})
        page.goto('http://127.0.0.1:3000/hop', wait_until='networkidle')
        time.sleep(1)
        
        # Click Tab 14
        page.click('button[data-tab="tab-truythu"]')
        time.sleep(1)
        
        # Panel 1: Loai
        page.screenshot(path='scratch/tt_panel1_loai.png')
        print("Captured Panel 1: Loai")
        
        # Panel 2: AM
        page.click('#btn-tt-amticket')
        time.sleep(1)
        page.screenshot(path='scratch/tt_panel2_am.png')
        print("Captured Panel 2: AM")
        
        # Panel 3: BC Giao & Tỉnh
        page.click('#btn-tt-bcgiao')
        time.sleep(1)
        page.screenshot(path='scratch/tt_panel3_bcgiao.png')
        print("Captured Panel 3: BC Giao")
        
        # Panel 4: BC Ticket
        page.click('#btn-tt-bcticket')
        time.sleep(1)
        page.screenshot(path='scratch/tt_panel4_bcticket.png')
        print("Captured Panel 4: BC Ticket")
        
        browser.close()

if __name__ == '__main__':
    main()
