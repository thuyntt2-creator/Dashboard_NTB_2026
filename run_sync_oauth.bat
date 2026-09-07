@echo off
cd /d "%~dp0"
title Google Sheets OAuth Synchronizer
echo ===================================================
echo   DONG BO GOOGLE SHEETS VOI OAUTH 2.0 (GOOGLE LOGIN)
echo ===================================================
echo.
python sync_google_sheets_oauth.py
pause
