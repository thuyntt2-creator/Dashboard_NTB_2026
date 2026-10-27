import os, sys, glob
sys.stdout.reconfigure(encoding='utf-8')

print("--- Searching for COD / QR / Chuyen khoan in scratch or root ---")
# Check python scripts that handled COD / QR before
for f in glob.glob("*.py") + glob.glob("scratch/*.py"):
    try:
        with open(f, 'r', encoding='utf-8', errors='ignore') as fp:
            text = fp.read()
            if 'cod_report' in text or 'tab-qrcode' in text or '13. QR Code' in text or 'Báo Cáo COD' in text or 'chuyen_khoan' in text or 'tien_mat' in text:
                print("Relevant script:", f)
    except Exception as e:
        pass
