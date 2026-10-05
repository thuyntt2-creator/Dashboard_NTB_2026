import asyncio
import os
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={'width': 1600, 'height': 1200})
        index_path = os.path.abspath('index.html').replace('\\', '/')
        await page.goto(f'file:///{index_path}')
        await page.wait_for_timeout(2000)
        
        # Click Tab 3
        await page.click('button[data-tab="tab-gtc-tong"]')
        await page.wait_for_timeout(1000)
        rows_gtc = await page.eval_on_selector_all('#table-gtc-full-detailed tbody tr', 'trs => trs.slice(0, 5).map(tr => tr.innerText.replace(/\\t/g, " | "))')
        
        # Click Tab 6
        await page.click('button[data-tab="tab-odr"]')
        await page.wait_for_timeout(1000)
        rows_odr = await page.eval_on_selector_all('#table-odr-full-detailed tbody tr', 'trs => trs.slice(0, 5).map(tr => tr.innerText.replace(/\\t/g, " | "))')

        with open('scratch/sort_results_gtc_odr.txt', 'w', encoding='utf-8') as f:
            f.write('=== BANG GTC FULL 18 AM - TOP 5 ===\n')
            for r in rows_gtc:
                f.write(r + '\n')
            f.write('\n=== BANG ODR FULL 18 AM - TOP 5 ===\n')
            for r in rows_odr:
                f.write(r + '\n')
                
        await browser.close()
        print('DONE CHECK GTC ODR!')

asyncio.run(run())
