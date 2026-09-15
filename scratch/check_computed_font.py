# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto('http://127.0.0.1:3000/hop', wait_until='networkidle')
    card_val = page.locator('.kpi-tile-value').nth(4)
    font_info = card_val.evaluate("""el => {
        const s = window.getComputedStyle(el);
        return {
            fontFamily: s.fontFamily,
            fontSize: s.fontSize,
            fontVariantNumeric: s.fontVariantNumeric,
            letterSpacing: s.letterSpacing
        };
    }""")
    print("Computed styles for .kpi-tile-value:")
    print(font_info)
    browser.close()
