import streamlit as st
import os
import time
import random
import pandas as pd
import glob
import hashlib

# 1. Global Page Layout & Base Configurations
st.set_page_config(
    page_title="NexaEdge Network | Official Node Gateway",
    page_icon="🟢",
    layout="centered"
)

# =========================================================================
# 🔒 Multi-Process Shared Server Memory & Simulated Ledger Database
# =========================================================================
@st.cache_resource
def init_global_network_server():
    return {
        "active_device_set": set(),             # Tracks active real-time online running session IDs
        "total_online_viewers": random.randint(102, 125), # Base real-world online visitors simulation
        "device_balances": {},                  # Local device ledger {dev_id: {app_earned, total_energy_wh, session_seconds}}
        "user_db": {                            # Global Registered Accounts DB {email: {password_hash, wallet, score, reg_time}}
            "demo@nexaedge.ai": {
                "password_hash": hashlib.sha256("nexa2026".encode()).hexdigest(),
                "wallet": "GjvqAarpBirdGu2ahhKTrZ5sUcuPexGatMuGDmZLAb33",
                "score": 1479.0,
                "reg_time": "2026-05-18 14:22:05"
            }
        }
    }

global_server = init_global_network_server()

# --- 🔐 Hardware Fingerprint Extraction ---
if "device_fingerprint" not in st.session_state:
    ctx_headers = st.context.headers
    user_agent = ctx_headers.get("User-Agent", "Unknown-Device")
    remote_ip = ctx_headers.get("X-Forwarded-For", "127.0.0.1")
    raw_fingerprint = f"{user_agent}_{remote_ip}"
    st.session_state.device_fingerprint = hashlib.md5(raw_fingerprint.encode('utf-8')).hexdigest()[:12]

dev_id = st.session_state.device_fingerprint

# --- User Auth Session Initialization ---
if "current_user" not in st.session_state:
    st.session_state.current_user = None  # None represents Visitor Mode

# Initialize anonymous hardware profile
if dev_id not in global_server["device_balances"]:
    global_server["device_balances"][dev_id] = {
        "app_earned": 0.0,
        "total_energy_wh": 0.0,
        "session_seconds": 0
    }

# --- Data Linker: Mount Local Earnings to Logged Account ---
def sync_data_from_source():
    if st.session_state.current_user:
        email = st.session_state.current_user
        if 'app_earned' not in st.session_state or st.session_state.get('last_user') != email:
            st.session_state.app_earned = global_server["user_db"][email]["score"]
            st.session_state.total_energy_wh = global_server["device_balances"][dev_id]["total_energy_wh"]
            st.session_state.session_seconds = global_server["device_balances"][dev_id]["session_seconds"]
            st.session_state.last_user = email
    else:
        if 'app_earned' not in st.session_state or st.session_state.get('last_user') is not None:
            st.session_state.app_earned = global_server["device_balances"][dev_id]["app_earned"]
            st.session_state.total_energy_wh = global_server["device_balances"][dev_id]["total_energy_wh"]
            st.session_state.session_seconds = global_server["device_balances"][dev_id]["session_seconds"]
            st.session_state.last_user = None

sync_data_from_source()

if "session_id" not in st.session_state:
    st.session_state.session_id = f"node_{dev_id}_{random.randint(1000, 9999)}"
    global_server["total_online_viewers"] += 1

# --- Safe State Handlers ---
if 'app_running' not in st.session_state: st.session_state.app_running = False
if 'chart_history' not in st.session_state: st.session_state.chart_history = [22.0, 25.0, 24.0, 28.0, 27.0, 31.0, 29.0, 33.0, 31.0, 35.0, 33.0, 36.8]
if 'target_time_index' not in st.session_state: st.session_state.target_time_index = 2 
if 'last_tick_time' not in st.session_state: st.session_state.last_tick_time = 0.0
if 'my_referral_code' not in st.session_state: st.session_state.my_referral_code = ""
if 'registration_success' not in st.session_state: st.session_state.registration_success = False

# --- 📸 Auto Image Injector ---
def get_project_image():
    if os.path.exists("image.png"):
        return "image.png"
    png_files = glob.glob("*.png")
    if png_files:
        return png_files[0]
    return None

target_image = get_project_image()

def generate_referral_code(wallet_str):
    if not wallet_str:
        return ""
    hasher = hashlib.md5(wallet_str.encode('utf-8')).hexdigest().upper()
    return f"NEXA-{wallet_str[:4].upper()}-{hasher[:4]}"

