import streamlit as st
import time
import random
import pandas as pd

# ==========================================
# 1. 页面基础配置（必须是绝对的第一句）
# ==========================================
st.set_page_config(
    page_title="NexaEdge Network | Official Node Gateway",
    page_icon="🟢",
    layout="centered"
)

# ==========================================
# 🔒 服务器进程级内存安全锁（多线程安全）
# ==========================================
@st.cache_resource
def get_global_network_memory():
    # 设定安全的初始活跃基数
    return {
        "active_count": 451,
        "whitelist_db": []
    }

global_memory = get_global_network_memory()

# --- ⚙️ 顶层状态变量 ---
if 'app_earned' not in st.session_state: st.session_state.app_earned = 1452.7000
if 'chart_history' not in st.session_state: st.session_state.chart_history = [22.0, 25.0, 24.0, 28.0, 27.0, 31.0, 29.0, 33.0, 31.0, 35.0, 33.0, 36.8]
if 'target_time_index' not in st.session_state: st.session_state.target_time_index = 2 
if 'app_running' not in st.session_state: st.session_state.app_running = False
if 'just_finished' not in st.session_state: st.session_state.just_finished = False
if 'session_seconds' not in st.session_state: st.session_state.session_seconds = 0
if 'last_tick_time' not in st.session_state: st.session_state.last_tick_time = 0.0

# --- 🔄 跨页面/放视频 物理时间差精确补偿 ---
if st.session_state.app_running and st.session_state.last_tick_time > 0:
    now = time.time()
    elapsed_real_seconds = int(now - st.session_state.last_tick_time)
    if elapsed_real_seconds > 0:
        st.session_state.session_seconds += elapsed_real_seconds
        st.session_state.app_earned += elapsed_real_seconds * 0.25
        st.session_state.last_tick_time = now

# ==========================================
# 🟢 极客黑绿全套视觉样式表
# ==========================================
st.markdown("""
    <style>
    .stApp { background-color: #0b0f12; }
    /* NexaEdge 专属科技发光虚拟 Logo 样式 */
    .logo-container { text-align: center; padding: 35px 10px; background: radial-gradient(circle, rgba(162,255,0,0.09) 0%, rgba(11,15,18,0) 70%); border-radius: 20px; margin-bottom: 5px; }
    .logo-text { color: #A2FF00; font-size: 38px; font-weight: 900; letter-spacing: -1px; text-shadow: 0 0 25px rgba(162, 255, 0, 0.4); margin: 0; }
    /* 精致半透明黑卡片 */
    .app-card { background-color: #161c23; border: 1px solid #252e38; border-radius: 14px; padding: 15px; margin-bottom: 12px; }
    .app-title { font-size: 13px; color: #88929b; font-weight: bold; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 5px; }
    .app-value { font-family: 'Inter', sans-serif; color: #ffffff; font-size: 32px; font-weight: 700; }
    .neon-green-text { color: #A2FF00 !important; }
    .temp-section { display: flex; align-items: center; justify-content: space-between; background: #11171d; padding: 10px 14px; border-radius: 10px; margin-top: 4px; }
    .ratio-box { background-color: #11171d; border: 1px dashed #252e38; border-radius: 8px; padding: 8px 10px; margin-top: 8px; font-size: 12px; color: #88929b; }
    /* 按钮样式强化 */
    div.stButton > button:first-child {
        background-color: #A2FF00 !important; color: #0b0f12 !important; font-weight: 800 !important; font-size: 16px !important;
        width: 100%; border-radius: 12px !important; border: none !important; padding: 12px 0 !important; box-shadow: 0 0 15px rgba(162, 255, 0, 0.3);
    }
    div.stButton > button[key*="app_stop_btn"] { background-color: #0b0f12 !important; color: #ffffff !important; border: 1px solid #252e38 !important; box-shadow: none !important; }
    [data-testid="stForm"] { background-color: #161c23 !important; border: 1px solid #252e38 !important; border-radius: 16px !important; padding: 20px !important; margin-top: 20px !important; }
    </style>
""", unsafe_allow_html=True)
# ==========================================
# 🌐 语言包配置
# ==========================================
col_pad, col_lang = st.columns([4, 1])
with col_lang:
    lang = st.selectbox("🌐 Language", ["English", "中文"], index=1, label_visibility="collapsed", key="global_lang")

