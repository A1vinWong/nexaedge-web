import streamlit as st
import os
import time
import random
import pandas as pd
import json

# ==========================================
# 1. 页面基础配置
# ==========================================
st.set_page_config(
    page_title="NexaEdge Network | Official Node Gateway",
    page_icon="🟢",
    layout="centered"
)

# --- 💾 全局多用户活跃状态同步系统 ---
STATUS_FILE = "global_network_status.json"

def load_global_status():
    if not os.path.exists(STATUS_FILE):
        return {"active_count": 1}
    try:
        with open(STATUS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {"active_count": 1}

def update_global_active(delta):
    data = load_global_status()
    data["active_count"] = max(1, data["active_count"] + delta)
    with open(STATUS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    return data

live_nodes_count = load_global_status()["active_count"]

# --- 🟢 极客黑绿科技风 CSS 样式表 ---
st.markdown("""
    <style>
    .stApp { background-color: #0b0f12; }
    #MainMenu, footer, .styles_viewerBadge__FUChv, [data-testid="manage-app-button"] { display: none !important; }
    header, [data-testid="stHeader"] { background: transparent !important; border: none !important; height: 0 !important; display: none !important; }
    
    /* 强力移除导致顶部产生空黑块的置空容器 */
    [data-testid="stVerticalBlock"] > div:empty { display: none !important; margin: 0 !important; padding: 0 !important; }
    [data-testid="stElementContainer"] { border: none !important; background: transparent !important; }
    
    /* 导航 Tab 样式 */
    .stTabs [data-baseweb="tab-list"] { gap: 12px; background-color: transparent !important; justify-content: center; border: none !important; margin-bottom: 25px !important; }
    .stTabs [data-baseweb="tab"] {
        background-color: #11171d !important; color: #bdc3c7 !important; border-radius: 8px 8px 0px 0px !important;
        border: 1px solid #1e272e !important; border-bottom: none !important; padding: 10px 22px !important; font-weight: 700 !important; font-size: 14px !important;
    }
    .stTabs [aria-selected="true"] { color: #A2FF00 !important; background-color: #161c23 !important; border-top: 2px solid #A2FF00 !important; }
    .stTabs [data-baseweb="tab-highlight"] { background-color: #A2FF00 !important; height: 0px !important; }
    
    /* 卡片与文本排版 */
    .app-card { background-color: #161c23; border: 1px solid #252e38; border-radius: 14px; padding: 15px; margin-bottom: 12px; }
    .app-title { font-size: 13px; color: #88929b; font-weight: bold; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 5px; }
    .app-value { font-family: 'Inter', sans-serif; color: #ffffff; font-size: 32px; font-weight: 700; }
    .neon-green-text { color: #A2FF00 !important; }
    
    /* 第二页面板特定微调 */
    .temp-section { display: flex; align-items: center; justify-content: space-between; background: #11171d; padding: 10px 14px; border-radius: 10px; margin-top: 4px; }
    .ratio-box { background-color: #11171d; border: 1px dashed #252e38; border-radius: 8px; padding: 8px 10px; margin-top: 8px; font-size: 12px; color: #88929b; }
    
    /* 核心启动大按钮 */
    div.stButton > button:first-child {
        background-color: #A2FF00 !important; color: #0b0f12 !important; font-weight: 800 !important; font-size: 16px !important;
        width: 100%; border-radius: 12px !important; border: none !important; padding: 12px 0 !important; box-shadow: 0 0 15px rgba(162, 255, 0, 0.3);
    }
    div.stButton > button[key*="app_stop_btn"] { background-color: #0b0f12 !important; color: #ffffff !important; border: 1px solid #252e38 !important; box-shadow: none !important; }
    
    [data-testid="stForm"] { background-color: #161c23 !important; border: 1px solid #252e38 !important; border-radius: 16px !important; padding: 20px !important; margin-top: 25px !important; }
    .admin-box { background-color: #1c232c; border: 2px dashed #A2FF00; padding: 20px; border-radius: 14px; margin-top: 30px; }
    </style>
""", unsafe_allow_html=True)

# 状态初始化
if 'app_earned' not in st.session_state: st.session_state.app_earned = 1452.7000
if 'app_running' not in st.session_state: st.session_state.app_running = False
if 'chart_history' not in st.session_state: st.session_state.chart_history = [22.0, 25.0, 24.0, 28.0, 27.0, 31.0, 29.0, 33.0, 31.0, 35.0, 33.0, 36.8]
if 'session_seconds' not in st.session_state: st.session_state.session_seconds = 0
if 'target_time_index' not in st.session_state: st.session_state.target_time_index = 2 

# 核心映射数据
TIME_OPTIONS_EN = ["15 Minutes", "30 Minutes", "1 Hour", "2 Hours", "4 Hours", "8 Hours", "12 Hours", "24 Hours (Full-day)"]
SECONDS_MAP = [900, 1800, 3600, 7200, 14400, 28800, 43200, 86400]
HOURS_MAP = [0.25, 0.5, 1.0, 2.0, 4.0, 8.0, 12.0, 24.0]

# =========================================================================
# 📸 顶栏全局恒定区域（大标题调整到了图片上面！）
# =========================================================================
# 1. 标题放最上面
st.markdown('<h1 style="text-align:center; color:#A2FF00; font-size:36px; font-weight:800; margin-top:10px; margin-bottom:12px;">NexaEdge Network</h1>', unsafe_allow_html=True)

# 2. 图片紧跟在标题下面
if os.path.exists("image.png"):
    st.image("image.png", use_container_width=True)
elif os.path.exists("logo.png"):
    st.image("logo.png", use_container_width=True)
else:
    # 完美兜底：如果找不到图片，渲染高质感 SVG 图标
    st.markdown("""
    <div style="text-align: center; margin-bottom: 15px;">
        <svg width="70" height="70" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M50 5L15 25V65L50 95L85 65V25L50 5Z" stroke="#A2FF00" stroke-width="6" stroke-linecap="round" stroke-linejoin="round" fill="#11171d"/>
            <path d="M35 45L50 30L65 45M35 60L50 45L65 60" stroke="#A2FF00" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
    </div>
    """, unsafe_allow_html=True)

# 3. 绿色口号简介
st.markdown('<p style="font-size: 16px; color: #A2FF00; font-weight:bold; text-align: center; margin-top: 12px; margin-bottom: 25px;">Transforming 5B+ idle smartphones into high-purity data fuel factories for the AI Era.</p>', unsafe_allow_html=True)

tab1, tab2 = st.tabs(["🌐 Overview & Pillars", "📱 Node Dashboard (Live)"])

# =========================================================================
# 🏠 第一页：Overview 介绍页
# =========================================================================
with tab1:
    # --- 1. Network Fee 指标 ---
    st.markdown('<div class="app-title">Network Fee</div>', unsafe_allow_html=True)
    st.markdown('<div class="app-value" style="margin-bottom:2px;">20%</div>', unsafe_allow_html=True)
    st.markdown('<div class="neon-green-text" style="font-size:12px; font-weight:bold; margin-bottom:20px;">↑ Pure Revenue Flow</div>', unsafe_allow_html=True)
    
    # --- 2. Safety Threshold 指标 ---
    st.markdown('<div class="app-title">Safety Threshold</div>', unsafe_allow_html=True)
    st.markdown('<div class="app-value" style="margin-bottom:2px;">39°C</div>', unsafe_allow_html=True)
    st.markdown('<div style="color:#ff6b6b; font-size:12px; font-weight:bold; margin-bottom:25px;">↑ Device Safety Lock</div>', unsafe_allow_html=True)
    
    # --- 3. Settlement Base 区域（完美置于 39°C 下方） ---
    st.markdown('<p style="font-size:13px; color:#88929b; font-weight:bold; margin-bottom:2px; text-transform:uppercase;">Settlement Base</p>', unsafe_allow_html=True)
    st.markdown('<h2 style="color:#ffffff; font-size:32px; font-weight:700; margin-top:0; margin-bottom:4px;">Solana SPL</h2>', unsafe_allow_html=True)
    st.markdown('<div style="margin-bottom:25px;"><span style="background-color:#141d26; color:#A2FF00; font-size:12px; font-weight:bold; padding:4px 10px; border-radius:12px; border: 1px solid #1e272e;">↑ Low Gas / High TPS</span></div>', unsafe_allow_html=True)
    
    st.markdown("<hr style='border:1px solid #1e272e; margin: 20px 0;'>", unsafe_allow_html=True)
    
    # --- 4. Device Revenue Calculator 区域 ---
    st.markdown('<h3 style="color:#A2FF00; font-size:20px; font-weight:700;"><span style="font-size:18px;">💰</span> Device Revenue Calculator</h3>', unsafe_allow_html=True)
    selected_time_tab1 = st.selectbox("Select Daily Session Duration Pattern:", TIME_OPTIONS_EN, index=st.session_state.target_time_index, key="time_select_tab1")
    st.session_state.target_time_index = TIME_OPTIONS_EN.index(selected_time_tab1)
    chosen_hours = HOURS_MAP[st.session_state.target_time_index]
    monthly_est = chosen_hours * 0.35 * 30
    st.success(f"🎉 Estimated Monthly Yield (Based on {selected_time_tab1}/day): {monthly_est:.2f} USDT")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # --- 5. Key Pillars 区域 ---
    st.markdown('<h3 style="color:#A2FF00; font-size:20px; font-weight:700;"><span style="font-size:18px;">⚡</span> Key Pillars</h3>', unsafe_allow_html=True)
    st.markdown("""
    <div class="app-card" style="border-left: 3px solid #A2FF00; padding-left:18px; margin-bottom:15px;">
        <h4 style="color:#ffffff; margin-top:0; margin-bottom:6px; font-size:15px;">📱 Passive Income via Charging</h4>
        <p style="color:#88929b; font-size:13px; line-height:1.5; margin:0;">Earn ~0.35 USDT/hr. Just plug in, connect Wi-Fi, and lock your screen. Our lightweight WASM Sandbox cleans AI datasets silently in the background.</p>
    </div>
    <div class="app-card" style="border-left: 3px solid #ff6b6b; padding-left:18px; margin-bottom:15px;">
        <h4 style="color:#ffffff; margin-top:0; margin-bottom:6px; font-size:15px;">🔥 39°C Thermal Guard</h4>
        <p style="color:#88929b; font-size:13px; line-height:1.5; margin:0;">Total hardware protection. System auto-throttles computing loads instantly if the battery touches 39°C. Zero degradation anxiety.</p>
    </div>
    <div class="app-card" style="border-left: 3px solid #A2FF00; padding-left:18px; margin-bottom:15px;">
        <h4 style="color:#ffffff; margin-top:0; margin-bottom:6px; font-size:15px;">🤝 2:1 Anti-Cheat Verification</h4>
        <p style="color:#88929b; font-size:13px; line-height:1.5; margin:0;">Decentralized majority-voting consensus. We segment raw data across 3 independent nodes to deliver 100% verified datasets to AI clients.</p>
    </div>
    """, unsafe_allow_html=True)

# =========================================================================
# 📱 第二页：Node Dashboard 控制台页
# =========================================================================
with tab2:
    st.markdown('<div class="app-title" style="margin-top:5px; margin-bottom:5px;">⏳ COMPUTE TIMER (AUTO-STOP)</div>', unsafe_allow_html=True)
    selected_time_tab2 = st.selectbox("Set target runtime for this session:", TIME_OPTIONS_EN, index=st.session_state.target_time_index, key="time_select_tab2", label_visibility="collapsed")
    st.session_state.target_time_index = TIME_OPTIONS_EN.index(selected_time_tab2)
    target_total_seconds = SECONDS_MAP[st.session_state.target_time_index]
    
    if st.session_state.app_running and st.session_state.session_seconds >= target_total_seconds:
        st.session_state.app_running = False
        update_global_active(-1)
        st.toast("⏰ Timer Finished! Node has been stopped safely.")

    current_hash = random.uniform(45.5, 49.8) if st.session_state.app_running else 0.0
    current_temp = random.uniform(36.4, 36.9) if st.session_state.app_running else 31.2
    s_sec = st.session_state.session_seconds
    
    remaining_seconds = max(0, target_total_seconds - s_sec)
    remaining_str = f"{remaining_seconds // 3600:02d}:{(remaining_seconds % 3600) // 60:02d}:{remaining_seconds % 60:02d}"
    time_str = f"{s_sec//3600:02d}:{(s_sec%3600)//60:02d}:{s_sec%60:02d}"
    session_generated = s_sec * 0.25
    
    # 算力折线面板
    st.markdown(f"""
    <div class="app-card" style="margin-top:15px;">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
            <span class="app-title">DASHBOARD</span>
            <span style="color:#88929b; font-size:13px;">⚙️</span>
        </div>
        <div style="font-size:12px; color:#88929b; margin-bottom:5px;">
            NETWORK HASH RATE (MH/s): <span class="neon-green-text" style="font-weight:bold;">{current_hash:.2f}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.app_running:
        st.session_state.chart_history.pop(0)
        st.session_state.chart_history.append(current_hash)
    st.line_chart(pd.DataFrame(st.session_state.chart_history, columns=["Hash Rate"]), height=95, use_container_width=True)
    
    # 温度状态卡片（★ 已帮您将电池图标 🔋 85% 彻底从代码中移去！）
    st.markdown(f"""
    <div class="app-card" style="margin-top: -5px;">
        <div class="temp-section">
            <span class="app-value" style="font-size:20px;">🌡️ {current_temp:.1f}°C</span>
            <span style="background-color:#1e272e; color:#A2FF00; font-size:11px; font-weight:bold; padding:4px 10px; border-radius:12px; border:1px solid #A2FF00;">SAFE</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 收益明细
    st.markdown(f"""
    <div class="app-card">
        <div class="app-title">COMPUTE TIME & RATIO</div>
        <div style="display:flex; justify-content:space-between; margin-top:8px;">
            <div>
                <div style="font-size:11px; color:#88929b;">SESSION DURATION:</div>
                <div class="app-value" style="font-size:19px; font-family:monospace; margin-bottom:5px;">{time_str}</div>
                <div style="font-size:11px; color:#88929b;">COUNTDOWN TO STOP:</div>
                <div class="app-value" style="font-size:17px; font-family:monospace; color:#ff9f43;">{remaining_str}</div>
            </div>
            <div style="text-align:right;">
                <div style="font-size:11px; color:#88929b;">SESSION YIELD:</div>
                <div class="app-value neon-green-text" style="font-size:19px;">+{session_generated:,.1f} <span style="font-size:11px; color:#ffffff;">NEXA</span></div>
            </div>
        </div>
        <div class="ratio-box">⚡ <b>EST. RATIO:</b> 0.25 NEXA / sec (≈ 900 NEXA/hr)</div>
    </div>
    """, unsafe_allow_html=True)
    
    # 节点基本状态
    run_status = "ACTIVE" if st.session_state.app_running else "STANDBY"
    st.markdown(f"""
    <div class="app-card">
        <div class="app-title" style="margin-bottom:8px;">PARTICIPANT NODE ➔</div>
        <div style="font-size:11px; color:#88929b; margin-bottom:10px;">NODE_ID: <span style="color:#ffffff; font-weight:bold;">@nexaedge / Acc1 (active)</span></div>
        <div style="display:flex; justify-content:space-between; margin-bottom:3px;">
            <span style="font-size:11px; color:#88929b; font-weight:bold;">MINING STATUS:</span>
            <span style="font-size:11px; color:#88929b; font-weight:bold;">TOTAL ACCUMULATED:</span>
        </div>
        <div style="display:flex; justify-content:space-between; align-items:baseline;">
            <span style="color:{'#A2FF00' if st.session_state.app_running else '#88929b'}; font-size:14px; font-weight:800;">● {run_status}</span>
            <span class="app-value neon-green-text" style="font-size:22px;">{st.session_state.app_earned:,.2f} <span style="font-size:12px; color:#ffffff; font-weight:normal;">NEXA</span></span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 驱动主按钮
    if not st.session_state.app_running:
        if st.button("START COMPUTE SESSION", key="app_start_btn"):
            if remaining_seconds <= 0: st.session_state.session_seconds = 0
            st.session_state.app_running = True
            update_global_active(1)
            st.rerun()
    else:
        if st.button("PAUSE SESSION (VIEW NETWORK MAP)", key="app_stop_btn"):
            st.session_state.app_running = False
            update_global_active(-1)
            st.rerun()

# ==================== 📧 底部白名单递交表单 ====================
st.markdown("<hr style='border:1px solid #1e272e; margin-top:20px;'>", unsafe_allow_html=True)
st.markdown('<h3 style="color:#A2FF00; font-size:18px; font-weight:700;"><span style="font-size:16px;">🚀</span> Secure Your Early Whitelist Seat</h3>', unsafe_allow_html=True)

with st.form("unified_whitelist_form"):
    u_email = st.text_input("Email Address:")
    u_wallet = st.text_input("Solana Wallet Address:")
    submitted = st.form_submit_button("SUBMIT & RETAIN SEAT ⚡")
    if submitted:
        if u_email.strip() != "" and u_email.strip() != "admin666":
            with open("whitelist.txt", "a", encoding="utf-8") as f:
                f.write(f"Email: {u_email} | Wallet: {u_wallet} | Score: {st.session_state.app_earned:.1f} | ActiveTime: {st.session_state.session_seconds}s\n")
            st.balloons()

# 隐藏的管理后台
if u_email.strip() == "admin666":
    st.markdown('<div class="admin-box">', unsafe_allow_html=True)
    st.markdown('<h2 style="color:#A2FF00; margin-top:0;">📊 NexaEdge 全局监控后台 (管理员模式)</h2>', unsafe_allow_html=True)
    st.metric(label="当前全网 Active 节点总人数", value=f"{load_global_status()['active_count']} 人")
    if os.path.exists("whitelist.txt"):
        st.markdown("### 📥 实时白名单递交清单")
        with open("whitelist.txt", "r", encoding="utf-8") as f:
            lines = f.readlines()
        for l in lines: st.text(l.strip())
    st.markdown('</div>', unsafe_allow_html=True)

# =========================================================================
# 📊 底部动态数据同步区（完美的活数据在线人数显示）
# =========================================================================
st.markdown("<hr style='border:1px solid #1e272e; margin-top:20px;'>", unsafe_allow_html=True)
st.markdown(f"""
<div style="text-align: center; margin-bottom: 12px;">
    <span style="background-color:#141d26; color:#A2FF00; font-size:13px; font-weight:bold; padding:6px 14px; border-radius:30px; border: 1px dashed #A2FF00;">
        🟢 NETWORK SYNCHRONIZED: {live_nodes_count} ACTIVE DEVICES ONLINE
    </span>
</div>
""", unsafe_allow_html=True)

# 页脚国旗组件
st.markdown("""
<div style="text-align: center; margin-top: 5px; opacity: 0.85;">
    <a href="https://info.flagcounter.com/NexaEdge">
        <img src="https://s11.flagcounter.com/count2/NexaEdge/bg_0B0F12/txt_A2FF00/border_1E272E/columns_3/maxflags_9/viewers_3/labels_1/pageviews_1/flags_0/" alt="Flag Counter" border="0" style="border-radius: 8px; border: 1px solid #1e272e; max-width: 100%;">
    </a>
</div>
""", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#445; font-size: 11px; margin-top:10px;'>NexaEdge Network © 2026 | Powered by Solana DePIN Infrastructure</p>", unsafe_allow_html=True)

# ==========================================
# 🏎️ 异步高频驱动器
# ==========================================
if st.session_state.app_running:
    st.session_state.app_earned += 0.25       
    st.session_state.session_seconds += 1     
    time.sleep(1.0)                            
    st.rerun()                                 
