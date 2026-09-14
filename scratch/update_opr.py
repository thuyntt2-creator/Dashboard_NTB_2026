import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('app.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Tab 8: OPR TTS failed items & cards
js = js.replace('const oTot = r.w36_total !== undefined ? r.w36_total : 0;',
                'const oTot = r.w37_total !== undefined ? r.w37_total : (r.w36_total || 0);')

js = js.replace('const oTot = (r.vol_day === 0 && r.vol_night === 0) ? 0 : (r.w36_total !== undefined ? r.w36_total : (r.w35_total || 0));',
                'const oTot = (r.vol_day === 0 && r.vol_night === 0) ? 0 : (r.w37_total !== undefined ? r.w37_total : (r.w36_total || 0));')

js = js.replace('const oTot = (row.vol_day === 0 && row.vol_night === 0) ? 0 : (row.w36_total !== undefined ? row.w36_total : (row.w35_total || 0));',
                'const oTot = (row.vol_day === 0 && row.vol_night === 0) ? 0 : (row.w37_total !== undefined ? row.w37_total : (row.w36_total || 0));')

js = js.replace('.sort((a, b) => (a.w36_day || 0) - (b.w36_day || 0));',
                '.sort((a, b) => (a.w37_day || a.w36_day || 0) - (b.w37_day || b.w36_day || 0));')

js = js.replace('.sort((a, b) => (a.w36_night || 0) - (b.w36_night || 0));',
                '.sort((a, b) => (a.w37_night || a.w36_night || 0) - (b.w37_night || b.w36_night || 0));')

js = js.replace('const failedDay = _ams.filter(r => (r.vol_day || 0) > 0 && (r.w36_day || 0) < 0.80)',
                'const failedDay = _ams.filter(r => (r.vol_day || 0) > 0 && (r.w37_day !== undefined ? r.w37_day : (r.w36_day || 0)) < 0.80)')

js = js.replace('const failedNight = _ams.filter(r => (r.vol_night || 0) > 0 && (r.w36_night || 0) < 0.80)',
                'const failedNight = _ams.filter(r => (r.vol_night || 0) > 0 && (r.w37_night !== undefined ? r.w37_night : (r.w36_night || 0)) < 0.80)')

js = js.replace('const val = ((r.w36_total !== undefined ? r.w36_total : 0) * 100);',
                'const val = (((r.w37_total !== undefined ? r.w37_total : r.w36_total) || 0) * 100);')

js = js.replace('const rawDay = (r.vol_day === 0 || (r.w36_day || 0) > 1) ? 0 : (r.w36_day || 0);',
                'const rawDay = (r.vol_day === 0) ? 0 : (r.w37_day !== undefined ? r.w37_day : (r.w36_day || 0));')

js = js.replace('const rawNight = (r.vol_night === 0 || (r.w36_night || 0) > 1) ? 0 : (r.w36_night || 0);',
                'const rawNight = (r.vol_night === 0) ? 0 : (r.w37_night !== undefined ? r.w37_night : (r.w36_night || 0));')

js = js.replace('const val = d.w36_day !== undefined ? d.w36_day : (d.w35_day || 0);',
                'const val = d.w37_day !== undefined ? d.w37_day : (d.w36_day || 0);')

js = js.replace('const val = d.w36_night !== undefined ? d.w36_night : (d.w35_night || 0);',
                'const val = d.w37_night !== undefined ? d.w37_night : (d.w36_night || 0);')

js = js.replace('const val = d.w36_total !== undefined ? d.w36_total : (d.w35_total !== undefined ? d.w35_total : 0);',
                'const val = d.w37_total !== undefined ? d.w37_total : (d.w36_total || 0);')

js = js.replace('Toàn Vùng W36: 76.9%', 'Toàn Vùng W37: 76.9%')

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(js)
print('Updated OPR TTS specifics in app.js')
