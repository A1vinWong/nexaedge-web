import streamlit as st
import time
import random
import pandas as pd

st.set_page_config(
    page_title="NexaEdge Network | Official Node Gateway",
    page_icon="🟢",
    layout="centered"
)

@st.cache_resource
def get_global_network_memory():
    return {"active_count": 451, "whitelist_db": []}

global_memory = get_global_network_memory()

if 'app_earned' not in st.session_state: st.session_state.app_earned = 1452.7000
if 'chart_history' not in st.session_state: st.session_state.chart_history = [22.0, 25.0, 24.0, 28.0, 27.0, 31.0, 29.0, 33.0, 31.0, 35.0, 33.0, 36.8]
if 'target_time_index' not in st.session_state: st.session_state.target_time_index = 2 
if 'app_running' not in st.session_state: st.session_state.app_running = False
if 'just_finished' not in st.session_state: st.session_state.just_finished = False
if 'session_seconds' not in st.session_state: st.session_state.session_seconds = 0
if 'last_tick_time' not in st.session_state: st.session_state.last_tick_time = 0.0

if st.session_state.app_running and st.session_state.last_tick_time > 0:
    now = time.time()
    elapsed_real_seconds = int(now - st.session_state.last_tick_time)
    if elapsed_real_seconds > 0:
        st.session_state.session_seconds += elapsed_real_seconds
        st.session_state.app_earned += elapsed_real_seconds * 0.25
        st.session_state.last_tick_time = now

st.markdown("""
    <style>
    .stApp { background-color: #0b0f12; }
    .app-card { background-color: #161c23; border: 1px solid #252e38; border-radius: 14px; padding: 15px; margin-bottom: 12px; }
    .app-title { font-size: 13px; color: #88929b; font-weight: bold; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 5px; }
    .app-value { font-family: 'Inter', sans-serif; color: #ffffff; font-size: 32px; font-weight: 700; }
    .neon-green-text { color: #A2FF00 !important; }
    .temp-section { display: flex; align-items: center; justify-content: space-between; background: #11171d; padding: 10px 14px; border-radius: 10px; margin-top: 4px; }
    .ratio-box { background-color: #11171d; border: 1px dashed #252e38; border-radius: 8px; padding: 8px 10px; margin-top: 8px; font-size: 12px; color: #88929b; }
    div.stButton > button:first-child {
        background-color: #A2FF00 !important; color: #0b0f12 !important; font-weight: 800 !important; font-size: 16px !important;
        width: 100%; border-radius: 12px !important; border: none !important; padding: 12px 0 !important; box-shadow: 0 0 15px rgba(162, 255, 0, 0.3);
    }
    div.stButton > button[key*="app_stop_btn"] { background-color: #0b0f12 !important; color: #ffffff !important; border: 1px solid #252e38 !important; box-shadow: none !important; }
    [data-testid="stForm"] { background-color: #161c23 !important; border: 1px solid #252e38 !important; border-radius: 16px !important; padding: 20px !important; margin-top: 25px !important; }
    .admin-box { background-color: #1c232c; border: 2px dashed #A2FF00; padding: 20px; border-radius: 14px; margin-top: 30px; }
    </style>
""", unsafe_allow_html=True)
col_pad, col_lang = st.columns([4, 1])
with col_lang:
    lang = st.selectbox("🌐 Language", ["English", "中文"], index=0, label_visibility="collapsed", key="global_lang")

TIME_OPTIONS_EN = ["15 Minutes", "30 Minutes", "1 Hour", "2 Hours", "4 Hours", "8 Hours", "12 Hours", "24 Hours (Full-day)"]
TIME_OPTIONS_ZH = ["15 分钟", "30 分钟", "1 小时", "2 小时", "4 小时", "8 小时", "12 小时", "24 小时 (全天)"]
TIME_OPTIONS = TIME_OPTIONS_EN if lang == "English" else TIME_OPTIONS_ZH
SECONDS_MAP = [900, 1800, 3600, 7200, 14400, 28800, 43200, 86400]
HOURS_MAP = [0.25, 0.5, 1.0, 2.0, 4.0, 8.0, 12.0, 24.0]

