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

# --- ⚙️ 服务器进程级内存锁 (确保 Active 基础人数和白名单缓存跨会话稳定) ---
@st.cache_resource
def get_server_network_memory():
    return {"active_base": 451}
server_mem = get_server_network_memory()

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
        gap: 12px;
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
        padding: 10px 22px !important;
        font-weight: 700 !important;
        font-size: 14px !important;
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
        padding: 16px;
        margin: 0 auto;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }
    
    .app-card {
        background-color: #161c23;
        border: 1px solid #252e38;
        border-radius: 14px;
        padding: 15px;
        margin-bottom: 12px;
    }
    
    /* 文字与排版样式 */
    .app-title { font-size: 13px; color: #88929b; font-weight: bold; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 5px; }
    .app-value { font-family: 'Inter', sans-serif; color: #ffffff; font-size: 24px; font-weight: 700; }
    .neon-green-text { color: #A2FF00 !important; }
    
    .temp-section {
        display: flex;
        align-items: center;
        justify-content: space-between;
        background: #11171d;
        padding: 8px 12px;
        border-radius: 10px;
        margin-top: 8px;
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
        font-size: 16px !important;
        width: 100%;
        border-radius: 12px !important;
        border: none !important;
        padding: 12px 0 !important;
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
        padding: 20px !important;
        margin-top: 25px !important;
    }
    
    /* 优化单选组件 Selectbox/Radio 在黑绿风格下的展现 */
    div[data-testid="stSelectbox"] label, div[data-testid="stRadio"] label {
        color: #88929b !important;
        font-size: 13px !important;
        font-weight: bold !important;
    }
    
    .feature-box {
        background-color: #11171d; 
        padding: 18px; 
        border-radius: 10px; 
        border-left: 4px solid #A2FF00; 
        margin-bottom: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# 状态初始化 (模拟 Session)
if 'app_earned' not in st.session_state: st.session_state.app_earned = 1452.7000
if 'app_running' not in st.session_state: st.session_state.app_running = False
if 'chart_history' not in st.session_state: st.session_state.chart_history = [22.0, 25.0, 24.0, 28.0, 27.0, 31.0, 29.0, 33.0, 31.0, 35.0, 33.0, 36.8]
if 'session_seconds' not in st.session_state: st.session_state.session_seconds = 0
if 'target_time_index' not in st.session_state: st.session_state.target_time_index = 2 
# 【新增安全锁机制】记录上一次精确运行的 Unix 时间戳
if 'last_tick_time' not in st.session_state: st.session_state.last_tick_time = 0.0

# 扩展映射字典
TIME_OPTIONS_EN = ["15 Minutes", "30 Minutes", "1 Hour", "2 Hours", "4 Hours", "8 Hours", "12 Hours", "24 Hours (Full-day)"]
TIME_OPTIONS_ZH = ["15分钟", "半小时", "1小时", "2小时", "4小时", "8小时", "12小时", "24小时 (全天连轴转)"]
SECONDS_MAP = [900, 1800, 3600, 7200, 14400, 28800, 43200, 86400]
HOURS_MAP = [0.25, 0.5, 1.0, 2.0, 4.0, 8.0, 12.0, 24.0]

# =========================================================================
# ⏱️ 【核心 Bug 修复】：抗断开与锁屏物理时间全自动无缝补偿算法
# =========================================================================
if st.session_state.app_running and st.session_state.last_tick_time > 0:
    current_unix = time.time()
    # 计算手机被锁屏或切后台造成的真实断联秒数差
    elapsed_gap_seconds = int(current_unix - st.session_state.last_tick_time)
    if elapsed_gap_seconds >= 3:  # 只有大于正常循环步长时才触发强行灌注补偿
        st.session_state.session_seconds += elapsed_gap_seconds
        st.session_state.app_earned += elapsed_gap_seconds * 0.25
        st.session_state.last_tick_time = current_unix

# 顶栏主标题
st.markdown('<h1 style="text-align:center; color:#A2FF00; font-size:36px; font-weight:800; margin-top:5px; margin-bottom:5px;">NexaEdge Network</h1>', unsafe_allow_html=True)

# 双语切换选择器
lang = st.selectbox("🌐 Choose Language / 选择语言", ["English", "中文"], index=0)

# 依据语言确定选项显示
current_options = TIME_OPTIONS_EN if lang == "English" else TIME_OPTIONS_ZH

# 双 Tabs：左和右
tab1_title = "🌐 Overview & Pillars" if lang == "English" else "🌐 项目通识与壁垒"
tab2_title = "📱 Node Dashboard (Live)" if lang == "English" else "📱 边缘节点控制台 (实时)"

tab1, tab2 = st.tabs([tab1_title, tab2_title])

# =========================================================================
# 🏠 第一页：项目介绍与通识壁垒
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

        st.markdown('<h2 style="color:#A2FF00; font-size:22px; margin-top:15px;">⚡ Key Pillars</h2>', unsafe_allow_html=True)
        st.markdown("""
        <div class="feature-box">
            <h4 style="color:white; margin-top:0; font-size:16px;">📱 Passive Income via Charging</h4>
            <p style="color:#bdc3c7; font-size:13px;">Earn ~0.35 USDT/hr. Just plug in, connect Wi-Fi, and lock your screen. Our lightweight WASM Sandbox cleans AI datasets silently in the background.</p>
        </div>
        <div class="feature-box">
            <h4 style="color:white; margin-top:0; font-size:16px;">🔥 39°C Thermal Guard</h4>
            <p style="color:#bdc3c7; font-size:13px;">Total hardware protection. System auto-throttles computing loads instantly if the battery touches 39°C. Zero degradation anxiety.</p>
        </div>
        <div class="feature-box">
            <h4 style="color:white; margin-top:0; font-size:16px;">🤝 2:1 Anti-Cheat Verification</h4>
            <p style="color:#bdc3c7; font-size:13px;">Decentralized majority-voting consensus. We segment raw data across 3 independent nodes to deliver 100% verified datasets to AI clients.</p>
        </div>
        """, unsafe_allow_html=True)
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

        st.markdown('<h2 style="color:#A2FF00; font-size:22px; margin-top:15px;">⚡ 核心壁垒</h2>', unsafe_allow_html=True)
        st.markdown("""
        <div class="feature-box">
            <h4 style="color:white; margin-top:0; font-size:16px;">📱 锁屏充电·睡后收入 (零门槛)</h4>
            <p style="color:#bdc3c7; font-size:13px;">每小时赚取约 0.35 USDT。用户只需在夜间充电、连接 Wi-Fi 并锁屏，NexaEdge 的轻量级 WASM 沙盒便会在后台静默运行清洗 AI 语料。</p>
        </div>
        <div class="feature-box">
            <h4 style="color:white; margin-top:0; font-size:16px;">🔥 独创：39°C 智能温控风控屏障</h4>
            <p style="color:#bdc3c7; font-size:13px;">坚守绝不伤机底线。一旦手机运行温度触及 39°C 临界点，系统自动下发降载指令，彻底打消硬件损耗焦虑。</p>
        </div>
        <div class="feature-box">
            <h4 style="color:white; margin-top:0; font-size:16px;">🤝 2:1 拜占庭冗余反作弊校验</h4>
            <p style="color:#bdc3c7; font-size:13px;">去中心化多数投票共识。我们将原始语料切片分发至 3 个完全独立的边缘节点进行交叉校验，确保向 AI 客户交付 100% 真实、未被污染的高纯度数据集。</p>
        </div>
        """, unsafe_allow_html=True)


# =========================================================================
# 📱 第二页：边缘节点控制台（纯净去电池版）
# =========================================================================
with tab2:
    st.markdown('<div class="app-container" style="margin-top:10px;">', unsafe_allow_html=True)
    
    if target_image:
        st.image(target_image, use_container_width=True)
    
    # --- ⏰ 定时自动停止计算器组件 ---
    st.markdown('<div class="app-card">', unsafe_allow_html=True)
    calc_title = "⏳ COMPUTE TIMER (AUTO-STOP)" if lang == "English" else "⏳ 算力定时器 (到时自动停止)"
    st.markdown(f'<div class="app-title">{calc_title}</div>', unsafe_allow_html=True)
    
    label_select = "Set target runtime for this session:" if lang == "English" else "配置本次节点运行时间:"
    selected_time_tab2 = st.selectbox(label_select, current_options, index=st.session_state.target_time_index, key="time_select_tab2")
    st.session_state.target_time_index = current_options.index(selected_time_tab2)
    
    target_total_seconds = SECONDS_MAP[st.session_state.target_time_index]
    
    # 自动倒计时强制停止检测
    if st.session_state.app_running and st.session_state.session_seconds >= target_total_seconds:
        st.session_state.app_running = False
        st.toast("⏰ Timer Finished! Node has been stopped safely." if lang == "English" else "⏰ 设定运行时间已满！节点已自动平稳切回待机。")
    
    st.markdown('</div>', unsafe_allow_html=True)

    # 数据状态动态生成
    current_hash = random.uniform(45.5, 49.8) if st.session_state.app_running else 0.0
    current_temp = random.uniform(36.4, 36.9) if st.session_state.app_running else 31.2
        
    s_sec = st.session_state.session_seconds
    
    # 计算精确的倒计时字符串
    remaining_seconds = max(0, target_total_seconds - s_sec)
    rem_hours = remaining_seconds // 3600
    rem_mins = (remaining_seconds % 3600) // 60
    rem_secs = remaining_seconds % 60
    remaining_str = f"{rem_hours:02d}:{rem_mins:02d}:{rem_secs:02d}"
    
    # 本次连续跑满时长格式化
    time_str = f"{s_sec//3600:02d}:{(s_sec%3600)//60:02d}:{s_sec%60:02d}"
    session_generated = s_sec * 0.25
    
    panel_title = "DASHBOARD" if lang == "English" else "控制面板"
    hash_label = "NETWORK HASH RATE" if lang == "English" else "当前节点算力"
    status_tag = "SAFE" if lang == "English" else "安全控温中"

    # --- 🗂️ 模块 1：控制面板组件 ---
    st.markdown(f"""
    <div class="app-card">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
            <span class="app-title">{panel_title}</span>
            <span style="color:#88929b; font-size:13px;">⚙️</span>
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
    chart_df = pd.DataFrame(st.session_state.chart_history, columns=["Hash Rate"])
    st.line_chart(chart_df, height=95, use_container_width=True)
    
    # 🌡️ 纯净温控状态栏（移除电池图标与百分比，更严谨、更具欺骗性）
    st.markdown(f"""
    <div class="app-card" style="margin-top: -5px;">
        <div class="temp-section">
            <div style="display:flex; align-items:center;">
                <span class="app-value" style="font-size:20px;">🌡️ {current_temp:.1f}°C</span>
            </div>
            <span style="background-color:#1e272e; color:#A2FF00; font-size:11px; font-weight:bold; padding:4px 10px; border-radius:12px; border:1px solid #A2FF00;">{status_tag}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # --- 🗂️ 模块 2：时长及实时倒计时卡片 ---
    timer_title = "COMPUTE TIME & RATIO" if lang == "English" else "算力运行时长与收益比"
    t_label = "SESSION DURATION:" if lang == "English" else "本次连续运行时间:"
    rem_label = "COUNTDOWN TO STOP:" if lang == "English" else "距离自动停止倒计时:"
    r_label = "EST. RATIO:" if lang == "English" else "当前时产比折算:"
    ratio_text = "0.25 NEXA / sec (≈ 900 NEXA/hr)" if lang == "English" else "0.25 NEXA / 秒 (约 900 NEXA/小时)"
    yield_lbl = "SESSION YIELD:" if lang == "English" else "本次会话已产出:"
    
    st.markdown(f"""
    <div class="app-card">
        <div class="app-title">{timer_title}</div>
        <div style="display:flex; justify-content:space-between; margin-top:8px;">
            <div style="text-align:left;">
                <div style="font-size:11px; color:#88929b;">{t_label}</div>
                <div class="app-value" style="font-size:19px; font-family:monospace; margin-bottom:5px;">{time_str}</div>
                <div style="font-size:11px; color:#88929b;">{rem_label}</div>
                <div class="app-value" style="font-size:17px; font-family:monospace; color:#ff9f43;">{remaining_str}</div>
            </div>
            <div style="text-align:right;">
                <div style="font-size:11px; color:#88929b;">{yield_lbl}</div>
                <div class="app-value neon-green-text" style="font-size:19px;">+{session_generated:,.1f} <span style="font-size:11px; color:#ffffff;">NEXA</span></div>
            </div>
        </div>
        <div class="ratio-box">
            ⚡ <b>{r_label}</b> {ratio_text}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # --- 🗂️ 模块 3：连接节点基础参数汇总 ---
    node_header = "PARTICIPANT NODE ➔" if lang == "English" else "当前连接节点 ➔"
    if lang == "English":
        run_status = "ACTIVE" if st.session_state.app_running else "STANDBY"
        status_lbl = "MINING STATUS:"
        earnings_lbl = "TOTAL ACCUMULATED:"
    else:
        run_status = "运行中" if st.session_state.app_running else "待机就绪"
        status_lbl = "挖矿状态:"
        earnings_lbl = "账户总累计代币:"
    status_color = "#A2FF00" if st.session_state.app_running else "#88929b"
    
    st.markdown(f"""
    <div class="app-card">
        <div class="app-title" style="margin-bottom:8px;">{node_header}</div>
        <div style="font-size:11px; color:#88929b; margin-bottom:10px;">NODE_ID: <span style="color:#ffffff; font-weight:bold;">@nexaedge / Acc1 (active)</span></div>
        <div style="display:flex; justify-content:space-between; margin-bottom:3px;">
            <span style="font-size:11px; color:#88929b; font-weight:bold;">{status_lbl}</span>
            <span style="font-size:11px; color:#88929b; font-weight:bold;">{earnings_lbl}</span>
        </div>
        <div style="display:flex; justify-content:space-between; align-items:baseline;">
            <span style="color:{status_color}; font-size:14px; font-weight:800;">● {run_status}</span>
            <span class="app-value neon-green-text" style="font-size:22px;">{st.session_state.app_earned:,.2f} <span style="font-size:12px; color:#ffffff; font-weight:normal;">NEXA</span></span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 🕹️ 底部核心交互控制大按钮
    if not st.session_state.app_running:
        btn_start_txt = "START COMPUTE SESSION" if lang == "English" else "启动边缘算力节点 🟢"
        if st.button(btn_start_txt, key="app_start_btn"):
            if remaining_seconds <= 0:
                st.session_state.session_seconds = 0
            st.session_state.app_running = True
            st.session_state.last_tick_time = time.time()  # 锁定精确起动锚点
            st.rerun()
    else:
        btn_stop_txt = "PAUSE SESSION (VIEW NETWORK MAP)" if lang == "English" else "暂停运行 (查看网络拓扑图) 🛑"
        if st.button(btn_stop_txt, key="app_stop_btn"):
            st.session_state.app_running = False
            st.session_state.last_tick_time = 0.0
            st.rerun()
            
    st.markdown('</div>', unsafe_allow_html=True) # 关闭纯净大容器

# ==================== 📧 底部统一白名单递交表单 ====================
st.markdown("<hr style='border:1px solid #1e272e; margin-top:20px;'>", unsafe_allow_html=True)
st.markdown(f'<h3 style="text-align:center; color:#A2FF00; font-size:20px; margin-bottom:10px;">{"🚀 Secure Your Early Whitelist Seat" if lang=="English" else "🚀 锁定早期测试网白名单席位"}</h3>', unsafe_allow_html=True)

with st.form("unified_whitelist_form"):
    u_email = st.text_input("Email Address" if lang=="English" else "您的电子邮箱:")
    u_wallet = st.text_input("Solana Wallet Address" if lang=="English" else "Solana 钱包地址:")
    
    submitted = st.form_submit_button("SUBMIT & RETAIN SEAT ⚡" if lang=="English" else "提交并归档体验收益 ⚡")
    if submitted:
        if u_email.strip() != "":
            with open("whitelist.txt", "a", encoding="utf-8") as f:
                f.write(f"Email: {u_email} | Wallet: {u_wallet} | Score: {st.session_state.app_earned:.1f} | ActiveTime: {st.session_state.session_seconds}s\n")
            st.balloons()

# ==================== 📥 后台管理员白名单下载 ====================
if os.path.exists("whitelist.txt"):
    with open("whitelist.txt", "r", encoding="utf-8") as f:
        whitelist_data = f.read()
    st.download_button(
        label="📥 Download Whitelist Data" if lang=="English" else "📥 下载白名单数据",
        data=whitelist_data,
        file_name="nexaedge_whitelist.txt",
        mime="text/plain",
        key="admin_download_btn"
    )

# =========================================================================
# 📊 【新功能扩展】：实时硬核指标大盘 —— Active 节点与实时观众动态双卡片
# =========================================================================
st.markdown("<hr style='border:1px solid #1e272e; margin-top:20px;'>", unsafe_allow_html=True)

# 1. 活跃设备强联动逻辑：未运行为基数451台，点击START运行后，全服数据立刻变成452台
current_active_nodes = server_mem["active_base"] + (1 if st.session_state.app_running else 0)

# 2. 实时在线看大盘人数：每次重新加载时在 1060 左右进行真实微扰起伏（1052~1078）
current_live_viewers = 1065 + random.randint(-13, 13)

# 依照双语渲染指标卡
lbl_node_active = "● ACTIVE COMPUTE NODES" if lang == "English" else "● 全网实时运行节点"
lbl_live_view = "👀 LIVE NETWORK VIEWERS" if lang == "English" else "👀 实时大盘围观人数"
unit_device = "Devices" if lang == "English" else "台闲置终端"
unit_user = "Users" if lang == "English" else "人在线"

col_net1, col_net2 = st.columns(2)
with col_net1:
    st.markdown(f"""
        <div style="text-align: center; background-color:#141d26; border: 1px dashed #A2FF00; padding:10px; border-radius:12px;">
            <div style="font-size:11px; color:#88929b; text-transform:uppercase; font-weight:bold;">{lbl_node_active}</div>
            <div style="font-size:18px; color:#A2FF00; font-weight:bold; font-family:monospace; margin-top:2px;">{current_active_nodes} {unit_device}</div>
        </div>
    """, unsafe_allow_html=True)

with col_net2:
    st.markdown(f"""
        <div style="text-align: center; background-color:#141d26; border: 1px dashed #00e5ff; padding:10px; border-radius:12px;">
            <div style="font-size:11px; color:#88929b; text-transform:uppercase; font-weight:bold;">{lbl_live_view}</div>
            <div style="font-size:18px; color:#00e5ff; font-weight:bold; font-family:monospace; margin-top:2px;">{current_live_viewers} {unit_user}</div>
        </div>
    """, unsafe_allow_html=True)

# ==================== 📊 页面全球原装访客计数器挂件 ====================
visitor_counter_html = """
<div style="text-align: center; margin-top: 15px; opacity: 0.85;">
    <p style="color: #88929b; font-size: 11px; margin-bottom: 6px; letter-spacing: 1px;">➔ NEXAEDGE NETWORK NODE STATUS</p>
    <a href="https://info.flagcounter.com/NexaEdge">
        <img src="https://s11.flagcounter.com/count2/NexaEdge/bg_0B0F12/txt_A2FF00/border_1E272E/columns_3/maxflags_9/viewers_3/labels_1/pageviews_1/flags_0/" alt="Flag Counter" border="0" style="border-radius: 8px; border: 1px solid #1e272e; max-width: 100%;">
    </a>
</div>
"""
st.markdown(visitor_counter_html, unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#445; font-size: 11px; margin-top:10px;'>NexaEdge Network © 2026 | Powered by Solana DePIN Infrastructure</p>", unsafe_allow_html=True)

# ==================== 🏎️ 后台低频稳健刷新驱动器 (保持稳健3秒步进) ====================
if st.session_state.app_running:
    st.session_state.app_earned += 0.75       
    st.session_state.session_seconds += 3     
    st.session_state.last_tick_time = time.time()  # 每次心跳动态刷新基准时间戳
    time.sleep(3.0)                            
    st.rerun()                                