TIME_OPTIONS_EN = ["15 Minutes", "30 Minutes", "1 Hour", "2 Hours", "4 Hours", "8 Hours", "12 Hours", "24 Hours (Full-day)"]
TIME_OPTIONS_ZH = ["15 分钟", "30 分钟", "1 小时", "2 小时", "4 小时", "8 小时", "12 小时", "24 小时 (全天)"]
TIME_OPTIONS = TIME_OPTIONS_EN if lang == "English" else TIME_OPTIONS_ZH

SECONDS_MAP = [900, 1800, 3600, 7200, 14400, 28800, 43200, 86400]
HOURS_MAP = [0.25, 0.5, 1.0, 2.0, 4.0, 8.0, 12.0, 24.0]

T = {
    "slogan": {"English": "Transforming 5B+ idle smartphones into high-purity data fuel factories for the AI Era.", "中文": "将全球 50亿+ 闲置智能手机转化为 AI 时代的高纯度数据燃料工厂。"},
    "tab1": {"English": "🌐 Overview & Pillars", "中文": "🌐 项目概述与核心支柱"},
    "tab2": {"English": "📱 Node Dashboard (Live)", "中文": "📱 节点控制台 (实时)"},
    "net_fee": {"English": "Network Fee", "中文": "网络服务费比例"},
    "net_fee_sub": {"English": "↑ Pure Revenue Flow", "中文": "↑ 纯粹网络收益分配流"},
    "safety": {"English": "Safety Threshold", "中文": "硬件安全温度阈值"},
    "safety_sub": {"English": "↑ Device Safety Lock", "中文": "↑ 设备高温自动安全锁"},
    "base": {"English": "Settlement Base", "中文": "底层结算公链"},
    "base_sub": {"English": "↑ Low Gas / High TPS", "中文": "↑ 极低 Gas 消耗 / 高并发 TPS"},
    "calc_title": {"English": "💰 Device Revenue Calculator", "中文": "💰 设备收益预估计算器"},
    "calc_label": {"English": "Select Daily Session Duration Pattern:", "中文": "选择每日设备预计在线运行时长:"},
    "calc_res": {"English": "🎉 Estimated Monthly Yield (Based on {}/day): {:.2f} USDT", "中文": "🎉 预估每月稳健收益 (基于 每日{}/在线): {:.2f} USDT"},
    "pillar_title": {"English": "⚡ Key Pillars", "中文": "⚡ 核心技术支柱"},
    "p1_t": {"English": "📱 Passive Income via Charging", "中文": "📱 充电即可获得的被动收入"},
    "p1_d": {"English": "Earn ~0.35 USDT/hr. Just plug in, connect Wi-Fi, and lock your screen. Our lightweight WASM Sandbox cleans AI datasets silently in the background.", "中文": "每小时约赚 0.35 USDT。只需插上充电器，连接 Wi-Fi 并锁屏，我们的轻量级 WASM 沙箱就会在后台静默清洗 AI 数据集。"},
    "p2_t": {"English": "🔥 39°C Thermal Guard", "中文": "🔥 39°C 电池热量守护者"},
    "p2_d": {"English": "Total hardware protection. System auto-throttles computing loads instantly if the battery touches 39°C. Zero degradation anxiety.", "中文": "全方位硬件保护。一旦电池温度触及 39°C，系统将瞬间自动降频、削减计算负载。完全不用担心电池损耗问题。"},
    "timer_t": {"English": "⏳ COMPUTE TIMER (AUTO-STOP)", "中文": "⏳ 计算计时器 (到时自动停止)"},
    "dash": {"English": "DASHBOARD", "中文": "核心控制面板"},
    "hash": {"English": "NETWORK HASH RATE (MH/s):", "中文": "当前节点算力 (MH/s):"},
    "safe_tag": {"English": "SAFE", "中文": "安全运行"},
    "compute_time_ratio": {"English": "COMPUTE TIME & RATIO", "中文": "计算时长与速率明细"},
    "duration": {"English": "SESSION DURATION:", "中文": "本次在线时长:"},
    "countdown": {"English": "COUNTDOWN TO STOP:", "中文": "距离自动停止倒计时:"},
    "yield": {"English": "SESSION YIELD:", "中文": "本次产生收益:"},
    "ratio": {"English": "⚡ <b>EST. RATIO:</b> 0.25 NEXA / sec (≈ 900 NEXA/hr)", "中文": "⚡ <b>预估速率:</b> 0.25 NEXA / 秒 (≈ 900 NEXA/小时)"},
    "node_title": {"English": "PARTICIPANT NODE ➔", "中文": "参与节点信息 ➔"},
    "status": {"English": "MINING STATUS:", "中文": "当前挖矿状态:"},
    "status_active": {"English": "ACTIVE", "中文": "进行中"},
    "status_standby": {"English": "STANDBY", "中文": "待机中"},
    "acc": {"English": "TOTAL ACCUMULATED:", "中文": "累计已获得总收益:"},
    "btn_start": {"English": "START COMPUTE SESSION", "中文": "启动计算节点会话"},
    "btn_stop": {"English": "PAUSE SESSION (VIEW NETWORK MAP)", "中文": "暂停会话 (查看全网网络拓扑)"},
    "wl_title": {"English": "🚀 Secure Your Early Whitelist Seat", "中文": "🚀 锁定早期创世白名单席位"},
    "wl_mail": {"English": "Email Address:", "中文": "电子邮箱地址:"},
    "wl_wallet": {"English": "Solana Wallet Address:", "中文": "Solana 钱包接收地址:"},
    "wl_btn": {"English": "SUBMIT & RETAIN SEAT ⚡", "中文": "提交并保留创世资格 ⚡"},
    "net_sync": {"English": "🟢 NETWORK SYNCHRONIZED: {} ACTIVE DEVICES ONLINE", "中文": "🟢 全网数据实时同步: 当前共有 {} 个活跃设备在线"}
}

