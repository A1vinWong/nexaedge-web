import streamlit as st
import os
import time
import random
import pandas as pd
import glob
from datetime import datetime, timedelta

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

# --- 🟢 极客黑绿科技风 CSS 样式 ---
st.markdown("""
    <style>
    .stApp { background-color: #0b0f12; }
    #MainMenu, footer, .styles_viewerBadge__FUChv, [data-testid="manage-app-button"], 
    header, [data-testid="stHeader"] {
        display: none !important;
    }
    .feature-box {
        background-color: #11171d; 
        padding: 20px; 
        border-radius: 10px; 
        border-left: 5px solid #A2FF00; 
        margin-bottom: 20px;
    }
    [data-testid="stContainer"] {
        background-color: #161c23 !important;
        border: 1px solid #252e38 !important;
        border-radius: 16px !important;
        padding: 18px !important;
        margin-bottom: 15px !important;
    }
    .app-title { font-size: 14px; color: #88929b; font-weight: bold; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 5px; }
    .app-value { font-family: 'Inter', sans-serif; color: #ffffff; font-size: 26px; font-weight: 700; }
    .neon-green-text { color: #A2FF00 !important; }
    
    .temp-section {
        display: flex;
        align-items: center;
        justify-content: space-between;
        background: #11171d;
        padding: 10px 15px;
        border-radius: 12px;
        margin-top: 6px;
        margin-bottom: 4px;
    }
    
    .ratio-box {
        background-color: #11171d;
        border: 1px dashed #252e38;
        border-radius: 8px;
        padding: 10px 12px;
        margin-top: -2px;
        margin-bottom: 5px;
        font-size: 12px;
        color: #88929b;
    }
    
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
    
    .snapshot-box {
        background-color: #121e15;
        border: 1px solid #00ff66;
        border-left: 5px solid #00ff66;
        border-radius: 8px;
        padding: 12px;
        margin-bottom: 15px;
        color: #ccffdd;
    }
    </style>
""", unsafe_allow_html=True)

# --- 🚀 全局状态机初始化 ---
if 'current_page' not in st.session_state: st.session_state.current_page = "page1"  # 页码状态锁定锁
if 'app_earned' not in st.session_state: st.session_state.app_earned = 1452.7000
if 'app_running' not in st.session_state: st.session_state.app_running = False
if 'chart_history' not in st.session_state: st.session_state.chart_history = [22.0, 25.0, 24.0, 28.0, 27.0, 31.0, 29.0, 33.0, 31.0, 35.0, 33.0, 36.8]

# ⏱️ 时长控制器状态机
if 'target_duration_min' not in st.session_state: st.session_state.target_duration_min = 10  
if 'elapsed_seconds' not in st.session_state: st.session_state.elapsed_seconds = 0
if 'start_time_str' not in st.session_state: st.session_state.start_time_str = ""
if 'end_time_str' not in st.session_state: st.session_state.end_time_str = ""
if 'timer_completed' not in st.session_state: st.session_state.timer_completed = False
if 'last_completed_yield' not in st.session_state: st.session_state.last_completed_yield = 0.0

# 顶栏主标题与语言切换
st.markdown('<h1 style="text-align:center; color:#A2FF00; font-size:38px; font-weight:800; margin-top:10px; margin-bottom:5px;">NexaEdge Network</h1>', unsafe_allow_html=True)
lang = st.selectbox("🌐 Choose Language / 选择语言", ["English", "中文"], index=0)

# --- 🛰️ 自定义固态高级导航栏（代替 st.tabs 解决乱跳 Bug） ---
st.markdown("<div style='margin-bottom: 15px;'></div>", unsafe_allow_html=True)
nav_col1, nav_col2 = st.columns(2)
with nav_col1:
    page1_btn_label = "🌐 Overview & Pillars" if lang == "English" else "🌐 项目通识与核心介绍"
    if st.button(page1_btn_label, key="nav_p1_btn"):
        st.session_state.current_page = "page1"
        st.rerun()
with nav_col2:
    page2_btn_label = "📱 Node Dashboard (Live)" if lang == "English" else "📱 边缘节点实时控制台"
    if st.button(page2_btn_label, key="nav_p2_btn"):
        st.session_state.current_page = "page2"
        st.rerun()

# 渲染项目主视觉图
if target_image:
    st.image(target_image, caption="NexaEdge Official Gateway", use_container_width=True)

