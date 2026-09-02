from playwright.sync_api import sync_playwright

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1600, "height": 950})
        page.goto("http://localhost:3000/hop")
        page.wait_for_timeout(1000)

        # click tab-gtc-tong
        page.click("button[data-tab='tab-gtc-tong']")
        page.wait_for_timeout(500)

        # click button to switch to TTS segment in tab 3
        page.click("button[onclick*=\"setGtcTongSegment('tts')\"]")
        page.wait_for_timeout(1000)

        page.screenshot(path="gtc_tong_tts_fixed_preview.png")
        print("Saved gtc_tong_tts_fixed_preview.png")

        browser.close()

if __name__ == "__main__":
    main()