# --- 🟢 Advanced Cyberpunk UI Styles Injection ---
st.markdown("""
    <style>
    .stApp { background-color: #0b0f12; }
    #MainMenu, footer, .styles_viewerBadge__FUChv, [data-testid="manage-app-button"] { display: none !important; }
    header, [data-testid="stHeader"] { background: transparent !important; border: none !important; height: 0 !important; display: none !important; }
    [data-testid="stVerticalBlock"] > div:empty { display: none !important; margin: 0 !important; padding: 0 !important; }
    [data-testid="stElementContainer"] { border: none !important; background: transparent !important; margin-bottom: 6px !important; }
    
    /* Elegant Clean Tabs Styling */
    .stTabs [data-baseweb="tab-list"] { gap: 6px; background-color: transparent !important; justify-content: flex-start; border: none !important; overflow-x: auto; }
    .stTabs [data-baseweb="tab"] { background-color: #11171d !important; color: #bdc3c7 !important; border-radius: 8px 8px 0px 0px !important; border: 1px solid #1e272e !important; border-bottom: none !important; padding: 6px 12px !important; font-weight: 700 !important; font-size: 12px !important; white-space: nowrap; }
    .stTabs [aria-selected="true"] { color: #A2FF00 !important; background-color: #161c23 !important; border-top: 2px solid #A2FF00 !important; }
    .stTabs [data-baseweb="tab-highlight"] { background-color: #A2FF00 !important; height: 0px !important; }
    
    /* Component Cards & Containers */
    .app-container { background-color: #11171d; border: 1px solid #1e272e; border-radius: 20px; padding: 14px; margin: 0 auto; box-shadow: 0 10px 30px rgba(0,0,0,0.5); }
    .app-card { background-color: #161c23; border: 1px solid #252e38; border-radius: 14px; padding: 12px; margin-bottom: 10px; }
    .app-title { font-size: 11px; color: #88929b; font-weight: bold; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 4px; }
    .app-value { font-family: 'Inter', sans-serif; color: #ffffff; font-size: 22px; font-weight: 700; }
    
    .neon-green-text { color: #A2FF00 !important; }
    .neon-blue-text { color: #00e5ff !important; }
    .temp-section { display: flex; align-items: center; justify-content: space-between; background: #11171d; padding: 6px 12px; border-radius: 10px; margin-top: 6px; }
    
    /* Interactive Button Matrix Override */
    div.stButton > button:first-child { background-color: #A2FF00 !important; color: #0b0f12 !important; font-weight: 800 !important; font-size: 14px !important; width: 100% !important; border-radius: 12px !important; border: none !important; padding: 10px 4px !important; box-shadow: 0 0 15px rgba(162, 255, 0, 0.3); transition: all 0.2s; }
    div.stButton > button[key*="app_stop_btn"] { background-color: #0b0f12 !important; color: #ffffff !important; border: 1px solid #f43f5e !important; box-shadow: none !important; }
    div.stButton > button[key*="logout_btn"] { background-color: #343a40 !important; color: #ffc107 !important; box-shadow: none !important; padding: 4px 10px !important; font-size: 12px !important; width: auto !important; }
    
    /* Forms and Input Boxes styling */
    [data-testid="stForm"] { background-color: #161c23 !important; border: 1px solid #252e38 !important; border-radius: 16px !important; padding: 12px !important; }
    .user-badge { background: #1e293b; padding: 8px 12px; border-radius: 10px; border-left: 3px solid #00e5ff; margin-bottom: 12px; font-size: 12px; color: #e2e8f0; }
    .mini-stat-card { text-align: center; background-color:#141d26; padding: 8px 4px; border-radius: 10px; min-height: 55px; display: flex; flex-direction: column; justify-content: center; align-items: center; }
    .mini-stat-title { font-size: 9px !important; color: #88929b; font-weight: bold; white-space: nowrap; }
    .mini-stat-value { font-size: 13px !important; font-weight: bold; font-family: monospace; margin-top: 2px; }
    
    .feature-box { background-color: #11171d; padding: 14px; border-radius: 10px; border-left: 4px solid #A2FF00; margin-bottom: 10px; }
    .social-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(65px, 1fr)); gap: 4px; margin: 6px 0; }
    .social-btn { display: block; text-align: center; padding: 4px; background-color: #11171d; border: 1px solid #252e38; border-radius: 6px; color: #bdc3c7 !important; font-size: 10px; font-weight: bold; text-decoration: none; }
    .social-btn:hover { border-color: #A2FF00; color: #A2FF00 !important; }

    /* Compact Form Inputs Override */
    [data-testid="stForm"] div[data-testid="stWidgetLabel"] p { font-size: 11px !important; margin-bottom: -4px !important; }
    [data-testid="stForm"] input { padding: 6px 10px !important; font-size: 12px !important; }

    /* Back-office Database Admin Table Styling */
    .admin-table { width: 100%; border-collapse: collapse; margin-top: 10px; font-size: 12px; color: #cdfaee; }
    .admin-table th { background-color: #1f2937; color: #A2FF00; text-align: left; padding: 8px; border: 1px solid #374151; }
    .admin-table td { padding: 8px; border: 1px solid #374151; background-color: #111827; }
    </style>
""", unsafe_allow_html=True)

