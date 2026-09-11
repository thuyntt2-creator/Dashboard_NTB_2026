@echo off
chcp 65001 >nul
title ĐỒNG BỘ CHI PHÍ VẬN TẢI & KTC TỪ 7 GOOGLE SHEETS NCC
color 0b

echo =====================================================================
echo    GHN NAM TRUNG BỘ — HỆ THỐNG ĐỒNG BỘ CHI PHÍ VẬN TẢI & TRUNG CHUYỂN
echo =====================================================================
echo.
echo [1/3] Đang quét và trích xuất dữ liệu từ 7 Google Sheets NCC...
python scratch\sync_ncc_transport_costs.py
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ❌ LỖI: Không thể đồng bộ số liệu NCC! Vui lòng kiểm tra lại kết nối mạng hoặc token Google.
    pause
    exit /b 1
)

echo.
echo [2/3] Đang cập nhật tệp dữ liệu hiển thị (data.js / data.json)...
python build_data_js.py

echo.
echo [3/3] Đang đẩy dữ liệu mới lên Dashboard Vercel (namtrungbo.vercel.app)...
git add scratch/transport_costs.json transport_costs.json data.js data.json templates/index.html
git commit -m "Auto update NCC transport costs from Google Sheets"
git push origin main

echo.
echo =====================================================================
echo 🎉 THÀNH CÔNG: Đã cập nhật xong dữ liệu Chi Phí Vận Tải lên Dashboard!
echo Sếp và bạn có thể vào link https://namtrungbo.vercel.app để xem ngay.
echo =====================================================================
echo.
pause
