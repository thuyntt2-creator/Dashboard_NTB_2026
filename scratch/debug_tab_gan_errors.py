from playwright.sync_api import sync_playwright

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1600, "height": 1100})
        
        errors = []
        page.on("pageerror", lambda err: errors.append(str(err)))
        page.on("console", lambda msg: print("CONSOLE:", msg.type, msg.text))

        page.goto("http://localhost:3000/hop")
        page.wait_for_timeout(1000)

        # click tab-gan
        page.click("button[data-tab='tab-gan']")
        page.wait_for_timeout(1000)

        print("Page Errors:", errors)
        browser.close()

if __name__ == "__main__":
    main()