# Update network nodes state live
if st.session_state.app_running:
    global_server["active_device_set"].add(st.session_state.session_id)
else:
    global_server["active_device_set"].discard(st.session_state.session_id)

# 🔄 Time Anti-Suspension Mechanism
if st.session_state.app_running and st.session_state.last_tick_time > 0:
    current_unix = time.time()
    elapsed_gap = int(current_unix - st.session_state.last_tick_time)
    if elapsed_gap >= 1:
        st.session_state.session_seconds += elapsed_gap
        st.session_state.app_earned += elapsed_gap * 0.01
        st.session_state.total_energy_wh += 5.1 * (elapsed_gap / 3600.0)
        st.session_state.last_tick_time = current_unix
        
        # Real-time writing back to global simulated DB
        if st.session_state.current_user:
            global_server["user_db"][st.session_state.current_user]["score"] = st.session_state.app_earned
        else:
            global_server["device_balances"][dev_id]["app_earned"] = st.session_state.app_earned
        global_server["device_balances"][dev_id]["total_energy_wh"] = st.session_state.total_energy_wh
        global_server["device_balances"][dev_id]["session_seconds"] = st.session_state.session_seconds

# --- Global Header Banner ---
st.markdown('<h1 style="text-align:center; color:#A2FF00; font-size:32px; font-weight:800; margin-bottom:0px;">NexaEdge Network</h1>', unsafe_allow_html=True)

# Strict Separation of Language Content Matrices
lang = st.selectbox("🌐 Language Switcher", ["English", "中文"], index=0, label_visibility="collapsed")

TIME_OPTIONS_EN = ["15 Minutes", "30 Minutes", "1 Hour", "2 Hours", "4 Hours", "8 Hours", "12 Hours", "24 Hours"]
TIME_OPTIONS_ZH = ["15分钟", "半小时", "1小时", "2小时", "4小时", "8小时", "12小时", "24小时"]
SECONDS_MAP = [900, 1800, 3600, 7200, 14400, 28800, 43200, 86400]
HOURS_MAP = [0.25, 0.5, 1.0, 2.0, 4.0, 8.0, 12.0, 24.0]
current_options = TIME_OPTIONS_EN if lang == "English" else TIME_OPTIONS_ZH

if lang == "English":
    st.markdown('<p style="font-size: 14px; color: #A2FF00; font-weight:bold; text-align: center; margin-top: 5px;">Transforming idle smartphones into high-purity data network for AI Era.</p>', unsafe_allow_html=True)
else:
    st.markdown('<p style="font-size: 14px; color: #A2FF00; font-weight:bold; text-align: center; margin-top: 5px;">让全球闲置手机，成为 AI 时代的高纯度分布式算力网络</p>', unsafe_allow_html=True)

# ==========================================
# 👑 2:1 LAYOUT STRUCTURE RE-MIGRATED
# ==========================================
intro_left, intro_right = st.columns([2, 1])

with intro_left:
    if target_image:
        st.image(target_image, use_container_width=True)

with intro_right:
    st.markdown("<div style='height: 5px;'></div>", unsafe_allow_html=True)
    if lang == "English":
        st.markdown("""
        <div style="background-color: #11171d; border: 1px solid #1e272e; padding: 12px; border-radius: 14px; height: 100%;">
            <p style="color:#A2FF00; font-size:13px; font-weight:800; margin-bottom:6px; text-transform:uppercase;">⚡ Project Briefing</p>
            <p style="color:#ffffff; font-size:11px; line-height:1.4; margin:0;">
                NexaEdge empowers users to monetize unutilized smartphone capabilities. By creating an encrypted decentralized sandbox network, your device seamlessly routes localized data verification processes to unlock institutional level rewards while you sleep.
            </p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="background-color: #11171d; border: 1px solid #1e272e; padding: 12px; border-radius: 14px; height: 100%;">
            <p style="color:#A2FF00; font-size:13px; font-weight:800; margin-bottom:6px; text-transform:uppercase;">⚡ 项目核心简报</p>
            <p style="color:#ffffff; font-size:11px; line-height:1.4; margin:0;">
                NexaEdge 赋予普通用户将闲置手机性能变现的完整权利。通过建立端到端的加密去中心化沙盒环境，您的设备可在充电且闲置时自动承接分布式 AI 数据清洗与验证任务，安全赚取行业先锋红利。
            </p>
        </div>
        """, unsafe_allow_html=True)

