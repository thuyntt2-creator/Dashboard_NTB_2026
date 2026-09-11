import re

with open('templates/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update CSS around .sidebar and .main-content
old_sidebar_css = """.sidebar {
            width: 260px;
            background-color: var(--bg-secondary);
            border-right: 1px solid var(--border-color);
            display: flex;
            flex-direction: column;
            position: fixed;
            height: 100vh;
            z-index: 10;
        }"""

new_sidebar_css = """/* Sidebar Auto-hide & 3D Drawer System */
        .sidebar {
            width: 275px;
            background: rgba(255, 255, 255, 0.98);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border-right: 1px solid var(--border-color);
            display: flex;
            flex-direction: column;
            position: fixed;
            top: 0;
            left: 0;
            height: 100vh;
            z-index: 1000;
            box-shadow: 10px 0 30px rgba(15, 23, 42, 0.12);
            transform: translateX(-100%);
            transition: transform 0.32s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.3s ease;
        }

        .sidebar.open,
        .sidebar.pinned,
        body.sidebar-is-pinned .sidebar {
            transform: translateX(0);
        }

        /* Hover Sensor Strip at left edge */
        #sidebar-hover-sensor {
            position: fixed;
            top: 0;
            left: 0;
            width: 20px;
            height: 100vh;
            z-index: 999;
            cursor: pointer;
            background: transparent;
        }

        /* Backdrop overlay */
        #sidebar-backdrop {
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            background: rgba(15, 23, 42, 0.3);
            backdrop-filter: blur(2px);
            z-index: 998;
            opacity: 0;
            pointer-events: none;
            transition: opacity 0.25s ease;
        }

        #sidebar-backdrop.active {
            opacity: 1;
            pointer-events: auto;
        }

        /* Toggle pill in header */
        .sidebar-toggle-pill {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 7px 15px;
            background: #ffffff;
            border: 1.5px solid rgba(255, 95, 0, 0.35);
            border-radius: 9999px;
            color: #ff5f00;
            font-size: 13px;
            font-weight: 700;
            cursor: pointer;
            box-shadow: inset 0 1px 1.5px #fff, 0 3px 8px rgba(255, 95, 0, 0.12);
            transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
        }

        .sidebar-toggle-pill:hover {
            background: linear-gradient(135deg, rgba(255, 95, 0, 0.12), rgba(255, 133, 51, 0.08));
            border-color: #ff5f00;
            transform: translateY(-1px);
            box-shadow: inset 0 1px 1.5px #fff, 0 5px 14px rgba(255, 95, 0, 0.25);
        }

        .sidebar-toggle-pill i {
            font-size: 14px;
        }"""

assert old_sidebar_css in html, "old_sidebar_css not found"
html = html.replace(old_sidebar_css, new_sidebar_css, 1)

# 2. Update .main-content in CSS
old_main_css = """.main-content {
            margin-left: 260px;
            flex-grow: 1;
            padding: 24px 32px;
            max-width: calc(100% - 260px);
        }"""

new_main_css = """.main-content {
            margin-left: 0;
            flex-grow: 1;
            padding: 24px 32px;
            max-width: 100%;
            width: 100%;
            transition: margin-left 0.32s cubic-bezier(0.16, 1, 0.3, 1), max-width 0.32s ease;
        }

        body.sidebar-is-pinned .main-content {
            margin-left: 275px;
            max-width: calc(100% - 275px);
        }"""

assert old_main_css in html, "old_main_css not found"
html = html.replace(old_main_css, new_main_css, 1)

# 3. Enhance .menu-item CSS for 3D depth and hover effects
old_menu_item_css = """.menu-item {
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 12px 16px;
            color: var(--text-secondary);
            text-decoration: none;
            border-radius: 8px;
            font-size: 14px;
            font-weight: 500;
            transition: all 0.2s ease;
            cursor: pointer;
        }

        .menu-item:hover {
            transform: translateX(4px);
            filter: brightness(0.96);
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
        }

        .menu-item.active {
            color: #ffffff !important;
            background: var(--color-indigo-gradient) !important;
            border-color: transparent !important;
            box-shadow: 0 4px 14px rgba(255, 95, 0, 0.35) !important;
            transform: translateX(4px);
        }

        .menu-item.active i {
            color: #ffffff !important;
        }"""

new_menu_item_css = """.menu-item {
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 11px 15px;
            color: var(--text-secondary);
            text-decoration: none;
            border-radius: 10px;
            font-size: 13.5px;
            letter-spacing: 0.15px;
            transition: all 0.22s cubic-bezier(0.16, 1, 0.3, 1);
            cursor: pointer;
            user-select: none;
            position: relative;
        }

        .menu-item:hover {
            transform: translateX(5px) scale(1.015);
            box-shadow: inset 0 1px 2px rgba(255, 255, 255, 1), 0 5px 14px rgba(0, 0, 0, 0.09) !important;
            filter: brightness(1.03);
        }

        .menu-item.active {
            color: #ffffff !important;
            background: linear-gradient(135deg, #ff5f00 0%, #ff7c26 100%) !important;
            border: 1.5px solid rgba(255, 255, 255, 0.4) !important;
            box-shadow: inset 0 1px 2.5px rgba(255, 255, 255, 0.8), 0 6px 18px rgba(255, 95, 0, 0.45) !important;
            transform: translateX(5px);
        }

        .menu-item.active i {
            color: #ffffff !important;
            filter: drop-shadow(0 2px 4px rgba(0,0,0,0.25)) !important;
        }"""

assert old_menu_item_css in html, "old_menu_item_css not found"
html = html.replace(old_menu_item_css, new_menu_item_css, 1)

# 4. Insert hover sensor and backdrop right before <aside class="sidebar">
old_aside_start = """<div class="app-layout">
        <!-- Sidebar Navigation -->
        <aside class="sidebar">
            <div class="sidebar-brand" style="padding: 16px 20px; display: flex; align-items: center; justify-content: center; border-bottom: 1px solid var(--border-color); background-color: #ffffff;">
                <img src="/static/ghn_logo.png" alt="GHN Logo" style="max-height: 48px; max-width: 100%; object-fit: contain; filter: drop-shadow(0 2px 4px rgba(0,0,0,0.02));">
            </div>"""

new_aside_start = """<div class="app-layout">
        <!-- Sidebar Edge Hover Sensor & Backdrop -->
        <div id="sidebar-hover-sensor" title="Di chuột để mở Menu Danh Mục"></div>
        <div id="sidebar-backdrop" onclick="closeSidebar()"></div>

        <!-- Sidebar Navigation -->
        <aside class="sidebar">
            <div class="sidebar-brand" style="padding: 14px 18px; display: flex; align-items: center; justify-content: space-between; border-bottom: 1px solid var(--border-color); background-color: #ffffff;">
                <img src="/static/ghn_logo.png" alt="GHN Logo" style="max-height: 44px; max-width: 135px; object-fit: contain; filter: drop-shadow(0 2px 4px rgba(0,0,0,0.02));">
                <div style="display: flex; align-items: center; gap: 6px;">
                    <button id="sidebar-pin-btn" onclick="togglePinSidebar(event)" title="Ghim thanh menu cố định (không tự ẩn)" style="background: rgba(0,0,0,0.03); border: 1px solid var(--border-color); border-radius: 6px; padding: 5px 8px; cursor: pointer; color: var(--text-secondary); transition: all 0.2s; font-size: 13px;">
                        <i class="fa-solid fa-thumbtack" id="sidebar-pin-icon" style="transform: rotate(45deg); transition: transform 0.2s ease;"></i>
                    </button>
                    <button onclick="closeSidebar()" title="Ẩn thanh menu" style="background: rgba(0,0,0,0.03); border: 1px solid var(--border-color); border-radius: 6px; padding: 5px 8px; cursor: pointer; color: var(--text-secondary); transition: all 0.2s; font-size: 13px;">
                        <i class="fa-solid fa-xmark"></i>
                    </button>
                </div>
            </div>"""

assert old_aside_start in html, "old_aside_start not found"
html = html.replace(old_aside_start, new_aside_start, 1)

# 5. Replace menu items with rich 3D Pastel Glassmorphism recipes
old_menu_items = """            <ul class="sidebar-menu">
                <li class="menu-item active" id="nav-tab-introduction" onclick="switchTab('tab-introduction', this)" style="background: linear-gradient(135deg, rgba(147, 51, 234, 0.10), rgba(168, 85, 247, 0.08)); border: 1px solid rgba(147, 51, 234, 0.28); font-weight: 700; color: #7e22ce;">
                    <i class="fa-solid fa-map-location-dot" style="color: #9333ea;"></i> Giới thiệu NTB
                </li>
                <li class="menu-item" id="nav-tab-dashboard" onclick="switchTab('tab-dashboard', this)" style="background: linear-gradient(135deg, rgba(13, 148, 136, 0.10), rgba(20, 184, 166, 0.08)); border: 1px solid rgba(13, 148, 136, 0.28); font-weight: 700; color: #0f766e;">
                    <i class="fa-solid fa-chart-pie" style="color: #0d9488;"></i> Tổng quan
                </li>
                <li class="menu-item" id="nav-tab-ntb-summary" onclick="switchTab('tab-ntb-summary', this)" style="background: linear-gradient(135deg, rgba(79, 70, 229, 0.10), rgba(99, 102, 241, 0.08)); border: 1px solid rgba(79, 70, 229, 0.28); font-weight: 700; color: #4338ca;">
                    <i class="fa-solid fa-chart-line" style="color: #4f46e5;"></i> Chỉ số NTB
                </li>
                <li class="menu-item" id="nav-tab-operational" onclick="switchTab('tab-operational', this)" style="background: linear-gradient(135deg, rgba(5, 150, 105, 0.10), rgba(16, 185, 129, 0.08)); border: 1px solid rgba(5, 150, 105, 0.28); font-weight: 700; color: #047857;">
                    <i class="fa-solid fa-truck-ramp-box" style="color: #059669;"></i> Báo cáo Vận hành
                </li>
                <li class="menu-item" id="nav-tab-opr" onclick="switchTab('tab-opr', this)" style="background: linear-gradient(135deg, rgba(37, 99, 235, 0.10), rgba(59, 130, 246, 0.08)); border: 1px solid rgba(37, 99, 235, 0.28); font-weight: 700; color: #1d4ed8;">
                    <i class="fa-solid fa-user-clock" style="color: #2563eb;"></i> OPR TTS
                </li>
                <li class="menu-item" id="nav-tab-backlog" onclick="switchTab('tab-backlog', this)" style="background: linear-gradient(135deg, rgba(217, 119, 6, 0.10), rgba(245, 158, 11, 0.08)); border: 1px solid rgba(217, 119, 6, 0.28); font-weight: 700; color: #b45309;">
                    <i class="fa-solid fa-boxes-stacked" style="color: #d97706;"></i> Giám sát Backlog
                </li>
                <li class="menu-item" id="nav-tab-unstable-po" onclick="switchTab('tab-unstable-po', this)" style="background: linear-gradient(135deg, rgba(225, 29, 72, 0.10), rgba(244, 63, 94, 0.08)); border: 1px solid rgba(225, 29, 72, 0.28); font-weight: 700; color: #be123c;">
                    <i class="fa-solid fa-triangle-exclamation" style="color: #e11d48;"></i> Bưu cục bất ổn
                </li>
                <li class="menu-item" id="nav-tab-off-spe" onclick="switchTab('tab-off-spe', this)" style="background: linear-gradient(135deg, rgba(192, 38, 211, 0.10), rgba(217, 70, 239, 0.08)); border: 1px solid rgba(192, 38, 211, 0.28); font-weight: 700; color: #a21caf;">
                    <i class="fa-solid fa-power-off" style="color: #c026d3;"></i> OFF Tuyến SPE
                </li>
                <li class="menu-item" id="nav-tab-volume-creation" onclick="switchTab('tab-volume-creation', this)" style="background: linear-gradient(135deg, rgba(2, 132, 199, 0.10), rgba(14, 165, 233, 0.08)); border: 1px solid rgba(2, 132, 199, 0.28); font-weight: 700; color: #0369a1;">
                    <i class="fa-solid fa-file-invoice" style="color: #0284c7;"></i> Volume tạo đơn
                </li>
                <li class="menu-item" id="nav-tab-heavy-10kg" onclick="switchTab('tab-heavy-10kg', this)" style="background: linear-gradient(135deg, rgba(194, 65, 12, 0.10), rgba(234, 88, 12, 0.08)); border: 1px solid rgba(194, 65, 12, 0.28); font-weight: 700; color: #9a3412;">
                    <i class="fa-solid fa-weight-hanging" style="color: #c2410c;"></i> Hàng Nặng >10kg
                </li>
                <li class="menu-item" id="nav-tab-ca-report" onclick="switchTab('tab-ca-report', this)" style="background: linear-gradient(135deg, rgba(101, 163, 13, 0.10), rgba(132, 204, 22, 0.08)); border: 1px solid rgba(101, 163, 13, 0.28); font-weight: 700; color: #4d7c0f;">
                    <i class="fa-solid fa-cubes" style="color: #65a30d;"></i> Báo cáo Sản lượng Ca
                </li>
                <li class="menu-item" id="nav-tab-productivity-realtime" onclick="switchTab('tab-productivity-realtime', this)" style="background: linear-gradient(135deg, rgba(202, 138, 4, 0.10), rgba(234, 179, 8, 0.08)); border: 1px solid rgba(202, 138, 4, 0.28); font-weight: 700; color: #a16207;">
                    <i class="fa-solid fa-bolt" style="color: #ca8a04;"></i> Năng suất NVPTTT Real time
                </li>
                <li class="menu-item" id="nav-tab-fd" onclick="switchTab('tab-fd', this)" style="background: linear-gradient(135deg, rgba(239, 68, 68, 0.10), rgba(248, 113, 113, 0.08)); border: 1px solid rgba(239, 68, 68, 0.28); font-weight: 700; color: #b91c1c;">
                    <i class="fa-solid fa-circle-xmark" style="color: #dc2626;"></i> Chỉ số FD
                </li>
                <li class="menu-item" id="nav-tab-nhan-su" onclick="switchTab('tab-nhan-su', this)" style="background: linear-gradient(135deg, rgba(109, 40, 217, 0.10), rgba(124, 58, 237, 0.08)); border: 1px solid rgba(109, 40, 217, 0.28); font-weight: 700; color: #5b21b6;">
                    <i class="fa-solid fa-users" style="color: #6d28d9;"></i> Quản lý Nhân sự
                </li>
                <li class="menu-item" id="nav-tab-kinh-doanh" onclick="switchTab('tab-kinh-doanh', this)" style="background: linear-gradient(135deg, rgba(242, 101, 34, 0.12), rgba(249, 115, 22, 0.08)); border: 1px solid rgba(242, 101, 34, 0.3); font-weight: 700; color: #ea580c;">
                    <i class="fa-solid fa-crown" style="color: #f26522;"></i> Khách Hàng Nhóm A
                </li>
                <li class="menu-item" id="nav-tab-transport-cost" onclick="switchTab('tab-transport-cost', this)" style="background: linear-gradient(135deg, rgba(2, 132, 199, 0.12), rgba(59, 130, 246, 0.12)); border: 1px solid rgba(2, 132, 199, 0.3); font-weight: 700; color: #0284c7;">
                    <i class="fa-solid fa-truck-moving" style="color: #0284c7;"></i> Chi Phí Vận Tải & KTC
                </li>
                <li class="menu-item" id="nav-tab-sync" onclick="switchTab('tab-sync', this)" style="background: linear-gradient(135deg, rgba(71, 85, 105, 0.10), rgba(100, 116, 139, 0.08)); border: 1px solid rgba(71, 85, 105, 0.28); font-weight: 700; color: #334155;">
                    <i class="fa-solid fa-rotate" style="color: #475569;"></i> Đồng bộ & Files
                </li>
            </ul>"""

new_menu_items = """            <ul class="sidebar-menu">
                <li class="menu-item active" id="nav-tab-introduction" onclick="switchTab('tab-introduction', this)" style="background: linear-gradient(135deg, rgba(147, 51, 234, 0.15) 0%, rgba(236, 72, 153, 0.10) 100%); border: 1.5px solid rgba(147, 51, 234, 0.35); box-shadow: inset 0 1px 1.5px rgba(255, 255, 255, 0.9), 0 3px 8px rgba(147, 51, 234, 0.10); font-weight: 800; color: #6b21a8;">
                    <i class="fa-solid fa-map-location-dot" style="color: #9333ea; filter: drop-shadow(0 1px 2px rgba(147, 51, 234, 0.3));"></i> Giới thiệu NTB
                </li>
                <li class="menu-item" id="nav-tab-dashboard" onclick="switchTab('tab-dashboard', this)" style="background: linear-gradient(135deg, rgba(13, 148, 136, 0.15) 0%, rgba(56, 189, 248, 0.10) 100%); border: 1.5px solid rgba(13, 148, 136, 0.35); box-shadow: inset 0 1px 1.5px rgba(255, 255, 255, 0.9), 0 3px 8px rgba(13, 148, 136, 0.10); font-weight: 800; color: #0f766e;">
                    <i class="fa-solid fa-chart-pie" style="color: #0d9488; filter: drop-shadow(0 1px 2px rgba(13, 148, 136, 0.3));"></i> Tổng quan
                </li>
                <li class="menu-item" id="nav-tab-ntb-summary" onclick="switchTab('tab-ntb-summary', this)" style="background: linear-gradient(135deg, rgba(79, 70, 229, 0.15) 0%, rgba(147, 51, 234, 0.10) 100%); border: 1.5px solid rgba(79, 70, 229, 0.35); box-shadow: inset 0 1px 1.5px rgba(255, 255, 255, 0.9), 0 3px 8px rgba(79, 70, 229, 0.10); font-weight: 800; color: #4338ca;">
                    <i class="fa-solid fa-chart-line" style="color: #4f46e5; filter: drop-shadow(0 1px 2px rgba(79, 70, 229, 0.3));"></i> Chỉ số NTB
                </li>
                <li class="menu-item" id="nav-tab-operational" onclick="switchTab('tab-operational', this)" style="background: linear-gradient(135deg, rgba(5, 150, 105, 0.15) 0%, rgba(16, 185, 129, 0.10) 100%); border: 1.5px solid rgba(5, 150, 105, 0.35); box-shadow: inset 0 1px 1.5px rgba(255, 255, 255, 0.9), 0 3px 8px rgba(5, 150, 105, 0.10); font-weight: 800; color: #047857;">
                    <i class="fa-solid fa-truck-ramp-box" style="color: #059669; filter: drop-shadow(0 1px 2px rgba(5, 150, 105, 0.3));"></i> Báo cáo Vận hành
                </li>
                <li class="menu-item" id="nav-tab-opr" onclick="switchTab('tab-opr', this)" style="background: linear-gradient(135deg, rgba(37, 99, 235, 0.15) 0%, rgba(59, 130, 246, 0.10) 100%); border: 1.5px solid rgba(37, 99, 235, 0.35); box-shadow: inset 0 1px 1.5px rgba(255, 255, 255, 0.9), 0 3px 8px rgba(37, 99, 235, 0.10); font-weight: 800; color: #1d4ed8;">
                    <i class="fa-solid fa-user-clock" style="color: #2563eb; filter: drop-shadow(0 1px 2px rgba(37, 99, 235, 0.3));"></i> OPR TTS
                </li>
                <li class="menu-item" id="nav-tab-backlog" onclick="switchTab('tab-backlog', this)" style="background: linear-gradient(135deg, rgba(217, 119, 6, 0.15) 0%, rgba(245, 158, 11, 0.10) 100%); border: 1.5px solid rgba(217, 119, 6, 0.35); box-shadow: inset 0 1px 1.5px rgba(255, 255, 255, 0.9), 0 3px 8px rgba(217, 119, 6, 0.10); font-weight: 800; color: #b45309;">
                    <i class="fa-solid fa-boxes-stacked" style="color: #d97706; filter: drop-shadow(0 1px 2px rgba(217, 119, 6, 0.3));"></i> Giám sát Backlog
                </li>
                <li class="menu-item" id="nav-tab-unstable-po" onclick="switchTab('tab-unstable-po', this)" style="background: linear-gradient(135deg, rgba(225, 29, 72, 0.15) 0%, rgba(244, 63, 94, 0.10) 100%); border: 1.5px solid rgba(225, 29, 72, 0.35); box-shadow: inset 0 1px 1.5px rgba(255, 255, 255, 0.9), 0 3px 8px rgba(225, 29, 72, 0.10); font-weight: 800; color: #be123c;">
                    <i class="fa-solid fa-triangle-exclamation" style="color: #e11d48; filter: drop-shadow(0 1px 2px rgba(225, 29, 72, 0.3));"></i> Bưu cục bất ổn
                </li>
                <li class="menu-item" id="nav-tab-off-spe" onclick="switchTab('tab-off-spe', this)" style="background: linear-gradient(135deg, rgba(192, 38, 211, 0.15) 0%, rgba(217, 70, 239, 0.10) 100%); border: 1.5px solid rgba(192, 38, 211, 0.35); box-shadow: inset 0 1px 1.5px rgba(255, 255, 255, 0.9), 0 3px 8px rgba(192, 38, 211, 0.10); font-weight: 800; color: #a21caf;">
                    <i class="fa-solid fa-power-off" style="color: #c026d3; filter: drop-shadow(0 1px 2px rgba(192, 38, 211, 0.3));"></i> OFF Tuyến SPE
                </li>
                <li class="menu-item" id="nav-tab-volume-creation" onclick="switchTab('tab-volume-creation', this)" style="background: linear-gradient(135deg, rgba(2, 132, 199, 0.15) 0%, rgba(14, 165, 233, 0.10) 100%); border: 1.5px solid rgba(2, 132, 199, 0.35); box-shadow: inset 0 1px 1.5px rgba(255, 255, 255, 0.9), 0 3px 8px rgba(2, 132, 199, 0.10); font-weight: 800; color: #0369a1;">
                    <i class="fa-solid fa-file-invoice" style="color: #0284c7; filter: drop-shadow(0 1px 2px rgba(2, 132, 199, 0.3));"></i> Volume tạo đơn
                </li>
                <li class="menu-item" id="nav-tab-heavy-10kg" onclick="switchTab('tab-heavy-10kg', this)" style="background: linear-gradient(135deg, rgba(194, 65, 12, 0.15) 0%, rgba(234, 88, 12, 0.10) 100%); border: 1.5px solid rgba(194, 65, 12, 0.35); box-shadow: inset 0 1px 1.5px rgba(255, 255, 255, 0.9), 0 3px 8px rgba(194, 65, 12, 0.10); font-weight: 800; color: #9a3412;">
                    <i class="fa-solid fa-weight-hanging" style="color: #c2410c; filter: drop-shadow(0 1px 2px rgba(194, 65, 12, 0.3));"></i> Hàng Nặng >10kg
                </li>
                <li class="menu-item" id="nav-tab-ca-report" onclick="switchTab('tab-ca-report', this)" style="background: linear-gradient(135deg, rgba(101, 163, 13, 0.15) 0%, rgba(132, 204, 22, 0.10) 100%); border: 1.5px solid rgba(101, 163, 13, 0.35); box-shadow: inset 0 1px 1.5px rgba(255, 255, 255, 0.9), 0 3px 8px rgba(101, 163, 13, 0.10); font-weight: 800; color: #4d7c0f;">
                    <i class="fa-solid fa-cubes" style="color: #65a30d; filter: drop-shadow(0 1px 2px rgba(101, 163, 13, 0.3));"></i> Báo cáo Sản lượng Ca
                </li>
                <li class="menu-item" id="nav-tab-productivity-realtime" onclick="switchTab('tab-productivity-realtime', this)" style="background: linear-gradient(135deg, rgba(202, 138, 4, 0.15) 0%, rgba(234, 179, 8, 0.10) 100%); border: 1.5px solid rgba(202, 138, 4, 0.35); box-shadow: inset 0 1px 1.5px rgba(255, 255, 255, 0.9), 0 3px 8px rgba(202, 138, 4, 0.10); font-weight: 800; color: #a16207;">
                    <i class="fa-solid fa-bolt" style="color: #ca8a04; filter: drop-shadow(0 1px 2px rgba(202, 138, 4, 0.3));"></i> Năng suất NVPTTT Real time
                </li>
                <li class="menu-item" id="nav-tab-fd" onclick="switchTab('tab-fd', this)" style="background: linear-gradient(135deg, rgba(239, 68, 68, 0.15) 0%, rgba(248, 113, 113, 0.10) 100%); border: 1.5px solid rgba(239, 68, 68, 0.35); box-shadow: inset 0 1px 1.5px rgba(255, 255, 255, 0.9), 0 3px 8px rgba(239, 68, 68, 0.10); font-weight: 800; color: #b91c1c;">
                    <i class="fa-solid fa-circle-xmark" style="color: #dc2626; filter: drop-shadow(0 1px 2px rgba(239, 68, 68, 0.3));"></i> Chỉ số FD
                </li>
                <li class="menu-item" id="nav-tab-nhan-su" onclick="switchTab('tab-nhan-su', this)" style="background: linear-gradient(135deg, rgba(109, 40, 217, 0.15) 0%, rgba(124, 58, 237, 0.10) 100%); border: 1.5px solid rgba(109, 40, 217, 0.35); box-shadow: inset 0 1px 1.5px rgba(255, 255, 255, 0.9), 0 3px 8px rgba(109, 40, 217, 0.10); font-weight: 800; color: #5b21b6;">
                    <i class="fa-solid fa-users" style="color: #6d28d9; filter: drop-shadow(0 1px 2px rgba(109, 40, 217, 0.3));"></i> Quản lý Nhân sự
                </li>
                <li class="menu-item" id="nav-tab-kinh-doanh" onclick="switchTab('tab-kinh-doanh', this)" style="background: linear-gradient(135deg, rgba(255, 95, 0, 0.20) 0%, rgba(16, 185, 129, 0.18) 100%); border: 1.5px solid rgba(255, 95, 0, 0.42); box-shadow: inset 0 1px 2px rgba(255, 255, 255, 0.95), inset 0 -1px 2px rgba(255, 95, 0, 0.12), 0 4px 12px rgba(255, 95, 0, 0.18); font-weight: 800; color: #c2410c;">
                    <i class="fa-solid fa-crown" style="color: #ff5f00; filter: drop-shadow(0 2px 4px rgba(255, 95, 0, 0.4));"></i> Khách Hàng Nhóm A
                </li>
                <li class="menu-item" id="nav-tab-transport-cost" onclick="switchTab('tab-transport-cost', this)" style="background: linear-gradient(135deg, rgba(2, 132, 199, 0.20) 0%, rgba(99, 102, 241, 0.18) 100%); border: 1.5px solid rgba(2, 132, 199, 0.42); box-shadow: inset 0 1px 2px rgba(255, 255, 255, 0.95), inset 0 -1px 2px rgba(2, 132, 199, 0.12), 0 4px 12px rgba(2, 132, 199, 0.18); font-weight: 800; color: #0369a1;">
                    <i class="fa-solid fa-truck-moving" style="color: #0284c7; filter: drop-shadow(0 2px 4px rgba(2, 132, 199, 0.4));"></i> Chi Phí Vận Tải & KTC
                </li>
                <li class="menu-item" id="nav-tab-sync" onclick="switchTab('tab-sync', this)" style="background: linear-gradient(135deg, rgba(71, 85, 105, 0.15) 0%, rgba(100, 116, 139, 0.10) 100%); border: 1.5px solid rgba(71, 85, 105, 0.35); box-shadow: inset 0 1px 1.5px rgba(255, 255, 255, 0.9), 0 3px 8px rgba(71, 85, 105, 0.10); font-weight: 800; color: #334155;">
                    <i class="fa-solid fa-rotate" style="color: #475569; filter: drop-shadow(0 1px 2px rgba(71, 85, 105, 0.3));"></i> Đồng bộ & Files
                </li>
            </ul>"""

assert old_menu_items in html, "old_menu_items not found"
html = html.replace(old_menu_items, new_menu_items, 1)

# 6. Add Toggle Button into top-header
old_top_header = """            <header class="top-header">
                <div class="header-title">
                    <h1 id="page-title">GIỚI THIỆU VÙNG NAM TRUNG BỘ</h1>
                    <p id="last-sync-time">Lần đồng bộ cuối: Chưa có</p>
                </div>"""

new_top_header = """            <header class="top-header">
                <div class="header-title" style="display: flex; align-items: center; gap: 14px;">
                    <button id="sidebar-toggle-btn" class="sidebar-toggle-pill" onclick="toggleSidebar(event)" title="Chạm / Bấm để mở Menu Danh Mục">
                        <i class="fa-solid fa-bars-staggered"></i>
                        <span>Menu Danh Mục</span>
                    </button>
                    <div>
                        <h1 id="page-title">GIỚI THIỆU VÙNG NAM TRUNG BỘ</h1>
                        <p id="last-sync-time">Lần đồng bộ cuối: Chưa có</p>
                    </div>
                </div>"""

assert old_top_header in html, "old_top_header not found"
html = html.replace(old_top_header, new_top_header, 1)

# 7. Update switchTab and add Sidebar JS logic
old_switch_tab = """        // Tab switching
        function switchTab(tabId, el) {
            document.querySelectorAll('.menu-item').forEach(item => item.classList.remove('active'));"""

new_switch_tab = """        // ================= Sidebar Auto-Hide / Pin System =================
        let sidebarPinned = localStorage.getItem('ghn_sidebar_pinned') === 'true';
        let sidebarHoverTimer = null;

        function initSidebarState() {
            const sidebar = document.querySelector('.sidebar');
            const pinIcon = document.getElementById('sidebar-pin-icon');
            const pinBtn = document.getElementById('sidebar-pin-btn');
            if (sidebarPinned) {
                document.body.classList.add('sidebar-is-pinned');
                if (sidebar) sidebar.classList.add('pinned');
                if (pinIcon) pinIcon.style.transform = 'rotate(0deg)';
                if (pinBtn) { pinBtn.style.color = '#ff5f00'; pinBtn.style.background = 'rgba(255, 95, 0, 0.1)'; }
            } else {
                document.body.classList.remove('sidebar-is-pinned');
                if (sidebar) sidebar.classList.remove('pinned');
                if (pinIcon) pinIcon.style.transform = 'rotate(45deg)';
                if (pinBtn) { pinBtn.style.color = 'var(--text-secondary)'; pinBtn.style.background = 'rgba(0,0,0,0.03)'; }
            }
        }

        function openSidebar() {
            const sidebar = document.querySelector('.sidebar');
            const backdrop = document.getElementById('sidebar-backdrop');
            if (!sidebarPinned && sidebar) {
                sidebar.classList.add('open');
                if (backdrop) backdrop.classList.add('active');
            }
        }

        function closeSidebar() {
            const sidebar = document.querySelector('.sidebar');
            const backdrop = document.getElementById('sidebar-backdrop');
            if (!sidebarPinned && sidebar) {
                sidebar.classList.remove('open');
                if (backdrop) backdrop.classList.remove('active');
            }
        }

        function toggleSidebar(e) {
            if (e) e.stopPropagation();
            const sidebar = document.querySelector('.sidebar');
            if (sidebar && sidebar.classList.contains('open')) {
                closeSidebar();
            } else {
                openSidebar();
            }
        }

        function togglePinSidebar(e) {
            if (e) e.stopPropagation();
            sidebarPinned = !sidebarPinned;
            localStorage.setItem('ghn_sidebar_pinned', sidebarPinned ? 'true' : 'false');
            const sidebar = document.querySelector('.sidebar');
            const backdrop = document.getElementById('sidebar-backdrop');
            if (backdrop) backdrop.classList.remove('active');
            if (sidebar) sidebar.classList.remove('open');
            initSidebarState();
        }

        // Setup hover triggers on edge sensor and sidebar
        document.addEventListener('DOMContentLoaded', () => {
            initSidebarState();
            const sensor = document.getElementById('sidebar-hover-sensor');
            const sidebar = document.querySelector('.sidebar');
            const backdrop = document.getElementById('sidebar-backdrop');

            if (sensor) {
                sensor.addEventListener('mouseenter', () => {
                    clearTimeout(sidebarHoverTimer);
                    openSidebar();
                });
            }

            if (sidebar) {
                sidebar.addEventListener('mouseenter', () => {
                    clearTimeout(sidebarHoverTimer);
                });
                sidebar.addEventListener('mouseleave', () => {
                    if (!sidebarPinned) {
                        sidebarHoverTimer = setTimeout(() => {
                            closeSidebar();
                        }, 260);
                    }
                });
            }

            if (backdrop) {
                backdrop.addEventListener('click', () => {
                    closeSidebar();
                });
            }
        });

        // Tab switching
        function switchTab(tabId, el) {
            if (!sidebarPinned) {
                closeSidebar();
            }
            document.querySelectorAll('.menu-item').forEach(item => item.classList.remove('active'));"""

assert old_switch_tab in html, "old_switch_tab not found"
html = html.replace(old_switch_tab, new_switch_tab, 1)

with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("SUCCESS: index.html updated successfully with Auto-hide sidebar & 3D Pastel Glass tabs!")
