import streamlit as st
import os
import time
import random
import pandas as pd
import hashlib

# 1. Page Configuration
st.set_page_config(
    page_title="NexaEdge Network | Official Node Gateway",
    page_icon="🟢",
    layout="centered"
)

# =========================================================================
# 🔒 Global Server Database Mock (Persistent Ledger Simulation)
# =========================================================================
@st.cache_resource
def init_global_network_server():
    # Modified database schema to include display_name and username
    return {
        "active_device_set": set(),             
        "total_online_viewers": random.randint(102, 125), 
        "device_balances": {},                  
        "user_db": {                            # Keyed by 'username' for your requirement
            "nexa_admin": {
                "email": "admin@nexaedge.ai",
                "display_name": "管理员",
                "password_hash": hashlib.sha256("nexa2026".encode()).hexdigest(),
                "wallet": "GjvqAarpBirdGu2ahhKTrZ5sUcuPexGatMuGDmZLAb33",
                "score": 1479.0,
                "reg_time": "2026-05-18 14:22:05"
            }
        }
    }

global_server = init_global_network_server()

# --- 🔐 Hardware Device Fingerprint ---
if "device_fingerprint" not in st.session_state:
    ctx_headers = st.context.headers
    user_agent = ctx_headers.get("User-Agent", "Unknown-Device")
    remote_ip = ctx_headers.get("X-Forwarded-For", "127.0.0.1")
    raw_fingerprint = f"{user_agent}_{remote_ip}"
    st.session_state.device_fingerprint = hashlib.md5(raw_fingerprint.encode('utf-8')).hexdigest()[:12]

dev_id = st.session_state.device_fingerprint

# --- User Session Initialization ---
if "current_user" not in st.session_state:
    st.session_state.current_user = None  # Stores the English 'username' when logged in

# Initialize anonymous hardware balance
if dev_id not in global_server["device_balances"]:
    global_server["device_balances"][dev_id] = {
        "app_earned": 0.0,
        "total_energy_wh": 0.0,
        "session_seconds": 0
    }

# --- Sync Data Source ---
def sync_data_from_source():
    if st.session_state.current_user:
        username = st.session_state.current_user
        if 'app_earned' not in st.session_state or st.session_state.get('last_user') != username:
            st.session_state.app_earned = global_server["user_db"][username]["score"]
            st.session_state.total_energy_wh = global_server["device_balances"][dev_id]["total_energy_wh"]
            st.session_state.session_seconds = global_server["device_balances"][dev_id]["session_seconds"]
            st.session_state.last_user = username
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

if 'app_running' not in st.session_state: st.session_state.app_running = False
if 'chart_history' not in st.session_state: st.session_state.chart_history = [22.0, 25.0, 24.0, 28.0, 27.0, 31.0, 29.0, 33.0, 31.0, 35.0, 33.0, 36.8]
if 'target_time_index' not in st.session_state: st.session_state.target_time_index = 2 
if 'last_tick_time' not in st.session_state: st.session_state.last_tick_time = 0.0

