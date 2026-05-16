import streamlit as st
import os
import time
import random
import pandas as pd

# 1. 全局页面基础配置
st.set_page_config(
    page_title="NexaEdge Network | Official Node Gateway",
    page_icon="🟢",
    layout="centered"
)

# --- 🟢 极客黑绿科技风 1:1 还原 CSS 样式 ---
st.markdown("""
    <style>
    /* 全局深色底色 */
    .stApp { background-color: #0b0f12; }
    
    /* 核心介绍卡片样式 */
    .feature-box {
        background-color: #11171d; 
        padding: 20px; 
        border-radius: 10px; 
        border-left: 5px solid #A2FF00; 
        margin-bottom: 20px;
    }
    
    /* --- 📱 像素级手机 App 容器样式 --- */
    .app-container {
        background-color: #11171d;
        border: 2px solid #1e272e;
        border-radius: 24px;
        padding: 25px;
        max-width: 450px;
        margin: 0 auto;
        box-shadow: 0 15px 35px rgba(0,0,0,0.6);
        text-align: center;
    }
    
    /* App 内部的黑色子模块小面板 */
    .app-card {
        background-color: #161c23;
        border: 1px solid #252e38;
        border-radius: 16px;
        padding: 18px;
        margin-bottom: 15px;
        text-align: left;
    }
    
    /* 字体与高亮颜色 */
    .app-title { font-size: 14px; color: #88929b; font-weight: bold; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 5px; }
    .app-value { font-family: 'Inter', sans-serif; color: #ffffff; font-size: 26px; font-weight: 700; }
    .neon-green-text { color: #A2FF00 !important; }
    
    /* 模拟日志终端 */
    .app-log {
        font-family: 'Courier New', monospace;
        color: #88929b;
        font-size: 11px;
        background-color: #0b0f12;
        padding: 10px;
        border-radius: 8px;
        height: 65px;
        overflow-y: hidden;
        border: 1px solid #1e272e;
    }
    
    /* 温度计整块区域排版 */
    .temp-section {
        display: flex;
        align-items: center;
        justify-content: space-between;
        background: #11171d;
        padding: 10px 15px;
        border-radius: 12px;
        margin-top: 10px;
    }
    .thermometer-icon {
        color: #A2FF00;
        font-size: 24px;
        margin-right: 8px;
    }
    
    /* Streamlit 原生 Tab 标签样式重写 */
    .stTabs [data-baseweb="tab-list"] { gap: 10px; justify-content: center; }
    .stTabs [data-baseweb="tab"] {
        background-color: #11171d !important;
        color: #bdc3c7 !important;
        border-radius: 8px 8px 0px 0px !important;
        padding: 10px 20px !important;
        font-weight: 700 !important;
    }
    .stTabs [aria-selected="true"] {
        color: #A2FF00 !important;
        border-bottom-color: #A2FF00 !important;
    }
    
    /* 荧光绿主行动大按钮 */
    div.stButton > button:first-child {
        background-color: #A2FF00 !important;
        color: #0b0f12 !important;
        font-weight: 800 !important;
        font-size: 16px !important;
        width: 100%;
        border-radius: 12px !important;
        border: none !important;
        padding: 12px 0 !important;
        text-transform: uppercase;
        letter-spacing: 1px;
        box-shadow: 0 0 15px rgba(162, 255, 0, 0.4);
    }
    
    /* 灰黑色辅助/暂停按钮颜色 */
    div.stButton > button[key*="app_stop_btn"] {
        background-color: #0b0f12 !important;
        color: #ffffff !important;
        border: 1px solid #252e38 !important;
        box-shadow: none !important;
    }
    </style>
""", unsafe_allow_html=True)

# ==================== 🌐 TOP: 状态初始化与语言选择 ====================
if 'app_earned' not in st.session_state:
    st.session_state.app_earned = 1452.7000
if 'app_running' not in st.session_state:
    st.session_state.app_running = False
if 'chart_history' not in st.session_state:
    st.session_state.chart_history = [22.0, 25.0, 24.0, 28.0, 27.0, 31.0, 29.0, 33.0, 31.0, 35.0, 33.0, 36.8]

