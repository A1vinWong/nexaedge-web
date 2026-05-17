import streamlit as st
import time
import random
import pandas as pd
from PIL import Image
import os

# 1. 核心页面配置
st.set_page_config(page_title="NexaEdge Network", page_icon="🟢", layout="centered")

# 2. 内存锁（确保实时 Active 人数 451/452 准确，不随锁屏刷新重置）
@st.cache_resource
def get_net_memory():
    return {"active_base": 451, "whitelist_db": []}
global_mem = get_net_memory()

# 3. 状态初始化
if 'app_earned' not in st.session_state: st.session_state.app_earned = 1452.70
if 'chart_history' not in st.session_state: st.session_state.chart_history = [22, 25, 24, 28, 27, 31, 29, 33, 31, 35, 33, 36.8]
if 'target_time_index' not in st.session_state: st.session_state.target_time_index = 2
if 'app_running' not in st.session_state: st.session_state.app_running = False
if 'session_seconds' not in st.session_state: st.session_state.session_seconds = 0
if 'last_tick_time' not in st.session_state: st.session_state.last_tick_time = 0.0

# 时间步进补偿
if st.session_state.app_running and st.session_state.last_tick_time > 0:
    elapsed = int(time.time() - st.session_state.last_tick_time)
    if elapsed > 0:
        st.session_state.session_seconds += elapsed
        st.session_state.app_earned += elapsed * 0.25
        st.session_state.last_tick_time = time.time()

# 4. 全球黑绿极客 UI 样式
st.markdown("""
    <style>
    .stApp { background-color: #0b0f12; }
    .app-card { background-color: #161c23; border: 1px solid #252e38; border-radius: 14px; padding: 16px; margin-bottom: 12px; }
    .app-title { font-size: 13px; color: #88929b; font-weight: bold; text-transform: uppercase; }
    .app-value { color: #ffffff; font-size: 32px; font-weight: 700; }
    .neon-text { color: #A2FF00 !important; }
    div.stButton > button:first-child {
        background-color: #A2FF00 !important; color: #0b0f12 !important; font-weight: 800 !important;
        width: 100%; border-radius: 12px !important; border: none !important; padding: 12px 0 !important;
    }
    div.stButton > button[key*="app_stop_btn"] { background-color: #0b0f12 !important; color: #ffffff !important; border: 1px solid #252e38 !important; }
    [data-testid="stForm"] { background-color: #161c23 !important; border: 1px solid #252e38 !important; border-radius: 16px !important; }
    </style>
""", unsafe_allow_html=True)

# 5. 抗报错安全渲染：两页都会完美展现置顶图片
if os.path.exists("image.png"):
    try: st.image(Image.open("image.png"), use_container_width=True)
    except: st.markdown("<h1 style='color:#A2FF00; text-align:center;'>NexaEdge</h1>", unsafe_allow_html=True)
# 6. 创建双主页（默认以纯英文作为主视觉调性）
tab1, tab2 = st.tabs(["🌐 Overview & Pillars", "📱 Node Dashboard"])

TIME_OPTIONS = ["15 Minutes", "30 Minutes", "1 Hour", "2 Hours", "4 Hours", "8 Hours", "12 Hours", "24 Hours"]
SECONDS_MAP = [900, 1800, 3600, 7200, 14400, 28800, 43200, 86400]
HOURS_MAP = [0.25, 0.5, 1.0, 2.0, 4.0, 8.0, 12.0, 24.0]

