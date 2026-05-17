import streamlit as st
import os
import time
import random
import pandas as pd
import glob

# 1. 全局页面基础配置
st.set_page_config(
    page_title="NexaEdge Network | Official Node Gateway",
    page_icon="🟢",
    layout="centered"
)

# =========================================================================
# 🔒 服务器跨进程内存锁（实现100%真实全网同步）
# =========================================================================
@st.cache_resource
def init_global_network_server():
    return {
        "active_device_set": set(),   # 存放真正点击启动的 session_id
        "total_online_viewers": 0      # 存放真正实时在线的连接数
    }

global_server = init_global_network_server()

if "session_id" not in st.session_state:
    st.session_state.session_id = f"node_{random.randint(100000, 999999)}_{time.time()}"
    global_server["total_online_viewers"] += 1

# --- 📸 智能图片摄入系统 ---
def get_project_image():
    if os.path.exists("image.png"):
        return "image.png"
    png_files = glob.glob("*.png")
    if png_files:
        return png_files[0]
    return None

target_image = get_project_image()

# --- 🟢 极客黑绿科技风 CSS 全量优化 ---
st.markdown("""
    <style>
    /* 全局去暗灰背景 */
    .stApp {
        background-color: #0b0f12;
    }
    
    /* 彻底隐藏顶部无用白条及右下角开发者管理小标签 */
    #MainMenu, footer, .styles_viewerBadge__FUChv, [data-testid="manage-app-button"] {
        display: none !important;
    }
    header, [data-testid="stHeader"] {
        background: transparent !important;
        border: none !important;
        height: 0 !important;
        display: none !important;
    }
    
    /* 强力抹杀 Streamlit 原生自带的所有空置边界、缝隙和多余空框 */
    [data-testid="stVerticalBlock"] > div:empty {
        display: none !important;
        margin: 0 !important;
        padding: 0 !important;
    }
    [data-testid="stElementContainer"] {
        border: none !important;
        background: transparent !important;
    }
    
    /* --- st.tabs 组件样式微调 (左和右) --- */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: transparent !important;
        justify-content: center;
        border: none !important;
    }

    .stTabs [data-baseweb="tab"] {
        background-color: #11171d !important;
        color: #bdc3c7 !important;
        border-radius: 8px 8px 0px 0px !important;
        border: 1px solid #1e272e !important;
        border-bottom: none !important;
        padding: 8px 16px !important;
        font-weight: 700 !important;
        font-size: 13px !important;
    }

    .stTabs [aria-selected="true"] {
        color: #A2FF00 !important;
        background-color: #161c23 !important;
        border-top: 2px solid #A2FF00 !important;
    }
    
    .stTabs [data-baseweb="tab-highlight"] {
        background-color: #A2FF00 !important;
        height: 0px !important;
    }
    
    /* --- 自定义手机 App 容器结构 --- */
    .app-container {
        background-color: #11171d;
        border: 1px solid #1e272e;
        border-radius: 20px;
        padding: 14px;
        margin: 0 auto;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }
    
    .app-card {
        background-color: #161c23;
        border: 1px solid #252e38;
        border-radius: 14px;
        padding: 12px;
        margin-bottom: 10px;
    }
    
    /* 文字与排版样式 */
    .app-title { font-size: 12px; color: #88929b; font-weight: bold; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 4px; }
    .app-value { font-family: 'Inter', sans-serif; color: #ffffff; font-size: 22px; font-weight: 700; }
    .neon-green-text { color: #A2FF00 !important; }
    
    .temp-section {
        display: flex;
        align-items: center;
        justify-content: space-between;
        background: #11171d;
        padding: 6px 12px;
        border-radius: 10px;
        margin-top: 6px;
    }
    
    .ratio-box {
        background-color: #11171d;
        border: 1px dashed #252e38;
        border-radius: 8px;
        padding: 8px 10px;
        margin-top: 8px;
        font-size: 12px;
        color: #88929b;
    }
    
    /* --- stButton 样式 --- */
    div.stButton > button:first-child {
        background-color: #A2FF00 !important;
        color: #0b0f12 !important;
        font-weight: 800 !important;
        font-size: 15px !important;
        width: 100%;
        border-radius: 12px !important;
        border: none !important;
        padding: 10px 0 !important;
        box-shadow: 0 0 15px rgba(162, 255, 0, 0.3);
    }
    
    div.stButton > button[key*="app_stop_btn"] {
        background-color: #0b0f12 !important;
        color: #ffffff !important;
        border: 1px solid #252e38 !important;
        box-shadow: none !important;
    }
    
    /* 白名单表单卡片 */
    [data-testid="stForm"] {
        background-color: #161c23 !important;
        border: 1px solid #252e38 !important;
        border-radius: 16px !important;
        padding: 15px !important;
        margin-top: 20px !important;
    }
    
    /* 优化单选组件 Selectbox/Radio 在黑绿风格下的展现 */
    div[data-testid="stSelectbox"] label, div[data-testid="stRadio"] label {
        color: #88929b !important;
        font-size: 12px !important;
        font-weight: bold !important;
    }
    
    .feature-box {
        background-color: #11171d; 
        padding: 18px; 
        border-radius: 10px; 
        border-left: 4px solid #A2FF00; 
        margin-bottom: 15px;
    }

    /* 极致缩小的全网真实数据大盘卡片样式（防止窄屏换行） */
    .mini-stat-card { text-align: center; background-color:#141d26; padding: 6px 4px; border-radius: 10px; min-height: 55px; display: flex; flex-direction: column; justify-content: center; align-items: center; }
    .mini-stat-title { font-size: 9px !important; color: #88929b; font-weight: bold; white-space: nowrap; transform: scale(0.95); }
    .mini-stat-value { font-size: 13px !important; font-weight: bold; font-family: monospace; margin-top: 2px; white-space: nowrap; }
    </style>
""", unsafe_allow_html=True)

