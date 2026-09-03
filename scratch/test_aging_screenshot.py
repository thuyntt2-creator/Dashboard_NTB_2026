from playwright.sync_api import sync_playwright

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=['--no-sandbox', '--disable-setuid-sandbox'])
        page = browser.new_page(viewport={"width": 1600, "height": 1100})
        page.goto("http://localhost:3000/hop", timeout=30000)
        page.wait_for_timeout(1000)

        # click tab-aging
        page.click("button[data-tab='tab-aging']")
        page.wait_for_timeout(500)

        # click button Aging (>5 Ngày)
        page.click("#btn-aging-aging")
        page.wait_for_timeout(500)

        # scroll down to tables
        page.evaluate("window.scrollTo(0, 600)")
        page.wait_for_timeout(500)

        page.screenshot(path="aging_5days_exact_preview.png")
        print("Saved aging_5days_exact_preview.png")

        browser.close()

if __name__ == "__main__":
    main()
