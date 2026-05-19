import streamlit as st
import os
import time
import random
import pandas as pd
import glob
import hashlib
import plotly.graph_objects as go # 👈 引入 plotly

# 💡 在这里统一配置你的新合约地址
DEFAULT_CA = "D7h9MvFDkVxPYeJwSTcE7VkKXo6mygCHYph36P8oeic2"

# 1. 全局页面基础配置
st.set_page_config(
    page_title="NexaEdge Network | Official Node Gateway",
    page_icon="🟢",
    layout="centered"
)

# =========================================================================
# 🔒 服务器跨进程内存锁 与 数据库模拟
# =========================================================================
@st.cache_resource
def init_global_network_server():
    return {
        "active_device_set": set(),             
        "total_online_viewers": random.randint(102, 125), 
        "device_balances": {},                  
        "user_db": {                            
            "contact@nexaedge.org": {
                "password_hash": hashlib.sha256("nexa2026".encode()).hexdigest(),
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
if "current_user" not in st.session_state: st.session_state.current_user = None  

if dev_id not in global_server["device_balances"]:
    global_server["device_balances"][dev_id] = {"app_earned": 0.0, "total_energy_wh": 0.0, "session_seconds": 0}

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

if 'app_running' not in st.session_state: st.session_state.app_running = False
if 'chart_history' not in st.session_state: st.session_state.chart_history = [45.2, 46.8, 45.1, 47.3, 46.0, 48.2, 45.9, 49.1, 47.5, 48.8, 46.2, 47.9]
if 'target_time_index' not in st.session_state: st.session_state.target_time_index = 2 
if 'last_tick_time' not in st.session_state: st.session_state.last_tick_time = 0.0

# --- 🟢 CSS 全局注入 ---
st.markdown("""
    <style>
    .stApp { background-color: #0b0f12; }
    /* 极致去边距 */
    [data-testid="stPlotlyChart"] { margin: -10px -10px -20px -10px !important; }
    .chart-wrapper { 
        background-color: #161c23; border: 1px solid #252e38; border-radius: 14px; 
        padding: 15px; margin-bottom: 12px; overflow: hidden;
    }
    .chart-title-lbl { font-size: 11px; color: #88929b; font-weight: bold; text-transform: uppercase; margin-bottom: 6px; }
    </style>
""", unsafe_allow_html=True)

# (其余逻辑代码保持不变，将你的 TAB 2 部分替换为下文)

# ... [中间逻辑部分保持你的原代码即可] ...

# ==========================================
# TAB 2: Dashboard 算力控制台 (完美美观版)
# ==========================================
with tab2:
    if st.session_state.app_running:
        current_hash = random.uniform(45.5, 49.8)
        st.session_state.chart_history.pop(0)
        st.session_state.chart_history.append(current_hash)
    
    # 3. 📈 Plotly 极致绘图
    st.markdown('<div class="chart-title-lbl">📶 Edge Node Real-time Hashrate Trend</div>', unsafe_allow_html=True)
    st.markdown('<div class="chart-wrapper">', unsafe_allow_html=True)
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        y=st.session_state.chart_history,
        mode='lines',
        line=dict(color='#A2FF00', width=3),
        fill='tozeroy',
        fillcolor='rgba(162, 255, 0, 0.1)'
    ))
    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        height=150,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(visible=False),
        yaxis=dict(visible=False)
    )
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    st.markdown('</div>', unsafe_allow_html=True)

    # ... [你的其他卡片逻辑] ...