# =========================================================================
# 🏠 模式 A：第一页 - 项目介绍与核心通识壁垒
# =========================================================================
if st.session_state.current_page == "page1":
    st.markdown("<hr style='border:1px solid #1e272e; margin: 15px 0;'>", unsafe_allow_html=True)
    if lang == "English":
        st.markdown('<p style="font-size: 19px; color: #A2FF00; font-weight:bold; text-align: center; margin-bottom: 20px;">Transforming 5B+ idle smartphones into high-purity data fuel factories for the AI Era.</p>', unsafe_allow_html=True)
        
        c1, c2, c3 = st.columns(3)
        with c1: st.metric(label="Network Fee", value="20%", delta="Pure Revenue Flow")
        with c2: st.metric(label="Smart Timer", value="Customized", delta="Auto-Stop Safeguard")
        with c3: st.metric(label="Settlement Base", value="Solana SPL", delta="Low Gas / High TPS")
        
        with st.container(border=True):
            st.markdown("""
            <div class="feature-box">
                <b style="font-size:16px; color:#A2FF00;">📱 Screen-Lock Mining & Passive Income</b><br>
                <span style="font-size:13px; color:#bdc3c7;">Earn approx 0.35 USDT/hour. Just connect to Wi-Fi and lock your screen at night, NexaEdge's lightweight WASM sandbox will clean AI training data silently in the background.</span>
            </div>
            <div class="feature-box">
                <b style="font-size:16px; color:#A2FF00;">🔥 39°C Intelligent Thermal Overload Guard</b><br>
                <span style="font-size:13px; color:#bdc3c7;">Zero hardware damage. If your phone's operational temperature hits the 39°C threshold, the system automatically downclocks to protect your device battery perfectly.</span>
            </div>
            <div class="feature-box">
                <b style="font-size:16px; color:#A2FF00;">🤝 2:1 Byzantine Redundancy Verification</b><br>
                <span style="font-size:13px; color:#bdc3c7;">Decentralized consensus voting. Raw datasets are split and dispatched to 3 independent nodes for cross-validation to ensure 100% clean and authentic data delivery.</span>
            </div>
            """, unsafe_allow_html=True)
            
        st.markdown('<h2 style="color:#A2FF00; font-size:24px; margin-top:15px;">💰 Device Revenue Calculator</h2>', unsafe_allow_html=True)
        hours = st.slider("Estimated Overnight Duration (Hours/Day):", min_value=1, max_value=12, value=6)
        monthly_est = hours * 0.35 * 30
        st.success(f"🎉 Estimated Monthly Yield: {monthly_est:.2f} USDT")
    else:
        st.markdown('<p style="font-size: 19px; color: #A2FF00; font-weight:bold; text-align: center; margin-bottom: 20px;">让全球 50 亿部闲置手机，成为 AI 时代的高纯度语料燃料工厂</p>', unsafe_allow_html=True)
        
        c1, c2, c3 = st.columns(3)
        with c1: st.metric(label="平台技术抽成", value="20%", delta="纯现金流造血")
        with c2: st.metric(label="智能时长控制器", value="自主定时", delta="到期自动断开保护")
        with c3: st.metric(label="算力结算底座", value="Solana SPL", delta="极速、低 Gas")
        
        with st.container(border=True):
            st.markdown("""
            <div class="feature-box">
                <b style="font-size:16px; color:#A2FF00;">📱 锁屏充电·睡后收入 (零门槛)</b><br>
                <span style="font-size:13px; color:#bdc3c7;">每小时赚取约 0.35 USDT。用户只需在夜间充电、连接 Wi-Fi 并锁屏，NexaEdge 的轻量级 WASM 沙盒便会在后台静默运行清洗 AI 语料。</span>
            </div>
            <div class="feature-box">
                <b style="font-size:16px; color:#A2FF00;">🔥 独创：39°C 智能温控风控屏障</b><br>
                <span style="font-size:13px; color:#bdc3c7;">坚守绝不伤机的底线。一旦手机运行温度触及 39°C 临界点，系统自动下发降载指令，彻底打消硬件损耗焦虑。</span>
            </div>
            <div class="feature-box">
                <b style="font-size:16px; color:#A2FF00;">🤝 2:1 拜占庭冗余反作弊校验</b><br>
                <span style="font-size:13px; color:#bdc3c7;">去中心化多数投票共识。我们将原始语料切片分发至 3 个完全独立的边缘节点进行交叉校验，确保向 AI 客户交付 100% 真实、未被污染的高纯度数据集。</span>
            </div>
            """, unsafe_allow_html=True)
            
        st.markdown('<h2 style="color:#A2FF00; font-size:24px; margin-top:15px;">💰 设备收益计算器</h2>', unsafe_allow_html=True)
        hours = st.slider("预估每日夜间闲置充电时长 (小时/天):", min_value=1, max_value=12, value=6)
        monthly_est = hours * 0.35 * 30
        st.success(f"🎉 预计每月可为您带来收益约: {monthly_est:.2f} USDT")

