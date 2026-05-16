import streamlit as st
import os

# 1. 全局页面基础配置
st.set_page_config(
    page_title="NexaEdge Network | Official Gateway",
    page_icon="🟢",
    layout="centered"
)

# --- 🟢 超酷暗黑科技风全局 CSS 样式 ---
st.markdown("""
    <style>
    /* 整体背景微调 */
    .stApp { background-color: #0b0f12; }
    
    /* 核心三大壁垒卡片样式 */
    .feature-box {
        background-color: #11171d; 
        padding: 20px; 
        border-radius: 10px; 
        border-left: 5px solid #A2FF00; 
        margin-bottom: 20px;
    }
    
    /* 表单提交按钮高亮荧光绿样式 */
    div.stButton > button:first-child {
        background-color: #A2FF00 !important;
        color: #0b0f12 !important;
        font-weight: 800 !important;
        width: 100%;
        border-radius: 8px !important;
        border: none !important;
        padding: 10px 0 !important;
    }
    </style>
""", unsafe_allow_html=True)

# ==================== 🌐 TOP: 置顶语言一键切换选项 ====================
# 使用两列布局，在网页最顶端、Logo上方放置语言选择框
lang_col1, lang_col2 = st.columns([3, 1])
with lang_col2:
    lang = st.selectbox(
        "🌐 Language", 
        ["English", "中文"], 
        index=0,
        label_visibility="collapsed" # 隐藏多余的标签，让界面极简
    )

st.markdown("<div style='margin-top: -10px;'></div>", unsafe_allow_html=True)

# ==================== 🪐 LOGO & 标语门面 ====================
# 在页面中央渲染你的高值 Logo
if os.path.exists("logo.png"):
    st.image("logo.png", use_container_width=True)
else:
    # 备用文字 Logo
    st.markdown(f'<h1 style="text-align:center; color:#A2FF00; font-size:42px; font-weight:800; margin-bottom:0;">{"NexaEdge Network" if lang == "English" else "NexaEdge 算力网络"}</h1>', unsafe_allow_html=True)

