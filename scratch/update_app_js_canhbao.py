import re

with open('app.js', 'r', encoding='utf-8') as f:
    js = f.read()

# 1. Update renderBcCanhBaoTable to render to all .table-bc-canh-bao-body
old_func = """  function renderBcCanhBaoTable() {
    const tblBody = document.querySelector('#table-bc-canh-bao tbody');
    if (!tblBody) return;"""

new_func = """  function renderBcCanhBaoTable() {
    const tblBodies = document.querySelectorAll('.table-bc-canh-bao-body, #table-bc-canh-bao tbody, #table-bc-canh-bao-overview tbody, #table-bc-canhbao-tab tbody');
    if (!tblBodies || tblBodies.length === 0) return;"""

if old_func in js:
    js = js.replace(old_func, new_func)
    print("Updated renderBcCanhBaoTable selector to match all table bodies!")

# Replace tblBody.innerHTML = ... with tblBodies.forEach(tblBody => tblBody.innerHTML = rowsHtml)
old_render_call = """    tblBody.innerHTML = list.map((row, i) => {"""
new_render_call = """    const rowsHtml = list.map((row, i) => {"""
old_render_end = """    }).join('');
  }"""
new_render_end = """    }).join('');

    tblBodies.forEach(tblBody => {
      tblBody.innerHTML = rowsHtml;
    });
  }"""

if old_render_call in js and old_render_end in js:
    js = js.replace(old_render_call, new_render_call)
    js = js.replace(old_render_end, new_render_end)
    print("Updated innerHTML assignment to loop over all bodies!")

# 2. Add window.switchTabDirect
switch_tab_direct_js = """
  window.switchTabDirect = function(tabId) {
    const tabBtn = document.querySelector(`.tab-item[data-tab="${tabId}"]`);
    if (tabBtn) {
      tabBtn.click();
    } else {
      document.querySelectorAll('.tab-item').forEach(t => t.classList.remove('active'));
      document.querySelectorAll('.tab-view').forEach(v => v.classList.remove('active'));
      const v = document.getElementById(tabId);
      if (v) v.classList.add('active');
    }
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };
"""

if 'window.switchTabDirect =' not in js:
    pos = js.find('function renderAll() {')
    if pos != -1:
        js = js[:pos] + switch_tab_direct_js + "\n  " + js[pos:]
        print("Added window.switchTabDirect to app.js!")

# 3. Call renderBcCanhBaoTable in renderAll()
if 'renderBcCanhBaoTable();' not in js[js.find('function renderAll() {'):js.find('renderAllCharts();')]:
    js = js.replace(
        'renderAll() {\n    renderOverviewTab();',
        'renderAll() {\n    renderOverviewTab();\n    renderBcCanhBaoTable();'
    )
    print("Hooked renderBcCanhBaoTable into renderAll()!")

# 4. In renderTabCharts: add tab-bc-canhbao
if "tabId === 'tab-bc-canhbao'" not in js:
    js = js.replace(
        "} else if (tabId === 'tab-truythu') {",
        "} else if (tabId === 'tab-bc-canhbao') {\n      renderBcCanhBaoTable();\n    } else if (tabId === 'tab-truythu') {"
    )
    print("Added tab-bc-canhbao case to renderTabCharts!")

# 5. Attach search to all .search-bc-input
old_search_listener = """    const searchBcCanhBao = document.getElementById('search-bc-canh-bao');
    if (searchBcCanhBao) {
      searchBcCanhBao.addEventListener('input', e => {
        state.searchBcCanhBao = e.target.value.toLowerCase().trim();
        renderBcCanhBaoTable();
        if (window.lucide) lucide.createIcons();
      });
    }"""

new_search_listener = """    const searchBcInputs = document.querySelectorAll('.search-bc-input, #search-bc-canh-bao');
    searchBcInputs.forEach(input => {
      input.addEventListener('input', e => {
        state.searchBcCanhBao = e.target.value.toLowerCase().trim();
        // Sync values across all search boxes
        searchBcInputs.forEach(si => { if (si !== e.target) si.value = e.target.value; });
        renderBcCanhBaoTable();
        if (window.lucide) lucide.createIcons();
      });
    });"""

if old_search_listener in js:
    js = js.replace(old_search_listener, new_search_listener)
    print("Updated searchBcCanhBao event listener for multi-inputs!")

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("Saved app.js successfully!")
