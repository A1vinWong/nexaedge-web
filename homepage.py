import streamlit as st
import os
import time
import random

# 1. 页面基础全局配置
st.set_page_config(
    page_title="NexaEdge | Web-Node Experience",
    page_icon="🟢",
    layout="centered"
)

# --- 🟢 暗黑科技风全局 CSS 样式 ---
st.markdown("""
    <style>
    .stApp { background-color: #0b0f12; }
    .node-box {
        background-color: #11171d; 
        padding: 25px; 
        border-radius: 15px; 
        border: 1px solid #A2FF00;
        text-align: center;
        margin: 20px 0;
    }
    .metric-text { font-family: 'Courier New', monospace; color: #A2FF00; font-size: 32px; font-weight: bold; }
    .status-log { font-family: 'Courier New', monospace; color: #bdc3c7; font-size: 12px; height: 80px; overflow-y: auto; text-align: left; background: #000; padding: 10px; border-radius: 5px; }
    div.stButton > button:first-child {
        background-color: #A2FF00 !important;
        color: #0b0f12 !important;
        font-weight: 800 !important;
        width: 100%;
        border-radius: 8px !important;
        border: none !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- 🌐 置顶语言一键切换（已修复重复 ID 问题） ---
lang_col1, lang_col2 = st.columns([3, 1])
with lang_col2:
    lang = st.selectbox(
        "🌐 Language Selector", 
        ["English", "中文"], 
        index=0,
        label_visibility="collapsed",
        key="unique_top_language_selector"  # 加上唯一KEY，彻底解决报错
    )

st.markdown("<div style='margin-top: -10px;'></div>", unsafe_allow_html=True)

# ==================== 🪐 LOGO 门面区域 ====================
# 这里已经完美适配你上传的 IMG_7651.jpeg 文件
if os.path.exists("IMG_7651.jpeg"):
    st.image("IMG_7651.jpeg", use_container_width=True)
elif os.path.exists("logo.png"):
    st.image("logo.png", use_container_width=True)
else:
    st.markdown(f'<h3 style="text-align:center; color:#A2FF00;">{"NexaEdge Network" if lang == "English" else "NexaEdge 算力网络"}</h3>', unsafe_allow_html=True)

# ==================== ⚡ WEB-NODE 虚拟收益体验舱 ====================
if 'nexa_earned' not in st.session_state:
    st.session_state.nexa_earned = 0.0
if 'is_running' not in st.session_state:
    st.session_state.is_running = False

text_intro = (
    "Run the virtual WASM node to see how your device generates $NEXA." 
    if lang == "English" else 
    "开启虚拟 WASM 节点，直观感受手机如何通过底层算力产生 $NEXA 收益。"
)
st.markdown(f'<div style="text-align:center; color:#bdc3c7; font-size:14px; margin-bottom:15px;">{text_intro}</div>', unsafe_allow_html=True)

# 虚拟矿机渲染
st.markdown('<div class="node-box">', unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col1:
    st.caption("EST. EARNINGS" if lang == "English" else "预计累计收益")
    st.markdown(f'<div class="metric-text">{st.session_state.nexa_earned:.5f} <span style="font-size:14px;">$NEXA</span></div>', unsafe_allow_html=True)
with col2:
    temp = random.uniform(34.5, 38.8) if st.session_state.is_running else 32.0
    st.caption("REAL-TIME TEMP" if lang == "English" else "智能温控保护")
    st.markdown(f'<div class="metric-text" style="color:{"#ff4b4b" if temp > 38 else "#A2FF00"}">{temp:.1f}°C</div>', unsafe_allow_html=True)

# 日志数据流模拟
logs = [
    "> Initializing WASM Sandbox running environment...",
    "> Connecting to Solana cluster via RPC-Node...",
    "> Fetching unverified AI Shards #8821...",
    "> Processing natural language dataset sorting...",
    "> Submitting 2:1 validation proof to smart contract..."
]

if st.session_state.is_running:
    st.markdown(f'<div class="status-log">{random.choice(logs)}<br>{random.choice(logs)}</div>', unsafe_allow_html=True)
    st.session_state.nexa_earned += 0.00037
    time.sleep(0.4)
    st.rerun()
else:
    standby_text = "System Standby. Click the button below to initialize web-node mining." if lang == "English" else "系统正在待命。点击下方按钮开始模拟算力挖矿。"
    st.markdown(f'<div class="status-log">> {standby_text}</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# 控制按钮
if not st.session_state.is_running:
    if st.button("🚀 ACTIVATE WEB-NODE" if lang == "English" else "🚀 激活 WEB-NODE 算力体验"):
        st.session_state.is_running = True
        st.rerun()
else:
    if st.button("🛑 STOP & RECORD YIELD" if lang == "English" else "🛑 停止并记录收益"):
        st.session_state.is_running = False
        st.rerun()

# ==================== 📊 价值传递与通缩逻辑 ====================
st.markdown("<hr style='border:1px solid #1e272e;'>", unsafe_allow_html=True)

if lang == "English":
    st.markdown("""
    <h3 style="color:#A2FF00; font-size:22px;">How Does It Work?</h3>
    <p style="color:#bdc3c7; font-size:14px;">Your browser is currently simulating our lightweight WASM sandbox. In our live network, this protocol activates silently at the OS level whenever your phone is charging on Wi-Fi, turning idle energy into high-purity AI data fuel.</p>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <h3 style="color:#A2FF00; font-size:22px;">它是如何产生收益的？</h3>
    <p style="color:#bdc3c7; font-size:14px;">您的浏览器目前正成功通过轻量级 WASM 沙盒进行模拟运算。在未来的正式网络中，只要您的手机连接 Wi-Fi 充电锁屏，该协议就会在系统底层自动静默运行，将闲置资源转化为大模型急需的高纯度语料燃料。</p>
    """, unsafe_allow_html=True)

# ==================== 📧 收益存档与白名单（已修复 Submit Button 问题） ====================
st.markdown("<hr style='border:1px solid #1e272e;'>", unsafe_allow_html=True)
st.markdown(f'<h3 style="color:#A2FF00; font-size:22px;">{"🚀 Save Mock Yield to Whitelist" if lang == "English" else "🚀 将当前收益归档至早期白名单"}</h3>', unsafe_allow_html=True)

# 使用唯一的 Form 名字
with st.form(key="final_whitelist_submission_form"):
    user_email = st.text_input("Email Address" if lang == "English" else "输入您的电子邮箱:")
    wallet_addr = st.text_input("Solana Address (Optional)" if lang == "English" else "Solana 接收地址 (选填):")
    
    # 必须通过 st.form_submit_button 触发提交，修复第一个报错
    submitted = st.form_submit_button("LOCK IN MY SEAT & AIRDROP ⚡" if lang == "English" else "锁定测试网优先空投资格 ⚡")
    
    if submitted:
        if user_email:
            st.balloons()
            success_msg = "Successfully Whitelisted!" if lang == "English" else "恭喜！已成功锁定空投资格。"
            st.success(f"🎯 {success_msg}")
            with open("whitelist.txt", "a") as f:
                f.write(f"{user_email},{wallet_addr},{st.session_state.nexa_earned:.5f}\n")
        else:
            err_msg = "Please enter a valid email address." if lang == "English" else "请输入有效的电子邮箱地址。"
            st.error(err_msg)

st.markdown("<br><p style='text-align:center; color:#445;'>NexaEdge Network © 2026 | Powered by Solana DePIN Ecosystem</p>", unsafe_allow_html=True)