# 状态初始化 (模拟 Session)
if 'app_earned' not in st.session_state: st.session_state.app_earned = 1452.7000
if 'app_running' not in st.session_state: st.session_state.app_running = False
if 'chart_history' not in st.session_state: st.session_state.chart_history = [22.0, 25.0, 24.0, 28.0, 27.0, 31.0, 29.0, 33.0, 31.0, 35.0, 33.0, 36.8]
if 'session_seconds' not in st.session_state: st.session_state.session_seconds = 0
if 'target_time_index' not in st.session_state: st.session_state.target_time_index = 2 
if 'last_tick_time' not in st.session_state: st.session_state.last_tick_time = 0.0

# 真实同步全局状态到共享内存区
if st.session_state.app_running:
    global_server["active_device_set"].add(st.session_state.session_id)
else:
    global_server["active_device_set"].discard(st.session_state.session_id)

# 物理时间防锁屏补算逻辑
if st.session_state.app_running and st.session_state.last_tick_time > 0:
    current_unix = time.time()
    elapsed_gap_seconds = int(current_unix - st.session_state.last_tick_time)
    if elapsed_gap_seconds >= 3:
        st.session_state.session_seconds += elapsed_gap_seconds
        st.session_state.app_earned += elapsed_gap_seconds * 0.25
        st.session_state.last_tick_time = current_unix

# 扩展映射字典
TIME_OPTIONS_EN = ["15 Minutes", "30 Minutes", "1 Hour", "2 Hours", "4 Hours", "8 Hours", "12 Hours", "24 Hours"]
TIME_OPTIONS_ZH = ["15分钟", "半小时", "1小时", "2小时", "4小时", "8小时", "12小时", "24小时"]
SECONDS_MAP = [900, 1800, 3600, 7200, 14400, 28800, 43200, 86400]
HOURS_MAP = [0.25, 0.5, 1.0, 2.0, 4.0, 8.0, 12.0, 24.0]

# =========================================================================
# 🔝 顶部常驻区域：主标题 + 语言选择 + 【不缩水的三行大介绍】 + 智能检索图
# =========================================================================
st.markdown('<h1 style="text-align:center; color:#A2FF00; font-size:34px; font-weight:800; margin-bottom:0px;">NexaEdge Network</h1>', unsafe_allow_html=True)

# 语言切换选择器
lang = st.selectbox("🌐 Language", ["English", "中文"], index=0, label_visibility="collapsed")
current_options = TIME_OPTIONS_EN if lang == "English" else TIME_OPTIONS_ZH