# --- Public Frontend Navigation Tabs ---
tab1, tab2, tab3 = st.tabs([
    "🌐 Overview" if lang=="English" else "🌐 项目通识", 
    "📱 Dashboard" if lang=="English" else "📱 算力控制台", 
    "🔑 Identity Portal" if lang=="English" else "🔑 账户管理中心"
])

# ==========================================
# TAB 1: OVERVIEW & PILLARS
# ==========================================
with tab1:
    c1, c2, c3 = st.columns(3)
    if lang == "English":
        with c1: st.metric(label="Network Fee", value="20%", delta="Pure Revenue")
        with c2: st.metric(label="Safety Lock", value="39°C", delta="Device Safety", delta_color="inverse")
        with c3: st.metric(label="Settlement Base", value="Solana SPL", delta="Low Gas / TPS")
        st.markdown('<h2 style="color:#A2FF00; font-size:18px; margin-top:10px;">💰 Revenue Calculator</h2>', unsafe_allow_html=True)
        selected_time_tab1 = st.selectbox("Select Session Pattern:", current_options, index=st.session_state.target_time_index, key="calc_box_en")
        st.session_state.target_time_index = current_options.index(selected_time_tab1)
        st.success(f"🎉 Estimated Monthly Income: {HOURS_MAP[st.session_state.target_time_index] * 0.35 * 30:.2f} USDT")
        
        st.markdown("""
        <div class="feature-box">
            <h4 style="color:white; margin:0; font-size:14px;">📱 Passive Income via Charging</h4>
            <p style="color:#bdc3c7; font-size:12px; margin:4px 0 0 0;">Just plug in and connect Wi-Fi at night, NexaEdge's lightweight WASM Sandbox cleans AI datasets silently in the background.</p>
        </div>
        <div class="feature-box">
            <h4 style="color:white; margin:0; font-size:14px;">🔥 39°C Thermal Guard Barrier</h4>
            <p style="color:#bdc3c7; font-size:12px; margin:4px 0 0 0;">Total hardware protection. System auto-throttles load instantly if battery hits 39°C. Zero hardware degradation anxiety.</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        with c1: st.metric(label="平台技术抽成", value="20%", delta="纯现金流造血")
        with c2: st.metric(label="智能硬件风控", value="39°C", delta="秒级控温预警", delta_color="inverse")
        with c3: st.metric(label="算力结算底座", value="Solana SPL", delta="极速、低 Gas")
        st.markdown('<h2 style="color:#A2FF00; font-size:18px; margin-top:10px;">💰 设备收益计算器</h2>', unsafe_allow_html=True)
        selected_time_tab1 = st.selectbox("选择运行时间档位:", current_options, index=st.session_state.target_time_index, key="calc_box_zh")
        st.session_state.target_time_index = current_options.index(selected_time_tab1)
        st.success(f"🎉 预计每月可带来收益: {HOURS_MAP[st.session_state.target_time_index] * 0.35 * 30:.2f} USDT")
        
        st.markdown("""
        <div class="feature-box">
            <h4 style="color:white; margin:0; font-size:14px;">📱 充电即赚·睡后收入</h4>
            <p style="color:#bdc3c7; font-size:12px; margin:4px 0 0 0;">只需在夜间充电并连接 Wi-Fi，NexaEdge 的轻量级 WASM 沙盒便会在后台静默运行清洗 AI 语料。</p>
        </div>
        <div class="feature-box">
            <h4 style="color:white; margin:0; font-size:14px;">🔥 39°C 智能温控屏障</h4>
            <p style="color:#bdc3c7; font-size:12px; margin:4px 0 0 0;">坚守绝不伤机底线。一旦手机运行温度触及 39°C 临界点，系统自动下发降载指令，打消损耗焦虑。</p>
        </div>
        """, unsafe_allow_html=True)

    # 🛡️ COMPACT WHITELIST FORM (Exclusively isolated inside Tab 1 bottom)
    st.markdown("<br>", unsafe_allow_html=True)
    with st.form("unified_whitelist_form"):
        wl_title = "🎁 Genesis Whitelist & Referral Boosters" if lang=="English" else "🎁 申领创世白名单与社媒双倍奖励"
        st.markdown(f'<div style="font-size:12px; font-weight:bold; color:#A2FF00; margin-bottom:2px;">{wl_title}</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="social-grid">
            <a class="social-btn" href="https://www.instagram.com/nexaedge__?igsh=eXp0MTlmdDR6dm10&utm_source=qr" target="_blank">📸 Instagram</a>
            <a class="social-btn" href="https://x.com/nexaedge_?s=21&t=8onO0h_fTxzmAGu431ZxXw" target="_blank">🐦 X</a>
            <a class="social-btn" href="https://www.facebook.com/share/18eXN6P3Ge/?mibextid=wwXIfr" target="_blank">👥 Facebook</a>
            <a class="social-btn" href="https://www.tiktok.com/@nexaedge7?_r=1&_t=ZS-96QbSMyso5v" target="_blank">🎵 TikTok</a>
            <a class="social-btn" href="https://t.me/NexaEdge7" target="_blank">📢 Telegram</a>
        </div>
        """, unsafe_allow_html=True)
        
        u_email = st.text_input("Registration Email:" if lang=="English" else "申请邮箱:", key="wl_mail").strip()
        u_wallet = st.text_input("Solana Wallet Address:" if lang=="English" else "Solana 钱包:", key="wl_wall").strip()
        u_ref_input = st.text_input("Referrer Invitation Code (Optional):" if lang=="English" else "推荐人邀请码 (选填):", key="wl_ref").strip()
        
        btn_wl = "Lock Seating ⚡" if lang=="English" else "锁定席位 ⚡"
        if st.form_submit_button(btn_wl):
            if not u_email or not u_wallet:
                st.error("❌ Form incomplete!" if lang=="English" else "❌ 请完整填写表单！")
            else:
                generated_code = generate_referral_code(u_wallet)
                st.session_state.my_referral_code = generated_code
                st.session_state.registration_success = True
                with open("whitelist.txt", "a", encoding="utf-8") as f:
                    f.write(f"Email: {u_email} | Wallet: {u_wallet} | Score: {st.session_state.app_earned:.2f} | RefCode: {generated_code}\n")
                st.toast("Allocation Record Locked!")
                st.rerun()

    if st.session_state.registration_success and st.session_state.my_referral_code:
        lbl_ref = "YOUR EXCLUSIVE SHARING CODE:" if lang=="English" else "您的专属邀请裂变码:"
        st.markdown(f'<div class="app-card" style="border:1px solid #A2FF00; text-align:center; padding: 4px;"><span style="font-size:10px; color:#88929b;">{lbl_ref}</span><br><span style="font-size:16px; font-weight:800; color:#A2FF00; font-family:monospace;">{st.session_state.my_referral_code}</span></div>', unsafe_allow_html=True)