# 100% 安全挂载：纯代码渲染极客科技发光 Logo（告别 st.image 引起的红字报错）
st.markdown('<div class="logo-container"><p class="logo-text">NexaEdge Network</p></div>', unsafe_allow_html=True)
st.markdown(f'<p style="font-size: 14px; color: #A2FF00; font-weight:bold; text-align: center; margin-bottom: 25px;">{T["slogan"][lang]}</p>', unsafe_allow_html=True)

tab1, tab2 = st.tabs([T["tab1"][lang], T["tab2"][lang]])

# --- Tab 1 内容 ---
with tab1:
    st.markdown(f'<div class="app-card"><div class="app-title">{T["net_fee"][lang]}</div><div class="app-value">20%</div><div class="neon-green-text" style="font-size:12px; font-weight:bold;">{T["net_fee_sub"][lang]}</div></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="app-card"><div class="app-title">{T["safety"][lang]}</div><div class="app-value">39°C</div><div style="color:#ff6b6b; font-size:12px; font-weight:bold;">{T["safety_sub"][lang]}</div></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="app-card"><div class="app-title">{T["base"][lang]}</div><div class="app-value" style="font-size:26px;">Solana SPL</div><div class="neon-green-text" style="font-size:11px;">{T["base_sub"][lang]}</div></div>', unsafe_allow_html=True)
    
    st.markdown(f'<h3 style="color:#A2FF00; font-size:18px; font-weight:700; margin-top:15px;">{T["calc_title"][lang]}</h3>', unsafe_allow_html=True)
    selected_time_tab1 = st.selectbox(T["calc_label"][lang], TIME_OPTIONS, index=st.session_state.target_time_index, key="time_select_tab1")
    st.session_state.target_time_index = TIME_OPTIONS.index(selected_time_tab1)
    monthly_est = HOURS_MAP[st.session_state.target_time_index] * 0.35 * 30
    st.success(T["calc_res"][lang].format(selected_time_tab1, monthly_est))
    
    st.markdown(f'<h3 style="color:#A2FF00; font-size:18px; font-weight:700; margin-top:15px;">{T["pillar_title"][lang]}</h3>', unsafe_allow_html=True)
    st.markdown(f'<div class="app-card" style="border-left: 3px solid #A2FF00; padding-left:12px; margin-bottom:10px;"><h4 style="color:#ffffff; margin:0 0 4px 0; font-size:14px;">{T["p1_t"][lang]}</h4><p style="color:#88929b; font-size:12px; margin:0;">{T["p1_d"][lang]}</p></div><div class="app-card" style="border-left: 3px solid #ff6b6b; padding-left:12px; margin-bottom:10px;"><h4 style="color:#ffffff; margin:0 0 4px 0; font-size:14px;">{T["p2_t"][lang]}</h4><p style="color:#88929b; font-size:12px; margin:0;">{T["p2_d"][lang]}</p></div>', unsafe_allow_html=True)

