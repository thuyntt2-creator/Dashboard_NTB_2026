from playwright.sync_api import sync_playwright

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1600, "height": 1100})
        page.goto("http://localhost:3000/hop")
        page.wait_for_timeout(1000)

        # click tab-ltc
        page.click("button[data-tab='tab-ltc']")
        page.wait_for_timeout(500)

        # scroll down to tables
        page.evaluate("window.scrollTo(0, 600)")
        page.wait_for_timeout(500)

        page.screenshot(path="ltc_tab_5_provinces_preview.png")
        print("Saved ltc_tab_5_provinces_preview.png")

        browser.close()

if __name__ == "__main__":
    main()
