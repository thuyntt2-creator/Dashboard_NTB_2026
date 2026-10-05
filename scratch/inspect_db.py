
import sys, json
sys.stdout.reconfigure(encoding='utf-8')
with open('data.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

print('=== 5. GAN ===')
for x in sorted(d['gan']['am'], key=lambda k: k.get('ca1ton_w40', 0), reverse=True)[:5]:
    print('  Top Ca1+Ton: %s (vol %s) %.1f%% -> %.1f%% (diff: %+.1f%%p)' % (x['am'], x['vol'], x['ca1ton_w39']*100, x['ca1ton_w40']*100, x['ca1ton_diff']*100))
for x in sorted(d['gan']['am'], key=lambda k: k.get('ca1ton_w40', 0))[:5]:
    print('  Bot Ca1+Ton: %s (vol %s) %.1f%% -> %.1f%% (diff: %+.1f%%p)' % (x['am'], x['vol'], x['ca1ton_w39']*100, x['ca1ton_w40']*100, x['ca1ton_diff']*100))
for x in sorted(d['gan']['am'], key=lambda k: k.get('ca1ton_diff', 0), reverse=True)[:4]:
    print('  Bứt phá Ca1+Ton: %s %+.1f%%p (%.1f%% -> %.1f%%)' % (x['am'], x['ca1ton_diff']*100, x['ca1ton_w39']*100, x['ca1ton_w40']*100))
for x in sorted(d['gan']['am'], key=lambda k: k.get('tong_w40', 0), reverse=True)[:4]:
    print('  Top Tong: %s %.1f%% -> %.1f%%' % (x['am'], x['tong_w39']*100, x['tong_w40']*100))
for x in sorted(d['gan']['am'], key=lambda k: k.get('tong_w40', 0))[:5]:
    print('  Bot Tong: %s %.1f%% -> %.1f%%' % (x['am'], x['tong_w39']*100, x['tong_w40']*100))

print('\n=== 6. ODR ===')
for x in d['odr'].get('tinh_full', []):
    print('  Tinh Full: %s %.2f%% -> %.2f%%' % (x['tinh'], x['w39']*100, x['w40']*100))
for x in sorted(d['odr']['am_full'], key=lambda k: k.get('w40', 0), reverse=True)[:4]:
    print('  Top AM Full: %s %.1f%%' % (x['am'], x['w40']*100))
for x in sorted(d['odr']['am_full'], key=lambda k: k.get('w40', 0))[:5]:
    print('  Bot AM Full: %s %.1f%%' % (x['am'], x['w40']*100))
for x in sorted(d['odr']['am_tts'], key=lambda k: k.get('w40', 0), reverse=True)[:4]:
    print('  Top AM TTS: %s %.1f%%' % (x['am'], x['w40']*100))
for x in sorted(d['odr']['am_tts'], key=lambda k: k.get('w40', 0))[:5]:
    print('  Bot AM TTS: %s %.1f%%' % (x['am'], x['w40']*100))

print('\n=== 7. LTC ===')
for x in sorted(d['ltc']['am'], key=lambda k: k.get('w40', 0), reverse=True)[:4]:
    print('  Top LTC: %s %.1f%%' % (x['am'], x.get('w40',0)*100))
for x in sorted(d['ltc']['am'], key=lambda k: k.get('w40', 0))[:5]:
    print('  Bot LTC: %s %.1f%%' % (x['am'], x.get('w40',0)*100))

print('\n=== 8. OPR TTS ===')
for x in sorted(d['opr_tts']['am'], key=lambda k: k.get('w40_night', 0))[:5]:
    print('  Bot Night: %s %.1f%% (vol_night: %s)' % (x['am'], x['w40_night']*100, x['vol_night']))

print('\n=== 9. ROT LC ===')
print('Overview:', d['rot_lc']['overview'])
for x in sorted(d['rot_lc']['am'], key=lambda k: k.get('w40', 0), reverse=True)[:5]:
    print('  AM rot LC: %s %.2f%% (rot %s / %s)' % (x['am'], x['w40']*100, x.get('don_rot',0), x.get('vol_can_lc',0)))
for x in d['rot_lc']['top_bc'][1:6]:
    print('  BC rot LC: %s | %s | rot: %s | pct: %s' % (x['bc'], x['am'], x.get('vol_rot_lc'), x.get('pct_rot')))

print('\n=== 10. FD ===')
print('Overview:', d['fd']['overview'])
for x in d['fd']['top_bc'][:6]:
    print('  BC FD: %s | %s | %.2f%% (ret: %s / %s)' % (x['bc'], x['am'], x['rate']*100, x['ret'], x['vol']))

print('\n=== 13. COD & QR ===')
for x in d['cod_report']['metrics']:
    print('  Metric: %s | %s' % (x['label'], x['value']))
for x in sorted(d['cod_report']['am_comparison'], key=lambda k: k.get('w40_cash_rate', 0), reverse=True)[:5]:
    print('  AM High Cash: %s | TM: %.1f%% | chênh %+.1f%%p' % (x['am'], x['w40_cash_rate'], x['diff_cash_rate']))
for x in sorted(d['cod_report']['am_comparison'], key=lambda k: k.get('w40_cash_rate', 0))[:4]:
    print('  AM Low Cash (High QR): %s | TM: %.1f%%' % (x['am'], x['w40_cash_rate']))

print('\n=== 14. TRUY THU ===')
print('Summary:', d['truy_thu_report']['summary'])
for x in d['truy_thu_report']['by_loai']:
    print('  Loai TT: %s | W40: %.1f Tr' % (x['loai'], x['tien_w40']/1e6))
for x in sorted(d['truy_thu_report']['by_am'], key=lambda k: k.get('tien_w40', 0), reverse=True)[:5]:
    print('  AM TT: %s | W40: %.1f Tr (tickets: %s)' % (x['am'], x['tien_w40']/1e6, x['so_w40']))
for x in d['truy_thu_report']['top_bc'][:5]:
    print('  BC TT: %s | %s | %.1f Tr' % (x['bc'], x['am'], x['can_thu']/1e6))
