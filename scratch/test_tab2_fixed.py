from playwright.sync_api import sync_playwright

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1600, "height": 950})
        page.goto("http://localhost:3000/hop")
        page.wait_for_timeout(1000)

        # click tab-volume
        page.click("button[data-tab='tab-volume']")
        page.wait_for_timeout(1000)
        page.screenshot(path="tab_volume_fixed_preview.png")
        print("Saved tab_volume_fixed_preview.png")

        browser.close()

if __name__ == "__main__":
    main()
