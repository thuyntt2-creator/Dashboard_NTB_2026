import asyncio
from playwright.async_api import async_playwright

async def verify_top_treo():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={'width': 1600, 'height': 900})
        await page.goto('http://127.0.0.1:3000/hop', wait_until='networkidle')
        await page.wait_for_timeout(1000)

        # Tab Aging/Treo LC
        await page.click('button[data-tab="tab-aging"]')
        await page.wait_for_timeout(500)
        # Click Treo LC subtab
        await page.click('#btn-aging-treo')
        await page.wait_for_timeout(600)

        card = page.locator('#tab-aging .grid-row-2')
        await card.screenshot(path='scratch/verify_treo_cards_split.png')
        print('Captured Treo Split Cards!')

        await browser.close()

asyncio.run(verify_top_treo())