st.markdown('<h1 style="text-align:center; color:#A2FF00; font-size:36px; font-weight:800; margin-bottom:12px;">NexaEdge Network</h1>', unsafe_allow_html=True)
st.image("image.png", use_container_width=True)

tab1, tab2 = st.tabs(["🌐 Overview", "📱 Dashboard"])

with tab1:
    st.markdown('<div class="app-card"><div class="app-title">Network Fee</div><div class="app-value">20%</div></div>', unsafe_allow_html=True)
    selected_time_tab1 = st.selectbox("Calculator", TIME_OPTIONS, index=st.session_state.target_time_index, key="t1")
    st.session_state.target_time_index = TIME_OPTIONS.index(selected_time_tab1)

with tab2:
    if st.session_state.app_running:
        target_total_seconds = SECONDS_MAP[st.session_state.target_time_index]
        st.selectbox("Runtime", TIME_OPTIONS, index=st.session_state.target_time_index, key="t2_dis", disabled=True)
    else:
        selected_time_tab2 = st.selectbox("Runtime", TIME_OPTIONS, index=st.session_state.target_time_index, key="t2")
        st.session_state.target_time_index = TIME_OPTIONS.index(selected_time_tab2)
        target_total_seconds = SECONDS_MAP[st.session_state.target_time_index]
    
    if st.session_state.app_running and st.session_state.session_seconds >= target_total_seconds:
        st.session_state.app_running = False
        st.session_state.just_finished = True 
        global_memory["active_count"] = max(451, global_memory["active_count"] - 1)
        st.rerun()

    current_hash = random.uniform(45.5, 49.8) if st.session_state.app_running else 0.0
    current_temp = random.uniform(36.4, 36.9) if st.session_state.app_running else 31.2
    s_sec = st.session_state.session_seconds
    remaining_seconds = max(0, target_total_seconds - s_sec)
    
    time_str = f"{s_sec//3600:02d}:{(s_sec%3600)//60:02d}:{s_sec%60:02d}"
    rem_str = f"{remaining_seconds // 3600:02d}:{(remaining_seconds % 3600) // 60:02d}:{remaining_seconds % 60:02d}"
    
    st.markdown(f'<div class="app-card"><div class="app-title">Hash Rate: {current_hash:.2f}</div></div>', unsafe_allow_html=True)
    if st.session_state.app_running:
        st.session_state.chart_history.pop(0)
        st.session_state.chart_history.append(current_hash)
    st.line_chart(pd.DataFrame(st.session_state.chart_history, columns=["Hash Rate"]), height=95)
    
    st.markdown(f'<div class="app-card"><div class="app-title">Duration: {time_str}</div><div class="app-title" style="color:#ff9f43;">Countdown: {rem_str}</div><div class="app-value neon-green-text">+{s_sec * 0.25:,.1f} NEXA</div></div>', unsafe_allow_html=True)

    if not st.session_state.app_running:
        if st.button("START COMPUTE SESSION", key="app_start_btn"):
            st.session_state.session_seconds = 0
            st.session_state.just_finished = False
            st.session_state.app_running = True
            st.session_state.last_tick_time = time.time()
            global_memory["active_count"] += 1
            st.rerun()
    else:
        if st.button("PAUSE SESSION", key="app_stop_btn"):
            st.session_state.app_running = False
            global_memory["active_count"] = max(451, global_memory["active_count"] - 1)
            st.rerun()

with st.form("wl_form"):
    u_email = st.text_input("Email:").strip()
    u_wallet = st.text_input("Wallet:").strip()
    if st.form_submit_button("SUBMIT"):
        global_memory["whitelist_db"].append({"email": u_email, "wallet": u_wallet, "score": f"{st.session_state.app_earned:.1f}"})
        st.success("Success!")

st.markdown(f'<div style="text-align: center;"><span style="color:#A2FF00;">🟢 ONLINE DEVICES: {global_memory["active_count"]}</span></div>', unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#445; font-size: 11px;'>NexaEdge Network © 2026</p>", unsafe_allow_html=True)

if st.session_state.app_running:
    time.sleep(1.0)
    st.session_state.app_earned += 0.25       
    st.session_state.session_seconds += 1     
    st.session_state.last_tick_time = time.time()
    st.rerun()
