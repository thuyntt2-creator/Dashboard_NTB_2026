from playwright.sync_api import sync_playwright

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=['--no-sandbox', '--disable-setuid-sandbox'])
        page = browser.new_page(viewport={"width": 1600, "height": 400})
        page.goto("http://localhost:3000/hop", timeout=30000)
        page.wait_for_timeout(500)

        page.screenshot(path="header_date_preview.png")
        print("Saved header_date_preview.png")

        browser.close()

if __name__ == "__main__":
    main()