# ==========================================
# 🟢 Hacker Cyberpunk CSS Injections
# ==========================================
st.markdown("""
    <style>
    .stApp { background-color: #0b0f12; }
    #MainMenu, footer, .styles_viewerBadge__FUChv, [data-testid="manage-app-button"] { display: none !important; }
    header, [data-testid="stHeader"] { background: transparent !important; border: none !important; height: 0 !important; display: none !important; }
    
    /* Tabs Customization */
    .stTabs [data-baseweb="tab-list"] { gap: 4px; background-color: transparent !important; justify-content: flex-start; border: none !important; overflow-x: auto; }
    .stTabs [data-baseweb="tab"] { background-color: #11171d !important; color: #bdc3c7 !important; border-radius: 8px 8px 0px 0px !important; border: 1px solid #1e272e !important; border-bottom: none !important; padding: 6px 12px !important; font-weight: 700 !important; font-size: 12px !important; white-space: nowrap; }
    .stTabs [aria-selected="true"] { color: #A2FF00 !important; background-color: #161c23 !important; border-top: 2px solid #A2FF00 !important; }
    
    /* Container & Cards */
    .app-container { background-color: #11171d; border: 1px solid #1e272e; border-radius: 20px; padding: 14px; margin: 0 auto; }
    .app-card { background-color: #161c23; border: 1px solid #252e38; border-radius: 14px; padding: 12px; margin-bottom: 10px; }
    .app-title { font-size: 11px; color: #88929b; font-weight: bold; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 4px; }
    .app-value { font-family: 'Inter', sans-serif; color: #ffffff; font-size: 22px; font-weight: 700; }
    
    .neon-green-text { color: #A2FF00 !important; }
    .neon-blue-text { color: #00e5ff !important; }
    
    /* Buttons & Forms */
    div.stButton > button:first-child { background-color: #A2FF00 !important; color: #0b0f12 !important; font-weight: 800 !important; font-size: 14px !important; width: 100% !important; border-radius: 12px !important; border: none !important; padding: 10px 4px !important; }
    div.stButton > button[key*="app_stop_btn"] { background-color: #0b0f12 !important; color: #ffffff !important; border: 1px solid #f43f5e !important; }
    div.stButton > button[key*="logout_btn"] { background-color: #343a40 !important; color: #ffc107 !important; width: auto !important; padding: 4px 10px !important; }
    
    [data-testid="stForm"] { background-color: #161c23 !important; border: 1px solid #252e38 !important; border-radius: 16px !important; padding: 15px !important; }
    .user-badge { background: #1e293b; padding: 8px 12px; border-radius: 10px; border-left: 3px solid #00e5ff; margin-bottom: 12px; font-size: 13px; color: #e2e8f0; }
    .mini-stat-card { text-align: center; background-color:#141d26; padding: 8px 4px; border-radius: 10px; min-height: 55px; }
    .mini-stat-title { font-size: 9px !important; color: #88929b; font-weight: bold; }
    .mini-stat-value { font-size: 13px !important; font-weight: bold; margin-top: 2px; }
    
    .admin-table { width: 100%; border-collapse: collapse; margin-top: 10px; font-size: 12px; }
    .admin-table th { background-color: #1f2937; color: #A2FF00; text-align: left; padding: 8px; border: 1px solid #374151; }
    .admin-table td { padding: 8px; border: 1px solid #374151; background-color: #111827; color: #cdfaee; }
    
    /* Simulating a chat/display room look */
    .chat-box { background-color: #11171d; border: 1px dashed #252e38; padding: 10px; border-radius: 8px; margin-top: 8px;}
    </style>
""", unsafe_allow_html=True)

if st.session_state.app_running:
    global_server["active_device_set"].add(st.session_state.session_id)
else:
    global_server["active_device_set"].discard(st.session_state.session_id)

# --- Background Time Engine Calculate ---
if st.session_state.app_running and st.session_state.last_tick_time > 0:
    current_unix = time.time()
    elapsed_gap = int(current_unix - st.session_state.last_tick_time)
    if elapsed_gap >= 1:
        st.session_state.session_seconds += elapsed_gap
        st.session_state.app_earned += elapsed_gap * 0.01
        st.session_state.total_energy_wh += 5.1 * (elapsed_gap / 3600.0)
        st.session_state.last_tick_time = current_unix
        
        if st.session_state.current_user:
            global_server["user_db"][st.session_state.current_user]["score"] = st.session_state.app_earned
        else:
            global_server["device_balances"][dev_id]["app_earned"] = st.session_state.app_earned
        global_server["device_balances"][dev_id]["total_energy_wh"] = st.session_state.total_energy_wh
        global_server["device_balances"][dev_id]["session_seconds"] = st.session_state.session_seconds

# --- Header ---
st.markdown('<h1 style="text-align:center; color:#A2FF00; font-size:32px; font-weight:800; margin-bottom:0px;">NexaEdge Network</h1>', unsafe_allow_html=True)
lang = st.selectbox("🌐 Language", ["English", "中文"], index=0, label_visibility="collapsed")

# --- Tabs Setup (Pure English Default) ---
tab1, tab2, tab3, tab4 = st.tabs([
    "🌐 Overview" if lang=="English" else "🌐 项目通识", 
    "📱 Dashboard" if lang=="English" else "📱 算力控制台", 
    "🔑 Auth Portal" if lang=="English" else "🔑 账户注册/登录",
    "🛡️ Admin Panel" if lang=="English" else "🛡️ 节点内网管理"
])

