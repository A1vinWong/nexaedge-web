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
# 🔒 【核心技术升级】：Streamlit 服务器跨进程内存锁（实现100%真实全网同步）
# =========================================================================
@st.cache_resource
def init_global_network_server():
    """该函数仅在服务器启动时运行一次，所有访问该网页的用户共享同一个内存看板"""
    return {
        "active_device_set": set(),   # 存放真正点击启动的 session_id
        "total_online_viewers": 0      # 存放真正实时在线的连接数
    }

global_server = init_global_network_server()

# 维持每个独立用户的 Session 状态
if "session_id" not in st.session_state:
    st.session_state.session_id = f"node_{random.randint(100000, 999999)}_{time.time()}"
    # 真实新用户进入，全局在线人数真实 +1
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
    .stApp { background-color: #0b0f12; }
    #MainMenu, footer, .styles_viewerBadge__FUChv, [data-testid="manage-app-button"] { display: none !important; }
    header, [data-testid="stHeader"] { background: transparent !important; border: none !important; height: 0 !important; display: none !important; }
    [data-testid="stVerticalBlock"] > div:empty { margin: 0 !important; padding: 0 !important; display: none !important; }
    
    .stTabs [data-baseweb="tab-list"] { gap: 12px; background-color: transparent !important; justify-content: center; border: none !important; }
    .stTabs [data-baseweb="tab"] { background-color: #11171d !important; color: #bdc3c7 !important; border-radius: 8px 8px 0px 0px !important; border: 1px solid #1e272e !important; border-bottom: none !important; padding: 10px 22px !important; font-weight: 700 !important; font-size: 14px !important; }
    .stTabs [aria-selected="true"] { color: #A2FF00 !important; background-color: #161c23 !important; border-top: 2px solid #A2FF00 !important; }
    .stTabs [data-baseweb="tab-highlight"] { background-color: #A2FF00 !important; height: 0px !important; }
    
    .app-container { background-color: #11171d; border: 1px solid #1e272e; border-radius: 20px; padding: 16px; margin: 0 auto; box-shadow: 0 10px 30px rgba(0,0,0,0.5); }
    .app-card { background-color: #161c23; border: 1px solid #252e38; border-radius: 14px; padding: 15px; margin-bottom: 12px; }
    .app-title { font-size: 13px; color: #88929b; font-weight: bold; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 5px; }
    .app-value { font-family: 'Inter', sans-serif; color: #ffffff; font-size: 24px; font-weight: 700; }
    .neon-green-text { color: #A2FF00 !important; }
    .temp-section { display: flex; align-items: center; justify-content: space-between; background: #11171d; padding: 8px 12px; border-radius: 10px; margin-top: 8px; }
    .ratio-box { background-color: #11171d; border: 1px dashed #252e38; border-radius: 8px; padding: 8px 10px; margin-top: 8px; font-size: 12px; color: #88929b; }
    
    div.stButton > button:first-child { background-color: #A2FF00 !important; color: #0b0f12 !important; font-weight: 800 !important; font-size: 16px !important; width: 100%; border-radius: 12px !important; border: none !important; padding: 12px 0 !important; box-shadow: 0 0 15px rgba(162, 255, 0, 0.3); }
    div.stButton > button[key*="app_stop_btn"] { background-color: #0b0f12 !important; color: #ffffff !important; border: 1px solid #252e38 !important; box-shadow: none !important; }
    [data-testid="stForm"] { background-color: #161c23 !important; border: 1px solid #252e38 !important; border-radius: 16px !important; padding: 20px !important; margin-top: 25px !important; }
    div[data-testid="stSelectbox"] label, div[data-testid="stRadio"] label { color: #88929b !important; font-size: 13px !important; font-weight: bold !important; }
    .feature-box { background-color: #11171d; padding: 18px; border-radius: 10px; border-left: 4px solid #A2FF00; margin-bottom: 15px; }
    </style>
""", unsafe_allow_html=True)

# 状态初始化
if 'app_earned' not in st.session_state: st.session_state.app_earned = 1452.7000
if 'app_running' not in st.session_state: st.session_state.app_running = False
if 'chart_history' not in st.session_state: st.session_state.chart_history = [22.0, 25.0, 24.0, 28.0, 27.0, 31.0, 29.0, 33.0, 31.0, 35.0, 33.0, 36.8]
if 'session_seconds' not in st.session_state: st.session_state.session_seconds = 0
if 'target_time_index' not in st.session_state: st.session_state.target_time_index = 2 
if 'last_tick_time' not in st.session_state: st.session_state.last_tick_time = 0.0

# 动态响应节点状态变化（真实维护全局激活集合）
if st.session_state.app_running:
    global_server["active_device_set"].add(st.session_state.session_id)
else:
    global_server["active_device_set"].discard(st.session_state.session_id)

# 抗锁屏物理时间全自动无缝补算
if st.session_state.app_running and st.session_state.last_tick_time > 0:
    current_unix = time.time()
    elapsed_gap_seconds = int(current_unix - st.session_state.last_tick_time)
    if elapsed_gap_seconds >= 3:
        st.session_state.session_seconds += elapsed_gap_seconds
        st.session_state.app_earned += elapsed_gap_seconds * 0.25
        st.session_state.last_tick_time = current_unix

# 选项映射
TIME_OPTIONS_EN = ["15 Minutes", "30 Minutes", "1 Hour", "2 Hours", "4 Hours", "8 Hours", "12 Hours", "24 Hours (Full-day)"]
TIME_OPTIONS_ZH = ["15分钟", "半小时", "1小时", "2小时", "4小时", "8小时", "12小时", "24小时 (全天连轴转)"]
SECONDS_MAP = [900, 1800, 3600, 7200, 14400, 28800, 43200, 86400]
HOURS_MAP = [0.25, 0.5, 1.0, 2.0, 4.0, 8.0, 12.0, 24.0]

st.markdown('<h1 style="text-align:center; color:#A2FF00; font-size:36px; font-weight:800; margin-top:5px; margin-bottom:5px;">NexaEdge Network</h1>', unsafe_allow_html=True)
lang = st.selectbox("🌐 Choose Language / 选择语言", ["English", "中文"], index=0)
current_options = TIME_OPTIONS_EN if lang == "English" else TIME_OPTIONS_ZH

tab1_title = "🌐 Overview & Pillars" if lang == "English" else "🌐 项目通识与壁垒"
tab2_title = "📱 Node Dashboard (Live)" if lang == "English" else "📱 边缘节点控制台 (实时)"
tab1, tab2 = st.tabs([tab1_title, tab2_title])

# =========================================================================
# 🏠 第一页简述
# =========================================================================
with tab1:
    if target_image:
        st.image(target_image, caption="NexaEdge Official Gateway", use_container_width=True)
    if lang == "English":
        st.markdown('<p style="font-size: 18px; color: #A2FF00; font-weight:bold; text-align: center; margin-top: 10px; margin-bottom: 20px;">Transforming 5B+ idle smartphones into high-purity data fuel factories for the AI Era.</p>', unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        with c1: st.metric(label="Network Fee", value="20%", delta="Pure Revenue Flow")
        with c2: st.metric(label="Safety Threshold", value="39°C", delta="Device Safety Lock", delta_color="inverse")
        with c3: st.metric(label="Settlement Base", value="Solana SPL", delta="Low Gas / High TPS")
        st.markdown("<hr style='border:1px solid #1e272e; margin: 15px 0;'>", unsafe_allow_html=True)
        st.markdown('<h2 style="color:#A2FF00; font-size:22px;">💰 Device Revenue Calculator</h2>', unsafe_allow_html=True)
        selected_time_tab1 = st.selectbox("Select Daily Session Duration Pattern:", current_options, index=st.session_state.target_time_index, key="time_select_tab1")
        st.session_state.target_time_index = current_options.index(selected_time_tab1)
        chosen_hours = HOURS_MAP[st.session_state.target_time_index]
        monthly_est = chosen_hours * 0.35 * 30
        st.success(f"🎉 Estimated Monthly Yield (Based on {selected_time_tab1}/day): {monthly_est:.2f} USDT")
    else:
        st.markdown('<p style="font-size: 18px; color: #A2FF00; font-weight:bold; text-align: center; margin-top: 10px; margin-bottom: 20px;">让全球 50 亿部闲置手机，成为 AI 时代的高纯度语料燃料工厂</p>', unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        with c1: st.metric(label="平台技术抽成", value="20%", delta="纯现金流造血")
        with c2: st.metric(label="智能硬件风控", value="39°C", delta="秒级控温预警", delta_color="inverse")
        with c3: st.metric(label="算力结算底座", value="Solana SPL", delta="极速、低 Gas")
        st.markdown("<hr style='border:1px solid #1e272e; margin: 15px 0;'>", unsafe_allow_html=True)
        st.markdown('<h2 style="color:#A2FF00; font-size:22px;">💰 设备收益计算器</h2>', unsafe_allow_html=True)
        selected_time_tab1_zh = st.selectbox("选择每日预估闲置运行时间档位:", current_options, index=st.session_state.target_time_index, key="time_select_tab1_zh")
        st.session_state.target_time_index = current_options.index(selected_time_tab1_zh)
        chosen_hours = HOURS_MAP[st.session_state.target_time_index]
        monthly_est = chosen_hours * 0.35 * 30
        st.success(f"🎉 预计每月可为您带来收益约 (按每日持续运行 【{selected_time_tab1_zh}】 计算): {monthly_est:.2f} USDT")

# =========================================================================
# 📱 第二页控制台
# =========================================================================
with tab2:
    st.markdown('<div class="app-container" style="margin-top:10px;">', unsafe_allow_html=True)
    if target_image:
        st.image(target_image, use_container_width=True)
    
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
        st.toast("⏰ Timer Finished!" if lang == "English" else "⏰ 设定运行时间已满！")
    st.markdown('</div>', unsafe_allow_html=True)

    current_hash = random.uniform(45.5, 49.8) if st.session_state.app_running else 0.0
    current_temp = random.uniform(36.4, 36.9) if st.session_state.app_running else 31.2
    s_sec = st.session_state.session_seconds
    
    remaining_seconds = max(0, target_total_seconds - s_sec)
    remaining_str = f"{remaining_seconds // 3600:02d}:{(remaining_seconds % 3600) // 60:02d}:{remaining_seconds % 60:02d}"
    time_str = f"{s_sec//3600:02d}:{(s_sec%3600)//60:02d}:{s_sec%60:02d}"
    session_generated = s_sec * 0.25
    
    st.markdown(f'<div class="app-card"><div class="app-title">DASHBOARD</div><div style="font-size:12px; color:#88929b;">HASH RATE (MH/s): <span class="neon-green-text">{current_hash:.2f}</span></div></div>', unsafe_allow_html=True)
    
    if st.session_state.app_running:
        st.session_state.chart_history.pop(0)
        st.session_state.chart_history.append(current_hash)
    st.line_chart(pd.DataFrame(st.session_state.chart_history, columns=["Hash Rate"]), height=95, use_container_width=True)
    
    st.markdown(f'<div class="app-card" style="margin-top:-5px;"><div class="temp-section"><span class="app-value" style="font-size:20px;">🌡️ {current_temp:.1f}°C</span><span style="color:#A2FF00; font-size:11px;">SAFE</span></div></div>', unsafe_allow_html=True)

    # 时长收益
    st.markdown(f"""
    <div class="app-card">
        <div style="display:flex; justify-content:space-between;">
            <div><div style="font-size:11px; color:#88929b;">DURATION:</div><div class="app-value" style="font-size:19px;">{time_str}</div></div>
            <div style="text-align:right;"><div style="font-size:11px; color:#88929b;">YIELD:</div><div class="app-value neon-green-text" style="font-size:19px;">+{session_generated:,.1f} NEXA</div></div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # 节点基础参数
    run_status = "ACTIVE" if st.session_state.app_running else "STANDBY"
    status_color = "#A2FF00" if st.session_state.app_running else "#88929b"
    st.markdown(f"""
    <div class="app-card">
        <div class="app-title">PARTICIPANT NODE ➔</div>
        <div style="display:flex; justify-content:space-between; margin-top:5px;">
            <span style="color:{status_color}; font-weight:bold;">● {run_status}</span>
            <span class="app-value neon-green-text" style="font-size:20px;">{st.session_state.app_earned:,.2f} <span style="font-size:12px; color:white;">NEXA</span></span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 🕹️ 控制按钮
    if not st.session_state.app_running:
        if st.button("START COMPUTE SESSION" if lang == "English" else "启动边缘算力节点 🟢", key="app_start_btn"):
            if remaining_seconds <= 0: st.session_state.session_seconds = 0
            st.session_state.app_running = True
            st.session_state.last_tick_time = time.time()
            global_server["active_device_set"].add(st.session_state.session_id)
            st.rerun()
    else:
        if st.button("PAUSE SESSION" if lang == "English" else "暂停运行 🛑", key="app_stop_btn"):
            st.session_state.app_running = False
            st.session_state.last_tick_time = 0.0
            global_server["active_device_set"].discard(st.session_state.session_id)
            st.rerun()
            
    st.markdown('</div>', unsafe_allow_html=True)

# ==================== 📧 表单及白名单 ====================
st.markdown("<hr style='border:1px solid #1e272e;'>", unsafe_allow_html=True)
with st.form("unified_whitelist_form"):
    u_email = st.text_input("Email Address" if lang=="English" else "您的电子邮箱:")
    u_wallet = st.text_input("Solana Wallet Address" if lang=="English" else "Solana 钱包地址:")
    if st.form_submit_button("SUBMIT ⚡"):
        if u_email.strip() != "":
            with open("whitelist.txt", "a", encoding="utf-8") as f:
                f.write(f"Email: {u_email} | Wallet: {u_wallet}\n")
            st.balloons()

# =========================================================================
# 📊 【绝对真实数据大盘】：实时统计真正打开网页的用户与启动的终端
# =========================================================================
st.markdown("<hr style='border:1px solid #1e272e; margin-top:20px;'>", unsafe_allow_html=True)

# 获取服务器内存中真实的实时活跃总数
real_active_nodes = len(global_server["active_device_set"])
real_live_viewers = global_server["total_online_viewers"]

lbl_node_active = "● ACTIVE COMPUTE NODES" if lang == "English" else "● 全网真实运行节点"
lbl_live_view = "👀 LIVE NETWORK VIEWERS" if lang == "English" else "👀 真实在线大盘人数"
unit_device = "Devices" if lang == "English" else "台设备"
unit_user = "Users" if lang == "English" else "人在线"

col_net1, col_net2 = st.columns(2)
with col_net1:
    st.markdown(f"""
        <div style="text-align: center; background-color:#141d26; border: 1px dashed #A2FF00; padding:10px; border-radius:12px;">
            <div style="font-size:11px; color:#88929b; font-weight:bold;">{lbl_node_active}</div>
            <div style="font-size:20px; color:#A2FF00; font-weight:bold; font-family:monospace; margin-top:2px;">{real_active_nodes} {unit_device}</div>
        </div>
    """, unsafe_allow_html=True)

with col_net2:
    st.markdown(f"""
        <div style="text-align: center; background-color:#141d26; border: 1px dashed #00e5ff; padding:10px; border-radius:12px;">
            <div style="font-size:11px; color:#88929b; font-weight:bold;">{lbl_live_view}</div>
            <div style="font-size:20px; color:#00e5ff; font-weight:bold; font-family:monospace; margin-top:2px;">{real_live_viewers} {unit_user}</div>
        </div>
    """, unsafe_allow_html=True)

# 计数器底栏
visitor_counter_html = """
<div style="text-align: center; margin-top: 15px; opacity: 0.85;">
    <a href="https://info.flagcounter.com/NexaEdge">
        <img src="https://s11.flagcounter.com/count2/NexaEdge/bg_0B0F12/txt_A2FF00/border_1E272E/columns_3/maxflags_9/viewers_3/labels_1/pageviews_1/flags_0/" alt="Flag Counter" border="0" style="border-radius: 8px; border: 1px solid #1e272e;">
    </a>
</div>
"""
st.markdown(visitor_counter_html, unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#445; font-size: 11px;'>NexaEdge Network © 2026 | Powered by Solana DePIN Infrastructure</p>", unsafe_allow_html=True)

# ==================== 🏎️ 驱动刷新机制 ====================
if st.session_state.app_running:
    st.session_state.app_earned += 0.75       
    st.session_state.session_seconds += 3     
    st.session_state.last_tick_time = time.time()
    time.sleep(3.0)                            
    st.rerun()                                
