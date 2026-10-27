# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright

with open('app.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print(f"Total lines in app.js: {len(lines)}")

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()

    def check_snippet(snippet):
        res = page.evaluate("""(code) => {
            try {
                new Function(code);
                return { ok: true };
            } catch (e) {
                return { ok: false, msg: e.message };
            }
        }""", snippet)
        return res

    # Binary search or search by blocks?
    # Notice that JavaScript needs balanced brackets to parse, but let's check recent git changes first!
    browser.close()