# ==========================================
# TAB 2: NODE CONTROL DASHBOARD
# ==========================================
with tab2:
    st.markdown('<div class="app-container">', unsafe_allow_html=True)
    
    # Render Status Badges
    if st.session_state.current_user:
        badge_txt = f"🟢 Connected Cloud Account: <b>{st.session_state.current_user}</b>" if lang=="English" else f"🟢 已成功挂载云端账户: <b>{st.session_state.current_user}</b>"
        st.markdown(f'<div class="user-badge">{badge_txt}</div>', unsafe_allow_html=True)
    else:
        badge_txt = "⚠️ Running as Visitor (Data stays local. Go to [Identity Portal] to secure your assets)" if lang=="English" else "⚠️ 游客节点运行（当前数量仅存在本地，建议立即去 [账户管理中心] 注册以保障资产安全）"
        st.markdown(f'<div class="user-badge" style="border-left-color:#ffb300; color:#ffb300;">{badge_txt}</div>', unsafe_allow_html=True)

    lbl_tgt = "Set Target Session Runtime:" if lang=="English" else "配置目标运行时间:"
    selected_time_tab2 = st.selectbox(lbl_tgt, current_options, index=st.session_state.target_time_index, key="console_box")
    st.session_state.target_time_index = current_options.index(selected_time_tab2)
    target_total_seconds = SECONDS_MAP[st.session_state.target_time_index]

    if st.session_state.app_running and st.session_state.session_seconds >= target_total_seconds:
        st.session_state.app_running = False
        st.rerun()

    if st.session_state.app_running:
        current_hash = random.uniform(45.5, 49.8)
        current_temp = random.uniform(36.4, 36.9)
        current_power = random.uniform(4.85, 5.35)
    else:
        current_hash = 0.0
        current_temp = 30.5
        current_power = random.uniform(0.12, 0.18)
        
    s_sec = st.session_state.session_seconds
    time_str = f"{s_sec//3600:02d}:{(s_sec%3600)//60:02d}:{s_sec%60:02d}"
    
    st.markdown(f'<div class="app-card"><div class="app-title">DASHBOARD</div><div style="font-size:12px; color:#88929b;">NETWORK HASH RATE (MH/s): <span class="neon-green-text" style="font-weight:bold;">{current_hash:.2f}</span></div></div>', unsafe_allow_html=True)
    
    if st.session_state.app_running:
        st.session_state.chart_history.pop(0)
        st.session_state.chart_history.append(current_hash)
    st.line_chart(pd.DataFrame(st.session_state.chart_history, columns=["Hash Rate"]), height=85, use_container_width=True)
    
    # 🌡️ THERMOMETER ICON ADDED BACK
    lbl_safe = "Hardware Temp" if lang=="English" else "硬件运行温度"
    st.markdown(f'<div class="app-card" style="margin-top: -5px;"><div class="temp-section"><span class="app-value" style="font-size:16px;">🌡️ {lbl_safe}: {current_temp:.1f}°C</span><span style="background-color:#1e272e; color:#A2FF00; font-size:11px; font-weight:bold; padding:2px 8px; border-radius:5px;">SAFE</span></div></div>', unsafe_allow_html=True)

    # 🔋 BATTERY ICON PLACED IN CUMULATIVE ENERGY SECTION
    lbl_p1 = "Input Power:" if lang=="English" else "实时输入功耗:"
    lbl_p2 = "Cumulative Energy:" if lang=="English" else "🔋 累计电力消耗:"
    st.markdown(f"""
    <div class="app-card">
        <div style="display:grid; grid-template-columns: 1fr 1fr; gap:6px;">
            <div style="background:#11171d; padding:6px; border-radius:8px;">
                <div style="font-size:9px; color:#88929b; font-weight:bold;">{lbl_p1}</div>
                <div class="app-value neon-blue-text" style="font-size:14px; font-family:monospace;">{current_power:.2f} W</div>
            </div>
            <div style="background:#11171d; padding:6px; border-radius:8px;">
                <div style="font-size:9px; color:#88929b; font-weight:bold;">{lbl_p2}</div>
                <div class="app-value" style="font-size:14px; font-family:monospace; color:#ffffff;">{st.session_state.total_energy_wh:.4f} Wh</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    lbl_d1 = "Continuous Runtime:" if lang=="English" else "本次运行时长:"
    lbl_d2 = "Your Account Balance:" if lang=="English" else "当前个体账户拥有的 NEXA 总数:"
    st.markdown(f"""
    <div class="app-card">
        <div style="display:flex; justify-content:space-between;">
            <div><div style="font-size:10px; color:#88929b; font-weight:bold;">{lbl_d1}</div><div class="app-value" style="font-size:17px;">{time_str}</div></div>
            <div style="text-align:right;"><div style="font-size:10px; color:#88929b; font-weight:bold;">{lbl_d2}</div><div class="app-value neon-green-text" style="font-size:17px;">{st.session_state.app_earned:,.2f} NEXA</div></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if not st.session_state.app_running:
        btn_start = "START COMPUTE SESSION" if lang=="English" else "激活并启动边缘算力节点"
        if st.button(btn_start, key="app_start_btn"):
            st.session_state.app_running = True
            st.session_state.last_tick_time = time.time()
            st.rerun()
    else:
        btn_stop = "PAUSE COMPUTE SESSION" if lang=="English" else "暂停当前算力 Session"
        if st.button(btn_stop, key="app_stop_btn"):
            st.session_state.app_running = False
            st.session_state.last_tick_time = 0.0
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# TAB 3: 🔑 IDENTITY PORTAL & ADMIN PANEL MIGRATED HERE
# ==========================================
with tab3:
    if st.session_state.current_user:
        st.markdown('<div class="app-card" style="text-align:center; padding:20px 10px;">', unsafe_allow_html=True)
        title_auth = "<b>Secure Network Node Engaged</b>" if lang=="English" else "<b>智能网络已安全连接</b>"
        st.markdown(f"🎉 {title_auth}", unsafe_allow_html=True)
        lbl_id = f"Active Identity: <span class='neon-blue-text' style='font-weight:bold;'>{st.session_state.current_user}</span>" if lang=="English" else f"当前在线身份：<span class='neon-blue-text' style='font-weight:bold;'>{st.session_state.current_user}</span>"
        st.markdown(lbl_id, unsafe_allow_html=True)
        
        box_txt = f"Total Synchronized Cloud Earnings<br><span class='neon-green-text' style='font-size:26px; font-weight:bold;'>{st.session_state.app_earned:,.2f} NEXA</span>" if lang=="English" else f"您账户绑定的全网总收益<br><span class='neon-green-text' style='font-size:26px; font-weight:bold;'>{st.session_state.app_earned:,.2f} NEXA</span>"
        st.markdown(f"<div style='margin:15px 0; background:#11171d; padding:10px; border-radius:10px;'>{box_txt}</div>", unsafe_allow_html=True)
        
        btn_logout = "Logout Account Location" if lang=="English" else "安全退出当前登录账户"
        if st.button(btn_logout, key="logout_btn"):
            st.session_state.current_user = None
            st.session_state.app_running = False
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        opt_auth = ["Register Node Account", "Login Existing Node"] if lang=="English" else ["注册新节点账户", "登录已有账户"]
        auth_mode = st.radio("Auth Selection:", opt_auth, horizontal=True, label_visibility="collapsed")
        
        if auth_mode in ["Register Node Account", "注册新节点账户"]:
            with st.form("reg_form"):
                form_title = "🚀 Register Unified Cloud Node (Inherit & Merge Current NEXA Gains)" if lang=="English" else "🚀 注册统一网络账户（自动继承并合并当前已有NEXA数量）"
                st.markdown(f'<div style="font-size:12px; font-weight:bold; color:#A2FF00; margin-bottom:6px;">{form_title}</div>', unsafe_allow_html=True)
                r_email = st.text_input("Email Address:", placeholder="example@nexa.com").strip()
                r_pwd = st.text_input("Choose Node Password:", type="password", placeholder="Enter your secure password")
                r_wallet = st.text_input("Solana Receiving Address:", placeholder="Solana Wallet Address").strip()
                
                btn_reg_txt = "Create Unified Node Profile ⚡" if lang=="English" else "创建全网统一账户 ⚡"
                if st.form_submit_button(btn_reg_txt):
                    if not r_email or not r_pwd or not r_wallet:
                        err_txt = "❌ All parameters (Email, Password, Wallet) are strictly mandatory!" if lang=="English" else "❌ 邮箱、密码与Solana钱包全为必填项！"
                        st.error(err_txt)
                    elif r_email in global_server["user_db"]:
                        err_dup = "❌ Email is already occupied. Please switch to Login." if lang=="English" else "❌ 该邮箱已被占用，请直接切换至登录。"
                        st.error(err_dup)
                    else:
                        inherited_nexa = st.session_state.app_earned
                        global_server["user_db"][r_email] = {
                            "password_hash": hashlib.sha256(r_pwd.encode()).hexdigest(),
                            "wallet": r_wallet,
                            "score": inherited_nexa,
                            "reg_time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                        }
                        st.session_state.current_user = r_email
                        suc_reg = "🎉 Registration complete! Your local NEXA data has successfully migrated to Cloud." if lang=="English" else "🎉 账户注册成功！本地 NEXA 数据已完美迁移同步。"
                        st.success(suc_reg)
                        time.sleep(0.5)
                        st.rerun()
        else:
            with st.form("login_form"):
                login_title = "🔑 Connect Node Endpoint Terminal" if lang=="English" else "🔑 登录 NexaEdge 算力账户"
                st.markdown(f'<div style="font-size:12px; font-weight:bold; color:#00e5ff; margin-bottom:6px;">{login_title}</div>', unsafe_allow_html=True)
                l_email = st.text_input("Account Email:").strip()
                l_pwd = st.text_input("Security Verification Password:", type="password")
                
                btn_l_txt = "Authenticate & Load Assets ⚡" if lang=="English" else "验证并载入云端档案 ⚡"
                if st.form_submit_button(btn_l_txt):
                    p_hash = hashlib.sha256(l_pwd.encode()).hexdigest()
                    if l_email in global_server["user_db"] and global_server["user_db"][l_email]["password_hash"] == p_hash:
                        st.session_state.current_user = l_email
                        st.session_state.app_earned = global_server["user_db"][l_email]["score"]
                        suc_l = "⚡ Authentication verified! Loaded your private balance ecosystem." if lang=="English" else "⚡ 鉴权成功！已成功加载您的个人专属 NEXA 资产底盘。"
                        st.success(suc_l)
                        time.sleep(0.5)
                        st.rerun()
                    else:
                        err_l = "❌ Invalid email combination or password mismatch!" if lang=="English" else "❌ 账号或密码输入有误，请重试！"
                        st.error(err_l)

    # =========================================================================
    # 🛡️ 🔍 PURE BACK-OFFICE HIDDEN PANEL (Now safely locked inside Tab 3 bottom)
    # =========================================================================
    st.markdown("<br><hr style='border:1px solid #1e272e; margin-top:20px;'>", unsafe_allow_html=True)
    expander_title = "⚙️ Core Infrastructure Port Lock (System Admins Only)"
    with st.expander(expander_title):
        st.markdown('<div style="font-size:12px; font-weight:bold; color:#f43f5e; margin-bottom:4px;">🔒 Encrypted Internal Ledger Audit Engine</div>', unsafe_allow_html=True)
        adm_key = st.text_input("Enter Root Master Secret Key to decrypt database view:", type="password", placeholder="Enter admin key here", key="adm_pwd_box")
        
        if adm_key == "nexaadmin":
            st.toast("🔓 Access Granted. Network Database Decrypted Successfully.", icon="🟢")
            c_a1, c_a2 = st.columns(2)
            with c_a1: st.markdown(f'<div class="mini-stat-card" style="border:1px solid #f43f5e;"><div class="mini-stat-title">TOTAL REGISTERED USERS</div><div class="mini-stat-value" style="color:#f43f5e;">{len(global_server["user_db"])} Nodes Profiles</div></div>', unsafe_allow_html=True)
            with c_a2: st.markdown(f'<div class="mini-stat-card" style="border:1px solid #A2FF00;"><div class="mini-stat-title">COMPUTE REALTIME DEVICES</div><div class="mini-stat-value" style="color:#A2FF00;">{len(global_server["active_device_set"])} Online</div></div>', unsafe_allow_html=True)
            
            st.markdown("<p style='font-size:11px; font-weight:bold; margin-top:10px; color:#A2FF00;'>📋 LIVE REGISTERED USERS ACCOUNT BALANCE AUDIT DIRECTORY:</p>", unsafe_allow_html=True)
            table_html = """
            <table class="admin-table">
                <tr><th>ID</th><th>User Registered Email</th><th>Solana Bound Wallet</th><th>NEXA Tokens Assets Owned</th><th>Activation Time (UTC)</th></tr>
            """
            for idx, (email, info) in enumerate(global_server["user_db"].items(), 1):
                table_html += f"<tr><td>{idx}</td><td>{email}</td><td style='font-family:monospace; color:#9ca3af;'>{info['wallet'][:12]}...{info['wallet'][-8:] if len(info['wallet'])>12 else ''}</td><td style='color:#A2FF00; font-weight:bold;'>{info['score']:,.2f} NEXA</td><td>{info['reg_time']}</td></tr>"
            table_html += "</table>"
            st.markdown(table_html, unsafe_allow_html=True)
        elif adm_key != "":
            st.error("❌ Master authentication failed. Data decrypt matrix access denied.")

# ==========================================
# 📊 MACRO NETWORKS METRICS SECTION
# ==========================================
st.markdown("<br>", unsafe_allow_html=True)
col_net1, col_net2 = st.columns(2)
with col_net1: st.markdown(f'<div class="mini-stat-card" style="border:1px dashed #A2FF00;"><div class="mini-stat-title">● NETWORK ACTIVE NODES</div><div class="mini-stat-value" style="color:#A2FF00;">{len(global_server["active_device_set"])} Devices</div></div>', unsafe_allow_html=True)
with col_net2: st.markdown(f'<div class="mini-stat-card" style="border:1px dashed #00e5ff;"><div class="mini-stat-title">👀 LIVE REAL VIEWERS</div><div class="mini-stat-value" style="color:#00e5ff;">{global_server["total_online_viewers"]} Online</div></div>', unsafe_allow_html=True)

st.markdown("<p style='text-align:center; color:#445; font-size: 10px; margin-top:12px;'>NexaEdge Network © 2026 | Powered by Solana DePIN Infrastructure</p>", unsafe_allow_html=True)

# ==================== 👑 HIGH-FREQUENCY DRIVE CORE ====================
if st.session_state.app_running:
    st.session_state.app_earned += 0.01
    st.session_state.session_seconds += 1
    st.session_state.total_energy_wh += (5.1 / 3600.0)
    
    if st.session_state.current_user:
        global_server["user_db"][st.session_state.current_user]["score"] = st.session_state.app_earned
    else:
        global_server["device_balances"][dev_id]["app_earned"] = st.session_state.app_earned
        
    st.session_state.last_tick_time = time.time()
    time.sleep(1.0)
    st.rerun()
