from playwright.sync_api import sync_playwright
import time

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1600, "height": 900})
        
        print("Navigating to KTC tab...")
        page.goto('http://127.0.0.1:3000/hop')
        page.wait_for_load_state('networkidle')
        time.sleep(2)
        
        # Click KTC tab
        ktc_btn = page.query_selector('button[data-tab="tab-ktc"]')
        if ktc_btn:
            ktc_btn.click()
            time.sleep(1)
            page.screenshot(path='scratch/ktc_backlog_preview.png', full_page=False)
            print("Backlog tab screenshot saved")
        else:
            print("ERROR: KTC tab button not found")
            page.screenshot(path='scratch/ktc_error_preview.png')
        
        # Click Fill Rate sub-view
        fr_btn = page.query_selector('#btn-ktc-fillrate')
        if fr_btn:
            fr_btn.click()
            time.sleep(1.5)
            page.screenshot(path='scratch/ktc_fillrate_preview.png', full_page=False)
            print("Fill rate screenshot saved")
            
            # Switch to weekly view
            weekly_btn = page.query_selector('#btn-fr-weekly')
            if weekly_btn:
                weekly_btn.click()
                time.sleep(1)
                page.screenshot(path='scratch/ktc_fillrate_weekly_preview.png', full_page=False)
                print("Weekly fill rate screenshot saved")
        
        browser.close()

main()
