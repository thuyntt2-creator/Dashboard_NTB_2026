from playwright.sync_api import sync_playwright
import time

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1600, "height": 900})
        
        page.goto('http://127.0.0.1:3000/hop')
        page.wait_for_load_state('networkidle')
        time.sleep(2)
        
        # Click KTC tab
        page.click('button[data-tab="tab-ktc"]')
        time.sleep(1)
        
        # Click Fill Rate
        page.click('#btn-ktc-fillrate')
        time.sleep(1.5)
        
        # Switch to weekly and scroll to chart
        page.click('#btn-fr-weekly')
        time.sleep(1)
        
        # Scroll to chart
        page.evaluate("window.scrollTo(0, 600)")
        time.sleep(0.5)
        page.screenshot(path='scratch/ktc_fillrate_chart_preview.png', full_page=False)
        print("Fill rate chart screenshot saved")
        
        # Scroll to causes table
        page.evaluate("window.scrollTo(0, 1200)")
        time.sleep(0.5)
        page.screenshot(path='scratch/ktc_fillrate_causes_preview.png', full_page=False)
        print("Causes table screenshot saved")
        
        # Click leadtime sub-view
        page.click('#btn-ktc-leadtime')
        time.sleep(1)
        page.screenshot(path='scratch/ktc_leadtime_preview.png', full_page=False)
        print("Leadtime screenshot saved")
        
        browser.close()

main()
