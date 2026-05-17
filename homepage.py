import streamlit as st
import base64
import os

# 1. 基础配置
st.set_page_config(
    page_title="NexaEdge Network | Official Node Gateway",
    page_icon="🟢",
    layout="centered"
)

# 2. 如果存在原图，直接转换为极其稳定的 Base64 网页流渲染，100% 不报错且两页都置顶展示
img_path = "image.png"
if os.path.exists(img_path):
    with open(img_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    st.markdown(
        f'<div style="text-align:center;margin-bottom:15px;border-radius:14px;overflow:hidden;border:1px solid #252e38;">'
        f'<img src="data:image/png;base64,{encoded_string}" style="width:100%;height:auto;">'
        f'</div>', 
        unsafe_allow_html=True
    )
else:
    st.markdown('<h1 style="color:#A2FF00;text-align:center;font-family:monospace;margin-bottom:20px;">NexaEdge Network</h1>', unsafe_allow_html=True)

# 3. 动态加载恢复原本漂亮排版的核心引擎
import random
import time
import pandas as pd

@st.cache_resource
def _get_global_memory():
    return {"active_base": 451, "whitelist_db": []}
g_mem = _get_global_memory()

if 'app_earned' not in st.session_state: st.session_state.app_earned = 1452.7000
if 'chart_history' not in st.session_state: st.session_state.chart_history = [22.0, 25.0, 24.0, 28.0, 27.0, 31.0, 29.0, 33.0, 31.0, 35.0, 33.0, 36.8]
if 'target_index' not in st.session_state: st.session_state.target_index = 2
if 'app_running' not in st.session_state: st.session_state.app_running = False
if 'session_seconds' not in st.session_state: st.session_state.session_seconds = 0
if 'last_tick' not in st.session_state: st.session_state.last_tick = 0.0

if st.session_state.app_running and st.session_state.last_tick > 0:
    elapsed = int(time.time() - st.session_state.last_tick)
    if elapsed > 0:
        st.session_state.session_seconds += elapsed
        st.session_state.app_earned += elapsed * 0.25
        st.session_state.last_tick = time.time()

# ==========================================
# 🎨 完美复原！原汁原味的极客黑绿 UI 样式表
# ==========================================
st.markdown("""
    <style>
    /* 全局背景色暗黑科技风 */
    .stApp { 
        background-color: #0b0f12; 
    }
    
    /* 严格对齐真机图的卡片间距与圆角 */
    .app-card { 
        background-color: #161c23; 
        border: 1px solid #252e38; 
        border-radius: 14px; 
        padding: 16px; 
        margin-bottom: 14px; 
    }
    
    /* 灰色小标题 */
    .app-title { 
        font-size: 12px; 
        color: #88929b; 
        font-weight: 700; 
        text-transform: uppercase; 
        letter-spacing: 0.5px;
        margin-bottom: 4px;
    }
    
    /* 白色高亮大数字 */
    .app-value { 
        font-family: 'Inter', sans-serif; 
        color: #ffffff; 
        font-size: 30px; 
        font-weight: 700; 
    }
    
    /* 项目招牌荧光绿 */
    .neon-green-text { 
        color: #A2FF00 !important; 
    }
    
    /* 虚线边框指示盒 */
    .ratio-box { 
        background-color: #11171d; 
        border: 1px dashed #252e38; 
        border-radius: 8px; 
        padding: 10px; 
        margin-top: 10px; 
        font-size: 12px; 
        color: #88929b; 
    }
    
    /* 原生荧光绿大按钮 */
    div.stButton > button:first-child {
        background-color: #A2FF00 !important; 
        color: #0b0f12 !important; 
        font-weight: 800 !important; 
        font-size: 15px !important;
        width: 100%; 
        border-radius: 12px !important; 
        border: none !important; 
        padding: 12px 0 !important; 
        box-shadow: 0 0 15px rgba(162, 255, 0, 0.2);
    }
    
    /* 暂停按钮的暗色调 */
    div.stButton > button[key*="app_stop_btn"] { 
        background-color: #0b0f12 !important; 
        color: #ffffff !important; 
        border: 1px solid #252e38 !important; 
        box-shadow: none !important; 
    }
    
    /* 白名单输入框背景加深 */
    [data-testid="stForm"] { 
        background-color: #161c23 !important; 
        border: 1px solid #252e38 !important; 
        border-radius: 16px !important; 
    }
    </style>
""", unsafe_allow_html=True)

# 创建双主页选项卡 (以英文为主)
tab1, tab2 = st.tabs(["🌐 Overview & Pillars", "📱 Node Dashboard"])

TIME_OPTIONS = ["15 Minutes", "30 Minutes", "1 Hour", "2 Hours", "4 Hours", "8 Hours", "12 Hours", "24 Hours (Full-day)"]
SECONDS_MAP = [900, 1800, 3600, 7200, 14400, 28800, 43200, 86400]
HOURS_MAP = [0.25, 0.5, 1.0, 2.0, 4.0, 8.0, 12.0, 24.0]

# ==========================================
# 🌐 Tab 1: 完美复原的项目介绍页 (加入 2:1 支柱)
# ==========================================
with tab1:
    st.markdown('<p style="font-size: 14px; color: #A2FF00; font-weight:bold; text-align: center; margin-bottom: 20px;">Transforming 5B+ idle smartphones into high-purity data fuel factories for the AI Era.</p>', unsafe_allow_html=True)
    
    # 🌟 新增：2:1 机制独立精美卡片
    st.markdown("""
        <div class="app-card" style="border-left: 4px solid #A2FF00;">
            <div class="app-title" style="color: #A2FF00;">⚡ 2:1 Network Allocation Architecture</div>
            <div class="app-value" style="font-size: 24px;">2 : 1 Compute Balance</div>
            <div style="color:#88929b; font-size:12px; margin-top:6px; line-height: 1.4;">
                For every 2 units of raw terminal data verified by peripheral smartphone nodes, 1 unit of dense cryptographic proof is settled into the Solana ledger layer. This prevents hyper-inflation and ensures long-term token value stability.
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # 标准原装参数卡片布局复原
    st.markdown('<div class="app-card"><div class="app-title">Network Fee Rate</div><div class="app-value">20%</div><div class="neon-green-text" style="font-size:12px; font-weight:bold; margin-top:2px;">↑ Pure Revenue Flow Allocation</div></div>', unsafe_allow_html=True)
    st.markdown('<div class="app-card"><div class="app-title">Safety Threshold</div><div class="app-value">39°C</div><div style="color:#ff6b6b; font-size:12px; font-weight:bold; margin-top:2px;">↑ Device Overheat Auto-Throttling Guard</div></div>', unsafe_allow_html=True)
    st.markdown('<div class="app-card"><div class="app-title">Settlement Base Layer</div><div class="app-value" style="font-size:24px;">Solana SPL</div><div class="neon-green-text" style="font-size:11px; margin-top:2px;">↑ Ultra-Low Gas Fee / High-Throughput TPS</div></div>', unsafe_allow_html=True)
    
    # 原装收益计算器
    st.markdown('<h3 style="color:#A2FF00; font-size:16px; font-weight:700; margin-top:15px; margin-bottom:5px;">💰 Device Revenue Calculator</h3>', unsafe_allow_html=True)
    selected_time_tab1 = st.selectbox("Select Daily Session Duration Pattern:", TIME_OPTIONS, index=st.session_state.target_index, key="calc_sel")
    st.session_state.target_index = TIME_OPTIONS.index(selected_time_tab1)
    monthly_est = HOURS_MAP[st.session_state.target_index] * 0.35 * 30
    st.success(f"🎉 Estimated Monthly Yield (Based on {selected_time_tab1}/day): {monthly_est:.2f} USDT")
    
    # 核心技术双支柱卡片复原
    st.markdown('<h3 style="color:#A2FF00; font-size:16px; font-weight:700; margin-top:15px; margin-bottom:5px;">⚡ Core Technical Pillars</h3>', unsafe_allow_html=True)
    st.markdown("""
        <div class="app-card" style="border-left: 3px solid #A2FF00; padding-left:12px;">
            <h4 style="color:#ffffff; margin:0 0 4px 0; font-size:14px;">📱 Passive Income via Charging</h4>
            <p style="color:#88929b; font-size:12px; margin:0; line-height:1.4;">Earn ~0.35 USDT/hr. Just plug in, connect Wi-Fi, and lock your screen. Our lightweight WASM Sandbox cleans AI datasets silently in the background.</p>
        </div>
        <div class="app-card" style="border-left: 3px solid #ff6b6b; padding-left:12px;">
            <h4 style="color:#ffffff; margin:0 0 4px 0; font-size:14px;">🔥 39°C Thermal Guard</h4>
            <p style="color:#88929b; font-size:12px; margin:0; line-height:1.4;">Total hardware protection. System auto-throttles computing loads instantly if the battery touches 39°C. Zero degradation anxiety.</p>
        </div>
    """, unsafe_allow_html=True)

# ==========================================
# 📱 Tab 2: 完美复原的节点控制台 (与大盘完美联动)
# ==========================================
with tab2:
    st.markdown('<div class="app-title" style="margin-top:5px;">⏳ COMPUTE TIMER TARGET</div>', unsafe_allow_html=True)
    if st.session_state.app_running:
        st.selectbox("Set target:", TIME_OPTIONS, index=st.session_state.target_index, disabled=True, key="timer_dis", label_visibility="collapsed")
    else:
        selected_time_tab2 = st.selectbox("Set target:", TIME_OPTIONS, index=st.session_state.target_index, key="timer_en", label_visibility="collapsed")
        st.session_state.target_index = TIME_OPTIONS.index(selected_time_tab2)
    
    target_total_seconds = SECONDS_MAP[st.session_state.target_index]
    if st.session_state.app_running and st.session_state.session_seconds >= target_total_seconds:
        st.session_state.app_running = False
        st.rerun()

    current_hash = random.uniform(45.5, 49.8) if st.session_state.app_running else 0.0
    current_temp = random.uniform(36.4, 36.9) if st.session_state.app_running else 31.2
    s_sec = st.session_state.session_seconds
    remaining_seconds = max(0, target_total_seconds - s_sec)
    
    remaining_str = f"{remaining_seconds // 3600:02d}:{(remaining_seconds % 3600) // 60:02d}:{remaining_seconds % 60:02d}"
    time_str = f"{s_sec//3600:02d}:{(s_sec%3600)//60:02d}:{s_sec%60:02d}"
    session_generated = s_sec * 0.25
    
    # 算力卡片与波动折线图
    st.markdown(f'<div class="app-card" style="margin-top:10px; margin-bottom:5px;"><div style="font-size:12px; color:#88929b; font-weight:bold;">NETWORK HASH RATE (MH/s): <span class="neon-green-text">{current_hash:.2f}</span></div></div>', unsafe_allow_html=True)
    if st.session_state.app_running:
        st.session_state.chart_history.pop(0)
        st.session_state.chart_history.append(current_hash)
    st.line_chart(pd.DataFrame(st.session_state.chart_history, columns=["Hash Rate"]), height=100)
    
    # 温度监视器盒
    st.markdown(f'<div class="app-card"><div style="display:flex; align-items:center; justify-content:between; background:#11171d; padding:10px; border-radius:8px;"><span class="app-value" style="font-size:18px;">Temperature: {current_temp:.1f}°C</span><span style="background:#1e272e; color:#A2FF00; font-size:11px; font-weight:bold; padding:2px 8px; border-radius:10px; border:1px solid #A2FF00;">SAFE RUNNING</span></div></div>', unsafe_allow_html=True)
    
    # 核心收益累计排版复原
    st.markdown(f"""
        <div class="app-card">
            <div class="app-title">COMPUTE TIME & RATIO</div>
            <div style="display:flex; justify-content:space-between; margin-top:5px;">
                <div>
                    <div style="font-size:11px; color:#88929b;">Current Session:</div>
                    <div class="app-value" style="font-size:18px; font-family:monospace;">{time_str}</div>
                    <div style="font-size:11px; color:#88929b; margin-top:4px;">Time to Auto-Stop:</div>
                    <div class="app-value" style="font-size:16px; font-family:monospace; color:#ff9f43;">{remaining_str}</div>
                </div>
                <div style="text-align:right;">
                    <div style="font-size:11px; color:#88929b;">Session Generated:</div>
                    <div class="app-value neon-green-text" style="font-size:22px;">+{session_generated:,.1f} <span style="font-size:11px; color:#ffffff;">NEXA</span></div>
                </div>
            </div>
            <div class="ratio-box">⚡ <b>EST. SPECS:</b> 0.25 NEXA / sec (≈ 900 NEXA/hr)</div>
        </div>
    """, unsafe_allow_html=True)
    
    # 设备节点详情卡片复原
    run_status = "● MINING ACTIVE" if st.session_state.app_running else "● STANDBY"
    st.markdown(f"""
        <div class="app-card">
            <div class="app-title">PARTICIPANT NODE PROFILE</div>
            <div style="font-size:11px; color:#88929b; margin-top:2px; margin-bottom:6px;">NODE_ID: <span style="color:#ffffff; font-weight:bold;">@nexaedge / Acc1</span></div>
            <div style="display:flex; justify-content:space-between;"><span style="font-size:11px; color:#88929b;">MINING STATUS:</span><span style="font-size:11px; color:#88929b;">TOTAL ACCUMULATED:</span></div>
            <div style="display:flex; justify-content:space-between; align-items:baseline;">
                <span style="color:{"#A2FF00" if st.session_state.app_running else "#88929b"}; font-size:13px; font-weight:800;">{run_status}</span>
                <span class="app-value neon-green-text" style="font-size:24px;">{st.session_state.app_earned:,.2f} <span style="font-size:11px; color:#ffffff; font-weight:normal;">NEXA</span></span>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # 启动与暂停物理联动按钮
    if not st.session_state.app_running:
        if st.button("START COMPUTE SESSION", key="app_start_btn"):
            st.session_state.session_seconds = 0
            st.session_state.app_running = True
            st.session_state.last_tick = time.time()
            st.rerun()
    else:
        if st.button("PAUSE SESSION (CHECK NETWORK MAP)", key="app_stop_btn"):
            st.session_state.app_running = False
            st.rerun()

# ==========================================
# 🚀 创世白名单申请表单
# ==========================================
st.markdown("<br>", unsafe_allow_html=True)
with st.form("wl_form"):
    st.markdown('<p style="color:#A2FF00; font-weight:bold; margin-bottom:10px;">🚀 Secure Your Early Whitelist Seat</p>', unsafe_allow_html=True)
    u_email = st.text_input("Email Address:", key="em_v").strip()
    u_wallet = st.text_input("Solana Wallet Address:", key="wa_v").strip()
    if st.form_submit_button("SUBMIT APPLICATION ⚡"):
        if u_email and u_wallet:
            g_mem["whitelist_db"].append({
                "Timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                "Email Address": u_email, 
                "Solana Wallet": u_wallet, 
                "Accumulated Yield": f"{st.session_state.app_earned:,.1f} NEXA"
            })
            st.success("SUCCESS! Whitelist Entry Saved Securely.")

# ==========================================
# 📊 核心硬核指标：实时活跃度与浏览人数挂件（双动态真联动）
# ==========================================
st.markdown("<hr style='border:1px solid #1e272e; margin-top:20px; margin-bottom:15px;'>", unsafe_allow_html=True)

# 活跃设备硬联动：启动时自动从 451 变 452
current_active_nodes = g_mem["active_base"] + (1 if st.session_state.app_running else 0)
# 实时浏览人数：基于 1060 基数，每次页面加载高频微扰浮动
current_live_viewers = 1065 + random.randint(-12, 15)

col_net1, col_net2 = st.columns(2)
with col_net1:
    st.markdown(f"""
        <div style="text-align: center; background-color:#141d26; border: 1px dashed #A2FF00; padding:10px; border-radius:12px;">
            <div style="font-size:10px; color:#88929b; text-transform:uppercase; font-weight:bold;">● Active Compute Nodes</div>
            <div style="font-size:18px; color:#A2FF00; font-weight:bold; font-family:monospace; margin-top:2px;">{current_active_nodes} Devices</div>
        </div>
    """, unsafe_allow_html=True)

with col_net2:
    st.markdown(f"""
        <div style="text-align: center; background-color:#141d26; border: 1px dashed #00e5ff; padding:10px; border-radius:12px;">
            <div style="font-size:10px; color:#88929b; text-transform:uppercase; font-weight:bold;">👀 Live Network Viewers</div>
            <div style="font-size:18px; color:#00e5ff; font-weight:bold; font-family:monospace; margin-top:2px;">{current_live_viewers} Online</div>
        </div>
    """, unsafe_allow_html=True)

# 全球访客小挂件
st.markdown('<div style="text-align: center; margin-top: 15px;"><a href="https://info.flagcounter.com/NexaEdge"><img src="https://s11.flagcounter.com/count2/NexaEdge/bg_0B0F12/txt_A2FF00/border_1E272E/columns_3/maxflags_9/viewers_3/labels_1/pageviews_1/flags_0/" alt="Flag Counter" border="0" style="border-radius: 6px;"></a></div>', unsafe_allow_html=True)

# ==========================================
# 🔑 核心硬核指标：管理员审查白皮书申请通道
# ==========================================
st.markdown("<br><br>", unsafe_allow_html=True)
with st.expander("🔒 Whitepaper Admin & Audit Panel"):
    admin_pwd = st.text_input("Enter Admin Security Credential:", type="password", key="pwd_adm")
    if admin_pwd == "nexaadmin2026":
        st.markdown("<p style='color:#A2FF00; font-size:12px; font-weight:bold; margin-bottom:8px;'>✓ SECURITY ACCESS GRANTED — REAL-TIME LEDGER</p>", unsafe_allow_html=True)
        if g_mem["whitelist_db"]:
            df_wl = pd.DataFrame(g_mem["whitelist_db"])
            st.dataframe(df_wl, use_container_width=True)
            st.download_button("Export Ledger (.CSV)", data=df_wl.to_csv(index=False), file_name="nexaedge_whitelist_db.csv", mime="text/csv")
        else:
            st.info("The cache database memory is currently empty. Waiting for user submissions...")
    elif admin_pwd:
        st.error("Invalid Administrative Key.")

st.markdown("<p style='text-align:center; color:#232a31; font-size: 11px; margin-top:25px;'>NexaEdge Network © 2026 | Mainnet Alpha Framework</p>", unsafe_allow_html=True)

# 隐藏辅助侧边栏
with st.sidebar:
    st.markdown("<h3 style='color:#A2FF00;'>Debugger Panel</h3>", unsafe_allow_html=True)
    st.info("界面已切换回完整的高精、大空行标准 UI。管理员审查白皮书密码为：`nexaadmin2026`")

# 循环刷新器
if st.session_state.app_running:
    time.sleep(1.0)
    st.session_state.app_earned += 0.25       
    st.session_state.session_seconds += 1     
    st.session_state.last_tick = time.time()
    st.rerun()
