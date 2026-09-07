@echo off
title Tao Bao Cao Nong Top 5 Buu Cuc
cd /d "c:\Users\lap4all\Desktop\New folder"
echo ------------------------------------------------------------
echo DANG TU DONG TAO BAO CAO NONG TOP 5...
echo ------------------------------------------------------------
python tu_dong_bao_cao_nong.py
if exist Bao_Cao_Nong_Tu_Dong.txt (
    echo.
    echo Da tao xong bao cao! Dang tu dong mo file bang Notepad...
    start notepad.exe Bao_Cao_Nong_Tu_Dong.txt
) else (
    echo.
    echo Khong tim thay file bao cao. Vui long kiem tra loi ben tren.
)
pause