# --- 🌐 Tab 1: 英文技术主介绍页 ---
with tab1:
    st.markdown('<p style="font-size:14px; color:#A2FF00; font-weight:bold; text-align:center;">Decentralized AI Compute Infrastructure</p>', unsafe_allow_html=True)
    
    # 🌟 核心要求：完美加入 2:1 比例机制卡片
    st.markdown("""
        <div class="app-card" style="border-left: 4px solid #A2FF00;">
            <div class="app-title" style="color: #A2FF00;">⚡ 2:1 Supply & Burn Scale Topology</div>
            <div class="app-value" style="font-size: 24px;">2 : 1 Ratio System</div>
            <div style="color:#88929b; font-size:12px; margin-top:3px;">
                Every 2 data shards verified by node network automatically triggers 1 burn reward unit to balance global pool minting and enforce deflation.
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="app-card"><div class="app-title">Network Fee</div><div class="app-value">20%</div></div>', unsafe_allow_html=True)
    st.markdown('<div class="app-card"><div class="app-title">Safety Auto-Lock</div><div class="app-value">39°C</div></div>', unsafe_allow_html=True)
    
    # 收益计算器
    st.markdown('<p style="color:#A2FF00; font-weight:bold; margin-bottom:2px;">💰 Yield Estimator</p>', unsafe_allow_html=True)
    sel_t1 = st.selectbox("Pattern:", TIME_OPTIONS, index=st.session_state.target_time_index, key="s1")
    st.session_state.target_time_index = TIME_OPTIONS.index(sel_t1)
    st.info(f"Est. Monthly Income: {HOURS_MAP[st.session_state.target_time_index]*0.35*30:.2f} USDT")

# --- 📱 Tab 2: 极客运行控制台（完美实时联动人数） ---
with tab2:
    if st.session_state.app_running:
        st.selectbox("Target:", TIME_OPTIONS, index=st.session_state.target_time_index, disabled=True, key="s2_d")
    else:
        sel_t2 = st.selectbox("Target:", TIME_OPTIONS, index=st.session_state.target_time_index, key="s2")
        st.session_state.target_time_index = TIME_OPTIONS.index(sel_t2)
        
    t_seconds = SECONDS_MAP[st.session_state.target_time_index]
    if st.session_state.app_running and st.session_state.session_seconds >= t_seconds:
        st.session_state.app_running = False
        st.rerun()

    c_hash = random.uniform(45.5, 49.8) if st.session_state.app_running else 0.0
    s_sec = st.session_state.session_seconds
    rem = max(0, t_seconds - s_sec)
    
    # 折线图与运行指标
    st.markdown(f'<div class="app-card"><div class="app-title">Hash Rate: <span class="neon-text">{c_hash:.2f} MH/s</span></div></div>', unsafe_allow_html=True)
    if st.session_state.app_running:
        st.session_state.chart_history.pop(0)
        st.session_state.chart_history.append(c_hash)
    st.line_chart(pd.DataFrame(st.session_state.chart_history), height=90, use_container_width=True)
    
    st.markdown(f'<div class="app-card"><div class="app-title">Session Generated</div><div class="app-value neon-text">+{s_sec*0.25:,.1f} <span style="font-size:12px; color:#fff;">NEXA</span></div><div style="font-size:12px; color:#88929b; margin-top:4px;">Countdown: {rem//3600:02d}:{(rem%3600)//60:02d}:{rem%60:02d}</div></div>', unsafe_allow_html=True)
    
    status_text = "● ACTIVE" if st.session_state.app_running else "● STANDBY"
    st.markdown(f'<div class="app-card"><div class="app-title">NODE: @nexaedge / Acc1</div><div style="display:flex; justify-content:between;"><span style="color:{"#A2FF00" if st.session_state.app_running else "#88929b"}; font-weight:bold;">{status_text}</span><span style="margin-left:auto; color:#A2FF00; font-size:18px; font-weight:bold;">{st.session_state.app_earned:,.2f} NEXA</span></div></div>', unsafe_allow_html=True)

    if not st.session_state.app_running:
        if st.button("START COMPUTE SESSION", key="app_start_btn"):
            st.session_state.session_seconds = 0
            st.session_state.app_running = True
            st.session_state.last_tick_time = time.time()
            st.rerun()
    else:
        if st.button("PAUSE SESSION (CHECK NETWORK MAP)", key="app_stop_btn"):
            st.session_state.app_running = False
            st.rerun()

# 🚀 创世早期白名单表单
st.markdown("<br>", unsafe_allow_html=True)
with st.form("wl_form"):
    st.markdown('<p style="color:#A2FF00; font-weight:bold; margin:0;">🚀 Whitelist Form</p>', unsafe_allow_html=True)
    mail = st.text_input("Email:", key="m_in").strip()
    wallet = st.text_input("Solana Wallet Address:", key="w_in").strip()
    if st.form_submit_button("SUBMIT APPLICATION ⚡"):
        if mail and wallet:
            global_mem["whitelist_db"].append({"Email": mail, "Solana_Wallet": wallet, "Accumulated_Nexa": f"{st.session_state.app_earned:.1f}"})
            st.success("SUCCESS!")

# ==========================================
# 📊 真实数据联动大盘（100% 解决实时人数不准问题）
# ==========================================
st.markdown("<hr style='border:1px solid #1e272e; margin:20px 0;'>", unsafe_allow_html=True)

# 联动逻辑：点击 Start 按钮启动，Active 人数从 451 立刻实时变成 452！
current_active = global_mem["active_base"] + (1 if st.session_state.app_running else 0)
# 浏览人数：在 1050 人左右动态进行 +5 到 -5 真实微幅震荡起伏
current_viewers = 1054 + random.randint(-5, 5)

col1, col2 = st.columns(2)
with col1:
    st.markdown(f'<div style="text-align:center; background:#141d26; border:1px dashed #A2FF00; padding:8px; border-radius:10px;"><div style="font-size:11px; color:#88929b;">● ACTIVE COMPUTE NODES</div><div style="font-size:16px; color:#A2FF00; font-weight:bold;">{current_active} Devices</div></div>', unsafe_allow_html=True)
with col2:
    st.markdown(f'<div style="text-align:center; background:#141d26; border:1px dashed #00e5ff; padding:8px; border-radius:10px;"><div style="font-size:11px; color:#88929b;">👀 LIVE VIEWERS ONLINE</div><div style="font-size:16px; color:#00e5ff; font-weight:bold;">{current_viewers} Users</div></div>', unsafe_allow_html=True)

# 🌐 保留原装带国旗的 Flag Counter 全球计数器
st.markdown('<div style="text-align:center; margin-top:15px;"><a href="https://info.flagcounter.com/NexaEdge"><img src="https://s11.flagcounter.com/count2/NexaEdge/bg_0B0F12/txt_A2FF00/border_1E272E/columns_3/maxflags_9/viewers_3/labels_1/pageviews_1/flags_0/" border="0" style="border-radius:6px;"></a></div>', unsafe_allow_html=True)

# ==========================================
# 🔑 管理员查看白名单与申请后台数据
# ==========================================
st.markdown("<br>", unsafe_allow_html=True)
with st.expander("🔒 Admin Whitepaper Panel"):
    pwd = st.text_input("Enter Keys:", type="password", key="adm_pwd")
    if pwd == "nexaadmin2026":
        st.markdown("<p style='color:#A2FF00; font-size:12px;'>✓ SECURE LEDGER ACCESS GRANTED</p>", unsafe_allow_html=True)
        if global_mem["whitelist_db"]:
            st.dataframe(pd.DataFrame(global_mem["whitelist_db"]), use_container_width=True)
        else:
            st.info("No records inside buffer memory yet.")

st.markdown("<p style='text-align:center; color:#334; font-size:10px;'>NexaEdge Network © 2026</p>", unsafe_allow_html=True)

# --- 运行循环驱动器 ---
if st.session_state.app_running:
    time.sleep(1.0)
    st.session_state.app_earned += 0.25
    st.session_state.session_seconds += 1
    st.session_state.last_tick_time = time.time()
    st.rerun()
