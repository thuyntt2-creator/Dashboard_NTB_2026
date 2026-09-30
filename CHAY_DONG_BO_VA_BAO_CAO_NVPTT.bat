@echo off
chcp 65001 >nul
echo ========================================================
echo   CHAY QUY TRINH: DONG BO NANG SUAT & GUI ANH GTALK
echo ========================================================
echo.
echo [1/2] Dang dong bo so lieu Lastmile vao Google Sheet...
python fetch_lastmile_productivity.py
if %ERRORLEVEL% NEQ 0 (
    echo [LOI] Dong bo so lieu that bai!
    pause
    exit /b %ERRORLEVEL%
)

echo.
echo [Cho 10 giay de Google Sheet tinh toan xong cong thuc tab BaoCao...]
timeout /t 10 /nobreak >nul

echo.
echo [2/2] Dang tao anh BaoCao va gui vao kenh GTalk tung AM...
python send_report_nvptt_realtime.py
if %ERRORLEVEL% NEQ 0 (
    echo [LOI] Gui bao cao GTalk that bai!
    pause
    exit /b %ERRORLEVEL%
)

echo.
echo ========================================================
echo   HOAN TAT XUAT SAC TOAN BO TIEN TRINH!
echo ========================================================
pause
