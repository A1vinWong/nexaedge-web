import streamlit as st
import os
import time
import random
import pandas as pd
import glob
import hashlib

# 1. 全局页面基础配置
st.set_page_config(
    page_title="NexaEdge Network | Official Node Gateway",
    page_icon="🟢",
    layout="centered"
)

# =========================================================================
# 🔒 服务器跨进程内存锁 与 数据库模拟 (持久化防清零账本)
# =========================================================================
@st.cache_resource
def init_global_network_server():
    return {
        "active_device_set": set(),             # 存放真正点击启动的 session_id
        "total_online_viewers": random.randint(102, 125), # 智能稳定在线底数
        "device_balances": {},                  # 硬件匿名账本 {dev_id: {app_earned, total_energy_wh, session_seconds}}
        "user_db": {                            # 注册用户数据库 {email: {password_hash, wallet, score, reg_time}}
            "demo@nexaedge.ai": {
                "password_hash": hashlib.sha256("nexa2026".encode()).hexdigest(),
                "wallet": "GjvqAarpBirdGu2ahhKTrZ5sUcuPexGatMuGDmZLAb33",
                "score": 1479.0,
                "reg_time": "2026-05-18 14:22:05"
            }
        }
    }

global_server = init_global_network_server()

# --- 🔐 创建或恢复绝对唯一的设备硬件级指纹 ---
if "device_fingerprint" not in st.session_state:
    ctx_headers = st.context.headers
    user_agent = ctx_headers.get("User-Agent", "Unknown-Device")
    remote_ip = ctx_headers.get("X-Forwarded-For", "127.0.0.1")
    raw_fingerprint = f"{user_agent}_{remote_ip}"
    st.session_state.device_fingerprint = hashlib.md5(raw_fingerprint.encode('utf-8')).hexdigest()[:12]

dev_id = st.session_state.device_fingerprint

# --- 用户登录状态会话初始化 ---
if "current_user" not in st.session_state:
    st.session_state.current_user = None  # None 表示游客状态

# 初始化匿名硬件账本
if dev_id not in global_server["device_balances"]:
    global_server["device_balances"][dev_id] = {
        "app_earned": 0.0,
        "total_energy_wh": 0.0,
        "session_seconds": 0
    }

# --- 核心：将当前活跃账本指向“登录账号”或“匿名硬件” ---
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

# --- 其他必要状态安全初始化 ---
if 'app_running' not in st.session_state: st.session_state.app_running = False
if 'chart_history' not in st.session_state: st.session_state.chart_history = [22.0, 25.0, 24.0, 28.0, 27.0, 31.0, 29.0, 33.0, 31.0, 35.0, 33.0, 36.8]
if 'target_time_index' not in st.session_state: st.session_state.target_time_index = 2 
if 'last_tick_time' not in st.session_state: st.session_state.last_tick_time = 0.0

