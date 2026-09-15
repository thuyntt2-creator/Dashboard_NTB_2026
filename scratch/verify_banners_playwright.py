import asyncio
from playwright.async_api import async_playwright

async def verify():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={'width': 1400, 'height': 900})
        await page.goto('http://127.0.0.1:3000/hop', wait_until='networkidle')
        await page.wait_for_timeout(1000)

        # Tab 1: FD Card
        fd_card = page.locator('#card-fd_pair')
        if await fd_card.count() > 0:
            await fd_card.screenshot(path='scratch/verify_fd_card.png')
            print("Captured FD Card screenshot: scratch/verify_fd_card.png")

        # Tab 4: GTC Ca 1
        await page.click('button[data-tab="tab-gtc-tts-ca1"]')
        await page.wait_for_timeout(500)
        banner_tab4 = page.locator('#tab-gtc-tts-ca1 .exec-banner')
        if await banner_tab4.count() > 0:
            await banner_tab4.screenshot(path='scratch/verify_tab4_banner.png')
            print("Captured Tab 4 Banner screenshot: scratch/verify_tab4_banner.png")

        # Tab 5: Gan
        await page.click('button[data-tab="tab-gan"]')
        await page.wait_for_timeout(500)
        banner_tab5 = page.locator('#tab-gan .exec-banner')
        if await banner_tab5.count() > 0:
            await banner_tab5.screenshot(path='scratch/verify_tab5_banner.png')
            print("Captured Tab 5 Banner screenshot: scratch/verify_tab5_banner.png")

        # Tab 6: ODR
        await page.click('button[data-tab="tab-odr"]')
        await page.wait_for_timeout(500)
        banner_tab6 = page.locator('#tab-odr .exec-banner')
        if await banner_tab6.count() > 0:
            await banner_tab6.screenshot(path='scratch/verify_tab6_banner.png')
            print("Captured Tab 6 Banner screenshot: scratch/verify_tab6_banner.png")

        # Tab 8: OPR
        await page.click('button[data-tab="tab-opr-tts"]')
        await page.wait_for_timeout(500)
        banner_tab8 = page.locator('#tab-opr-tts .exec-banner')
        if await banner_tab8.count() > 0:
            await banner_tab8.screenshot(path='scratch/verify_tab8_banner.png')
            print("Captured Tab 8 Banner screenshot: scratch/verify_tab8_banner.png")

        await browser.close()

asyncio.run(verify())