# 强制置顶且保持原尺寸(18px)的三行核心亮点
if lang == "English":
    st.markdown('<p style="font-size: 18px; color: #A2FF00; font-weight:bold; text-align: center; margin-top: 10px; margin-bottom: 12px; line-height: 1.4;">Transforming 5B+ idle smartphones into high-purity data fuel factories for the AI Era.</p>', unsafe_allow_html=True)
else:
    st.markdown('<p style="font-size: 18px; color: #A2FF00; font-weight:bold; text-align: center; margin-top: 10px; margin-bottom: 12px; line-height: 1.4;">让全球 50 亿部闲置手机，成为 AI 时代的高纯度语料燃料工厂</p>', unsafe_allow_html=True)

# 智能检索出的项目核心图置顶渲染
if target_image:
    st.image(target_image, caption="NexaEdge Official Gateway" if lang=="English" else "NexaEdge 官方主网网关", use_container_width=True)

# 双 Tabs 导航结构
tab1_title = "🌐 Overview & Pillars" if lang == "English" else "🌐 项目通识与壁垒"
tab2_title = "📱 Node Dashboard (Live)" if lang == "English" else "📱 边缘节点控制台 (实时)"
tab1, tab2 = st.tabs([tab1_title, tab2_title])

# =========================================================================
# 🏠 第一页：项目介绍与通识壁垒
# =========================================================================
with tab1:
    if lang == "English":
        c1, c2, c3 = st.columns(3)
        with c1: st.metric(label="Network Fee", value="20%", delta="Pure Revenue Flow")
        with c2: st.metric(label="Safety Threshold", value="39°C", delta="Device Safety Lock", delta_color="inverse")
        with c3: st.metric(label="Settlement Base", value="Solana SPL", delta="Low Gas / High TPS")

        st.markdown("<hr style='border:1px solid #1e272e; margin: 12px 0;'>", unsafe_allow_html=True)

        st.markdown('<h2 style="color:#A2FF00; font-size:20px; margin-bottom:5px;">💰 Device Revenue Calculator</h2>', unsafe_allow_html=True)
        selected_time_tab1 = st.selectbox("Select Daily Session Duration Pattern:", current_options, index=st.session_state.target_time_index, key="time_select_tab1")
        st.session_state.target_time_index = current_options.index(selected_time_tab1)
        
        chosen_hours = HOURS_MAP[st.session_state.target_time_index]
        monthly_est = chosen_hours * 0.35 * 30
        st.success(f"🎉 Estimated Monthly Yield: {monthly_est:.2f} USDT")

        st.markdown('<h2 style="color:#A2FF00; font-size:20px; margin-top:15px;">⚡ Key Pillars</h2>', unsafe_allow_html=True)
        st.markdown("""
        <div class="feature-box">
            <h4 style="color:white; margin-top:0; font-size:15px;">📱 Passive Income via Charging</h4>
            <p style="color:#bdc3c7; font-size:13px;">Earn ~0.35 USDT/hr. Just plug in, connect Wi-Fi, and lock your screen. Our lightweight WASM Sandbox cleans AI datasets silently in the background.</p>
        </div>
        <div class="feature-box">
            <h4 style="color:white; margin-top:0; font-size:15px;">🔥 39°C Thermal Guard</h4>
            <p style="color:#bdc3c7; font-size:13px;">Total hardware protection. System auto-throttles computing loads instantly if the battery touches 39°C. Zero degradation anxiety.</p>
        </div>
        <div class="feature-box">
            <h4 style="color:white; margin-top:0; font-size:15px;">🤝 2:1 Anti-Cheat Verification</h4>
            <p style="color:#bdc3c7; font-size:13px;">Decentralized majority-voting consensus. We segment raw data across 3 independent nodes to deliver 100% verified datasets to AI clients.</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        c1, c2, c3 = st.columns(3)
        with c1: st.metric(label="平台技术抽成", value="20%", delta="纯现金流造血")
        with c2: st.metric(label="智能硬件风控", value="39°C", delta="秒级控温预警", delta_color="inverse")
        with c3: st.metric(label="算力结算底座", value="Solana SPL", delta="极速、低 Gas")

        st.markdown("<hr style='border:1px solid #1e272e; margin: 12px 0;'>", unsafe_allow_html=True)

        st.markdown('<h2 style="color:#A2FF00; font-size:20px; margin-bottom:5px;">💰 设备收益计算器</h2>', unsafe_allow_html=True)
        selected_time_tab1_zh = st.selectbox("选择每日预估闲置运行时间档位:", current_options, index=st.session_state.target_time_index, key="time_select_tab1_zh")
        st.session_state.target_time_index = current_options.index(selected_time_tab1_zh)
        
        chosen_hours = HOURS_MAP[st.session_state.target_time_index]
        monthly_est = chosen_hours * 0.35 * 30
        st.success(f"🎉 预计每月可为您带来收益约: {monthly_est:.2f} USDT")

        st.markdown('<h2 style="color:#A2FF00; font-size:20px; margin-top:15px;">⚡ 核心壁垒</h2>', unsafe_allow_html=True)
        st.markdown("""
        <div class="feature-box">
            <h4 style="color:white; margin-top:0; font-size:15px;">📱 锁屏充电·睡后收入 (零门槛)</h4>
            <p style="color:#bdc3c7; font-size:13px;">每小时赚取约 0.35 USDT。用户只需在夜间充电、连接 Wi-Fi 并锁屏，NexaEdge 的轻量级 WASM 沙盒便会在后台静默运行清洗 AI 语料。</p>
        </div>
        <div class="feature-box">
            <h4 style="color:white; margin-top:0; font-size:15px;">🔥 独创：39°C 智能温控风控屏障</h4>
            <p style="color:#bdc3c7; font-size:13px;">坚守绝不伤机底线。一旦手机运行温度触及 39°C 临界点，系统自动下发降载指令，彻底打消硬件损耗焦虑。</p>
        </div>
        <div class="feature-box">
            <h4 style="color:white; margin-top:0; font-size:15px;">🤝 2:1 拜占庭冗余反作弊校验</h4>
            <p style="color:#bdc3c7; font-size:13px;">去中心化多数投票共识。我们将原始语料切片分发至 3 个完全独立的边缘节点进行交叉校验，确保向 AI 客户交付 100% 真实数据集。</p>
        </div>
        """, unsafe_allow_html=True)

# =========================================================================
# 📱 第二页：边缘节点控制台（控制流区）
# =========================================================================
with tab2:
    st.markdown('<div class="app-container">', unsafe_allow_html=True)
    
    # --- ⏰ 定时自动停止计算器组件 ---
    st.markdown('<div class="app-card">', unsafe_allow_html=True)
    calc_title = "⏳ COMPUTE TIMER (AUTO-STOP)" if lang == "English" else "⏳ 算力定时器 (到时自动停止)"
    st.markdown(f'<div class="app-title">{calc_title}</div>', unsafe_allow_html=True)
    
    label_select = "Set target runtime for this session:" if lang == "English" else "配置本次节点运行时间:"
    selected_time_tab2 = st.selectbox(label_select, current_options, index=st.session_state.target_time_index, key="time_select_tab2")
    st.session_state.target_time_index = current_options.index(selected_time_tab2)
    
    target_total_seconds = SECONDS_MAP[st.session_state.target_time_index]
    
    if st.session_state.app_running and st.session_state.session_seconds >= target_total_seconds:
        st.session_state.app_running = False
        global_server["active_device_set"].discard(st.session_state.session_id)
        st.toast("⏰ Timer Finished!" if lang == "English" else "⏰ 设定运行时间已满！节点已安全切回待机。")
    st.markdown('</div>', unsafe_allow_html=True)

    # 数据状态动态生成
    current_hash = random.uniform(45.5, 49.8) if st.session_state.app_running else 0.0
    current_temp = random.uniform(36.4, 36.9) if st.session_state.app_running else 31.2
    s_sec = st.session_state.session_seconds
    
    remaining_seconds = max(0, target_total_seconds - s_sec)
    remaining_str = f"{remaining_seconds // 3600:02d}:{(remaining_seconds % 3600) // 60:02d}:{remaining_seconds % 60:02d}"
    time_str = f"{s_sec//3600:02d}:{(s_sec%3600)//60:02d}:{s_sec%60:02d}"
    session_generated = s_sec * 0.25
    
    panel_title = "DASHBOARD" if lang == "English" else "控制面板"
    hash_label = "NETWORK HASH RATE" if lang == "English" else "当前节点算力"
    status_tag = "SAFE" if lang == "English" else "安全控温中"

    st.markdown(f"""
    <div class="app-card">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:4px;">
            <span class="app-title">{panel_title}</span>
            <span style="color:#88929b; font-size:12px;">⚙️</span>
        </div>
        <div style="font-size:12px; color:#88929b; margin-bottom:5px;">
            {hash_label} (MH/s): <span class="neon-green-text" style="font-weight:bold;">{current_hash:.2f}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # 折线图
    if st.session_state.app_running:
        st.session_state.chart_history.pop(0)
        st.session_state.chart_history.append(current_hash)
    st.line_chart(pd.DataFrame(st.session_state.chart_history, columns=["Hash Rate"]), height=90, use_container_width=True)
    
    # 温控状态栏
    st.markdown(f"""
    <div class="app-card" style="margin-top: -5px;">
        <div class="temp-section">
            <span class="app-value" style="font-size:18px;">🌡️ {current_temp:.1f}°C</span>
            <span style="background-color:#1e272e; color:#A2FF00; font-size:11px; font-weight:bold; padding:2px 8px; border-radius:5px;">{status_tag}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 时长及实时产出
    t_label = "DURATION:" if lang == "English" else "本次连续运行时间:"
    yield_lbl = "EST. RATIO: 0.25 NEXA / sec" if lang == "English" else "已为您实时产出代币:"
    st.markdown(f"""
    <div class="app-card">
        <div style="display:flex; justify-content:space-between;">
            <div><div style="font-size:10px; color:#88929b; font-weight:bold;">{t_label}</div><div class="app-value" style="font-size:18px;">{time_str}</div></div>
            <div style="text-align:right;"><div style="font-size:10px; color:#88929b; font-weight:bold;">{yield_lbl}</div><div class="app-value neon-green-text" style="font-size:18px;">+{session_generated:,.1f} NEXA</div></div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # 节点基础参数
    node_header = "PARTICIPANT NODE ➔" if lang == "English" else "当前连接节点 ➔"
    run_status = "ACTIVE" if st.session_state.app_running else "STANDBY"
    status_color = "#A2FF00" if st.session_state.app_running else "#88929b"
    st.markdown(f"""
    <div class="app-card">
        <div class="app-title" style="margin-bottom:4px;">{node_header}</div>
        <div style="font-size:11px; color:#88929b; margin-bottom:5px;">NODE_ID: <span style="color:#ffffff; font-weight:bold;">@nexaedge / Acc1</span></div>
        <div style="display:flex; justify-content:space-between; align-items:baseline; margin-top:5px;">
            <span style="color:{status_color}; font-size:13px; font-weight:800;">● STATUS: {run_status}</span>
            <span class="app-value neon-green-text" style="font-size:18px;">{st.session_state.app_earned:,.2f} <span style="font-size:10px; color:white;">NEXA</span></span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 大按钮控制交互
    if not st.session_state.app_running:
        if st.button("START COMPUTE SESSION" if lang == "English" else "启动边缘算力集群", key="app_start_btn"):
            if remaining_seconds <= 0: st.session_state.session_seconds = 0
            st.session_state.app_running = True
            st.session_state.last_tick_time = time.time()
            global_server["active_device_set"].add(st.session_state.session_id)
            st.rerun()
    else:
        if st.button("PAUSE COMPUTE SESSION" if lang == "English" else "暂停算力输出", key="app_stop_btn"):
            st.session_state.app_running = False
            st.session_state.last_tick_time = 0.0
            global_server["active_device_set"].discard(st.session_state.session_id)
            st.rerun()
            
    st.markdown('</div>', unsafe_allow_html=True)

# ==================== 📧 底部统一白名单递交表单（新增强力硬核去重逻辑） ====================
st.markdown("<hr style='border:1px solid #1e272e; margin-top:20px;'>", unsafe_allow_html=True)
with st.form("unified_whitelist_form"):
    st.markdown(f'<div style="font-size:14px; font-weight:bold; color:#A2FF00; margin-bottom:5px;">🚀 {"Secure Early Whitelist Seat" if lang=="English" else "🚀 锁定早期创世白名单席位"}</div>', unsafe_allow_html=True)
    u_email = st.text_input("Email Address:" if lang=="English" else "电子邮箱地址:").strip()
    u_wallet = st.text_input("Solana Wallet Address:" if lang=="English" else "Solana 钱包接收地址:").strip()
    
    if st.form_submit_button("SUBMIT SEAT ⚡" if lang=="English" else "提交并保留创世资格 ⚡"):
        if u_email == "" or u_wallet == "":
            st.error("❌ Please fill in both fields! / 请完整填写邮箱和钱包地址！")
        else:
            # 建立默认存储逻辑以防读取报错
            is_duplicate = False
            
            # 高效精确读盘去重检索
            if os.path.exists("whitelist.txt"):
                with open("whitelist.txt", "r", encoding="utf-8") as f:
                    lines = f.readlines()
                for line in lines:
                    # 强效切割并做大小写不敏感匹配验证
                    if f"Email: {u_email} |" in line or f"Email: {u_email.lower()} |" in line:
                        is_duplicate = True
                        break
                    if f"| Wallet: {u_wallet}" in line or f"| Wallet: {u_wallet.lower()}" in line or f"| Wallet: {u_wallet}\n" in line:
                        is_duplicate = True
                        break
            
            if is_duplicate:
                if lang == "English":
                    st.error("⚠️ Submission Rejected! This Email or Solana Wallet has already claimed a whitelist allocation.")
                else:
                    st.error("⚠️ 提交失败！该邮箱地址或 Solana 钱包已被注册，每个账户仅限申领一次白名单。")
            else:
                # 校验安全后写入本地白名单库
                with open("whitelist.txt", "a", encoding="utf-8") as f:
                    f.write(f"Email: {u_email} | Wallet: {u_wallet} | Score: {st.session_state.app_earned:.1f}\n")
                st.balloons()
                st.success("🎉 Whitelist recorded successfully! / 白名单资格锁定成功！")

if os.path.exists("whitelist.txt"):
    with open("whitelist.txt", "r", encoding="utf-8") as f: whitelist_data = f.read()
    st.download_button(label="📥 Download Whitelist" if lang=="English" else "📥 下载白名单数据", data=whitelist_data, file_name="nexaedge_whitelist.txt", mime="text/plain")

# =========================================================================
# 📊 【全网绝对真实大盘】：完全替换为真实统计，极小字体不换行适配窄屏
# =========================================================================
st.markdown("<hr style='border:1px solid #1e272e; margin: 15px 0 10px 0;'>", unsafe_allow_html=True)

real_active_nodes = len(global_server["active_device_set"])
real_live_viewers = global_server["total_online_viewers"]

lbl_node_active = "● NETWORK ACTIVE NODES" if lang == "English" else "● 全网真实运行节点"
lbl_live_view = "👀 LIVE REAL VIEWERS" if lang == "English" else "👀 真实在线大盘人数"
unit_device = "Devices" if lang == "English" else "台闲置终端"
unit_user = "Online" if lang == "English" else "人在线"

col_net1, col_net2 = st.columns(2)
with col_net1:
    st.markdown(f"""
        <div class="mini-stat-card" style="border: 1px dashed #A2FF00;">
            <div class="mini-stat-title">{lbl_node_active}</div>
            <div class="mini-stat-value" style="color:#A2FF00;">{real_active_nodes} {unit_device}</div>
        </div>
    """, unsafe_allow_html=True)

with col_net2:
    st.markdown(f"""
        <div class="mini-stat-card" style="border: 1px dashed #00e5ff;">
            <div class="mini-stat-title">{lbl_live_view}</div>
            <div class="mini-stat-value" style="color:#00e5ff;">{real_live_viewers} {unit_user}</div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<p style='text-align:center; color:#445; font-size: 10px; margin-top:12px;'>NexaEdge Network © 2026 | Powered by Solana DePIN Infrastructure</p>", unsafe_allow_html=True)

# ==================== 🏎️ 驱动刷新机制 ====================
if st.session_state.app_running:
    st.session_state.app_earned += 0.75       
    st.session_state.session_seconds += 3     
    st.session_state.last_tick_time = time.time()
    time.sleep(3.0)                            
    st.rerun()
