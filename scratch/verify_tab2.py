import os
import sys
import json
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={'width': 1600, 'height': 1200})
    file_path = os.path.abspath('index.html')
    url = 'file:///' + file_path.replace('\\', '/')
    page.goto(url)
    page.wait_for_timeout(1500)
    
    # Click Tab 2
    page.click("button[data-tab='tab-volume']")
    page.wait_for_timeout(1000)
    
    # Check rows in table-vol-tinh-full
    rows_3a = page.eval_on_selector_all('#table-vol-tinh-full tbody tr', '''rows => rows.map(r => ({
        rank: r.cells[0]?.innerText.trim(),
        name: r.cells[1]?.innerText.trim(),
        w40: r.cells[5]?.innerText.trim(),
        diff: r.cells[6]?.innerText.trim()
    }))''')

    # Check rows in table-vol-tinh-tts
    rows_3b = page.eval_on_selector_all('#table-vol-tinh-tts tbody tr', '''rows => rows.map(r => ({
        rank: r.cells[0]?.innerText.trim(),
        name: r.cells[1]?.innerText.trim(),
        w40: r.cells[5]?.innerText.trim(),
        diff: r.cells[6]?.innerText.trim()
    }))''')

    # Check rows in table-vol-full-detailed (AM 18)
    rows_am = page.eval_on_selector_all('#table-vol-full-detailed tbody tr', '''rows => rows.slice(0, 3).map(r => ({
        rank: r.cells[0]?.innerText.trim(),
        name: r.cells[1]?.innerText.trim(),
        diff: r.cells[5]?.innerText.trim()
    }))''')

    # Test clicking province Bình Thuận in Bảng 3A
    page.click('#table-vol-tinh-full tbody tr:first-child')
    page.wait_for_timeout(800)

    # Check if province-laser-box is present
    has_laser = page.eval_on_selector('#table-vol-tinh-full tbody tr:first-child', 'el => el.classList.contains("province-laser-box")')

    # Take screenshot of Tab 2
    page.screenshot(path='scratch/verify_tab2_final.png', full_page=False)
    browser.close()

    result = {
        "status": "SUCCESS",
        "bang_3a": rows_3a,
        "bang_3b": rows_3b,
        "top3_am": rows_am,
        "has_province_laser": has_laser
    }
    with open('scratch/verify_result.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print("VERIFICATION COMPLETED SUCCESSFULLY!")
