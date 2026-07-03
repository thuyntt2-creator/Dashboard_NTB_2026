@echo off
title Tu dong hoa bao cao van hanh NTB
cd /d "c:\Users\lap4all\Desktop\New folder"
echo ------------------------------------------------------------
echo 1. DANG TẠO BÁO CÁO LOCAL & ẢNH DASHBOARD...
echo ------------------------------------------------------------
python automate_report_and_dashboard.py

echo ------------------------------------------------------------
echo 1b. DANG DỒNG BỘ HÓA CÁC TAB SO SÁNH CHÍNH LÊN GOOGLE SHEETS...
echo ------------------------------------------------------------
python sync_to_gsheet.py

echo ------------------------------------------------------------
echo 2. DANG PHÂN TÍCH AM-TỈNH & VẼ BIỂU ĐỒ TRỰC TIẾP TRÊN GOOGLE SHEETS...
echo ------------------------------------------------------------
python sync_online_direct.py

echo ------------------------------------------------------------
echo 3. DANG PHÂN TÍCH OPR TTS & RỚT LC VÀ TẠO BIỂU ĐỒ...
echo ------------------------------------------------------------
python sync_opr_and_lc.py

echo ------------------------------------------------------------
echo 4. DANG TẠO BÁO CÁO BƯU CỤC BẤT ỔN & GỬI TELEGRAM + GTALK...
echo ------------------------------------------------------------
python report_BC_BatOn_html.py

echo ------------------------------------------------------------
echo 5. DANG TU DONG KICH HOAT DONG BO DU LIEU LEN VERCEL...
echo ------------------------------------------------------------
python -c "import requests; r=requests.post('https://ntb-ops-dashboard-five.vercel.app/api/sync', auth=('admin', 'admin123')); print('Ket qua:', r.json())"

echo ------------------------------------------------------------
echo HOÀN THÀNH TOÀN BỘ PIPELINE BÁO CÁO VẬN HÀNH VÀ ĐỒNG BỘ VERCEL!
echo ------------------------------------------------------------
if "%~1"=="/automated" exit /b 0
pause

