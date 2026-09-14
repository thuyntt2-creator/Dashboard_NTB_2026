import sys
import os
import json
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1440, "height": 900})
    page.goto("http://127.0.0.1:3000/hop", wait_until="networkidle")
    page.wait_for_timeout(1000)

    results = {}

    # 1. Check Overview
    title = page.title()
    badge = page.locator("#header-live-badge").inner_text()
    cards = page.locator(".kpi-tile").all_inner_texts()
    tltd_card = [c for c in cards if "TLTĐ" in c or "Lấp Đầy" in c]
    has_cod = any("COD" in c for c in cards)
    results["overview"] = {
        "title": title,
        "badge": badge,
        "tltd_card": tltd_card[0].replace("\n", " | ") if tltd_card else "NOT FOUND",
        "has_cod": has_cod
    }

    # 2. Check Tab 4 (GTC TTS Ca 1)
    page.click('[data-tab="tab-gtc-tts-ca1"]')
    page.wait_for_timeout(500)
    th_ca1 = page.locator("#table-gtc-tts-ca1-detailed thead tr").inner_text()
    rows_ca1 = page.locator("#table-gtc-tts-ca1-detailed tbody tr").count()
    results["tab4_gtc_ca1"] = {
        "thead": th_ca1.replace("\n", " | "),
        "row_count": rows_ca1
    }

    # 3. Check Tab 10 (FD)
    page.click('[data-tab="tab-fd"]')
    page.wait_for_timeout(500)
    fd_vol = page.locator("#kpi-fd-vol-full").inner_text()
    fd_rate = page.locator("#kpi-fd-rate-full").inner_text()
    th_fd = page.locator("#table-fd-am-detailed thead tr").inner_text()
    rows_fd_am = page.locator("#table-fd-am-detailed tbody tr").count()
    rows_fd_bc = page.locator("#table-fd-top-bc tbody tr").count()
    results["tab10_fd"] = {
        "vol_full": fd_vol.replace("\n", " | "),
        "rate_full": fd_rate.replace("\n", " | "),
        "thead": th_fd.replace("\n", " | "),
        "rows_am": rows_fd_am,
        "rows_bc": rows_fd_bc
    }

    # 4. Check Tab 11 (KTC)
    page.click('[data-tab="tab-ktc"]')
    page.wait_for_timeout(500)
    page.click("#btn-ktc-fillrate")
    page.wait_for_timeout(500)
    ktc_tile4 = page.locator("#tab-ktc .kpi-strip .kpi-tile").nth(3).inner_text()
    th_fr = page.locator("#table-ktc-fillrate-thead").inner_text()
    rows_fr = page.locator("#table-ktc-fillrate-tbody tr").count()
    first_row_fr = page.locator("#table-ktc-fillrate-tbody tr").first.inner_text() if rows_fr > 0 else "EMPTY"
    results["tab11_ktc"] = {
        "tile4": ktc_tile4.replace("\n", " | "),
        "thead": th_fr.replace("\n", " | "),
        "row_count": rows_fr,
        "first_row": first_row_fr.replace("\n", " | ")
    }

    # 5. Check Tab 14 (Kinh Doanh & Churn)
    page.click('[data-tab="tab-commercial"]')
    page.wait_for_timeout(500)
    th_churn = page.locator("#table-kd-churn-top10 thead").inner_text()
    rows_churn = page.locator("#table-kd-churn-top10 tbody tr").count()
    first_churn = page.locator("#table-kd-churn-top10 tbody tr").first.inner_text() if rows_churn > 0 else "EMPTY"
    results["tab14_churn"] = {
        "thead": th_churn.replace("\n", " | "),
        "row_count": rows_churn,
        "first_row": first_churn.replace("\n", " | ")
    }

    # Save screenshots
    page.screenshot(path="scratch/final_verification_tab14.png")
    page.click('[data-tab="tab-overview"]')
    page.wait_for_timeout(300)
    page.screenshot(path="scratch/final_verification_tab1.png")

    print(json.dumps(results, ensure_ascii=False, indent=2))
    browser.close()