# --- Tab 2 内容 ---
with tab2:
    st.markdown(f'<div class="app-title" style="margin-top:5px; margin-bottom:5px;">{T["timer_t"][lang]}</div>', unsafe_allow_html=True)
    if st.session_state.app_running:
        target_total_seconds = SECONDS_MAP[st.session_state.target_time_index]
        st.selectbox("Set target:", TIME_OPTIONS, index=st.session_state.target_time_index, key="time_select_tab2_disabled", disabled=True, label_visibility="collapsed")
    else:
        selected_time_tab2 = st.selectbox("Set target:", TIME_OPTIONS, index=st.session_state.target_time_index, key="time_select_tab2", label_visibility="collapsed")
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
    
    remaining_str = f"{remaining_seconds // 3600:02d}:{(remaining_seconds % 3600) // 60:02d}:{remaining_seconds % 60:02d}"
    time_str = f"{s_sec//3600:02d}:{(s_sec%3600)//60:02d}:{s_sec%60:02d}"
    session_generated = s_sec * 0.25
    
    st.markdown(f'<div class="app-card" style="margin-top:10px;"><div style="font-size:12px; color:#88929b;">{T["hash"][lang]} <span class="neon-green-text" style="font-weight:bold;">{current_hash:.2f}</span></div></div>', unsafe_allow_html=True)
    if st.session_state.app_running:
        st.session_state.chart_history.pop(0)
        st.session_state.chart_history.append(current_hash)
    st.line_chart(pd.DataFrame(st.session_state.chart_history, columns=["Hash Rate"]), height=95)
    
    st.markdown(f'<div class="app-card"><div class="temp-section"><span class="app-value" style="font-size:18px;">🌡️ {current_temp:.1f}°C</span><span style="background-color:#1e272e; color:#A2FF00; font-size:11px; font-weight:bold; padding:2px 8px; border-radius:10px; border:1px solid #A2FF00;">{T["safe_tag"][lang]}</span></div></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="app-card"><div class="app-title">{T["compute_time_ratio"][lang]}</div><div style="display:flex; justify-content:space-between; margin-top:5px;"><div><div style="font-size:11px; color:#88929b;">{T["duration"][lang]}</div><div class="app-value" style="font-size:18px; font-family:monospace;">{time_str}</div><div style="font-size:11px; color:#88929b; margin-top:3px;">{T["countdown"][lang]}</div><div class="app-value" style="font-size:16px; font-family:monospace; color:#ff9f43;">{remaining_str}</div></div><div style="text-align:right;"><div style="font-size:11px; color:#88929b;">{T["yield"][lang]}</div><div class="app-value neon-green-text" style="font-size:20px;">+{session_generated:,.1f} <span style="font-size:11px; color:#ffffff;">NEXA</span></div></div></div><div class="ratio-box">{T["ratio"][lang]}</div></div>', unsafe_allow_html=True)
    
    run_status = T["status_active"][lang] if st.session_state.app_running else T["status_standby"][lang]
    st.markdown(f'<div class="app-card"><div class="app-title">{T["node_title"][lang]}</div><div style="font-size:11px; color:#88929b; margin-bottom:5px;">NODE_ID: <span style="color:#ffffff; font-weight:bold;">@nexaedge / Acc1</span></div><div style="display:flex; justify-content:space-between;"><span style="font-size:11px; color:#88929b;">{T["status"][lang]}</span><span style="font-size:11px; color:#88929b;">{T["acc"][lang]}</span></div><div style="display:flex; justify-content:space-between; align-items:baseline;"><span style="color:{"#A2FF00" if st.session_state.app_running else "#88929b"}; font-size:14px; font-weight:800;">● {run_status}</span><span class="app-value neon-green-text" style="font-size:22px;">{st.session_state.app_earned:,.2f} <span style="font-size:11px; color:#ffffff; font-weight:normal;">NEXA</span></span></div></div>', unsafe_allow_html=True)

    if not st.session_state.app_running:
        if st.button(T["btn_start"][lang], key="app_start_btn"):
            st.session_state.session_seconds = 0
            st.session_state.just_finished = False
            st.session_state.app_running = True
            st.session_state.last_tick_time = time.time()
            global_memory["active_count"] += 1
            st.rerun()
    else:
        if st.button(T["btn_stop"][lang], key="app_stop_btn"):
            st.session_state.app_running = False
            global_memory["active_count"] = max(451, global_memory["active_count"] - 1)
            st.rerun()