# 根据选择的语言，动态渲染一整页的对应内容
if lang == "English":
    # ------------------ 🇺🇸 纯英文版页面内容 ------------------
    st.markdown('<p style="font-size: 18px; color: #bdc3c7; text-align: center; margin-top:10px; margin-bottom: 35px;">Transforming 5B+ idle smartphones into high-purity data fuel factories for the AI Era.</p>', unsafe_allow_html=True)

    # Metric Row
    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric(label="Network Fee", value="20%", delta="Pure Revenue Flow")
    with c2:
        st.metric(label="Safety Threshold", value="39°C", delta="Device Safety Lock", delta_color="inverse")
    with c3:
        st.metric(label="Settlement Base", value="Solana SPL", delta="Low Gas / High TPS")

    st.markdown("<hr style='border:1px solid #1e272e;'>", unsafe_allow_html=True)

    # Core Pillars
    st.markdown('<h2 style="color:#A2FF00; font-size:26px;">⚡ Key Pillars</h2>', unsafe_allow_html=True)
    st.markdown("""
    <div class="feature-box">
        <h4 style="color:white; margin-top:0; font-size:18px;">📱 Passive Income via Charging</h4>
        <p style="color:#bdc3c7; font-size:14px;">Earn ~0.35 USDT/hr. Just plug in, connect Wi-Fi, and lock your screen. Our lightweight WASM Sandbox cleans AI datasets silently in the background.</p>
    </div>
    <div class="feature-box">
        <h4 style="color:white; margin-top:0; font-size:18px;">🔥 39°C Thermal Guard</h4>
        <p style="color:#bdc3c7; font-size:14px;">Total hardware protection. System auto-throttles computing loads instantly if the battery touches 39°C. Zero degradation anxiety.</p>
    </div>
    <div class="feature-box">
        <h4 style="color:white; margin-top:0; font-size:18px;">🤝 2:1 Anti-Cheat Verification</h4>
        <p style="color:#bdc3c7; font-size:14px;">Decentralized majority-voting consensus. We segment raw data across 3 independent nodes to deliver 100% verified datasets to AI clients.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<hr style='border:1px solid #1e272e;'>", unsafe_allow_html=True)

    # Calculator
    st.markdown('<h2 style="color:#A2FF00; font-size:26px;">🧮 Interactive Yield Calculator</h2>', unsafe_allow_html=True)
    role = st.selectbox("Select Your Role in the Ecosystem:", ["Node Operator (Retail User)", "AI Enterprise Client (Data Buyer)"])

    if "Retail" in role:
        hours = st.slider("Estimated overnight session duration (Hours/Day):", 1, 12, 6)
        device = st.radio("Your Mobile Operating System:", ["iOS (iPhone)", "Android Device"])
        rate = 0.35 if "iOS" in device else 0.30
        monthly_earn = hours * rate * 30
        st.success(f"🎉 Estimated Monthly Cumulative Yield: **{monthly_earn:.2f} USDT** (Offsets your mobile carrier bill!)")
    else:
        gb = st.number_input("Dataset Size Required (GB):", min_value=1, value=100)
        st.warning(f"💼 Total Computing Procurement Budget: **{gb * 6.0:.2f} USD**")

    st.markdown("<hr style='border:1px solid #1e272e;'>", unsafe_allow_html=True)

    # Whitelist
    st.markdown('<h2 style="color:#A2FF00; font-size:26px;">🚀 Join the Alpha Testnet Whitelist</h2>', unsafe_allow_html=True)
    st.write("Submit your credentials below to lock in Genesis Node status and priority $NEXA airdrops.")
    
    with st.form("whitelist_form_en"):
        user_email = st.text_input("Enter your Email Address:")
        wallet_addr = st.text_input("Your Solana Wallet Address (Optional):")
        submitted = st.form_submit_button("SECURE MY GENESIS NODE SEAT NOW ⚡")
        if submitted:
            if user_email:
                st.balloons()
                st.success(f"🎯 Verified! {user_email} has been successfully whitelisted.")
                with open("whitelist.txt", "a") as f: f.write(f"{user_email},{wallet_addr}\n")
            else:
                st.error("Please enter a valid email address.")

else:
    # ------------------ 🇨🇳 纯中文版页面内容 ------------------
    st.markdown('<p style="font-size: 18px; color: #bdc3c7; text-align: center; margin-top:10px; margin-bottom: 35px;">让全球 50 亿部闲置手机，成为 AI 时代的高纯度语料燃料工厂</p>', unsafe_allow_html=True)

    # 数据行
    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric(label="平台技术抽成", value="20%", delta="纯现金流造血")
    with c2:
        st.metric(label="智能硬件风控", value="39°C", delta="多端联动秒级预警", delta_color="inverse")
    with c3:
        st.metric(label="算力结算底座", value="Solana SPL", delta="极速、低 Gas")

    st.markdown("<hr style='border:1px solid #1e272e;'>", unsafe_allow_html=True)

    # 核心壁垒
    st.markdown('<h2 style="color:#A2FF00; font-size:26px;">⚡ 核心壁垒</h2>', unsafe_allow_html=True)
    st.markdown("""
    <div class="feature-box">
        <h4 style="color:white; margin-top:0; font-size:18px;">📱 锁屏充电·睡后收入 (零门槛)</h4>
        <p style="color:#bdc3c7; font-size:14px;">每小时赚取约 0.35 USDT。用户只需在夜间充电、连接 Wi-Fi 并锁屏，NexaEdge 的轻量级 WASM 沙盒便会在后台静默运行清洗 AI 语料。</p>
    </div>
    <div class="feature-box">
        <h4 style="color:white; margin-top:0; font-size:18px;">🔥 独创：39°C 智能温控风控屏障</h4>
        <p style="color:#bdc3c7; font-size:14px;">坚守绝不伤机的底线。一旦手机运行温度触及 39°C 临界点，系统触发多端联动机制自动下发降载指令，彻底打消硬件焦虑。</p>
    </div>
    <div class="feature-box">
        <h4 style="color:white; margin-top:0; font-size:18px;">🤝 B端：2:1 多数表决防作弊机制</h4>
        <p style="color:#bdc3c7; font-size:14px;">原始语料切块多点分发，通过 3 节点冗余计算。平台采用去中心化的多数表决机制，彻底过滤模拟器行为，交付 100% 验证的数据集。</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<hr style='border:1px solid #1e272e;'>", unsafe_allow_html=True)

    # 计算器
    st.markdown('<h2 style="color:#A2FF00; font-size:26px;">🧮 生态双向收益计算器</h2>', unsafe_allow_html=True)
    role = st.selectbox("请选择您的身份：", ["我是手机持有者 (C端算力提供方)", "我是 AI 大模型厂商 (B端算力购买方)"])

    if "C端" in role:
        hours = st.slider("预估您每天夜间挂机打工的小时数：", 1, 12, 6)
        device = st.radio("您的设备系统：", ["iOS 苹果手机", "Android 安卓手机"])
        rate = 0.35 if "iOS" in device else 0.30
        monthly_earn = hours * rate * 30
        st.success(f"🎉 一个月（30天）累计可躺赚 **{monthly_earn:.2f} USDT**（轻松解决您的家庭宽带和手机网费！）")
    else:
        data_need = st.number_input("您需要平台全球手机节点为您清洗的语料大小 (GB):", min_value=1, value=100)
        st.warning(f"💼 您的算力采购预算总计：**{data_need * 6.0:.2f} USD**")

    st.markdown("<hr style='border:1px solid #1e272e;'>", unsafe_allow_html=True)

    # 白名单
    st.markdown('<h2 style="color:#A2FF00; font-size:26px;">🚀 抢先加入早期白名单 (Airdrop 预约)</h2>', unsafe_allow_html=True)
    st.write("提交您的邮箱，在 $NEXA 代币正式上线时，优先获得测试网上线空投奖励资格！")
    
    with st.form("whitelist_form_zh"):
        user_email = st.text_input("输入您的 Email 地址:")
        wallet_addr = st.text_input("您的 Solana 钱包接收地址 (选填):")
        submitted = st.form_submit_button("立刻锁定白名单席位 ⚡")
        if submitted:
            if user_email:
                st.balloons()
                st.success(f"🎯 恭喜！{user_email} 已成功列入 NexaEdge 早期白名单。")
                with open("whitelist.txt", "a") as f: f.write(f"{user_email},{wallet_addr}\n")
            else:
                st.error("请输入有效的邮箱地址。")
import streamlit as st
import os
import time
import random

# 1. Page Configuration
st.set_page_config(
    page_title="NexaEdge | Web-Node Experience",
    page_icon="🟢",
    layout="centered"
)

# --- 🟢 CYBER-TECH CSS STYLING ---
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
    }
    </style>