# ==========================================
# TAB 1: OVERVIEW
# ==========================================
with tab1:
    st.markdown('<p style="font-size: 14px; color: #A2FF00; font-weight:bold; text-align: center; margin-top: 5px;">Transforming idle smartphones into high-purity distributed computing power for the AI Era.</p>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1: st.metric(label="Network Fee", value="20%", delta="Revenue Model")
    with c2: st.metric(label="Smart Risk Lock", value="39°C", delta="Thermal Safeguard", delta_color="inverse")
    with c3: st.metric(label="Settlement Base", value="Solana SPL", delta="Ultra Low Gas")

# ==========================================
# TAB 2: DASHBOARD
# ==========================================
with tab2:
    st.markdown('<div class="app-container">', unsafe_allow_html=True)
    
    # 📌 Requirement Met: ONLY show English 'username' inside the status panel / chat window view
    if st.session_state.current_user:
        st.markdown(f'<div class="user-badge">🟢 Node Session Locked to Username: <b class="neon-green-text">{st.session_state.current_user}</b></div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="user-badge" style="border-left-color:#ffb300; color:#ffb300;">⚠️ Guest Mode Running (Data saved locally. Register/Login to secure rewards on Cloud).</div>', unsafe_allow_html=True)

    TIME_OPTIONS = ["15 Mins", "30 Mins", "1 Hour", "2 Hours", "4 Hours", "8 Hours", "12 Hours", "24 Hours"]
    selected_time = st.selectbox("Configure target runtime session:", TIME_OPTIONS, index=st.session_state.target_time_index)
    st.session_state.target_time_index = TIME_OPTIONS.index(selected_time)

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
    
    st.markdown(f'<div class="app-card" style="margin-top: -5px;"><div class="temp-section" style="display:flex; justify-content:space-between; background:#11171d; padding:6px 12px; border-radius:10px;"><span class="app-value" style="font-size:16px;">🌡️ {current_temp:.1f}°C</span><span style="background-color:#1e272e; color:#A2FF00; font-size:11px; font-weight:bold; padding:2px 8px; border-radius:5px;">SAFE</span></div></div>', unsafe_allow_html=True)

    # Power Meter Card
    st.markdown(f"""
    <div class="app-card">
        <div class="app-title">🔌 HARDWARE POWER METER (NODE_ID: {dev_id})</div>
        <div style="display:grid; grid-template-columns: 1fr 1fr; gap:6px;">
            <div style="background:#11171d; padding:6px; border-radius:8px;">
                <div style="font-size:9px; color:#88929b; font-weight:bold;">INPUT POWER:</div>
                <div class="app-value neon-blue-text" style="font-size:14px; font-family:monospace;">{current_power:.2f} W</div>
            </div>
            <div style="background:#11171d; padding:6px; border-radius:8px;">
                <div style="font-size:9px; color:#88929b; font-weight:bold;">CUMULATIVE ENERGY:</div>
                <div class="app-value" style="font-size:14px; font-family:monospace; color:#ffffff;">{st.session_state.total_energy_wh:.4f} Wh</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Earnings Card
    st.markdown(f"""
    <div class="app-card">
        <div style="display:flex; justify-content:space-between;">
            <div><div style="font-size:10px; color:#88929b; font-weight:bold;">DURATION:</div><div class="app-value" style="font-size:18px;">{time_str}</div></div>
            <div style="text-align:right;"><div style="font-size:10px; color:#88929b; font-weight:bold;">REALTIME MINTED:</div><div class="app-value neon-green-text" style="font-size:18px;">+{st.session_state.app_earned:,.2f} NEXA</div></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Simulated Chat/Display Window Requirement (Only showing username)
    active_user_display = st.session_state.current_user if st.session_state.current_user else f"Guest_{dev_id}"
    st.markdown(f"""
    <div class="chat-box">
        <div style="font-size:10px; color:#88929b; font-weight:bold; margin-bottom:4px;">💬 LIVE LOG STREAM (CHAT WINDOW VIEW)</div>
        <div style="font-family:monospace; font-size:12px; color:#ffffff;">
            [System] <span class='neon-blue-text'>@{active_user_display}</span> is actively broadcasting terminal telemetry signals.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if not st.session_state.app_running:
        if st.button("ACTIVATE EDGE COMPUTE NODE", key="app_start_btn"):
            st.session_state.app_running = True
            st.session_state.last_tick_time = time.time()
            st.rerun()
    else:
        if st.button("PAUSE COMPUTE SESSION", key="app_stop_btn"):
            st.session_state.app_running = False
            st.session_state.last_tick_time = 0.0
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# TAB 3: AUTH PORTAL (Modified Register & Login)
# ==========================================
with tab3:
    if st.session_state.current_user:
        st.markdown('<div class="app-card" style="text-align:center;">', unsafe_allow_html=True)
        st.success(f"🎉 Session Authenticated! Active Username: {st.session_state.current_user}")
        st.markdown(f"**Total Network Earnings:** <span class='neon-green-text' style='font-size:24px; font-weight:bold;'>{st.session_state.app_earned:,.2f} NEXA</span>", unsafe_allow_html=True)
        
        if st.button("Log out from Current Account", key="logout_btn"):
            st.session_state.current_user = None
            st.session_state.app_running = False
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        auth_mode = st.radio("Auth Selection", ["Register New Account", "Login Existing Account"], horizontal=True, label_visibility="collapsed")
        
        if auth_mode == "Register New Account":
            with st.form("register_form"):
                st.markdown('<div style="font-size:14px; font-weight:bold; color:#A2FF00; margin-bottom:8px;">🚀 Create NexaEdge Unified Node Identity</div>', unsafe_allow_html=True)
                
                # 📌 Requirement Met: Must have Email, Name, English Username, and Password for registration
                reg_email = st.text_input("Email Address:", placeholder="example@domain.com").strip()
                reg_display_name = st.text_input("User Name (Display Name / 姓名):", placeholder="e.g. 张三").strip()
                reg_username = st.text_input("English Username (Unique ID):", placeholder="e.g. jack_nexa12").strip()
                reg_pwd = st.text_input("Password:", type="password", placeholder="Enter secure password")
                reg_wallet = st.text_input("Solana Reward Wallet Address (Optional):", placeholder="Solana Wallet Address").strip()
                
                submit_reg = st.form_submit_button("Create Identity & Sync Rewards ⚡")
                if submit_reg:
                    if not reg_email or not reg_display_name or not reg_username or not reg_pwd:
                        st.error("❌ Registration Failed: Email, User Name, English Username, and Password are all required!")
                    elif reg_username in global_server["user_db"]:
                        st.error("❌ Username already taken. Please pick another unique English username.")
                    else:
                        inherited_score = st.session_state.app_earned
                        pwd_hash = hashlib.sha256(reg_pwd.encode()).hexdigest()
                        
                        # Store in simulated DB
                        global_server["user_db"][reg_username] = {
                            "email": reg_email,
                            "display_name": reg_display_name,
                            "password_hash": pwd_hash,
                            "wallet": reg_wallet if reg_wallet else f"Anon_{hashlib.md5(reg_username.encode()).hexdigest()[:8]}",
                            "score": inherited_score,
                            "reg_time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                        }
                        
                        st.session_state.current_user = reg_username
                        st.success("🎉 Registration successful! Local node data securely migrated to your Cloud profile.")
                        time.sleep(0.6)
                        st.rerun()
                        
        else:
            with st.form("login_form"):
                st.markdown('<div style="font-size:14px; font-weight:bold; color:#00e5ff; margin-bottom:8px;">🔑 Connect Node Terminal Endpoint</div>', unsafe_allow_html=True)
                
                # 📌 Requirement Met: Login only requires English Username and Password
                login_username = st.text_input("English Username:").strip()
                login_pwd = st.text_input("Password:", type="password")
                
                submit_login = st.form_submit_button("Verify & Bind Terminal")
                if submit_login:
                    pwd_hash = hashlib.sha256(login_pwd.encode()).hexdigest()
                    if login_username in global_server["user_db"] and global_server["user_db"][login_username]["password_hash"] == pwd_hash:
                        st.session_state.current_user = login_username
                        st.session_state.app_earned = global_server["user_db"][login_username]["score"]
                        st.success("⚡ Handshake validated! Your persistent ledger profile is now active.")
                        time.sleep(0.6)
                        st.rerun()
                    else:
                        st.error("❌ Authentication Denied: Invalid Username or Password.")

# ==========================================
# TAB 4: ADMIN PANEL
# ==========================================
with tab4:
    st.markdown('<div style="font-size:14px; font-weight:bold; color:#f43f5e; margin-bottom:8px;">🔒 Secure Admin Network Access</div>', unsafe_allow_html=True)
    admin_password = st.text_input("Enter Admin Secret Key:", type="password", placeholder="Core Secret Key")
    
    if admin_password == "nexaadmin":
        st.toast("🟢 Access Granted: Database Decrypted", icon="🔓")
        
        total_registered = len(global_server["user_db"])
        active_nodes_count = len(global_server["active_device_set"])
        live_viewers_count = global_server["total_online_viewers"]
        
        c_adm1, c_adm2, c_adm3 = st.columns(3)
        with c_adm1:
            st.markdown(f'<div class="mini-stat-card" style="border:1px solid #f43f5e;"><div class="mini-stat-title">Total Users</div><div class="mini-stat-value" style="color:#f43f5e; font-size:14px;">{total_registered} Registered</div></div>', unsafe_allow_html=True)
        with c_adm2:
            st.markdown(f'<div class="mini-stat-card" style="border:1px solid #A2FF00;"><div class="mini-stat-title">Active Nodes</div><div class="mini-stat-value" style="color:#A2FF00; font-size:14px;">{active_nodes_count} Computing</div></div>', unsafe_allow_html=True)
        with c_adm3:
            st.markdown(f'<div class="mini-stat-card" style="border:1px solid #00e5ff;"><div class="mini-stat-title">Live Viewers</div><div class="mini-stat-value" style="color:#00e5ff; font-size:14px;">{live_viewers_count} Online</div></div>', unsafe_allow_html=True)
            
        st.markdown("<p style='font-size:13px; font-weight:bold; margin-top:15px; color:#ffffff;'>📋 Live Network Registration Audit Matrix:</p>", unsafe_allow_html=True)
        
        table_html = """
        <table class="admin-table">
            <tr>
                <th>No.</th>
                <th>English Username</th>
                <th>Display Name</th>
                <th>Email</th>
                <th>Solana Address</th>
                <th>Balance Ledger</th>
            </tr>
        """
        for idx, (username, info) in enumerate(global_server["user_db"].items(), 1):
            table_html += f"""
            <tr>
                <td>{idx}</td>
                <td style='color:#00e5ff; font-weight:bold;'>{username}</td>
                <td>{info['display_name']}</td>
                <td>{info['email']}</td>
                <td style='font-family:monospace; color:#9ca3af;'>{info['wallet'][:8]}...</td>
                <td style='color:#A2FF00; font-weight:bold;'>{info['score']:,.2f} NEXA</td>
            </tr>
            """
        table_html += "</table>"
        st.markdown(table_html, unsafe_allow_html=True)
        
    elif admin_password != "":
        st.error("❌ Access Denied: Incorrect core key.")
    else:
        st.info("💡 Input administrative key `nexaadmin` to unlock global user record tracking matrices.")

# --- Bottom Network Matrix Status ---
st.markdown("<br>", unsafe_allow_html=True)
col_net1, col_net2 = st.columns(2)
with col_net1: 
    st.markdown(f'<div class="mini-stat-card" style="border:1px dashed #A2FF00;"><div class="mini-stat-title">● NETWORK ACTIVE NODES</div><div class="mini-stat-value" style="color:#A2FF00;">{len(global_server["active_device_set"])} Devices</div></div>', unsafe_allow_html=True)
with col_net2: 
    st.markdown(f'<div class="mini-stat-card" style="border:1px dashed #00e5ff;"><div class="mini-stat-title">👀 LIVE REAL VIEWERS</div><div class="mini-stat-value" style="color:#00e5ff;">{global_server["total_online_viewers"]} Online</div></div>', unsafe_allow_html=True)

# Main Loop Trigger for Realtime Refresh
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