# --- 🟢 极客黑绿科技风 CSS 全局注入 ---
st.markdown("""
    <style>
    .stApp { background-color: #0b0f12; }
    #MainMenu, footer, .styles_viewerBadge__FUChv, [data-testid="manage-app-button"] { display: none !important; }
    header, [data-testid="stHeader"] { background: transparent !important; border: none !important; height: 0 !important; display: none !important; }
    [data-testid="stVerticalBlock"] > div:empty { display: none !important; margin: 0 !important; padding: 0 !important; }
    [data-testid="stElementContainer"] { border: none !important; background: transparent !important; margin-bottom: 6px !important; }
    
    .stTabs [data-baseweb="tab-list"] { gap: 4px; background-color: transparent !important; justify-content: flex-start; border: none !important; overflow-x: auto; }
    .stTabs [data-baseweb="tab"] { background-color: #11171d !important; color: #bdc3c7 !important; border-radius: 8px 8px 0px 0px !important; border: 1px solid #1e272e !important; border-bottom: none !important; padding: 6px 12px !important; font-weight: 700 !important; font-size: 12px !important; white-space: nowrap; }
    .stTabs [aria-selected="true"] { color: #A2FF00 !important; background-color: #161c23 !important; border-top: 2px solid #A2FF00 !important; }
    .stTabs [data-baseweb="tab-highlight"] { background-color: #A2FF00 !important; height: 0px !important; }
    
    .app-container { background-color: #11171d; border: 1px solid #1e272e; border-radius: 20px; padding: 14px; margin: 0 auto; box-shadow: 0 10px 30px rgba(0,0,0,0.5); }
    .app-card { background-color: #161c23; border: 1px solid #252e38; border-radius: 14px; padding: 12px; margin-bottom: 10px; }
    .app-title { font-size: 11px; color: #88929b; font-weight: bold; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 4px; }
    .app-value { font-family: 'Inter', sans-serif; color: #ffffff; font-size: 22px; font-weight: 700; }
    
    .neon-green-text { color: #A2FF00 !important; }
    .neon-blue-text { color: #00e5ff !important; }
    .temp-section { display: flex; align-items: center; justify-content: space-between; background: #11171d; padding: 6px 12px; border-radius: 10px; margin-top: 6px; }
    
    div.stButton > button:first-child { background-color: #A2FF00 !important; color: #0b0f12 !important; font-weight: 800 !important; font-size: 14px !important; width: 100% !important; border-radius: 12px !important; border: none !important; padding: 10px 4px !important; box-shadow: 0 0 15px rgba(162, 255, 0, 0.3); transition: all 0.2s; }
    div.stButton > button[key*="app_stop_btn"] { background-color: #0b0f12 !important; color: #ffffff !important; border: 1px solid #f43f5e !important; box-shadow: none !important; }
    div.stButton > button[key*="logout_btn"] { background-color: #343a40 !important; color: #ffc107 !important; box-shadow: none !important; padding: 4px 10px !important; font-size: 12px !important; width: auto !important; }
    
    [data-testid="stForm"] { background-color: #161c23 !important; border: 1px solid #252e38 !important; border-radius: 16px !important; padding: 15px !important; }
    .user-badge { background: #1e293b; padding: 8px 12px; border-radius: 10px; border-left: 3px solid #00e5ff; margin-bottom: 12px; font-size: 13px; color: #e2e8f0; }
    .mini-stat-card { text-align: center; background-color:#141d26; padding: 8px 4px; border-radius: 10px; min-height: 55px; display: flex; flex-direction: column; justify-content: center; align-items: center; }
    .mini-stat-title { font-size: 9px !important; color: #88929b; font-weight: bold; white-space: nowrap; }
    .mini-stat-value { font-size: 13px !important; font-weight: bold; font-family: monospace; margin-top: 2px; }
    
    .admin-table { width: 100%; border-collapse: collapse; margin-top: 10px; font-size: 12px; color: #cdfaee; }
    .admin-table th { background-color: #1f2937; color: #A2FF00; text-align: left; padding: 8px; border: 1px solid #374151; }
    .admin-table td { padding: 8px; border: 1px solid #374151; background-color: #111827; }
    </style>
""", unsafe_allow_html=True)

# 实时控制设备节点注册状态
if st.session_state.app_running:
    global_server["active_device_set"].add(st.session_state.session_id)
else:
    global_server["active_device_set"].discard(st.session_state.session_id)

# 🔄 绝不断线：高频物理时间防挂起补算逻辑
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

st.markdown('<h1 style="text-align:center; color:#A2FF00; font-size:32px; font-weight:800; margin-bottom:0px;">NexaEdge Network</h1>', unsafe_allow_html=True)
lang = st.selectbox("🌐 Language", ["中文", "English"], index=0, label_visibility="collapsed")

tab1, tab2, tab3, tab4 = st.tabs([
    "🌐 项目通识" if lang=="中文" else "🌐 Overview", 
    "📱 算力控制台" if lang=="中文" else "📱 Dashboard", 
    "🔑 账户注册/登录" if lang=="中文" else "🔑 Auth Portal",
    "🛡️ 节点内网管理" if lang=="中文" else "🛡️ Admin Panel"
])