""", unsafe_allow_html=True)

# Language Selection at Top
lang = st.selectbox("🌐 Language", ["English", "中文"], index=0, label_visibility="collapsed")

# ==================== 🪐 HEADER ====================
if os.path.exists("logo.png"):
    st.image("logo.png", use_container_width=True)

st.markdown(f'<h3 style="text-align:center; color:#A2FF00;">{"Experience Web-Node Earning" if lang == "English" else "Web-Node 算力收益初体验"}</h3>', unsafe_allow_html=True)

# ==================== ⚡ WEB-NODE SIMULATOR ====================
# 初始化 Session State 用于存储模拟收益
if 'nexa_earned' not in st.session_state:
    st.session_state.nexa_earned = 0.0
if 'is_running' not in st.session_state:
    st.session_state.is_running = False

st.markdown(f"""
<div style="text-align:center; color:#bdc3c7; font-size:14px;">
    {'Run the virtual WASM node to see how your device generates $NEXA.' if lang == 'English' else '运行虚拟 WASM 节点，直观感受手机如何通过算力产生 $NEXA。'}
</div>
""", unsafe_allow_html=True)

with st.container():
    # 模拟矿机外壳
    st.markdown('<div class="node-box">', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.caption("EST. EARNINGS" if lang == "English" else "预计累计收益")
        st.markdown(f'<div class="metric-text">{st.session_state.nexa_earned:.5f} <span style="font-size:14px;">$NEXA</span></div>', unsafe_allow_html=True)
    with col2:
        temp = random.uniform(34.5, 38.8) if st.session_state.is_running else 32.0
        st.caption("TEMP GAARD" if lang == "English" else "实时温控")
        st.markdown(f'<div class="metric-text" style="color:{"#ff4b4b" if temp > 38 else "#A2FF00"}">{temp:.1f}°C</div>', unsafe_allow_html=True)
    
    # 状态日志模拟
    logs = [
        "> Initializing WASM Sandbox...",
        "> Connecting to Solana Mainnet...",
        "> Sharding Dataset #0921-AI...",
        "> Cleaning raw voice data...",
        "> Verification redundant check (2:1)...",
        "> Proof of Computation submitted."
    ]
    
    if st.session_state.is_running:
        st.markdown(f'<div class="status-log">{random.choice(logs)}<br>{random.choice(logs)}</div>', unsafe_allow_html=True)
        # 增加收益逻辑
        st.session_state.nexa_earned += 0.00021 
        time.sleep(0.5) # 稍微延迟增加真实感
        st.rerun() # 强制刷新页面产生跳动效果
    else:
        st.markdown(f'<div class="status-log">> {"System Standby. Click below to start." if lang == "English" else "系统待命。点击下方按钮开始体验。"}</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# 启动/停止按钮
if not st.session_state.is_running:
    if st.button("🚀 ACTIVATE WEB-NODE" if lang == "English" else "🚀 启动 WEB-NODE 体验"):
        st.session_state.is_running = True
        st.rerun()
else:
    if st.button("🛑 STOP & CLAIM" if lang == "English" else "🛑 停止并保存收益"):
        st.session_state.is_running = False
        st.success(f"Claimed {st.session_state.nexa_earned:.4f} $NEXA to your preview session!")
        st.rerun()

# ==================== 📊 VALUE PROP & CALCULATOR ====================
st.markdown("<hr style='border:1px solid #1e272e;'>", unsafe_allow_html=True)

if lang == "English":
    st.markdown("""
    <h2 style="color:#A2FF00;">Why it works?</h2>
    <p style="color:#bdc3c7;">Your browser is now a micro-worker. In the real app, this happens at the OS level, processing data for global AI labs while you sleep.</p>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <h2 style="color:#A2FF00;">为什么这能赚钱？</h2>
    <p style="color:#bdc3c7;">您的浏览器现在就是一个微型“打工人”。在正式 App 中，这将在系统底层运行，在您睡觉时为全球 AI 实验室清洗数据。</p>
    """, unsafe_allow_html=True)

# ==================== 📧 LEAD GENERATION ====================
st.markdown(f'<h2 style="color:#A2FF00;">{"🚀 Save Earnings to Whitelist" if lang == "English" else "🚀 将收益存档至白名单"}</h2>', unsafe_allow_html=True)

with st.form("whitelist_form"):
    user_email = st.text_input("Email" if lang == "English" else "电子邮箱")
    submitted = st.form_submit_button("SUBMIT & RESERVE AIRDROP" if lang == "English" else "提交并预约空投")
    if submitted and user_email:
        st.balloons()
        st.success("Reserved! Your session earnings have been recorded.")
        with open("whitelist.txt", "a") as f: f.write(f"{user_email},{st.session_state.nexa_earned}\n")

# Footer
st.markdown("<br><p style='text-align:center; color:#555;'>NexaEdge Network © 2025 | Tier-3 DePIN Protocol</p>", unsafe_allow_html=True)