# 顶栏语言切换
lang_col1, lang_col2 = st.columns([3, 1])
with lang_col2:
    lang = st.selectbox("🌐 Language", ["English", "中文"], index=0, label_visibility="collapsed", key="top_lang_selector")

st.markdown("<div style='margin-top: -10px;'></div>", unsafe_allow_html=True)
st.markdown(f'<h1 style="text-align:center; color:#A2FF00; font-size:38px; font-weight:800; margin-bottom:0;">NexaEdge Network</h1>', unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# ==================== 🗺️ 核心双页签切换系统 ====================
tab1_title = "🌐 Overview & Pillars" if lang == "English" else "🌐 项目通识与壁垒"
tab2_title = "📱 Node Dashboard (Live)" if lang == "English" else "📱 边缘节点控制台 (实时)"

tab1, tab2 = st.tabs([tab1_title, tab2_title])

# =========================================================================
# 🏠 第一页：项目核心数据、壁垒、计算器 + 顶部原图背书
# =========================================================================
with tab1:
    if lang == "English":
        st.markdown('<p style="font-size: 18px; color: #bdc3c7; text-align: center; margin-top:10px; margin-bottom: 25px;">Transforming 5B+ idle smartphones into high-purity data fuel factories for the AI Era.</p>', unsafe_allow_html=True)

        # 🪐 核心一：第一页顶部完美展示你上传的手机渲染原图进行高逼格背书
        if os.path.exists("image.png"):
            st.image("image.png", caption="NexaEdge Mobile App Interface Preview", use_container_width=True)
        else:
            st.info("💡 请确保你的 GitHub 仓库中上传了名为 image.png 的图片文件")
        
        st.markdown("<br>", unsafe_allow_html=True)

        # 核心数据指标
        c1, c2, c3 = st.columns(3)
        with c1: st.metric(label="Network Fee", value="20%", delta="Pure Revenue Flow")
        with c2: st.metric(label="Safety Threshold", value="39°C", delta="Device Safety Lock", delta_color="inverse")
        with c3: st.metric(label="Settlement Base", value="Solana SPL", delta="Low Gas / High TPS")

        st.markdown("<hr style='border:1px solid #1e272e;'>", unsafe_allow_html=True)

        # 三大核心壁垒
        st.markdown('<h2 style="color:#A2FF00; font-size:24px;">⚡ Key Pillars</h2>', unsafe_allow_html=True)
        st.markdown("""
        <div class="feature-box">
            <h4 style="color:white; margin-top:0; font-size:17px;">📱 Passive Income via Charging</h4>
            <p style="color:#bdc3c7; font-size:13px;">Earn ~0.35 USDT/hr. Just plug in, connect Wi-Fi, and lock your screen. Our lightweight WASM Sandbox cleans AI datasets silently in the background.</p>
        </div>
        <div class="feature-box">
            <h4 style="color:white; margin-top:0; font-size:17px;">🔥 39°C Thermal Guard</h4>
            <p style="color:#bdc3c7; font-size:13px;">Total hardware protection. System auto-throttles computing loads instantly if the battery touches 39°C. Zero degradation anxiety.</p>
        </div>
        <div class="feature-box">
            <h4 style="color:white; margin-top:0; font-size:17px;">🤝 2:1 Anti-Cheat Verification</h4>
            <p style="color:#bdc3c7; font-size:13px;">Decentralized majority-voting consensus. We segment raw data across 3 independent nodes to deliver 100% verified datasets to AI clients.</p>
        </div>
        """, unsafe_allow_html=True)

    else:
        # 中文页面
        st.markdown('<p style="font-size: 17px; color: #bdc3c7; text-align: center; margin-top:10px; margin-bottom: 25px;">让全球 50 亿部闲置手机，成为 AI 时代的高纯度语料燃料工厂</p>', unsafe_allow_html=True)

        if os.path.exists("image.png"):
            st.image("image.png", caption="NexaEdge 手机端 App 真实视觉预览", use_container_width=True)

        st.markdown("<br>", unsafe_allow_html=True)

        c1, c2, c3 = st.columns(3)
        with c1: st.metric(label="平台技术抽成", value="20%", delta="纯现金流造血")
        with c2: st.metric(label="智能硬件风控", value="39°C", delta="秒级控温预警", delta_color="inverse")
        with c3: st.metric(label="算力结算底座", value="Solana SPL", delta="极速、低 Gas")

        st.markdown("<hr style='border:1px solid #1e272e;'>", unsafe_allow_html=True)

        st.markdown('<h2 style="color:#A2FF00; font-size:24px;">⚡ 核心壁垒</h2>', unsafe_allow_html=True)
        st.markdown("""
        <div class="feature-box">
            <h4 style="color:white; margin-top:0; font-size:17px;">📱 锁屏充电·睡后收入 (零门槛)</h4>
            <p style="color:#bdc3c7; font-size:13px;">每小时赚取约 0.35 USDT。用户只需在夜间充电、连接 Wi-Fi 并锁屏，NexaEdge 的轻量级 WASM 沙盒便会在后台静默运行清洗 AI 语料。</p>
        </div>
        <div class="feature-box">
            <h4 style="color:white; margin-top:0; font-size:17px;">🔥 独创：39°C 智能温控风控屏障</h4>
            <p style="color:#bdc3c7; font-size:13px;">坚守绝不伤机的底线。一旦手机运行温度触及 39°C 临界点，系统自动下发降载指令，彻底打消硬件损耗焦虑。</p>
        </div>
        """, unsafe_allow_html=True)

# =========================================================================
# 📱 第二页：完美复刻原图设计的手机高保真动态控制台
# =========================================================================
with tab2:
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 📱 渲染虚拟手机外壳组件
    st.markdown('<div class="app-container">', unsafe_allow_html=True)
    
    # ✨ 核心改进：在控制台顶部引入你图片中的原厂标志性 NexaEdge 六角形 LOGO 区域！
    if os.path.exists("image.png"):
        # 我们巧妙地截取图片上半部分或者直接等比美化展示 Logo
        st.image("image.png", use_container_width=True)
    
    st.markdown("<div style='margin-top: 15px;'></div>", unsafe_allow_html=True)
    
    # 📊 模块 1：DASHBOARD 面板（1:1 还原波动折线、温度计与 SAFE 标签）
    st.markdown('<div class="app-card">', unsafe_allow_html=True)
    st.markdown('<div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">'
                '<span class="app-title">DASHBOARD</span>'
                '<span style="color:#88929b; font-size:14px;">⚙️</span>'
                '</div>', unsafe_allow_html=True)
    
    current_hash = random.uniform(45.5, 49.8) if st.session_state.app_running else 0.0
    st.markdown(f'<div style="font-size:11px; color:#88929b; margin-bottom:5px;">NETWORK HASH RATE (MH/s): <span class="neon-green-text" style="font-weight:bold;">{current_hash:.2f}</span></div>', unsafe_allow_html=True)
    
    # 动态波动算力表
    if st.session_state.app_running:
        st.session_state.chart_history.pop(0)
        st.session_state.chart_history.append(current_hash)
    chart_df = pd.DataFrame(st.session_state.chart_history, columns=["Hash Rate"])
    st.area_chart(chart_df, height=75, use_container_width=True)
    
    # 🌡️ 完美复刻的温度计显示器
    current_temp = random.uniform(36.4, 36.9) if st.session_state.app_running else 31.2
    st.markdown(f"""
    <div class="temp-section">
        <div style="display:flex; align-items:center;">
            <span class="thermometer-icon">🌡️</span>
            <span class="app-value" style="font-size:22px;">{current_temp:.1f}°C</span>
        </div>
        <span style="background-color:#1e272e; color:#A2FF00; font-size:11px; font-weight:bold; padding:4px 10px; border-radius:12px; border:1px solid #A2FF00; letter-spacing:1px;">SAFE</span>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 🟢 模块 2：PARTICIPANT NODE 面板（还原 NODE_ID、ACTIVE 状态和 NEXA 收益）
    st.markdown('<div class="app-card">', unsafe_allow_html=True)
    st.markdown('<div class="app-title" style="margin-bottom:12px;">PARTICIPANT NODE ➔</div>', unsafe_allow_html=True)
    st.markdown('<div style="font-size:12px; color:#88929b; margin-bottom:12px;">NODE_ID: <span style="color:#ffffff; font-weight:bold;">@nexaedge / Acc1 (active)</span></div>', unsafe_allow_html=True)
    
    run_status = "ACTIVE" if st.session_state.app_running else "STANDBY"
    status_color = "#A2FF00" if st.session_state.app_running else "#88929b"
    
    st.markdown(f"""
    <div style="display:flex; justify-content:space-between; margin-bottom:5px;">
        <span style="font-size:11px; color:#88929b; font-weight:bold;">MINING STATUS:</span>
        <span style="font-size:11px; color:#88929b; font-weight:bold;">TOKEN EARNINGS:</span>
    </div>
    <div style="display:flex; justify-content:space-between; align-items:baseline;">
        <span style="color:{status_color}; font-size:15px; font-weight:800; letter-spacing:0.5px;">● {run_status}</span>
        <span class="app-value neon-green-text" style="font-size:24px;">{st.session_state.app_earned:,.1f} <span style="font-size:13px; color:#ffffff; font-weight:normal;">NEXA</span></span>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # 🕹️ 模块 3：WASM 实时动态协议日志
    st.markdown('<div class="app-card">', unsafe_allow_html=True)
    st.markdown(f'<div class="app-title">WASM KERNEL LOGS</div>', unsafe_allow_html=True)
    logs_pool = [
        "> [SYSTEM] WASM Sandbox connection stable.",
        "> [COMPUTE] Shard verification successful.",
        "> [SECURITY] Battery temperature locked at safe range.",
        "> [LEDGER] Pushing verified data blocks to Solana SPL."
    ]
    if st.session_state.app_running:
        st.markdown(f'<div class="app-log">{random.choice(logs_pool)}<br>{random.choice(logs_pool)}</div>', unsafe_allow_html=True)
        # 模拟真实的金币在线持续累加增多！
        st.session_state.app_earned += 0.125
        time.sleep(0.5)
        st.rerun()
    else:
        st.markdown(f'<div class="app-log">> Node sleeping.<br>> Tap START COMPUTE below to active node...</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # ⚡ 模块 4：完全匹配设计图的手机端交互大按钮
    if not st.session_state.app_running:
        if st.button("START COMPUTE SESSION", key="app_start_btn"):
            st.session_state.app_running = True
            st.rerun()
    else:
        if st.button("PAUSE SESSION (VIEW NETWORK MAP)", key="app_stop_btn"):
            st.session_state.app_running = False
            st.rerun()
            
    st.markdown('</div>', unsafe_allow_html=True) # 手机外壳结束

# ==================== 📧 底部白名单系统 ====================
st.markdown("<hr style='border:1px solid #1e272e;'>", unsafe_allow_html=True)
st.markdown(f'<h3 style="text-align:center; color:#A2FF00; font-size:22px;">{"🚀 Secure Your Early Whitelist Seat" if lang=="English" else "🚀 锁定早期测试网白名单席位"}</h3>', unsafe_allow_html=True)

with st.form("unified_whitelist_form"):
    u_email = st.text_input("Email Address" if lang=="English" else "您的电子邮箱:")
    u_wallet = st.text_input("Solana Wallet Address" if lang=="English" else "Solana 钱包地址:")
    submitted = st.form_submit_button("SUBMIT & RETAIN SEAT ⚡" if lang=="English" else "提交并归档体验收益 ⚡")
    if submitted:
        if u_email:
            st.balloons()
            st.success(f"🎯 Whitelisted! Saved with {st.session_state.app_earned:,.1f} $NEXA score!")
            with open("whitelist.txt", "a") as f:
                f.write(f"{u_email},{u_wallet},{st.session_state.app_earned:.4f}\n")

st.markdown("<br><p style='text-align:center; color:#445;'>NexaEdge Network © 2026 | Powered by Solana DePIN Infrastructure</p>", unsafe_allow_html=True)
