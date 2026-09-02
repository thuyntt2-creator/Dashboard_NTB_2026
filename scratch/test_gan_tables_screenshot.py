from playwright.sync_api import sync_playwright

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1600, "height": 1100})
        page.goto("http://localhost:3000/hop")
        page.wait_for_timeout(1000)

        # click tab-gan
        page.click("button[data-tab='tab-gan']")
        page.wait_for_timeout(500)

        # scroll down to tables
        page.evaluate("window.scrollTo(0, 700)")
        page.wait_for_timeout(500)

        page.screenshot(path="gan_tab_tables_preview.png")
        print("Saved gan_tab_tables_preview.png")

        browser.close()

if __name__ == "__main__":
    main()
