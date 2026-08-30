@echo off
chcp 65001 >nul
echo ========================================================
echo   DANG NHAP LAI GOOGLE OAUTH CHO HE THONG DONG BO
echo ========================================================
echo.
echo Dang mo trinh duyet de ban dang nhap tai khoan Google...
echo.
python scratch\reauth_google.py
echo.
if %ERRORLEVEL% EQU 0 (
    echo ========================================================
    echo   DANG NHAP THANH CONG! He thong da co token moi.
    echo   Tien hanh dong bo ngay lap tuc...
    echo ========================================================
    python auto_sync_and_push.py
) else (
    echo [LOI] Dang nhap that bai hoac bi huy. Vui long thu lai!
)
pause
