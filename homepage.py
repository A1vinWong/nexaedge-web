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

# --- 📸 智能图片摄入系统 ---
def get_project_image():
    if os.path.exists("image.png"):
        return "image.png"
    png_files = glob.glob("*.png")
    if png_files:
        return png_files[0]
    return None

target_image = get_project_image()

# --- 🟢 极客黑绿科技风 1:1 还原 CSS 样式 ---
st.markdown("""
    <style>
    .stApp { background-color: #0b0f12; }
    .feature-box {
        background-color: #11171d; 
        padding: 20px; 
        border-radius: 10px; 
        border-left: 5px solid #A2FF00; 
        margin-bottom: 20px;
    }
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
    .app-card {
        background-color: #161c23;
        border: 1px solid #252e38;
        border-radius: 16px;
        padding: 18px;
        margin-bottom: 15px;
        text-align: left;
    }
    .app-title { font-size: 14px; color: #88929b; font-weight: bold; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 5px; }
    .app-value { font-family: 'Inter', sans-serif; color: #ffffff; font-size: 26px; font-weight: 700; }
    .neon-green-text { color: #A2FF00 !important; }
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
    .temp-section {
        display: flex;
        align-items: center;
        justify-content: space-between;
        background: #11171d;
        padding: 10px 15px;
        border-radius: 12px;
        margin-top: 10px;
    }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; justify-content: center; }
    .stTabs [data-baseweb="tab"] {
        background-color: #11171d !important;
        color: #bdc3c7 !important;
        border-radius: 8px 8px 0px 0px !important;
        padding: 10px 20px !important;
        font-weight: 700 !important;
    }
    .stTabs [aria-selected="true"] { color: #A2FF00 !important; border-bottom-color: #A2FF00 !important; }
    div.stButton > button:first-child {
        background-color: #A2FF00 !important;
        color: #0b0f12 !important;
        font-weight: 800 !important;
        font-size: 16px !important;
        width: 100%;
        border-radius: 12px !important;
        border: none !important;
        padding: 12px 0 !important;
        box-shadow: 0 0 15px rgba(162, 255, 0, 0.4);
    }
    div.stButton > button[key*="app_stop_btn"] {
        background-color: #0b0f12 !important;
        color: #ffffff !important;
        border: 1px solid #252e38 !important;
        box-shadow: none !important;
    }
    </style>
""", unsafe_allow_html=True)

# 状态初始化
if 'app_earned' not in st.session_state: st.session_state.app_earned = 1452.7000
if 'app_running' not in st.session_state: st.session_state.app_running = False
if 'chart_history' not in st.session_state: st.session_state.chart_history = [22.0, 25.0, 24.0, 28.0, 27.0, 31.0, 29.0, 33.0, 31.0, 35.0, 33.0, 36.8]

st.markdown(f'<h1 style="text-align:center; color:#A2FF00; font-size:38px; font-weight:800; margin-bottom:0;">NexaEdge Network</h1>', unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["🌐 Overview & Pillars", "📱 Node Dashboard (Live)"])

# =========================================================================
# 🏠 第一页
# =========================================================================
with tab1:
    st.markdown('<p style="font-size: 18px; color: #bdc3c7; text-align: center; margin-bottom: 25px;">Transforming 5B+ idle smartphones into high-purity data fuel factories for the AI Era.</p>', unsafe_allow_html=True)

    # 📸 第一页摄入图片展示
    if target_image:
        st.image(target_image, caption="NexaEdge App Preview", use_container_width=True)
    else:
        st.error(f"❌ 未检测到图片！当前根目录下的文件有: {os.listdir('.')}")
        st.info("💡 请确保你把 image.png 拖拽上传到了 GitHub 仓库的根目录下（和 homepage.py 放在一起）。")
    
    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1: st.metric(label="Network Fee", value="20%", delta="Pure Revenue Flow")
    with c2: st.metric(label="Safety Threshold", value="39°C", delta="Device Safety Lock", delta_color="inverse")
    with c3: st.metric(label="Settlement Base", value="Solana SPL", delta="Low Gas / High TPS")

# =========================================================================
# 📱 第二页：复刻版控制台
# =========================================================================
with tab2:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="app-container">', unsafe_allow_html=True)
    
    # 📸 第二页顶部成功摄入图片（包含官方 Logo 的部分）
    if target_image:
        st.image(target_image, use_container_width=True)
    
    st.markdown("<div style='margin-top: 15px;'></div>", unsafe_allow_html=True)
    
    # 📊 DASHBOARD 面板
    st.markdown('<div class="app-card">', unsafe_allow_html=True)
    st.markdown('<div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;"><span class="app-title">DASHBOARD</span><span style="color:#88929b; font-size:14px;">⚙️</span></div>', unsafe_allow_html=True)
    
    current_hash = random.uniform(45.5, 49.8) if st.session_state.app_running else 0.0
    st.markdown(f'<div style="font-size:11px; color:#88929b; margin-bottom:5px;">NETWORK HASH RATE (MH/s): <span class="neon-green-text" style="font-weight:bold;">{current_hash:.2f}</span></div>', unsafe_allow_html=True)
    
    if st.session_state.app_running:
        st.session_state.chart_history.pop(0)
        st.session_state.chart_history.append(current_hash)
    chart_df = pd.DataFrame(st.session_state.chart_history, columns=["Hash Rate"])
    st.area_chart(chart_df, height=75, use_container_width=True)
    
    current_temp = random.uniform(36.4, 36.9) if st.session_state.app_running else 31.2
    st.markdown(f"""
    <div class="temp-section">
        <div style="display:flex; align-items:center;"><span style="font-size:24px; margin-right:8px;">🌡️</span><span class="app-value" style="font-size:22px;">{current_temp:.1f}°C</span></div>
        <span style="background-color:#1e272e; color:#A2FF00; font-size:11px; font-weight:bold; padding:4px 10px; border-radius:12px; border:1px solid #A2FF00;">SAFE</span>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 🟢 PARTICIPANT NODE 面板
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
        <span style="color:{status_color}; font-size:15px; font-weight:800;">● {run_status}</span>
        <span class="app-value neon-green-text" style="font-size:24px;">{st.session_state.app_earned:,.1f} <span style="font-size:13px; color:#ffffff; font-weight:normal;">NEXA</span></span>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # 🕹️ 按键交互
    if not st.session_state.app_running:
        if st.button("START COMPUTE SESSION", key="app_start_btn"):
            st.session_state.app_running = True
            st.rerun()
    else:
        if st.button("PAUSE SESSION (VIEW NETWORK MAP)", key="app_stop_btn"):
            st.session_state.app_running = False
            st.rerun()
            
    if st.session_state.app_running:
        st.session_state.app_earned += 0.125
        time.sleep(0.5)
        st.rerun()
            
    st.markdown('</div>', unsafe_allow_html=True)
