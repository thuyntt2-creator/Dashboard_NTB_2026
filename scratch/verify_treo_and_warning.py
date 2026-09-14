import sys
sys.stdout.reconfigure(encoding='utf-8')
import time
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1600, "height": 1000})
    print("Navigating to http://127.0.0.1:3000/hop...")
    page.goto('http://127.0.0.1:3000/hop', wait_until='networkidle')
    time.sleep(2)

    # 1. Check Tab 12 (Aging & Treo LC)
    print("Clicking Tab 12 (Aging & Treo LC)...")
    page.locator('button[data-tab="tab-aging"]').click()
    time.sleep(1)

    print("Clicking Báo Cáo Treo Luân Chuyển (LC)...")
    page.locator('#btn-aging-treo').click()
    time.sleep(1)

    # Print first row of Table 1 AM and Table 2 BC
    t1_row = page.locator('#table-aging-am-detailed tbody tr').first.all_inner_texts()
    print("Treo LC AM Table Row 1:", t1_row)
    t2_row = page.locator('#table-aging-bc-detailed tbody tr').first.all_inner_texts()
    print("Treo LC BC Table Row 1:", t2_row)

    # Total row in Treo LC AM Table
    t1_total = page.locator('#table-aging-am-detailed tbody tr').last.all_inner_texts()
    print("Treo LC AM Total Row:", t1_total)

    page.screenshot(path='scratch/treo_lc_verified.png')
    print("Saved scratch/treo_lc_verified.png")

    # 2. Check Tab 3 (%GTC Tổng) - Warning Table
    print("\nClicking Tab 3 (%GTC Tổng)...")
    page.locator('button[data-tab="tab-gtc-tong"]').click()
    time.sleep(1)

    # Scroll to Bảng 3
    bc_table = page.locator('#table-bc-canh-bao')
    bc_table.scroll_into_view_if_needed()
    time.sleep(1)

    bc_count = page.locator('#table-bc-canh-bao tbody tr').count()
    print(f"Warning BC Table row count: {bc_count}")

    first_bc = page.locator('#table-bc-canh-bao tbody tr').first.all_inner_texts()
    print("Warning BC Row 1:", first_bc)

    page.screenshot(path='scratch/warning_bc_verified.png')
    print("Saved scratch/warning_bc_verified.png")

    browser.close()
    print("Verification finished successfully!")
