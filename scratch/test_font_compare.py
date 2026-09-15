# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright

html = """
<!DOCTYPE html>
<html>
<head>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@700;800&family=Inter:wght@700;800&display=swap" rel="stylesheet">
<style>
  body { padding: 20px; font-size: 24px; background: #fff; }
  .pjs { font-family: 'Plus Jakarta Sans', sans-serif; font-weight: 800; }
  .inter { font-family: 'Inter', sans-serif; font-weight: 800; }
  .segoe { font-family: 'Segoe UI', sans-serif; font-weight: 800; }
  .jb { font-family: 'JetBrains Mono', monospace; font-weight: 800; }
</style>
</head>
<body>
  <div class="pjs">Plus Jakarta: 93.3% Full Hàng</div>
  <div class="inter">Inter: 93.3% Full Hàng</div>
  <div class="segoe">Segoe UI: 93.3% Full Hàng</div>
  <div class="jb">JetBrains Mono: 93.3% Full Hàng</div>
</body>
</html>
"""

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.set_content(html)
    page.screenshot(path='scratch/font_comparison.png')
    browser.close()
print("Font comparison saved!")
