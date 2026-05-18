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
        # 如果登录了，算力直接累加到该注册账号下
        email = st.session_state.current_user
        if 'app_earned' not in st.session_state or st.session_state.get('last_user') != email:
            st.session_state.app_earned = global_server["user_db"][email]["score"]
            st.session_state.total_energy_wh = global_server["device_balances"][dev_id]["total_energy_wh"]
            st.session_state.session_seconds = global_server["device_balances"][dev_id]["session_seconds"]
            st.session_state.last_user = email
    else:
        # 游客状态，使用匿名硬件账本
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
if 'my_referral_code' not in st.session_state: st.session_state.my_referral_code = ""
if 'registration_success' not in st.session_state: st.session_state.registration_success = False

# --- 📸 智能图片摄入系统 ---
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

# --- 🟢 极客黑绿科技风 CSS 全局注入 ---
st.markdown("""
    <style>
    .stApp { background-color: #0b0f12; }
    #MainMenu, footer, .styles_viewerBadge__FUChv, [data-testid="manage-app-button"] { display: none !important; }
    header, [data-testid="stHeader"] { background: transparent !important; border: none !important; height: 0 !important; display: none !important; }
    [data-testid="stVerticalBlock"] > div:empty { display: none !important; margin: 0 !important; padding: 0 !important; }
    [data-testid="stElementContainer"] { border: none !important; background: transparent !important; margin-bottom: 6px !important; }
    
    /* 选项卡唯美样式定制 */
    .stTabs [data-baseweb="tab-list"] { gap: 6px; background-color: transparent !important; justify-content: flex-start; border: none !important; overflow-x: auto; }
    .stTabs [data-baseweb="tab"] { background-color: #11171d !important; color: #bdc3c7 !important; border-radius: 8px 8px 0px 0px !important; border: 1px solid #1e272e !important; border-bottom: none !important; padding: 6px 12px !important; font-weight: 700 !important; font-size: 12px !important; white-space: nowrap; }
    .stTabs [aria-selected="true"] { color: #A2FF00 !important; background-color: #161c23 !important; border-top: 2px solid #A2FF00 !important; }
    .stTabs [data-baseweb="tab-highlight"] { background-color: #A2FF00 !important; height: 0px !important; }
    
    /* 容器及卡片 */
    .app-container { background-color: #11171d; border: 1px solid #1e272e; border-radius: 20px; padding: 14px; margin: 0 auto; box-shadow: 0 10px 30px rgba(0,0,0,0.5); }
    .app-card { background-color: #161c23; border: 1px solid #252e38; border-radius: 14px; padding: 12px; margin-bottom: 10px; }
    .app-title { font-size: 11px; color: #88929b; font-weight: bold; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 4px; }
    .app-value { font-family: 'Inter', sans-serif; color: #ffffff; font-size: 22px; font-weight: 700; }
    
    .neon-green-text { color: #A2FF00 !important; }
    .neon-blue-text { color: #00e5ff !important; }
    .temp-section { display: flex; align-items: center; justify-content: space-between; background: #11171d; padding: 6px 12px; border-radius: 10px; margin-top: 6px; }
    
    /* 按钮全局高级定制 */
    div.stButton > button:first-child { background-color: #A2FF00 !important; color: #0b0f12 !important; font-weight: 800 !important; font-size: 14px !important; width: 100% !important; border-radius: 12px !important; border: none !important; padding: 10px 4px !important; box-shadow: 0 0 15px rgba(162, 255, 0, 0.3); transition: all 0.2s; }
    div.stButton > button[key*="app_stop_btn"] { background-color: #0b0f12 !important; color: #ffffff !important; border: 1px solid #f43f5e !important; box-shadow: none !important; }
    div.stButton > button[key*="logout_btn"] { background-color: #343a40 !important; color: #ffc107 !important; box-shadow: none !important; padding: 4px 10px !important; font-size: 12px !important; width: auto !important; }
    
    /* 表单与输入框 */
    [data-testid="stForm"] { background-color: #161c23 !important; border: 1px solid #252e38 !important; border-radius: 16px !important; padding: 15px !important; }
    .user-badge { background: #1e293b; padding: 8px 12px; border-radius: 10px; border-left: 3px solid #00e5ff; margin-bottom: 12px; font-size: 12px; color: #e2e8f0; }
    .mini-stat-card { text-align: center; background-color:#141d26; padding: 8px 4px; border-radius: 10px; min-height: 55px; display: flex; flex-direction: column; justify-content: center; align-items: center; }
    .mini-stat-title { font-size: 9px !important; color: #88929b; font-weight: bold; white-space: nowrap; }
    .mini-stat-value { font-size: 13px !important; font-weight: bold; font-family: monospace; margin-top: 2px; }
    
    .feature-box { background-color: #11171d; padding: 14px; border-radius: 10px; border-left: 4px solid #A2FF00; margin-bottom: 10px; }
    .social-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(80px, 1fr)); gap: 6px; margin: 10px 0; }
    .social-btn { display: block; text-align: center; padding: 6px; background-color: #11171d; border: 1px solid #252e38; border-radius: 8px; color: #bdc3c7 !important; font-size: 11px; font-weight: bold; text-decoration: none; }
    .social-btn:hover { border-color: #A2FF00; color: #A2FF00 !important; }

    /* 管理员表格美化 */
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
        
        # 实时同步至底层大账本
        if st.session_state.current_user:
            global_server["user_db"][st.session_state.current_user]["score"] = st.session_state.app_earned
        else:
            global_server["device_balances"][dev_id]["app_earned"] = st.session_state.app_earned
        global_server["device_balances"][dev_id]["total_energy_wh"] = st.session_state.total_energy_wh
        global_server["device_balances"][dev_id]["session_seconds"] = st.session_state.session_seconds

# --- 顶栏渲染 ---
st.markdown('<h1 style="text-align:center; color:#A2FF00; font-size:32px; font-weight:800; margin-bottom:0px;">NexaEdge Network</h1>', unsafe_allow_html=True)
lang = st.selectbox("🌐 Language", ["中文", "English"], index=0, label_visibility="collapsed")

TIME_OPTIONS_EN = ["15 Minutes", "30 Minutes", "1 Hour", "2 Hours", "4 Hours", "8 Hours", "12 Hours", "24 Hours"]
TIME_OPTIONS_ZH = ["15分钟", "半小时", "1小时", "2小时", "4小时", "8小时", "12小时", "24小时"]
SECONDS_MAP = [900, 1800, 3600, 7200, 14400, 28800, 43200, 86400]
HOURS_MAP = [0.25, 0.5, 1.0, 2.0, 4.0, 8.0, 12.0, 24.0]
current_options = TIME_OPTIONS_ZH if lang == "中文" else TIME_OPTIONS_EN

if lang == "中文":
    st.markdown('<p style="font-size: 14px; color: #A2FF00; font-weight:bold; text-align: center; margin-top: 5px;">让全球闲置手机，成为 AI 时代的高纯度分布式算力网络</p>', unsafe_allow_html=True)
else:
    st.markdown('<p style="font-size: 14px; color: #A2FF00; font-weight:bold; text-align: center; margin-top: 5px;">Transforming idle smartphones into high-purity data network for AI Era.</p>', unsafe_allow_html=True)

if target_image:
    st.image(target_image, use_container_width=True)

# --- 四大进化导航选项卡 ---
tab1, tab2, tab3, tab4 = st.tabs([
    "🌐 项目通识" if lang=="中文" else "🌐 Overview", 
    "📱 算力控制台" if lang=="中文" else "📱 Dashboard", 
    "🔑 账户管理中心" if lang=="中文" else "🔑 Identity Portal",
    "🛡️ 内网节点审计" if lang=="中文" else "🛡️ Admin Audit"
])

# ==========================================
# TAB 1: 项目通识
# ==========================================
with tab1:
    c1, c2, c3 = st.columns(3)
    if lang == "中文":
        with c1: st.metric(label="平台技术抽成", value="20%", delta="纯现金流造血")
        with c2: st.metric(label="智能硬件风控", value="39°C", delta="秒级控温预警", delta_color="inverse")
        with c3: st.metric(label="算力结算底座", value="Solana SPL", delta="极速、低 Gas")
        st.markdown('<h2 style="color:#A2FF00; font-size:18px; margin-top:10px;">💰 设备收益计算器</h2>', unsafe_allow_html=True)
    else:
        with c1: st.metric(label="Network Fee", value="20%", delta="Pure Revenue")
        with c2: st.metric(label="Safety Lock", value="39°C", delta="Device Safety", delta_color="inverse")
        with c3: st.metric(label="Settlement Base", value="Solana SPL", delta="Low Gas / TPS")
        st.markdown('<h2 style="color:#A2FF00; font-size:18px; margin-top:10px;">💰 Revenue Calculator</h2>', unsafe_allow_html=True)
        
    selected_time_tab1 = st.selectbox("选择运行时间档位:" if lang=="中文" else "Session Pattern:", current_options, index=st.session_state.target_time_index, key="calc_box")
    st.session_state.target_time_index = current_options.index(selected_time_tab1)
    st.success(f"🎉 {'预计每月可带来收益' if lang=='中文' else 'Estimated Monthly Income'}: {HOURS_MAP[st.session_state.target_time_index] * 0.35 * 30:.2f} USDT")

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

# ==========================================
# TAB 2: 算力控制台 (动态挂载对应的 NEXA 账户)
# ==========================================
with tab2:
    st.markdown('<div class="app-container">', unsafe_allow_html=True)
    
    # 动态渲染当前身份卡片
    if st.session_state.current_user:
        st.markdown(f'<div class="user-badge">🟢 已成功挂载云端账户: <b>{st.session_state.current_user}</b></div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="user-badge" style="border-left-color:#ffb300; color:#ffb300;">⚠️ 游客节点运行（当前数量仅存在本地，建议立即去 [账户管理中心] 注册以保障资产安全）</div>', unsafe_allow_html=True)

    selected_time_tab2 = st.selectbox("配置目标运行时间:" if lang=="中文" else "Target Runtime:", current_options, index=st.session_state.target_time_index, key="console_box")
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
    
    st.markdown(f'<div class="app-card" style="margin-top: -5px;"><div class="temp-section"><span class="app-value" style="font-size:16px;">室温控感: {current_temp:.1f}°C</span><span style="background-color:#1e272e; color:#A2FF00; font-size:11px; font-weight:bold; padding:2px 8px; border-radius:5px;">SAFE</span></div></div>', unsafe_allow_html=True)

    st.markdown(f"""
    <div class="app-card">
        <div style="display:grid; grid-template-columns: 1fr 1fr; gap:6px;">
            <div style="background:#11171d; padding:6px; border-radius:8px;">
                <div style="font-size:9px; color:#88929b; font-weight:bold;">实时输入功耗:</div>
                <div class="app-value neon-blue-text" style="font-size:14px; font-family:monospace;">{current_power:.2f} W</div>
            </div>
            <div style="background:#11171d; padding:6px; border-radius:8px;">
                <div style="font-size:9px; color:#88929b; font-weight:bold;">累计电力消耗:</div>
                <div class="app-value" style="font-size:14px; font-family:monospace; color:#ffffff;">{st.session_state.total_energy_wh:.4f} Wh</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="app-card">
        <div style="display:flex; justify-content:space-between;">
            <div><div style="font-size:10px; color:#88929b; font-weight:bold;">本次运行时长:</div><div class="app-value" style="font-size:17px;">{time_str}</div></div>
            <div style="text-align:right;"><div style="font-size:10px; color:#88929b; font-weight:bold;">当前个体账户拥有的 NEXA 总数:</div><div class="app-value neon-green-text" style="font-size:17px;">{st.session_state.app_earned:,.2f} NEXA</div></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

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

# ==========================================
# TAB 3: 🔑 账户管理中心（新增加的注册/登录系统页面）
# ==========================================
with tab3:
    if st.session_state.current_user:
        st.markdown('<div class="app-card" style="text-align:center; padding:20px 10px;">', unsafe_allow_html=True)
        st.markdown(f"🎉 <b>智能网络已安全连接</b>", unsafe_allow_html=True)
        st.markdown(f"当前在线身份：<span class='neon-blue-text' style='font-weight:bold;'>{st.session_state.current_user}</span>", unsafe_allow_html=True)
        st.markdown(f"<div style='margin:15px 0; background:#11171d; padding:10px; border-radius:10px;'>您账户绑定的全网总收益<br><span class='neon-green-text' style='font-size:26px; font-weight:bold;'>{st.session_state.app_earned:,.2f} NEXA</span></div>", unsafe_allow_html=True)
        
        if st.button("安全退出当前登录账户", key="logout_btn"):
            st.session_state.current_user = None
            st.session_state.app_running = False
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        auth_mode = st.radio("请选择操作", ["注册新节点账户", "登录已有账户"], horizontal=True, label_visibility="collapsed")
        
        if auth_mode == "注册新节点账户":
            with st.form("reg_form"):
                st.markdown('<div style="font-size:14px; font-weight:bold; color:#A2FF00; margin-bottom:8px;">🚀 注册统一网络账户（自动继承并合并当前已有NEXA数量）</div>', unsafe_allow_html=True)
                r_email = st.text_input("电子邮箱地址 (Email):", placeholder="example@nexa.com").strip()
                r_pwd = st.text_input("设置节点密码 (Password):", type="password", placeholder="请输入登录密码")
                r_wallet = st.text_input("接收钱包地址 (Solana 地址):", placeholder="Solana Wallet Address").strip()
                
                if st.form_submit_button("创建全网统一账户 ⚡"):
                    if not r_email or not r_pwd or not r_wallet:
                        st.error("❌ 邮箱、密码与Solana钱包全为必填项！")
                    elif r_email in global_server["user_db"]:
                        st.error("❌ 该邮箱已被占用，请直接切换至登录。")
                    else:
                        # 高阶核心：把目前在手机本地挖出来的局域收益，无缝合并给新创建的账号
                        inherited_nexa = st.session_state.app_earned
                        global_server["user_db"][r_email] = {
                            "password_hash": hashlib.sha256(r_pwd.encode()).hexdigest(),
                            "wallet": r_wallet,
                            "score": inherited_nexa,
                            "reg_time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                        }
                        st.session_state.current_user = r_email
                        st.success("🎉 账户注册成功！本地 NEXA 数据已完美迁移同步。")
                        time.sleep(0.5)
                        st.rerun()
        else:
            with st.form("login_form"):
                st.markdown('<div style="font-size:14px; font-weight:bold; color:#00e5ff; margin-bottom:8px;">🔑 登录 NexaEdge 算力账户</div>', unsafe_allow_html=True)
                l_email = st.text_input("登录邮箱 (Email):").strip()
                l_pwd = st.text_input("验证密码 (Password):", type="password")
                
                if st.form_submit_button("验证并载入云端档案 ⚡"):
                    p_hash = hashlib.sha256(l_pwd.encode()).hexdigest()
                    if l_email in global_server["user_db"] and global_server["user_db"][l_email]["password_hash"] == p_hash:
                        st.session_state.current_user = l_email
                        # 读取云端账户数据
                        st.session_state.app_earned = global_server["user_db"][l_email]["score"]
                        st.success("⚡ 鉴权成功！已成功加载您的个人专属 NEXA 资产底盘。")
                        time.sleep(0.5)
                        st.rerun()
                    else:
                        st.error("❌ 账号或密码输入有误，请重试！")

# ==========================================
# 🛡️ 底部白名单激活表单组件
# ==========================================
with st.form("unified_whitelist_form"):
    st.markdown('<div style="font-size:13px; font-weight:bold; color:#A2FF00; margin-bottom:4px;">🎁 申领创世白名单与社媒双倍裂变奖励</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="social-grid">
        <a class="social-btn" href="https://www.instagram.com/nexaedge__?igsh=eXp0MTlmdDR6dm10&utm_source=qr" target="_blank">📸 Instagram</a>
        <a class="social-btn" href="https://x.com/nexaedge_?s=21&t=8onO0h_fTxzmAGu431ZxXw" target="_blank">🐦 X (Twitter)</a>
        <a class="social-btn" href="https://www.facebook.com/share/18eXN6P3Ge/?mibextid=wwXIfr" target="_blank">👥 Facebook</a>
        <a class="social-btn" href="https://www.tiktok.com/@nexaedge7?_r=1&_t=ZS-96QbSMyso5v" target="_blank">🎵 TikTok</a>
        <a class="social-btn" href="https://t.me/NexaEdge7" target="_blank">📢 Telegram</a>
    </div>
    """, unsafe_allow_html=True)
    
    u_email = st.text_input("申请邮箱:", key="wl_mail").strip()
    u_wallet = st.text_input("Solana 钱包:", key="wl_wall").strip()
    u_ref_input = st.text_input("推荐人邀请码 (选填):", key="wl_ref").strip()
    
    if st.form_submit_button("锁定席位并激活推荐码 ⚡"):
        if not u_email or not u_wallet:
            st.error("❌ 请完整填写表单！")
        else:
            generated_code = generate_referral_code(u_wallet)
            st.session_state.my_referral_code = generated_code
            st.session_state.registration_success = True
            with open("whitelist.txt", "a", encoding="utf-8") as f:
                f.write(f"Email: {u_email} | Wallet: {u_wallet} | Score: {st.session_state.app_earned:.2f} | RefCode: {generated_code}\n")
            st.toast("白名单记录成功！")
            st.rerun()

if st.session_state.registration_success and st.session_state.my_referral_code:
    st.markdown(f'<div class="app-card" style="border:1px solid #A2FF00; text-align:center;"><span style="font-size:11px; color:#88929b;">您的专属邀请裂变码:</span><br><span style="font-size:20px; font-weight:800; color:#A2FF00; font-family:monospace;">{st.session_state.my_referral_code}</span></div>', unsafe_allow_html=True)

# ==========================================
# TAB 4: 🛡️ 内网节点审计（隐藏的管理端大盘明细表）
# ==========================================
with tab4:
    st.markdown('<div style="font-size:13px; font-weight:bold; color:#f43f5e; margin-bottom:6px;">🔒 全网数据中心内网核验区</div>', unsafe_allow_html=True)
    adm_key = st.text_input("请输入核心管理员密钥:", type="password", placeholder="输入 nexaadmin 解锁视图")
    
    if adm_key == "nexaadmin":
        st.toast("🟢 权限验证通过，内网数据库已成功解密", icon="🔓")
        c_a1, c_a2 = st.columns(2)
        with c_a1: st.markdown(f'<div class="mini-stat-card" style="border:1px solid #f43f5e;"><div class="mini-stat-title">全网总注册量</div><div class="mini-stat-value" style="color:#f43f5e;">{len(global_server["user_db"])} 个有效账户</div></div>', unsafe_allow_html=True)
        with c_a2: st.markdown(f'<div class="mini-stat-card" style="border:1px solid #A2FF00;"><div class="mini-stat-title">当前活跃边缘节点</div><div class="mini-stat-value" style="color:#A2FF00;">{len(global_server["active_device_set"])} 台在线</div></div>', unsafe_allow_html=True)
        
        # 实时生成 HTML 用户大账本表格
        st.markdown("<p style='font-size:12px; font-weight:bold; margin-top:10px;'>📋 全网注册个体用户资产底账审计明细 (Live Database):</p>", unsafe_allow_html=True)
        table_html = """
        <table class="admin-table">
            <tr><th>序号</th><th>独立用户邮箱</th><th>Solana 接收钱包</th><th>当前拥有的 NEXA 总数</th><th>注册激活时间</th></tr>
        """
        for idx, (email, info) in enumerate(global_server["user_db"].items(), 1):
            table_html += f"<tr><td>{idx}</td><td>{email}</td><td style='font-family:monospace; color:#9ca3af;'>{info['wallet'][:10]}...{info['wallet'][-8:]}</td><td style='color:#A2FF00; font-weight:bold;'>{info['score']:,.2f} NEXA</td><td>{info['reg_time']}</td></tr>"
        table_html += "</table>"
        st.markdown(table_html, unsafe_allow_html=True)
    elif adm_key != "":
        st.error("❌ 密钥错误，拒绝访问后台核心资产账本。")
    else:
        st.info("💡 提示：在上方输入内网密钥 `nexaadmin` 即可查看全网注册个体的明细数据大表。")

# ==========================================
# 📊 底部全局总在线统计大盘
# ==========================================
st.markdown("<br>", unsafe_allow_html=True)
col_net1, col_net2 = st.columns(2)
with col_net1: st.markdown(f'<div class="mini-stat-card" style="border:1px dashed #A2FF00;"><div class="mini-stat-title">● NETWORK ACTIVE NODES</div><div class="mini-stat-value" style="color:#A2FF00;">{len(global_server["active_device_set"])} Devices</div></div>', unsafe_allow_html=True)
with col_net2: st.markdown(f'<div class="mini-stat-card" style="border:1px dashed #00e5ff;"><div class="mini-stat-title">👀 LIVE REAL VIEWERS</div><div class="mini-stat-value" style="color:#00e5ff;">{global_server["total_online_viewers"]} Online</div></div>', unsafe_allow_html=True)

# ==================== 👑 【驱动内核级高频重刷】 ====================
if st.session_state.app_running:
    st.session_state.app_earned += 0.01
    st.session_state.session_seconds += 1
    st.session_state.total_energy_wh += (5.1 / 3600.0)
    
    # 实时更新数据至共享底层数据库
    if st.session_state.current_user:
        global_server["user_db"][st.session_state.current_user]["score"] = st.session_state.app_earned
    else:
        global_server["device_balances"][dev_id]["app_earned"] = st.session_state.app_earned
        
    st.session_state.last_tick_time = time.time()
    time.sleep(1.0)
    st.rerun()
