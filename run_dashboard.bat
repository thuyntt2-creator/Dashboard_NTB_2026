@echo off
title NTB Ops Dashboard Runner
echo ===================================================
echo   KHOI DONG NTB OPS CONTROL DASHBOARD SERVER
echo ===================================================
echo.
echo [1/2] Dang mo trinh duyet tai dia chi: http://127.0.0.1:5000/
start "" "http://127.0.0.1:5000/"
echo.
echo [2/2] Dang chay Flask Server...
echo (Ban co the thu nho cua so nay, khong dong no khi dang dung dashboard)
echo.
python app.py
pause
