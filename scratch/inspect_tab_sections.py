import re, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

def get_tab(content, tab_id, next_tab_id):
    start = content.find(f'id="{tab_id}"')
    if next_tab_id:
        end = content.find(f'id="{next_tab_id}"')
    else:
        end = len(content)
    return content[start:end]

vol_tab = get_tab(content, 'tab-volume', 'tab-gtc-tong')
print("=== TAB VOLUME ===")
print("Has table-vol-tinh-full:", 'table-vol-tinh-full' in vol_tab)
print("Position of banner:", vol_tab.find('class="exec-banner"'))
print("Position of chart:", vol_tab.find('id="vol-chart-title"'))
print("Position of am tables:", vol_tab.find('id="vol-tables-split-grid"'))
print("Position of tinh tables:", vol_tab.find('table-vol-tinh-full'))

gtc_tab = get_tab(content, 'tab-gtc-tong', 'tab-gtc-tts-ca1')
print("\n=== TAB GTC TONG ===")
print("Has table-gtc-tinh-full:", 'table-gtc-tinh-full' in gtc_tab)
print("Position of banner:", gtc_tab.find('class="exec-banner"'))
print("Position of chart:", gtc_tab.find('chart-gtc-tong-am-bar'))
print("Position of am tables:", gtc_tab.find('gtctong-tables-split-grid'))
print("Position of tinh tables:", gtc_tab.find('table-gtc-tinh-full'))
print("Position of bc canh bao:", gtc_tab.find('table-bc-canhbao-grid'))

odr_tab = get_tab(content, 'tab-odr', 'tab-ltc')
print("\n=== TAB ODR ===")
print("Has table-odr-tinh-full:", 'table-odr-tinh-full' in odr_tab)
print("Position of banner:", odr_tab.find('class="exec-banner"'))
print("Position of chart:", odr_tab.find('chart-odr-bar'))
print("Position of am tables:", odr_tab.find('table-odr-full-detailed'))
print("Position of tinh tables:", odr_tab.find('table-odr-tinh-full'))
