from playwright.sync_api import sync_playwright

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1600, "height": 1100})
        page.goto("http://localhost:3000/hop")
        page.wait_for_timeout(1000)

        # click tab-opr-tts
        page.click("button[data-tab='tab-opr-tts']")
        page.wait_for_timeout(1000)

        page.screenshot(path="opr_tts_chart_sorted_preview.png")
        print("Saved opr_tts_chart_sorted_preview.png")

        browser.close()

if __name__ == "__main__":
    main()
