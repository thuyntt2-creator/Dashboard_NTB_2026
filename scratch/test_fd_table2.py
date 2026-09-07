from playwright.sync_api import sync_playwright

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1600, "height": 1000})
        page.goto("http://127.0.0.1:3000/hop", wait_until="networkidle")
        page.wait_for_timeout(1000)

        # Click Tab 10 (%FD Hoàn Trả)
        page.click("button[data-tab='tab-fd']")
        page.wait_for_timeout(1000)

        # Scroll down to Bảng 2
        page.evaluate("window.scrollBy(0, 1400)")
        page.wait_for_timeout(1000)
        page.screenshot(path="scratch/fd_table2_preview.png")
        print("Captured scratch/fd_table2_preview.png")

        browser.close()

if __name__ == "__main__":
    main()
