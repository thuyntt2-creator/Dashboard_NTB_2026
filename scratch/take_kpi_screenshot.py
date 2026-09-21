import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 1400, "height": 900})
        await page.goto("http://127.0.0.1:3000/hop", wait_until="networkidle")
        await page.wait_for_timeout(2000)
        
        # Take screenshot of overview kpi tiles
        tiles = page.locator("#overview-kpi-tiles")
        await tiles.screenshot(path="scratch/kpi_tiles_screenshot.png")
        print("Screenshot saved to scratch/kpi_tiles_screenshot.png")
        await browser.close()

asyncio.run(main())
