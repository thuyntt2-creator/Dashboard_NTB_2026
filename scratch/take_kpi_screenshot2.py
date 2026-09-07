from playwright.sync_api import sync_playwright
import time

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1536, "height": 950})
        page.goto('http://127.0.0.1:3000/hop', wait_until='networkidle')
        time.sleep(2)
        
        # Screenshot of the executive banner and BOTH rows of KPI tiles
        page.screenshot(path='scratch/verify_both_rows_kpi.png', clip={"x": 0, "y": 60, "width": 1536, "height": 700})
        print("Captured scratch/verify_both_rows_kpi.png successfully!")
        browser.close()

if __name__ == '__main__':
    main()