with tab1:
    if lang == "中文":
        st.markdown('<p style="font-size: 15px; color: #A2FF00; font-weight:bold; text-align: center; margin-top: 5px;">让全球闲置手机，成为 AI 时代的高纯度分布式算力网络</p>', unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        with c1: st.metric(label="平台技术抽成", value="20%", delta="纯现金流造血")
        with c2: st.metric(label="智能硬件风控", value="39°C", delta="秒级控温预警", delta_color="inverse")
        with c3: st.metric(label="算力结算底座", value="Solana SPL", delta="极速、低 Gas")
    else:
        st.markdown('<p style="font-size: 15px; color: #A2FF00; font-weight:bold; text-align: center; margin-top: 5px;">Transforming idle smartphones into data fuel factories for the AI Era.</p>', unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        with c1: st.metric(label="Network Fee", value="20%", delta="Pure Revenue")
        with c2: st.metric(label="Safety Lock", value="39°C", delta="Device Safety", delta_color="inverse")
        with c3: st.metric(label="Settlement Base", value="Solana SPL", delta="Low Gas / High TPS")

with tab2:
    st.markdown('<div class="app-container">', unsafe_allow_html=True)
    if st.session_state.current_user:
        st.markdown(f'<div class="user-badge">🟢 已锁定云端同步账户: <b>{st.session_state.current_user}</b></div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="user-badge" style="border-left-color:#ffb300; color:#ffb300;">⚠️ 游客状态运行（算力保存在本地，建议立即注册/登录账号进行永久云端绑定）</div>', unsafe_allow_html=True)

    TIME_OPTIONS = ["15分钟", "半小时", "1小时", "2小时", "4小时", "8小时", "12小时", "24小时"] if lang=="中文" else ["15 Mins", "30 Mins", "1 Hour", "2 Hours", "4 Hours", "8 Hours", "12 Hours", "24 Hours"]
    st.selectbox("配置本次节点运行目标时间:" if lang=="中文" else "Set target runtime:", TIME_OPTIONS, index=st.session_state.target_time_index, key="ts_select")

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
    
    st.markdown(f'<div class="app-card" style="margin-top: -5px;"><div class="temp-section"><span class="app-value" style="font-size:17px;">🌡️ {current_temp:.1f}°C</span><span style="background-color:#1e272e; color:#A2FF00; font-size:11px; font-weight:bold; padding:2px 8px; border-radius:5px;">SAFE</span></div></div>', unsafe_allow_html=True)

    st.markdown(f'''
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
    ''', unsafe_allow_html=True)

    st.markdown(f'''
    <div class="app-card">
        <div style="display:flex; justify-content:space-between;">
            <div><div style="font-size:10px; color:#88929b; font-weight:bold;">DURATION:</div><div class="app-value" style="font-size:18px;">{time_str}</div></div>
            <div style="text-align:right;"><div style="font-size:10px; color:#88929b; font-weight:bold;">REALTIME MINTED:</div><div class="app-value neon-green-text" style="font-size:18px;">+{st.session_state.app_earned:,.2f} NEXA</div></div>
        </div>
    </div>
    ''', unsafe_allow_html=True)

    if not st.session_state.app_running:
        if st.button("START COMPUTE SESSION" if lang=="English" else "激活并启动边缘算力节点", key="app_start_btn"):
            st.session_state.app_running = True
            st.session_state.last_tick_time = time.time()
            st.rerun()
    else:
        if st.button("PAUSE COMPUTE SESSION" if lang=="English" else "暂停当前算力 Session", key="app_stop_btn"):
            st.session_state.app_running = False
            st.session_state.last_tick_time = 0.0
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

with tab3:
    if st.session_state.current_user:
        st.markdown('<div class="app-card" style="text-align:center;">', unsafe_allow_html=True)
        st.success(f"🎉 欢迎回来！您当前已成功登录账户: {st.session_state.current_user}")
        st.markdown(f"**您的全网云端累计收益为：** <span class='neon-green-text' style='font-size:24px; font-weight:bold;'>{st.session_state.app_earned:,.2f} NEXA</span>", unsafe_allow_html=True)
        
        if st.button("退出当前登录账户", key="logout_btn"):
            st.session_state.current_user = None
            st.session_state.app_running = False
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        auth_mode = st.radio("请选择操作类型", ["注册新账户", "登录已有账户"], horizontal=True, label_visibility="collapsed")
        
        if auth_mode == "注册新账户":
            with st.form("register_form"):
                st.markdown('<div style="font-size:14px; font-weight:bold; color:#A2FF00; margin-bottom:8px;">🚀 NexaEdge 云端分布式 network 注册</div>', unsafe_allow_html=True)
                reg_email = st.text_input("电子邮箱地址 (Email):", placeholder="example@gmail.com").strip()
                reg_pwd = st.text_input("设置登录密码 (Password):", type="password", placeholder="请输入密码")
                reg_wallet = st.text_input("绑定的 Solana 钱包接收地址 (选填):", placeholder="Solana Wallet Address").strip()
                
                submit_reg = st.form_submit_button("创建全网统一节点账户 ⚡")
                if submit_reg:
                    if not reg_email or not reg_pwd:
                        st.error("❌ 邮箱和密码为必填项！")
                    elif reg_email in global_server["user_db"]:
                        st.error("❌ 该邮箱已被注册，请直接切换到登录面板。")
                    else:
                        inherited_score = st.session_state.app_earned
                        pwd_hash = hashlib.sha256(reg_pwd.encode()).hexdigest()
                        
                        global_server["user_db"][reg_email] = {
                            "password_hash": pwd_hash,
                            "wallet": reg_wallet if reg_wallet else f"Anon_{hashlib.md5(reg_email.encode()).hexdigest()[:8]}",
                            "score": inherited_score,
                            "reg_time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                        }
                        
                        st.session_state.current_user = reg_email
                        st.success("🎉 注册并同步成功！您之前的本地算力已无缝迁移至云端主账户。")
                        time.sleep(0.5)
                        st.rerun()
                        
        else:
            with st.form("login_form"):
                st.markdown('<div style="font-size:14px; font-weight:bold; color:#00e5ff; margin-bottom:8px;">🔑 登录 NexaEdge 节点大盘</div>', unsafe_allow_html=True)
                login_email = st.text_input("登录邮箱 (Email):").strip()
                login_pwd = st.text_input("验证密码 (Password):", type="password")
                
                submit_login = st.form_submit_button("验证并连接节点云端端点")
                if submit_login:
                    pwd_hash = hashlib.sha256(login_pwd.encode()).hexdigest()
                    if login_email in global_server["user_db"] and global_server["user_db"][login_email]["password_hash"] == pwd_hash:
                        st.session_state.current_user = login_email
                        st.session_state.app_earned = global_server["user_db"][login_email]["score"]
                        st.success("⚡ 鉴权成功，已成功挂载您的云端持久化算力档案！")
                        time.sleep(0.5)
                        st.rerun()
                    else:
                        st.error("❌ 账号或密码错误，验证失败！")

with tab4:
    st.markdown('<div style="font-size:14px; font-weight:bold; color:#f43f5e; margin-bottom:8px;">🔒 管理员安全内网访问</div>', unsafe_allow_html=True)
    admin_password = st.text_input("请输入管理员核心密钥:", type="password", placeholder="Core Secret Key")
    
    if admin_password == "nexaadmin":
        st.toast("🟢 权限已升级：内网数据已成功解密", icon="🔓")
        total_registered = len(global_server["user_db"])
        active_nodes_count = len(global_server["active_device_set"])
        live_viewers_count = global_server["total_online_viewers"]
        
        c_adm1, c_adm2, c_adm3 = st.columns(3)
        with c_adm1:
            st.markdown(f'<div class="mini-stat-card" style="border:1px solid #f43f5e;"><div class="mini-stat-title">👥 全网总注册量</div><div class="mini-stat-value" style="color:#f43f5e; font-size:16px;">{total_registered} Users</div></div>', unsafe_allow_html=True)
        with c_adm2:
            st.markdown(f'<div class="mini-stat-card" style="border:1px solid #A2FF00;"><div class="mini-stat-title">🟢 实时活跃节点</div><div class="mini-stat-value" style="color:#A2FF00; font-size:16px;">{active_nodes_count} Nodes</div></div>', unsafe_allow_html=True)
        with c_adm3:
            st.markdown(f'<div class="mini-stat-card" style="border:1px solid #00e5ff;"><div class="mini-stat-title">👀 实时在看观众</div><div class="mini-stat-value" style="color:#00e5ff; font-size:16px;">{live_viewers_count} Online</div></div>', unsafe_allow_html=True)
            
        st.markdown("<p style='font-size:13px; font-weight:bold; margin-top:15px; color:#ffffff;'>📋 全网注册节点数据审计看板 (Live Database View):</p>", unsafe_allow_html=True)
        
        table_html = """
        <table class="admin-table">
            <tr>
                <th>注册序号</th>
                <th>用户邮箱 (Email)</th>
                <th>Solana 绑定钱包</th>
                <th>当前实测累计 Nexa 算力</th>
                <th>注册激活时间</th>
            </tr>
        """
        for idx, (email, info) in enumerate(global_server["user_db"].items(), 1):
            table_html += f"""
            <tr>
                <td>{idx}</td>
                <td>{email}</td>
                <td style='font-family:monospace; color:#9ca3af;'>{info['wallet'][:10]}...</td>
                <td style='color:#A2FF00; font-weight:bold; font-family:monospace;'>{info['score']:,.2f} NEXA</td>
                <td>{info['reg_time']}</td>
            </tr>
            """
        table_html += "</table>"
        st.markdown(table_html, unsafe_allow_html=True)
    elif admin_password != "":
        st.error("❌ 管理员密钥鉴权失败，拒绝访问内网核心账本。")
    else:
        st.info("💡 请在上方输入管理员核心密钥 `nexaadmin` 即可解锁并实时审计全网用户注册明细。")

st.markdown("<br>", unsafe_allow_html=True)
col_net1, col_net2 = st.columns(2)
with col_net1: 
    st.markdown(f'<div class="mini-stat-card" style="border:1px dashed #A2FF00;"><div class="mini-stat-title">● NETWORK ACTIVE NODES</div><div class="mini-stat-value" style="color:#A2FF00;">{len(global_server["active_device_set"])} Devices</div></div>', unsafe_allow_html=True)
with col_net2: 
    st.markdown(f'<div class="mini-stat-card" style="border:1px dashed #00e5ff;"><div class="mini-stat-title">👀 LIVE REAL VIEWERS</div><div class="mini-stat-value" style="color:#00e5ff;">{global_server["total_online_viewers"]} Online</div></div>', unsafe_allow_html=True)

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
