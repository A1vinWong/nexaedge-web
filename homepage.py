import streamlit as st
import os
import time
import random
import numpy as np

# 1. 全局页面基础配置
st.set_page_config(
    page_title="NexaEdge Network | Official Node Gateway",
    page_icon="🟢",
    layout="centered"
)

# --- 🟢 像素级复刻：黑绿科技风全局 CSS 样式 ---
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
    }
    
    /* App 内部的黑色子模块小面板 */
    .app-card {
        background-color: #0b0f12;
        border: 1px solid #1e272e;
        border-radius: 14px;
        padding: 15px;
        margin-bottom: 15px;
        text-align: left;
    }
    
    /* 字体与高亮颜色 */
    .app-title { font-size: 14px; color: #88929b; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 5px; }
    .app-value { font-family: 'Courier New', monospace; color: #f5f5f5; font-size: 28px; font-weight: bold; }
    .neon-green-text { color: #A2FF00 !important; }
    
    /* 模拟日志终端 */
    .app-log {
        font-family: 'Courier New', monospace;
        color: #88929b;
        font-size: 11px;
        background-color: #000000;
        padding: 10px;
        border-radius: 8px;
        height: 65px;
        overflow-y: hidden;
        border: 1px solid #1e272e;
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
    }
    
    /* 灰黑色辅助按钮 */
    div.stButton > button[key*="stop"] {
        background-color: #1e272e !important;
        color: #ff4b4b !important;
        border: 1px solid #ff4b4b !important;
    }
    </style>
""", unsafe_allow_html=True)

# ==================== 🌐 TOP: 语言一键切换与状态初始化 ====================
if 'app_earned' not in st.session_state:
    st.session_state.app_earned = 1452.70000  # 像素级同步截图中的初始代币量
if 'app_running' not in st.session_state:
    st.session_state.app_running = False
if 'chart_data' not in st.session_state:
    st.session_state.chart_data = list(np.random.uniform(20, 50, 15))

lang_col1, lang_col2 = st.columns([3, 1])
with lang_col2:
    lang = st.selectbox(
        "🌐 Language", ["English", "中文"], index=0,
        label_visibility="collapsed", key="top_lang_selector"
    )

st.markdown("<div style='margin-top: -10px;'></div>", unsafe_allow_html=True)

# ==================== 🪐 LOGO 门面横幅 ====================
if os.path.exists("IMG_7651.jpeg"):
    st.image("IMG_7651.jpeg", use_container_width=True)
else:
    st.markdown(f'<h1 style="text-align:center; color:#A2FF00; font-size:38px; font-weight:800; margin-bottom:0;">NexaEdge Network</h1>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ==================== 🗺️ 核心多页签系统 (Tabs) ====================
# 中英文动态标签菜单
tab1_title = "🌐 Overview & Pillars" if lang == "English" else "🌐 项目通识与壁垒"
tab2_title = "📱 Node Dashboard (Live)" if lang == "English" else "📱 边缘节点控制台 (实时)"

tab1, tab2 = st.tabs([tab1_title, tab2_title])

# =========================================================================
# 🏠 第一页：完整的项目官方硬核介绍与量化计算器
# =========================================================================
with tab1:
    if lang == "English":
        st.markdown('<p style="font-size: 18px; color: #bdc3c7; text-align: center; margin-top:10px; margin-bottom: 25px;">Transforming 5B+ idle smartphones into high-purity data fuel factories for the AI Era.</p>', unsafe_allow_html=True)

        # 核心数据流
        c1, c2, c3 = st.columns(3)
        with c1: st.metric(label="Network Fee", value="20%", delta="Pure Revenue Flow")
        with c2: st.metric(label="Safety Threshold", value="39°C", delta="Device Safety Lock", delta_color="inverse")
        with c3: st.metric(label="Settlement Base", value="Solana SPL", delta="Low Gas / High TPS")

        st.markdown("<hr style='border:1px solid #1e272e;'>", unsafe_allow_html=True)

        # 三大壁垒
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

        st.markdown("<hr style='border:1px solid #1e272e;'>", unsafe_allow_html=True)

        # 计算器
        st.markdown('<h2 style="color:#A2FF00; font-size:24px;">🧮 Interactive Yield Calculator</h2>', unsafe_allow_html=True)
        role = st.selectbox("Select Your Role:", ["Node Operator (Retail User)", "AI Enterprise Client (Data Buyer)"], key="role_en")
        if "Retail" in role:
            hours = st.slider("Estimated Overnight Duration (Hours/Day):", 1, 12, 6, key="hr_en")
            device = st.radio("Operating System:", ["iOS (iPhone)", "Android"], key="dev_en")
            monthly_earn = hours * (0.35 if "iOS" in device else 0.30) * 30
            st.success(f"🎉 Estimated Monthly Yield: **{monthly_earn:.2f} USDT**")
        else:
            gb = st.number_input("Dataset Size Required (GB):", min_value=1, value=100, key="gb_en")
            st.warning(f"💼 Total Procurement Budget: **{gb * 6.0:.2f} USD**")

    else:
        # 中文完整介绍
        st.markdown('<p style="font-size: 17px; color: #bdc3c7; text-align: center; margin-top:10px; margin-bottom: 25px;">让全球 50 亿部闲置手机，成为 AI 时代的高纯度语料燃料工厂</p>', unsafe_allow_html=True)

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
        <div class="feature-box">
            <h4 style="color:white; margin-top:0; font-size:17px;">🤝 B端：2:1 多数表决防作弊机制</h4>
            <p style="color:#bdc3c7; font-size:13px;">原始语料切块多点分发，通过 3 节点冗余计算。平台采用去中心化的多数表决机制，彻底过滤模拟器行为，交付 100% 验证的数据集。</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<hr style='border:1px solid #1e272e;'>", unsafe_allow_html=True)

        st.markdown('<h2 style="color:#A2FF00; font-size:24px;">🧮 生态双向收益计算器</h2>', unsafe_allow_html=True)
        role = st.selectbox("请选择您的身份：", ["我是手机持有者 (C端算力提供方)", "我是 AI 大模型厂商 (B端算力购买方)"], key="role_zh")
        if "C端" in role:
            hours = st.slider("预估您每天夜间挂机打工的小时数：", 1, 12, 6, key="hr_zh")
            device = st.radio("您的设备系统：", ["iOS 苹果手机", "Android 安卓手机"], key="dev_zh")
            monthly_earn = hours * (0.35 if "iOS" in device else 0.30) * 30
            st.success(f"🎉 一个月累计可躺赚 **{monthly_earn:.2f} USDT**")
        else:
            data_need = st.number_input("您需要清洗的语料大小 (GB):", min_value=1, value=100, key="gb_zh")
            st.warning(f"💼 您的算力采购预算总计：**{data_need * 6.0:.2f} USD**")

# =========================================================================
# 📱 第二页：像素级复刻手机端控制台交互体验
# =========================================================================
with tab2:
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 📱 渲染虚拟手机外壳
    st.markdown('<div class="app-container">', unsafe_allow_html=True)
    
    # 模块 1：DASHBOARD & 实时算力折线图
    st.markdown('<div class="app-card">', unsafe_allow_html=True)
    current_hash = random.uniform(42.5, 48.9) if st.session_state.app_running else 0.0
    st.markdown(f'<div class="app-title">DASHBOARD</div>', unsafe_allow_html=True)
    st.markdown(f'<div style="font-size:11px; color:#88929b; margin-bottom:10px;">NETWORK HASH RATE (MH/s): <span class="neon-green-text" style="font-weight:bold;">{current_hash:.2f}</span></div>', unsafe_allow_html=True)
    
    # 渲染波动的实时算力折线图（复刻截图中的折线走势）
    if st.session_state.app_running:
        st.session_state.chart_data.pop(0)
        st.session_state.chart_data.append(current_hash)
    st.sparkline(st.session_state.chart_data, height=60)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 模块 2：智能硬件控温面板
    st.markdown('<div class="app-card">', unsafe_allow_html=True)
    current_temp = random.uniform(36.2, 37.1) if st.session_state.app_running else 31.2
    st.markdown(f'<div class="app-title">THERMAL STATUS</div>', unsafe_allow_html=True)
    status_label = "SAFE" if current_temp < 38 else "WARNING"
    st.markdown(f"""
    <div style="display:flex; justify-content:space-between; align-items:center;">
        <div class="app-value {'neon-green-text' if status_label=='SAFE' else ''}">{current_temp:.1f}°C</div>
        <div style="background-color:#1e272e; color:#A2FF00; font-size:11px; font-weight:bold; padding:3px 8px; border-radius:5px; border:1px solid #A2FF00;">{status_label}</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 模块 3：当前节点运行状态与实时收益
    st.markdown('<div class="app-card">', unsafe_allow_html=True)
    st.markdown(f'<div class="app-title">PARTICIPANT NODE</div>', unsafe_allow_html=True)
    st.markdown('<div style="font-size:12px; color:#f5f5f5; margin-bottom:8px;">NODE_ID: <span style="color:#bdc3c7;">@nexaedge / Acc1 (active)</span></div>', unsafe_allow_html=True)
    
    run_status = "ACTIVE" if st.session_state.app_running else "STANDBY"
    status_color = "#A2FF00" if st.session_state.app_running else "#88929b"
    
    st.markdown(f"""
    <div style="display:flex; justify-content:space-between; margin-bottom:5px;">
        <span style="font-size:11px; color:#88929b;">MINING STATUS:</span>
        <span style="font-size:11px; color:#88929b;">TOKEN EARNINGS:</span>
    </div>
    <div style="display:flex; justify-content:space-between; align-items:baseline;">
        <span style="color:{status_color}; font-size:14px; font-weight:bold;">🟢 {run_status}</span>
        <span class="app-value neon-green-text" style="font-size:24px;">{st.session_state.app_earned:,.4f} <span style="font-size:12px; color:#bdc3c7;">NEXA</span></span>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # 模块 4：底层协议运行日志流组件
    st.markdown('<div class="app-card">', unsafe_allow_html=True)
    st.markdown(f'<div class="app-title">WASM KERNEL LOGS</div>', unsafe_allow_html=True)
    logs_pool = [
        "> [SYSTEM] WASM Core loaded successfully.",
        "> [NETWORK] P2P Node handshake completed on Solana.",
        "> [COMPUTE] Shard #4412 text data filtering via CPU...",
        "> [SECURITY] Battery telemetry verified: Normal.",
        "> [LEDGER] Submitting epoch proof of work to Solana SPL."
    ]
    if st.session_state.app_running:
        st.markdown(f'<div class="app-log">{random.choice(logs_pool)}<br>{random.choice(logs_pool)}</div>', unsafe_allow_html=True)
        # 实时挂机增加代币
        st.session_state.app_earned += 0.0042
        time.sleep(0.4)
        st.rerun()
    else:
        st.markdown(f'<div class="app-log">> Device node sleeping.<br>> Click button below to mount cluster...</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 📱 核心交互大按钮
    if not st.session_state.app_running:
        if st.button("START COMPUTE SESSION" if lang=="English" else "开始执行算力任务", key="app_start_btn"):
            st.session_state.app_running = True
            st.rerun()
    else:
        if st.button("PAUSE SESSION" if lang=="English" else "暂停算力任务", key="app_stop_btn"):
            st.session_state.app_running = False
            st.rerun()
            
    st.markdown('</div>', unsafe_allow_html=True) # 手机外壳结束

# ==================== 📧 底部统一白名单表单 ====================
st.markdown("<hr style='border:1px solid #1e272e;'>", unsafe_allow_html=True)
st.markdown(f'<h3 style="text-align:center; color:#A2FF00; font-size:22px;">{"🚀 Secure Your Early Whitelist Seat" if lang=="English" else "🚀 锁定早期测试网白名单席位"}</h3>', unsafe_allow_html=True)

with st.form("unified_whitelist_form"):
    u_email = st.text_input("Email Address" if lang=="English" else "您的电子邮箱:")
    u_wallet = st.text_input("Solana Wallet Address (Optional)" if lang=="English" else "Solana 钱包地址 (选填):")
    submitted = st.form_submit_button("SUBMIT & RETAIN SEAT ⚡" if lang=="English" else "提交并归档体验收益 ⚡")
    if submitted:
        if u_email:
            st.balloons()
            st.success(f"🎯 Whitelisted! Saved with {st.session_state.app_earned:,.2f} $NEXA score!")
            with open("whitelist.txt", "a") as f:
                f.write(f"{u_email},{u_wallet},{st.session_state.app_earned:.4f}\n")
        else:
            st.error("Please enter a valid email." if lang=="English" else "请输入有效的电子邮箱。")

st.markdown("<br><p style='text-align:center; color:#445;'>NexaEdge Network © 2026 | Powered by Solana DePIN Infrastructure</p>", unsafe_allow_html=True)

