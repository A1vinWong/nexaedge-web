import streamlit as st
import pandas as pd
import numpy as np
import time

# 页面配置
st.set_page_config(page_title="NexaEdge", layout="centered")

# CSS 注入：核心在于消除空白与布局对齐
st.markdown("""
    <style>
    .stApp { background-color: #0b0f12; }
    /* 移除所有冗余空白 */
    [data-testid="stVerticalBlock"] { gap: 0rem; }
    [data-testid="stMetric"] { background: #161c23; padding: 10px; border-radius: 10px; }
    /* 精确控制图表容器，消除顶部空白 */
    .chart-container { margin-top: -20px; margin-bottom: 0px; }
    </style>
""", unsafe_allow_html=True)

# 模拟数据逻辑
if 'hash_data' not in st.session_state:
    st.session_state.hash_data = pd.DataFrame({'hashrate': [20.0]*10})

# --- 布局开始 ---
st.title("NexaEdge Network")

# 选项卡
tab1, tab2, tab3 = st.tabs(["Overview", "Dashboard", "Auth Portal"])

with tab2:
    # 直接在下方放置提示，去掉中间空白框
    st.warning("Running as Visitor (Data stays local, register inside Auth Portal to sync)")
    
    st.write("### EDGE NODE REAL-TIME HASHRATE TREND")
    
    # 使用原生图表，避免依赖报错
    chart_data = st.session_state.hash_data
    st.line_chart(chart_data, height=200)

    # 硬件信息
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Hardware Temp", "36.9°C")
    with col2:
        st.metric("Input Power", "5.05 W")

    if st.button("START COMPUTE SESSION"):
        st.rerun()
