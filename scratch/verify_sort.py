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
        
        # Click Tab 2
        await page.click('button[data-tab="tab-volume"]')
        await page.wait_for_timeout(1000)
        
        rows_3a = await page.eval_on_selector_all('#table-vol-tinh-full tbody tr', 'trs => trs.map(tr => tr.innerText.replace(/\\t/g, " | "))')
        rows_3b = await page.eval_on_selector_all('#table-vol-tinh-tts tbody tr', 'trs => trs.map(tr => tr.innerText.replace(/\\t/g, " | "))')
        rows_1 = await page.eval_on_selector_all('#table-vol-full-detailed tbody tr', 'trs => trs.slice(0, 5).map(tr => tr.innerText.replace(/\\t/g, " | "))')
        
        with open('scratch/sort_results.txt', 'w', encoding='utf-8') as f:
            f.write('=== BANG 3A (FULL 5 TINH) ===\n')
            for r in rows_3a:
                f.write(r + '\n')
            f.write('\n=== BANG 3B (TTS 5 TINH) ===\n')
            for r in rows_3b:
                f.write(r + '\n')
            f.write('\n=== BANG 1 (FULL 18 AM - TOP 5) ===\n')
            for r in rows_1:
                f.write(r + '\n')
            
        await page.screenshot(path='verify_sorted_tables.png')
        await browser.close()
        print('DONE!')

asyncio.run(run())
