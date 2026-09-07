import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('app.js', 'r', encoding='utf-8') as f:
    js = f.read()

# 1. Add searchFdAm and searchFdBc state
state_old = "searchRotLc: '',"
state_new = "searchRotLc: '',\n    searchFdAm: '',\n    searchFdBc: '',"
if state_old in js and 'searchFdAm' not in js:
    js = js.replace(state_old, state_new, 1)

# 2. Add search listeners around line 498
search_target = '''    const searchRotLc = document.getElementById('search-rotlc-bc');
    if (searchRotLc) {
      searchRotLc.addEventListener('input', e => {
        state.searchRotLc = e.target.value.toLowerCase().trim();
        renderTransportTab();
        lucide.createIcons();
      });
    }'''

search_hook = '''    const searchRotLc = document.getElementById('search-rotlc-bc');
    if (searchRotLc) {
      searchRotLc.addEventListener('input', e => {
        state.searchRotLc = e.target.value.toLowerCase().trim();
        renderTransportTab();
        lucide.createIcons();
      });
    }

    const searchFdAm = document.getElementById('search-fd-am');
    if (searchFdAm) {
      searchFdAm.addEventListener('input', e => {
        state.searchFdAm = e.target.value.toLowerCase().trim();
        renderFdTab();
        if (window.lucide) lucide.createIcons();
      });
    }

    const searchFdBc = document.getElementById('search-fd-bc');
    if (searchFdBc) {
      searchFdBc.addEventListener('input', e => {
        state.searchFdBc = e.target.value.toLowerCase().trim();
        renderFdTab();
        if (window.lucide) lucide.createIcons();
      });
    }'''

if search_target in js:
    js = js.replace(search_target, search_hook, 1)
    print("Added search listeners for search-fd-am and search-fd-bc")

# 3. Add renderFdTab to renderAll
render_all_old = '''    renderTransportTab();
    renderAgingTab();'''
render_all_new = '''    renderTransportTab();
    renderFdTab();
    renderAgingTab();'''

if render_all_old in js:
    js = js.replace(render_all_old, render_all_new, 1)
    print("Added renderFdTab to renderAll")

# 4. Add tab-fd to renderTabCharts
chart_target = '''    } else if (tabId === 'tab-rot-lc') {
      renderRotLcChart();
    } else if (tabId === 'tab-aging') {'''

chart_hook = '''    } else if (tabId === 'tab-rot-lc') {
      renderRotLcChart();
    } else if (tabId === 'tab-fd') {
      renderFdTab();
      renderFdChart();
    } else if (tabId === 'tab-aging') {'''

if chart_target in js:
    js = js.replace(chart_target, chart_hook, 1)
    print("Added tab-fd to renderTabCharts")

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("app.js completely connected for FD Tab!")
