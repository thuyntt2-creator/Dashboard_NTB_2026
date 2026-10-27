# -*- coding: utf-8 -*-
import subprocess
from playwright.sync_api import sync_playwright

commits = [
    "4a0a3c29", "43b9eccb", "e506515f", "2a0c1c14", "85e7b338",
    "a56b47f0", "752a6de0", "3b73770c", "30dc54da", "18f8eb87"
]

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    for c in commits:
        try:
            res = subprocess.run(["git", "show", f"{c}:app.js"], capture_output=True, text=True, encoding='utf-8')
            js_code = res.stdout
            check = page.evaluate("""(code) => {
                try {
                    new Function(code);
                    return { ok: true };
                } catch (e) {
                    return { ok: false, msg: e.message };
                }
            }""", js_code)
            print(f"Commit {c}: ok={check['ok']} (lines: {len(js_code.splitlines())}) msg={check.get('msg')}")
        except Exception as e:
            print(f"Commit {c} error: {e}")
    browser.close()
