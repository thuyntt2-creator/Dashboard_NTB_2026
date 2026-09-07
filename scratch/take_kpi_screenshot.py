from playwright.sync_api import sync_playwright
import time

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1536, "height": 900})
        page.goto('http://127.0.0.1:3000/hop', wait_until='networkidle')
        time.sleep(2)
        
        # Screenshot of the executive banner and KPI tiles
        page.screenshot(path='scratch/verify_kpi_cards_w36.png', clip={"x": 0, "y": 60, "width": 1536, "height": 550})
        print("Captured scratch/verify_kpi_cards_w36.png successfully!")
        browser.close()

if __name__ == '__main__':
    main()