# =========================================================================
# 📱 模式 B：第二页 - 边缘节点实时控制台（含时控、对时、计数器、永不乱跳）
# =========================================================================
elif st.session_state.current_page == "page2":
    st.markdown("<hr style='border:1px solid #1e272e; margin: 15px 0;'>", unsafe_allow_html=True)
    st.markdown("<h2 style='color:#ffffff; font-size:22px; font-weight:800; margin-top:5px; margin-bottom:10px;'>📱 NODE DASHBOARD & TIMER</h2>", unsafe_allow_html=True)

    # ------ ⏱️ 核心逻辑：判断定时挂机时间是否到期 ------
    target_total_seconds = st.session_state.target_duration_min * 60

    if st.session_state.app_running and st.session_state.elapsed_seconds >= target_total_seconds:
        st.session_state.timer_completed = True
        st.session_state.last_completed_yield = st.session_state.elapsed_seconds * 0.25
        st.session_state.app_running = False
        st.toast("⏰ SESSION COMPLETED SUCCESSFULLY!", icon="✅")
        st.rerun()

    # 🟢 渲染定时任务圆满结束的“结算看板”
    if st.session_state.timer_completed:
        if lang == "English":
            st.markdown(f'<div class="snapshot-box"><b style="color:#00ff66; font-size:15px;">⏰ SMART TIMER: SESSION SECURED</b><br><span style="font-size:12px; color:#88929b;">Your scheduled compute plan has successfully completed.</span><hr style="border:0.5px solid #00ff66; margin:8px 0;"><div style="display:flex; justify-content:space-between; font-size:13px;"><span>📅 TIME FRAME: <b style="color:#ffffff;">{st.session_state.start_time_str} → {st.session_state.end_time_str}</b></span><span>💰 REVENUE: <b style="color:#A2FF00;">+{st.session_state.last_completed_yield:,.1f} NEXA</b></span></div></div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="snapshot-box"><b style="color:#00ff66; font-size:15px;">⏰ 智能定时器：算力计划圆满完成</b><br><span style="font-size:12px; color:#88929b;">您设定的定时挂机任务已安全到期，系统已执行自动下线保护。</span><hr style="border:0.5px solid #00ff66; margin:8px 0;"><div style="display:flex; justify-content:space-between; font-size:13px;"><span>📅 运行周期: <b style="color:#ffffff;">{st.session_state.start_time_str} 到 {st.session_state.end_time_str}</b></span><span>💰 会话净收益: <b style="color:#A2FF00;">+{st.session_state.last_completed_yield:,.1f} NEXA</b></span></div></div>', unsafe_allow_html=True)

    # --- ⏱️ 模块 1：时控配置面板 ---
    with st.container(border=True):
        if not st.session_state.app_running:
            config_title = "⏱️ COMPUTE TIMER CONFIG" if lang == "English" else "⏱️ 边缘挂机时长控制器"
            st.markdown(f'<div class="app-title">{config_title}</div>', unsafe_allow_html=True)
            
            st.session_state.target_duration_min = st.slider(
                "Select Plan Duration (Minutes):" if lang=="English" else "设定本次挂机总时长 (分钟):",
                min_value=1, max_value=480, value=10, step=1
            )
            
            now = datetime.now()
            est_end = now + timedelta(minutes=st.session_state.target_duration_min)
            est_gain = st.session_state.target_duration_min * 60 * 0.25
            
            st.markdown(f"""
            <div class="ratio-box" style="margin-top:10px;">
                ⏱️ <b>{"Estimated Timeline:" if lang=="English" else "预计运行时间段:"}</b> {now.strftime('%H:%M:%S')} ➔ {est_end.strftime('%H:%M:%S')}<br>
                💎 <b>{"Expected Session Yield:" if lang=="English" else "到期预估总产出:"}</b> <span class='neon-green-text'>+{est_gain:,.1f} NEXA</span>
            </div>
            """, unsafe_allow_html=True)
        else:
            active_title = "⚡ LIVE SESSION TIMELINE" if lang == "English" else "⚡ 当前会话运行时间轴"
            st.markdown(f'<div class="app-title">{active_title}</div>', unsafe_allow_html=True)
            st.markdown(f"""
            <div class="ratio-box" style="background-color:#1c241b; border:1px solid #A2FF00;">
                📅 <b>{"Active Mining Period:" if lang=="English" else "当前挂机有效时段:"}</b> <br>
                <span style="font-size:16px; color:#ffffff; font-family:monospace;">{st.session_state.start_time_str} ➔ {st.session_state.end_time_str}</span>
            </div>
            """, unsafe_allow_html=True)

    # 算力曲线数据模拟
    current_hash = random.uniform(45.5, 49.8) if st.session_state.app_running else 0.0
    current_battery = 34 if st.session_state.app_running else 85
    current_temp = 36.5 if st.session_state.app_running else 31.2

    if st.session_state.app_running:
        st.session_state.chart_history.pop(0)
        st.session_state.chart_history.append(current_hash)
    chart_df = pd.DataFrame(st.session_state.chart_history, columns=["Hash Rate"])

    # --- 📊 模块 2：大控制大面板 ---
    with st.container(border=True):
        panel_title = "DASHBOARD" if lang == "English" else "控制面板"
        st.markdown(f'<div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;"><span class="app-title">{panel_title}</span></div>', unsafe_allow_html=True)
        
        st.line_chart(chart_df, height=105, use_container_width=True)
        
        status_tag = "ACTIVE (TIMED)" if st.session_state.app_running else "STANDBY"
        status_style = "background-color:#142a1a; color:#A2FF00; border:1px solid #A2FF00;" if st.session_state.app_running else "background-color:#1e272e; color:#88929b; border:1px solid #88929b;"
            
        st.markdown(f"""
        <div class="temp-section">
            <div style="display:flex; align-items:center; line-height:1; gap:15px;">
                <div><span style="font-size:18px; margin-right:3px; vertical-align:middle;">🌡️</span><span class="app-value" style="font-size:18px; vertical-align:middle;">{current_temp:.1f}°C</span></div>
                <div><span style="font-size:18px; margin-right:3px; vertical-align:middle;">🔋</span><span class="app-value" style="font-size:18px; vertical-align:middle;">{current_battery}%</span></div>
            </div>
            <span style="{status_style} font-size:11px; font-weight:bold; padding:5px 12px; border-radius:12px; line-height:1;">{status_tag}</span>
        </div>
        """, unsafe_allow_html=True)

    # --- ⏱️ 模块 3：实时收益与倒计时 ---
    with st.container(border=True):
        timer_title = "REALTIME SESSION INCOME" if lang == "English" else "实时会话收益与计时"
        st.markdown(f'<div class="app-title">{timer_title}</div>', unsafe_allow_html=True)
        
        rem_sec = max(0, target_total_seconds - st.session_state.elapsed_seconds)
        countdown_str = f"{rem_sec//3600:02d}:{(rem_sec%3600)//60:02d}:{rem_sec%60:02d}"
        session_generated = st.session_state.elapsed_seconds * 0.25
        
        c_label = "TIME REMAINING:" if lang == "English" else "倒计时 (距离结束):"
        yield_lbl = "LIVE SESSION YIELD:" if lang == "English" else "本次已滚动产出:"
        
        st.markdown(f"""
        <div style="display:flex; justify-content:space-between; margin-top:8px; margin-bottom:5px;">
            <div style="text-align:left;">
                <div style="font-size:11px; color:#88929b; margin-bottom:2px;">{c_label}</div>
                <div class="app-value" style="font-size:22px; color:#ffffff; font-family:monospace;">{countdown_str}</div>
            </div>
            <div style="text-align:right;">
                <div style="font-size:11px; color:#88929b; margin-bottom:2px;">{yield_lbl}</div>
                <div class="app-value neon-green-text" style="font-size:22px;">+{session_generated:,.1f} <span style="font-size:11px; color:#ffffff;">NEXA</span></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # --- 🟢 模块 4：总账户资产详情 ---
    with st.container(border=True):
        node_header = "PARTICIPANT NODE ➔" if lang == "English" else "当前连接节点 ➔"
        st.markdown(f'<div class="app-title" style="margin-bottom:12px;">{node_header}</div>', unsafe_allow_html=True)
        
        run_status = "RUNNING" if st.session_state.app_running else "STANDBY"
        status_lbl = "MINING STATUS:" if lang=="English" else "挖矿状态:"
        earnings_lbl = "TOTAL ACCUMULATED:" if lang=="English" else "账户总累计代币:"
        status_color = "#A2FF00" if st.session_state.app_running else "#88929b"
        
        st.markdown(f"""
        <div style="display:flex; justify-content:space-between; margin-bottom:5px;">
            <span style="font-size:11px; color:#88929b; font-weight:bold;">{status_lbl}</span>
            <span style="font-size:11px; color:#88929b; font-weight:bold;">{earnings_lbl}</span>
        </div>
        <div style="display:flex; justify-content:space-between; align-items:baseline;">
            <span style="color:{status_color}; font-size:15px; font-weight:800;">● {run_status}</span>
            <span class="app-value neon-green-text" style="font-size:24px;">{st.session_state.app_earned:,.2f} <span style="font-size:13px; color:#ffffff; font-weight:normal;">NEXA</span></span>
        </div>
        """, unsafe_allow_html=True)

    # 🕹️ 核心驱动大按钮
    if not st.session_state.app_running:
        btn_start_txt = "ACTIVATE TIMED SESSION 🟢" if lang == "English" else "启动边缘算力节点（时控模式） 🟢"
        if st.button(btn_start_txt, key="app_start_btn"):
            now_dt = datetime.now()
            end_dt = now_dt + timedelta(minutes=st.session_state.target_duration_min)
            st.session_state.start_time_str = now_dt.strftime('%H:%M:%S')
            st.session_state.end_time_str = end_dt.strftime('%H:%M:%S')
            st.session_state.elapsed_seconds = 0
            st.session_state.timer_completed = False
            st.session_state.app_running = True
            st.rerun()
    else:
        btn_stop_txt = "FORCE TERMINATE SESSION 🛑" if lang == "English" else "强行终止当前会话 🛑"
        if st.button(btn_stop_txt, key="app_stop_btn"):
            st.session_state.app_running = False
            st.rerun()

    # 高频心跳驱动
    if st.session_state.app_running:
        st.session_state.app_earned += 0.25       
        st.session_state.elapsed_seconds += 1     
        time.sleep(1.0)  
        st.rerun()

# ==================== 📧 底部统一白名单递交表单 ====================
st.markdown("<hr style='border:1px solid #1e272e; margin-top:25px;'>", unsafe_allow_html=True)
st.markdown(f'<h3 style="text-align:center; color:#A2FF00; font-size:22px; margin-bottom:15px;">{"🚀 Secure Your Early Whitelist Seat" if lang=="English" else "🚀 锁定早期测试网白名单席位"}</h3>', unsafe_allow_html=True)

with st.form("unified_whitelist_form"):
    u_email = st.text_input("Email Address" if lang=="English" else "您的电子邮箱:")
    u_wallet = st.text_input("Solana Wallet Address" if lang=="English" else "Solana 钱包地址:")
    submitted = st.form_submit_button("SUBMIT & RETAIN SEAT ⚡" if lang=="English" else "提交并归档体验收益 ⚡")
    if submitted:
        if u_email.strip() != "":
            with open("whitelist.txt", "a", encoding="utf-8") as f:
                f.write(f"Email: {u_email} | Wallet: {u_wallet} | Score: {st.session_state.app_earned:.1f}\n")
            st.balloons()

if os.path.exists("whitelist.txt"):
    with open("whitelist.txt", "r", encoding="utf-8") as f:
        whitelist_data = f.read()
    st.download_button(
        label="📥 Download Whitelist Data" if lang=="English" else "📥 下载白名单数据",
        data=whitelist_data,
        file_name="nexaedge_whitelist.txt",
        mime="text/plain",
        key="admin_download_btn"
    )

# ==================== 📊 页面浏览量计数器 ====================
st.markdown("<hr style='border:1px solid #1e272e; margin-top:25px;'>", unsafe_allow_html=True)
visitor_counter_html = """
<div style="text-align: center; margin-top: 5px; opacity: 0.85;">
    <p style="color: #88929b; font-size: 11px; margin-bottom: 8px; letter-spacing: 1px;">➔ NEXAEDGE NETWORK NODE STATUS</p>
    <a href="https://info.flagcounter.com/NexaEdge">
        <img src="https://s11.flagcounter.com/count2/NexaEdge/bg_0B0F12/txt_A2FF00/border_1E272E/columns_3/maxflags_9/viewers_3/labels_1/pageviews_1/flags_0/" alt="Flag Counter" border="0" style="border-radius: 8px; border: 1px solid #1e272e; max-width: 100%;">
    </a>
</div>
"""
st.markdown(visitor_counter_html, unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#445; font-size: 11px; margin-top:15px;'>NexaEdge Network © 2026 | Powered by Solana DePIN Infrastructure</p>", unsafe_allow_html=True)
