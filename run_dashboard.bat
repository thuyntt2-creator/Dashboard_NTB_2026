@echo off
cd /d "%~dp0"
title NTB Ops Dashboard Runner
echo ===================================================
echo   KHOI DONG NTB OPS CONTROL DASHBOARD SERVER
echo ===================================================
echo.
echo Dang khoi dong Flask Server tren port 3000...
echo (Vui long giu cua so nay de duy tri server)
echo.
start "" cmd /c "timeout /t 2 /nobreak >nul & start http://127.0.0.1:3000/hop"
python app.py
pause