# --- 创世白名单申请 ---
with st.form("wl_form"):
    st.markdown(f'<p style="color:#A2FF00; font-weight:bold; margin:0;">{T["wl_title"][lang]}</p>', unsafe_allow_html=True)
    u_email = st.text_input(T["wl_mail"][lang], key="em").strip()
    u_wallet = st.text_input(T["wl_wallet"][lang], key="wa").strip()
    if st.form_submit_button(T["wl_btn"][lang]):
        if u_email and u_wallet:
            global_memory["whitelist_db"].append({"email": u_email, "wallet": u_wallet, "score": f"{st.session_state.app_earned:.1f}"})
            st.success("SUCCESS!")

# ==========================================
# 📊 全球数据实时同步挂件与 Flag Counter 访客计数器（100% 复原加回）
# ==========================================
st.markdown("<hr style='border:1px solid #1e272e; margin-top:20px;'>", unsafe_allow_html=True)
st.markdown(f'<div style="text-align: center; margin-bottom: 12px;"><span style="background-color:#141d26; color:#A2FF00; font-size:13px; font-weight:bold; padding:6px 14px; border-radius:30px; border: 1px dashed #A2FF00;">{T["net_sync"][lang].format(global_memory["active_count"])}</span></div>', unsafe_allow_html=True)

st.markdown("""
<div style="text-align: center; margin-top: 5px; opacity: 0.85;">
    <a href="https://info.flagcounter.com/NexaEdge">
        <img src="https://s11.flagcounter.com/count2/NexaEdge/bg_0B0F12/txt_A2FF00/border_1E272E/columns_3/maxflags_9/viewers_3/labels_1/pageviews_1/flags_0/" alt="Flag Counter" border="0" style="border-radius: 8px; border: 1px solid #1e272e; max-width: 100%;">
    </a>
</div>
""", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#445; font-size: 11px; margin-top:10px;'>NexaEdge Network © 2026 | Powered by Solana DePIN Infrastructure</p>", unsafe_allow_html=True)

if st.session_state.app_running:
    time.sleep(1.0)
    st.session_state.app_earned += 0.25       
    st.session_state.session_seconds += 1     
    st.session_state.last_tick_time = time.time()
    st.rerun()
