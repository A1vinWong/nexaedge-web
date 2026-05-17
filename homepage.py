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
    /* 全局去暗灰背景 */
    .stApp { background-color: #0b0f12; }
    
    /* 彻底隐藏顶部无用白条及右下角开发者管理小标签 */
    #MainMenu, footer, .styles_viewerBadge__FUChv, [data-testid="manage-app-button"], 
    header, [data-testid="stHeader"] {
        display: none !important;
    }
    
    /* 模块样式 */
    .feature-box {
        background-color: #11171d; 
        padding: 20px; 
        border-radius: 10px; 
        border-left: 5px solid #A2FF00; 
        margin-bottom: 20px;
    }
    
    /* 优化原生 st.container 卡片的背景色与边框 */
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
    
    /* 优化温度计：改成 flex 轴线对齐，并整体向上微调 */
    .temp-section {
        display: flex;
        align-items: center;
        justify-content: space-between;
        background: #11171d;
        padding: 12px 15px;
        border-radius: 12px;
        margin-top: 5px;
        margin-bottom: 2px;
    }
    
    /* 优化时产虚线框：向上提一点，更工整 */
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
    
    .stTabs [data-baseweb="tab-list"] { gap: 10px; justify-content: center; }
    .stTabs [data-baseweb="tab"] {
        background-color: #11171d !important;
        color: #bdc3c7 !important;
        border-radius: 8px 8px 0px 0px !important;
        padding: 10px 20px !important;
        font-weight: 700 !important;
    }
    .stTabs [aria-selected="true"] { color: #A2FF00 !important; border-bottom-color: #A2FF00 !important; }
    
    /* 按钮基础样式 */
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
if 'session_seconds' not in st.session_state: st.session_state.session_seconds = 0

# 顶栏主标题
st.markdown('<h1 style="text-align:center; color:#A2FF00; font-size:38px; font-weight:800; margin-top:10px; margin-bottom:10px;">NexaEdge Network</h1>', unsafe_allow_html=True)

# 双语切换选择器
lang = st.selectbox("🌐 Choose Language / 选择语言", ["English", "中文"], index=0)

tab1_title = "🌐 Overview & Pillars" if lang == "English" else "🌐 项目通识与壁垒"
tab2_title = "📱 Node Dashboard (Live)" if lang == "English" else "📱 边缘节点控制台 (实时)"

tab1, tab2 = st.tabs([tab1_title, tab2_title])

# =========================================================================
# 🏠 第一页：项目介绍与通识壁垒
# =========================================================================
with tab1:
    if target_image:
        st.image(target_image, caption="NexaEdge App Preview", use_container_width=True)

    if lang == "English":
        st.markdown('<p style="font-size: 19px; color: #A2FF00; font-weight:bold; text-align: center; margin-top: 15px; margin-bottom: 25px;">Transforming 5B+ idle smartphones into high-purity data fuel factories for the AI Era.</p>', unsafe_allow_html=True)
        
        c1, c2, c3 = st.columns(3)
        with c1: st.metric(label="Network Fee", value="20%", delta="Pure Revenue Flow")
        with c2: st.metric(label="Safety Threshold", value="39°C", delta="Device Safety Lock", delta_color="inverse")
        with c3: st.metric(label="Settlement Base", value="Solana SPL", delta="Low Gas / High TPS")

        st.markdown("<hr style='border:1px solid #1e272e;'>", unsafe_allow_html=True)

        st.markdown('<h2 style="color:#A2FF00; font-size:24px; margin-top:15px;">💰 Device Revenue Calculator</h2>', unsafe_allow_html=True)
        hours = st.slider("Estimated Overnight Duration (Hours/Day):", min_value=1, max_value=12, value=6)
        device_os = st.radio("Operating System:", ["iOS (iPhone)", "Android"], horizontal=True, key="os_en")
        monthly_est = hours * 0.35 * 30
        st.success(f"🎉 Estimated Monthly Yield: {monthly_est:.2f} USDT")

        st.markdown('<h2 style="color:#A2FF00; font-size:24px; margin-top:20px;">⚡ Key Pillars</h2>', unsafe_allow_html=True)
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
    else:
        st.markdown('<p style="font-size: 19px; color: #A2FF00; font-weight:bold; text-align: center; margin-top: 15px; margin-bottom: 25px;">让全球 50 亿部闲置手机，成为 AI 时代的高纯度语料燃料工厂</p>', unsafe_allow_html=True)

        c1, c2, c3 = st.columns(3)
        with c1: st.metric(label="平台技术抽成", value="20%", delta="纯现金流造血")
        with c2: st.metric(label="智能硬件风控", value="39°C", delta="秒级控温预警", delta_color="inverse")
        with c3: st.metric(label="算力结算底座", value="Solana SPL", delta="极速、低 Gas")

        st.markdown("<hr style='border:1px solid #1e272e;'>", unsafe_allow_html=True)

        st.markdown('<h2 style="color:#A2FF00; font-size:24px; margin-top:15px;">💰 设备收益计算器</h2>', unsafe_allow_html=True)
        hours = st.slider("预估每日夜间闲置充电时长 (小时/天):", min_value=1, max_value=12, value=6)
        device_os = st.radio("操作系统类型:", ["iOS (iPhone)", "Android"], horizontal=True, key="os_zh")
        monthly_est = hours * 0.35 * 30
        st.success(f"🎉 预计每月可为您带来收益约: {monthly_est:.2f} USDT")

        st.markdown('<h2 style="color:#A2FF00; font-size:24px; margin-top:20px;">⚡ 核心壁垒</h2>', unsafe_allow_html=True)
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
            <h4 style="color:white; margin-top:0; font-size:17px;">🤝 2:1 拜占庭冗余反作弊校验</h4>
            <p style="color:#bdc3c7; font-size:13px;">去中心化多数投票共识。我们将原始语料切片分发至 3 个完全独立的边缘节点进行交叉校验，确保向 AI 客户交付 100% 真实、未被污染的高纯度数据集。</p>
        </div>
        """, unsafe_allow_html=True)

# =========================================================================
# 📱 第二页：边缘节点控制台
# =========================================================================
with tab2:
    if target_image:
        st.image(target_image, use_container_width=True)
        
    st.markdown("<div style='margin-top:15px;'></div>", unsafe_allow_html=True)
    
    # --- 📊 模块 1：控制面板 ---
    with st.container(border=True):
        panel_title = "DASHBOARD" if lang == "English" else "控制面板"
        st.markdown(f'<div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;"><span class="app-title">{panel_title}</span><span style="color:#88929b; font-size:14px;">⚙️</span></div>', unsafe_allow_html=True)
        
        current_hash = random.uniform(45.5, 49.8) if st.session_state.app_running else 0.0
        hash_label = "NETWORK HASH RATE" if lang == "English" else "当前节点算力"
        st.markdown(f'<div style="font-size:11px; color:#88929b; margin-bottom:5px;">{hash_label} (MH/s): <span class="neon-green-text" style="font-weight:bold;">{current_hash:.2f}</span></div>', unsafe_allow_html=True)
        
        if st.session_state.app_running:
            st.session_state.chart_history.pop(0)
            st.session_state.chart_history.append(current_hash)
        chart_df = pd.DataFrame(st.session_state.chart_history, columns=["Hash Rate"])
        st.line_chart(chart_df, height=105, use_container_width=True)
        
        # 🟢 基础模拟温度生成
        current_temp = random.uniform(36.4, 36.9) if st.session_state.app_running else 31.2
        
        # ------ 🔥 【新增功能】系统级过热检测机制 ------
        # 注：若要测试弹窗效果，可以临时把 39.0 改成 36.6 
        if st.session_state.app_running and current_temp >= 39.0:
            # 1. 弹出系统级 Toast 气泡
            st.toast("🔥 OVERHEAT WARNING DETECTED!" if lang == "English" else "🔥 检测到硬件核心过热警告！", icon="⚠️")
            # 2. 顶部红色强力系统警告横幅
            st.error("⚠️ EMERGENCY STOP: Device temperature hit {:.1f}°C! Auto-throttling activated.".format(current_temp) if lang == "English" else "⚠️ 紧急停机：设备温度已达 {:.1f}°C！熔断控温机制已强制启动。".format(current_temp))
            # 3. 强制关停节点，防止损坏
            st.session_state.app_running = False
            time.sleep(1.0)
            st.rerun()
        # ---------------------------------------------
        
        status_tag = "SAFE" if lang == "English" else "安全控温中"
        
        st.markdown(f"""
        <div class="temp-section">
            <div style="display:flex; align-items:center; line-height:1;"><span style="font-size:22px; margin-right:8px; display:inline-block; vertical-align:middle;">🌡️</span><span class="app-value" style="font-size:22px; display:inline-block; vertical-align:middle;">{current_temp:.1f}°C</span></div>
            <span style="background-color:#1e272e; color:#A2FF00; font-size:11px; font-weight:bold; padding:5px 12px; border-radius:12px; border:1px solid #A2FF00; line-height:1;">{status_tag}</span>
        </div>
        """, unsafe_allow_html=True)
    
    # --- ⏱️ 模块 2：运行时长与收益比面板 ---
    with st.container(border=True):
        timer_title = "COMPUTE TIME & RATIO" if lang == "English" else "算力运行时长与收益比"
        st.markdown(f'<div class="app-title">{timer_title}</div>', unsafe_allow_html=True)
        
        s_sec = st.session_state.session_seconds
        time_str = f"{s_sec//3600:02d}:{(s_sec%3600)//60:02d}:{s_sec%60:02d}"
        session_generated = s_sec * 0.25
        
        t_label = "SESSION DURATION:" if lang == "English" else "本次连续运行时间:"
        r_label = "EST. RATIO:" if lang == "English" else "当前时产比折算:"
        ratio_text = "0.25 NEXA / sec (≈ 900 NEXA/hr)" if lang == "English" else "0.25 NEXA / 秒 (约 900 NEXA/小时)"
        yield_lbl = "SESSION YIELD:" if lang == "English" else "本次会话已产出:"
        
        st.markdown(f"""
        <div style="display:flex; justify-content:space-between; margin-top:8px; margin-bottom:12px;">
            <div style="text-align:left;">
                <div style="font-size:11px; color:#88929b; margin-bottom:2px;">{t_label}</div>
                <div class="app-value" style="font-size:20px; color:#ffffff; font-family:monospace;">{time_str}</div>
            </div>
            <div style="text-align:right;">
                <div style="font-size:11px; color:#88929b; margin-bottom:2px;">{yield_lbl}</div>
                <div class="app-value neon-green-text" style="font-size:20px;">+{session_generated:,.1f} <span style="font-size:11px; color:#ffffff;">NEXA</span></div>
            </div>
        </div>
        <div class="ratio-box">
            ⚡ <b>{r_label}</b> {ratio_text}
        </div>
        """, unsafe_allow_html=True)
    
    # --- 🟢 模块 3：节点全局总详情 ---
    with st.container(border=True):
        node_header = "PARTICIPANT NODE ➔" if lang == "English" else "当前连接节点 ➔"
        st.markdown(f'<div class="app-title" style="margin-bottom:12px;">{node_header}</div>', unsafe_allow_html=True)
        st.markdown('<div style="font-size:12px; color:#88929b; margin-bottom:12px;">NODE_ID: <span style="color:#ffffff; font-weight:bold;">@nexaedge / Acc1 (active)</span></div>', unsafe_allow_html=True)
        
        if lang == "English":
            run_status = "ACTIVE" if st.session_state.app_running else "STANDBY"
            status_lbl = "MINING STATUS:"
            earnings_lbl = "TOTAL ACCUMULATED:"
        else:
            run_status = "运行中" if st.session_state.app_running else "待机就绪"
            status_lbl = "挖矿状态:"
            earnings_lbl = "账户总累计代币:"
            
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

    # 🕹️ 核心控制大按钮
    if not st.session_state.app_running:
        btn_start_txt = "START COMPUTE SESSION" if lang == "English" else "启动边缘算力节点 🟢"
        if st.button(btn_start_txt, key="app_start_btn"):
            st.session_state.app_running = True
            st.rerun()
    else:
        btn_stop_txt = "PAUSE SESSION (VIEW NETWORK MAP)" if lang == "English" else "暂停运行 (查看网络拓扑图) 🛑"
        if st.button(btn_stop_txt, key="app_stop_btn"):
            st.session_state.app_running = False
            st.rerun()
            
    # 实时刷新时钟动画渲染
    if st.session_state.app_running:
        st.session_state.app_earned += 0.25       
        st.session_state.session_seconds += 1     
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
                f.write(f"Email: {u_email} | Wallet: {u_wallet} | Score: {st.session_state.app_earned:.1f} | ActiveTime: {st.session_state.session_seconds}s\n")
            st.balloons()
            st.success(f"🎯 Saved successfully with {st.session_state.app_earned:,.1f} $NEXA score!")

# ==================== 📥 后台管理员白名单下载 ====================
if os.path.exists("whitelist.txt"):
    with open("whitelist.txt", "r", encoding="utf-8") as f:
        whitelist_data = f.read()
    
    st.download_button(
        label="📥 Download Whitelist Data (Admin Only)" if lang=="English" else "📥 下载白名单数据 (管理员专用)",
        data=whitelist_data,
        file_name="nexaedge_whitelist.txt",
        mime="text/plain",
        key="admin_download_btn"
    )
else:
    st.markdown("<p style='text-align:center; color:#555; font-size:12px; margin-top:15px;'>暂无白名单数据提交 / No data submitted yet</p>", unsafe_allow_html=True)

# ==================== 📊 访客计数器展示 ====================
st.markdown("<hr style='border:1px solid #1e272e; margin-top:25px;'>", unsafe_allow_html=True)
visitor_counter_html = """
<div style="text-align: center; margin-top: 5px; opacity: 0.85;">
    <p style="color: #88929b; font-size: 11px; margin-bottom: 8px; letter-spacing: 1px;">
        ➔ NEXAEDGE NETWORK NODE STATUS
    </p>
    <a href="https://info.flagcounter.com/NexaEdge">
        <img src="https://s11.flagcounter.com/count2/NexaEdge/bg_0B0F12/txt_A2FF00/border_1E272E/columns_3/maxflags_9/viewers_3/labels_1/pageviews_1/flags_0/" 
             alt="Flag Counter" border="0" style="border-radius: 8px; border: 1px solid #1e272e; max-width: 100%;">
    </a>
</div>
"""
st.markdown(visitor_counter_html, unsafe_allow_html=True)

# 页脚版权
st.markdown("<p style='text-align:center; color:#445; font-size: 11px; margin-top:15px;'>NexaEdge Network © 2026 | Powered by Solana DePIN Infrastructure</p>", unsafe_allow_html=True)
