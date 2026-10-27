# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1440, "height": 900})
    page.goto('http://127.0.0.1:3000/hop')
    page.wait_for_timeout(1000)
    
    res = page.evaluate("""() => {
        let chartJsLoaded = typeof Chart !== 'undefined';
        let dLoaded = typeof D !== 'undefined';
        let weeks = dLoaded && D.meta ? D.meta.weeks : null;
        let kpis = dLoaded && D.overview ? D.overview.kpis_trend : null;
        
        let canvas = document.getElementById('chart-trend-san-luong');
        let canvasW = canvas ? canvas.width : 0;
        let canvasH = canvas ? canvas.height : 0;
        let canvasClientW = canvas ? canvas.clientWidth : 0;
        let canvasClientH = canvas ? canvas.clientHeight : 0;
        let canvasParent = canvas ? canvas.parentElement.className : '';
        let canvasParentDisplay = canvas ? window.getComputedStyle(canvas.parentElement).display : '';
        let canvasParentH = canvas ? canvas.parentElement.clientHeight : 0;
        
        return {
            chartJsLoaded,
            dLoaded,
            weeks,
            kpisCount: kpis ? kpis.length : 0,
            canvasW, canvasH,
            canvasClientW, canvasClientH,
            canvasParent, canvasParentDisplay, canvasParentH
        };
    }""")
    print("Page details:", res)
    browser.close()
