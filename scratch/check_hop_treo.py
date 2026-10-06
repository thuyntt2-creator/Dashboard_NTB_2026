import asyncio
from playwright.sync_api import sync_playwright
import sys
sys.stdout.reconfigure(encoding='utf-8')

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto('http://127.0.0.1:3000/hop', wait_until='networkidle')
    
    # Check Tab 12
    # Click Tab 12
    page.click('button[data-tab="tab-aging"]')
    page.wait_for_timeout(500)
    
    badge = page.inner_text('#aging-badge-summary')
    banner_desc = page.inner_text('#aging-banner-desc')
    print('=== TAB 12 (AGING & TREO LC) ===')
    print('Badge text:', badge)
    print('Banner desc:', banner_desc[:200])
    
    # Check KPIs default (aging)
    kpi1_title = page.inner_text('#kpi-aging-title-1')
    kpi1_val = page.inner_text('#kpi-aging-val-1')
    kpi1_meta = page.inner_text('#kpi-aging-meta-1')
    print(f'KPI 1: {kpi1_title} | {kpi1_val} | {kpi1_meta}')
    
    # Now click Treo LC button
    page.click('#btn-aging-treo')
    page.wait_for_timeout(500)
    
    print('\n=== AFTER CLICKING BÁO CÁO TREO LC ===')
    k1_title = page.inner_text('#kpi-aging-title-1')
    k1_val = page.inner_text('#kpi-aging-val-1')
    k1_meta = page.inner_text('#kpi-aging-meta-1')
    print(f'KPI 1: {k1_title} | {k1_val} | {k1_meta}')
    
    k2_title = page.inner_text('#kpi-aging-title-2')
    k2_val = page.inner_text('#kpi-aging-val-2')
    k2_meta = page.inner_text('#kpi-aging-meta-2')
    print(f'KPI 2: {k2_title} | {k2_val} | {k2_meta}')
    
    k3_title = page.inner_text('#kpi-aging-title-3')
    k3_val = page.inner_text('#kpi-aging-val-3')
    k3_meta = page.inner_text('#kpi-aging-meta-3')
    print(f'KPI 3: {k3_title} | {k3_val} | {k3_meta}')
    
    k4_title = page.inner_text('#kpi-aging-title-4')
    k4_val = page.inner_text('#kpi-aging-val-4')
    k4_meta = page.inner_text('#kpi-aging-meta-4')
    print(f'KPI 4: {k4_title} | {k4_val} | {k4_meta}')
    
    # Check first row of Table 1
    t1_r1 = page.inner_text('#table-aging-am-detailed tbody tr:first-child')
    print('\nTable 1 first row:', t1_r1)
    
    # Check last row of Table 1 (Total row)
    t1_last = page.inner_text('#table-aging-am-detailed tbody tr:last-child')
    print('Table 1 total row:', t1_last)
    
    # Check Table 2 first row
    t2_r1 = page.inner_text('#table-aging-bc-detailed tbody tr:first-child')
    print('Table 2 first row:', t2_r1)
    
    browser.close()
