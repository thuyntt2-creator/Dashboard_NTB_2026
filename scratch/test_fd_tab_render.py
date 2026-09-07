from playwright.sync_api import sync_playwright
import time

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1600, "height": 1000})
        # Force hard reload without cache
        page.goto("http://127.0.0.1:3000/hop", wait_until="networkidle")
        page.wait_for_timeout(1000)

        # Click Tab 10 (%FD Hoàn Trả)
        page.click("button[data-tab='tab-fd']")
        page.wait_for_timeout(1500)

        page.screenshot(path="scratch/fd_top_preview.png")
        print("Captured scratch/fd_top_preview.png")

        # Scroll down to see Bảng 1 and chart
        page.evaluate("window.scrollBy(0, 600)")
        page.wait_for_timeout(1000)
        page.screenshot(path="scratch/fd_table_preview.png")
        print("Captured scratch/fd_table_preview.png")

        browser.close()

if __name__ == "__main__":
    main()
