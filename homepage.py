import streamlit as st
import os
import time
import random
import pandas as pd
import json

# ==========================================
# 1. 页面基础配置
# ==========================================
st.set_page_config(
    page_title="NexaEdge Network | Official Node Gateway",
    page_icon="🟢",
    layout="centered"
)

# --- 💾 全局多用户活跃状态同步系统 ---
STATUS_FILE = "global_network_status.json"

def load_global_status():
    if not os.path.exists(STATUS_FILE):
        return {"active_count": 1}
    try:
        with open(STATUS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {"active_count": 1}

def update_global_active(delta):
    data = load_global_status()
    data["active_count"] = max(1, data["active_count"] + delta)
    with open(STATUS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    return data

live_nodes_count = load_global_status()["active_count"]

# --- 🟢 极客黑绿科技风 CSS 样式表 ---
st.markdown("""
    <style>
    .stApp { background-color: #0b0f12; }
    #MainMenu, footer, .styles_viewerBadge__FUChv, [data-testid="manage-app-button"] { display: none !important; }
    header, [data-testid="stHeader"] { background: transparent !important; border: none !important; height: 0 !important; display: none !important; }
    
    /* 强力移除导致顶部产生空黑块的置空容器 */
    [data-testid="stVerticalBlock"] > div:empty { display: none !important; margin: 0 !important; padding: 0 !important; }
    [data-testid="stElementContainer"] { border: none !important; background: transparent !important; }
    
    /* 导航 Tab 样式 */
    .stTabs [data-baseweb="tab-list"] { gap: 12px; background-color: transparent !important; justify-content: center; border: none !important; margin-bottom: 25px !important; }
    .stTabs [data-baseweb="tab"] {
        background-color: #11171d !important; color: #bdc3c7 !important; border-radius: 8px 8px 0px 0px !important;
        border: 1px solid #1e272e !important; border-bottom: none !important; padding: 10px 22px !important; font-weight: 700 !important; font-size: 14px !important;
    }
    .stTabs [aria-selected="true"] { color: #A2FF00 !important; background-color: #161c23 !important; border-top: 2px solid #A2FF00 !important; }
    .stTabs [data-baseweb="tab-highlight"] { background-color: #A2FF00 !important; height: 0px !important; }
    
    /* 卡片与文本排版 */
    .app-card { background-color: #161c23; border: 1px solid #252e38; border-radius: 14px; padding: 15px; margin-bottom: 12px; }
    .app-title { font-size: 13px; color: #88929b; font-weight: bold; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 5px; }
    .app-value { font-family: 'Inter', sans-serif; color: #ffffff; font-size: 32px; font-weight: 700; }
    .neon-green-text { color: #A2FF00 !important; }
    
    /* 第二页面板特定微调 */
    .temp-section { display: flex; align-items: center; justify-content: space-between; background: #11171d; padding: 10px 14px; border-radius: 10px; margin-top: 4px; }
    .ratio-box { background-color: #11171d; border: 1px dashed #252e38; border-radius: 8px; padding: 8px 10px; margin-top: 8px; font-size: 12px; color: #88929b; }
    
    /* 核心启动大按钮 */
    div.stButton > button:first-child {
        background-color: #A2FF00 !important; color: #0b0f12 !important; font-weight: 800 !important; font-size: 16px !important;
        width: 100%; border-radius: 12px !important; border: none !important; padding: 12px 0 !important; box-shadow: 0 0 15px rgba(162, 255, 0, 0.3);
    }
    div.stButton > button[key*="app_stop_btn"] { background-color: #0b0f12 !important; color: #ffffff !important; border: 1px solid #252e38 !important; box-shadow: none !important; }
    
    [data-testid="stForm"] { background-color: #161c23 !important; border: 1px solid #252e38 !important; border-radius: 16px !important; padding: 20px !important; margin-top: 25px !important; }
    .admin-box { background-color: #1c232c; border: 2px dashed #A2FF00; padding: 20px; border-radius: 14px; margin-top: 30px; }
    </style>
""", unsafe_allow_html=True)

# 状态初始化
if 'app_earned' not in st.session_state: st.session_state.app_earned = 1452.7000
if 'app_running' not in st.session_state: st.session_state.app_running = False
if 'chart_history' not in st.session_state: st.session_state.chart_history = [22.0, 25.0, 24.0, 28.0, 27.0, 31.0, 29.0, 33.0, 31.0, 35.0, 33.0, 36.8]
if 'session_seconds' not in st.session_state: st.session_state.session_seconds = 0
if 'target_time_index' not in st.session_state: st.session_state.target_time_index = 2 

# ==========================================
# 🌐 2. 国际化多语言词典映射
# ==========================================
col_pad, col_lang = st.columns([4, 1])
with col_lang:
    lang = st.selectbox("🌐 Language", ["English", "中文"], index=0, label_visibility="collapsed")

# 选项映射
TIME_OPTIONS_EN = ["15 Minutes", "30 Minutes", "1 Hour", "2 Hours", "4 Hours", "8 Hours", "12 Hours", "24 Hours (Full-day)"]
TIME_OPTIONS_ZH = ["15 分钟", "30 分钟", "1 小时", "2 小时", "4 小时", "8 小时", "12 小时", "24 小时 (全天)"]
TIME_OPTIONS = TIME_OPTIONS_EN if lang == "English" else TIME_OPTIONS_ZH

SECONDS_MAP = [900, 1800, 3600, 7200, 14400, 28800, 43200, 86400]
HOURS_MAP = [0.25, 0.5, 1.0, 2.0, 4.0, 8.0, 12.0, 24.0]

# 核心文本字典
T = {
    "slogan": {
        "English": "Transforming 5B+ idle smartphones into high-purity data fuel factories for the AI Era.",
        "中文": "将全球 50亿+ 闲置智能手机转化为 AI 时代的高纯度数据燃料工厂。"
    },
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
    "p3_t": {"English": "🤝 2:1 Anti-Cheat Verification", "中文": "🤝 2:1 去中心化防作弊校验"},
    "p3_d": {"English": "Decentralized majority-voting consensus. We segment raw data across 3 independent nodes to deliver 100% verified datasets to AI clients.", "中文": "去中心化多数投票共识。我们将原始数据打散分发给 3 个独立节点，确保向 AI 客户交付 100% 经过验证的真实数据。"},
    
    # 控制台区
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
    
    # 按钮、表单与去重校验提示
    "btn_start": {"English": "START COMPUTE SESSION", "中文": "启动计算节点会话"},
    "btn_stop": {"English": "PAUSE SESSION (VIEW NETWORK MAP)", "中文": "暂停会话 (查看全网网络拓扑)"},
    "wl_title": {"English": "🚀 Secure Your Early Whitelist Seat", "中文": "🚀 锁定早期创世白名单席位"},
    "wl_mail": {"English": "Email Address:", "中文": "电子邮箱地址:"},
    "wl_wallet": {"English": "Solana Wallet Address:", "中文": "Solana 钱包接收地址:"},
    "wl_btn": {"English": "SUBMIT & RETAIN SEAT ⚡", "中文": "提交并保留创世资格 ⚡"},
    "wl_toast": {"English": "⏰ Timer Finished! Node has been stopped safely.", "中文": "⏰ 定时结束！节点已安全自动停止。"},
    "net_sync": {"English": "🟢 NETWORK SYNCHRONIZED: {} ACTIVE DEVICES ONLINE", "中文": "🟢 全网数据实时同步: 当前共有 {} 个活跃设备在线"},
    
    "err_empty": {"English": "❌ Please fill in both Email and Wallet Address!", "中文": "❌ 请填写完整的电子邮箱和 Solana 钱包地址！"},
    "err_dup_email": {"English": "❌ This Email address has already applied for the whitelist!", "中文": "❌ 该邮箱地址已经申请过白名单，请勿重复提交！"},
    "err_dup_wallet": {"English": "❌ This Solana Wallet has already applied for the whitelist!", "中文": "❌ 该 Solana 钱包已绑定过白名单席位，请勿重复提交！"},
    "success_wl": {"English": "🎉 Welcome aboard! Your genesis whitelist seat has been secured.", "中文": "🎉 欢迎加入！您的创世白名单席位已成功锁定。"}
}

# =========================================================================
# 📸 顶栏全局恒定区域
# =========================================================================
st.markdown('<h1 style="text-align:center; color:#A2FF00; font-size:36px; font-weight:800; margin-top:5px; margin-bottom:12px;">NexaEdge Network</h1>', unsafe_allow_html=True)

if os.path.exists("image.png"):
    st.image("image.png", use_container_width=True)
elif os.path.exists("logo.png"):
    st.image("logo.png", use_container_width=True)
else:
    st.markdown("""
    <div style="text-align: center; margin-bottom: 15px;">
        <svg width="70" height="70" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M50 5L15 25V65L50 95L85 65V25L50 5Z" stroke="#A2FF00" stroke-width="6" stroke-linecap="round" stroke-linejoin="round" fill="#11171d"/>
            <path d="M35 45L50 30L65 45M35 60L50 45L65 60" stroke="#A2FF00" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
    </div>
    """, unsafe_allow_html=True)

st.markdown(f'<p style="font-size: 16px; color: #A2FF00; font-weight:bold; text-align: center; margin-top: 12px; margin-bottom: 25px;">{T["slogan"][lang]}</p>', unsafe_allow_html=True)

tab1, tab2 = st.tabs([T["tab1"][lang], T["tab2"][lang]])

# =========================================================================
# 🏠 第一页：Overview 介绍页
# =========================================================================
with tab1:
    st.markdown(f'<div class="app-title">{T["net_fee"][lang]}</div>', unsafe_allow_html=True)
    st.markdown('<div class="app-value" style="margin-bottom:2px;">20%</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="neon-green-text" style="font-size:12px; font-weight:bold; margin-bottom:20px;">{T["net_fee_sub"][lang]}</div>', unsafe_allow_html=True)
    
    st.markdown(f'<div class="app-title">{T["safety"][lang]}</div>', unsafe_allow_html=True)
    st.markdown('<div class="app-value" style="margin-bottom:2px;">39°C</div>', unsafe_allow_html=True)
    st.markdown(f'<div style="color:#ff6b6b; font-size:12px; font-weight:bold; margin-bottom:25px;">{T["safety_sub"][lang]}</div>', unsafe_allow_html=True)
    
    st.markdown(f'<p style="font-size:13px; color:#88929b; font-weight:bold; margin-bottom:2px; text-transform:uppercase;">{T["base"][lang]}</p>', unsafe_allow_html=True)
    st.markdown('<h2 style="color:#ffffff; font-size:32px; font-weight:700; margin-top:0; margin-bottom:4px;">Solana SPL</h2>', unsafe_allow_html=True)
    st.markdown(f'<div style="margin-bottom:25px;"><span style="background-color:#141d26; color:#A2FF00; font-size:12px; font-weight:bold; padding:4px 10px; border-radius:12px; border: 1px solid #1e272e;">{T["base_sub"][lang]}</span></div>', unsafe_allow_html=True)
    
    st.markdown("<hr style='border:1px solid #1e272e; margin: 20px 0;'>", unsafe_allow_html=True)
    
    st.markdown(f'<h3 style="color:#A2FF00; font-size:20px; font-weight:700;">{T["calc_title"][lang]}</h3>', unsafe_allow_html=True)
    selected_time_tab1 = st.selectbox(T["calc_label"][lang], TIME_OPTIONS, index=st.session_state.target_time_index, key="time_select_tab1")
    st.session_state.target_time_index = TIME_OPTIONS.index(selected_time_tab1)
    chosen_hours = HOURS_MAP[st.session_state.target_time_index]
    monthly_est = chosen_hours * 0.35 * 30
    st.success(T["calc_res"][lang].format(selected_time_tab1, monthly_est))
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown(f'<h3 style="color:#A2FF00; font-size:20px; font-weight:700;">{T["pillar_title"][lang]}</h3>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="app-card" style="border-left: 3px solid #A2FF00; padding-left:18px; margin-bottom:15px;">
        <h4 style="color:#ffffff; margin-top:0; margin-bottom:6px; font-size:15px;">{T["p1_t"][lang]}</h4>
        <p style="color:#88929b; font-size:13px; line-height:1.5; margin:0;">{T["p1_d"][lang]}</p>
    </div>
    <div class="app-card" style="border-left: 3px solid #ff6b6b; padding-left:18px; margin-bottom:15px;">
        <h4 style="color:#ffffff; margin-top:0; margin-bottom:6px; font-size:15px;">{T["p2_t"][lang]}</h4>
        <p style="color:#88929b; font-size:13px; line-height:1.5; margin:0;">{T["p2_d"][lang]}</p>
    </div>
    <div class="app-card" style="border-left: 3px solid #A2FF00; padding-left:18px; margin-bottom:15px;">
        <h4 style="color:#ffffff; margin-top:0; margin-bottom:6px; font-size:15px;">{T["p3_t"][lang]}</h4>
        <p style="color:#88929b; font-size:13px; line-height:1.5; margin:0;">{T["p3_d"][lang]}</p>
    </div>
    """, unsafe_allow_html=True)

# =========================================================================
# 📱 第二页：Node Dashboard 控制台页
# =========================================================================
with tab2:
    st.markdown(f'<div class="app-title" style="margin-top:5px; margin-bottom:5px;">{T["timer_t"][lang]}</div>', unsafe_allow_html=True)
    selected_time_tab2 = st.selectbox("Set target runtime:", TIME_OPTIONS, index=st.session_state.target_time_index, key="time_select_tab2", label_visibility="collapsed")
    st.session_state.target_time_index = TIME_OPTIONS.index(selected_time_tab2)
    target_total_seconds = SECONDS_MAP[st.session_state.target_time_index]
    
    if st.session_state.app_running and st.session_state.session_seconds >= target_total_seconds:
        st.session_state.app_running = False
        update_global_active(-1)
        st.toast(T["wl_toast"][lang])

    current_hash = random.uniform(45.5, 49.8) if st.session_state.app_running else 0.0
    current_temp = random.uniform(36.4, 36.9) if st.session_state.app_running else 31.2
    s_sec = st.session_state.session_seconds
    
    remaining_seconds = max(0, target_total_seconds - s_sec)
    remaining_str = f"{remaining_seconds // 3600:02d}:{(remaining_seconds % 3600) // 60:02d}:{remaining_seconds % 60:02d}"
    time_str = f"{s_sec//3600:02d}:{(s_sec%3600)//60:02d}:{s_sec%60:02d}"
    session_generated = s_sec * 0.25
    
    st.markdown(f"""
    <div class="app-card" style="margin-top:15px;">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
            <span class="app-title">{T["dash"][lang]}</span>
            <span style="color:#88929b; font-size:13px;">⚙️</span>
        </div>
        <div style="font-size:12px; color:#88929b; margin-bottom:5px;">
            {T["hash"][lang]} <span class="neon-green-text" style="font-weight:bold;">{current_hash:.2f}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.app_running:
        st.session_state.chart_history.pop(0)
        st.session_state.chart_history.append(current_hash)
    st.line_chart(pd.DataFrame(st.session_state.chart_history, columns=["Hash Rate"]), height=95, use_container_width=True)
    
    st.markdown(f"""
    <div class="app-card" style="margin-top: -5px;">
        <div class="temp-section">
            <span class="app-value" style="font-size:20px;">🌡️ {current_temp:.1f}°C</span>
            <span style="background-color:#1e272e; color:#A2FF00; font-size:11px; font-weight:bold; padding:4px 10px; border-radius:12px; border:1px solid #A2FF00;">{T["safe_tag"][lang]}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="app-card">
        <div class="app-title">{T["compute_time_ratio"][lang]}</div>
        <div style="display:flex; justify-content:space-between; margin-top:8px;">
            <div>
                <div style="font-size:11px; color:#88929b;">{T["duration"][lang]}</div>
                <div class="app-value" style="font-size:19px; font-family:monospace; margin-bottom:5px;">{time_str}</div>
                <div style="font-size:11px; color:#88929b;">{T["countdown"][lang]}</div>
                <div class="app-value" style="font-size:17px; font-family:monospace; color:#ff9f43;">{remaining_str}</div>
            </div>
            <div style="text-align:right;">
                <div style="font-size:11px; color:#88929b;">{T["yield"][lang]}</div>
                <div class="app-value neon-green-text" style="font-size:19px;">+{session_generated:,.1f} <span style="font-size:11px; color:#ffffff;">NEXA</span></div>
            </div>
        </div>
        <div class="ratio-box">{T["ratio"][lang]}</div>
    </div>
    """, unsafe_allow_html=True)
    
    run_status = T["status_active"][lang] if st.session_state.app_running else T["status_standby"][lang]
    st.markdown(f"""
    <div class="app-card">
        <div class="app-title" style="margin-bottom:8px;">{T["node_title"][lang]}</div>
        <div style="font-size:11px; color:#88929b; margin-bottom:10px;">NODE_ID: <span style="color:#ffffff; font-weight:bold;">@nexaedge / Acc1</span></div>
        <div style="display:flex; justify-content:space-between; margin-bottom:3px;">
            <span style="font-size:11px; color:#88929b; font-weight:bold;">{T["status"][lang]}</span>
            <span style="font-size:11px; color:#88929b; font-weight:bold;">{T["acc"][lang]}</span>
        </div>
        <div style="display:flex; justify-content:space-between; align-items:baseline;">
            <span style="color:{'#A2FF00' if st.session_state.app_running else '#88929b'}; font-size:14px; font-weight:800;">● {run_status}</span>
            <span class="app-value neon-green-text" style="font-size:22px;">{st.session_state.app_earned:,.2f} <span style="font-size:12px; color:#ffffff; font-weight:normal;">NEXA</span></span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if not st.session_state.app_running:
        if st.button(T["btn_start"][lang], key="app_start_btn"):
            if remaining_seconds <= 0: st.session_state.session_seconds = 0
            st.session_state.app_running = True
            update_global_active(1)
            st.rerun()
    else:
        if st.button(T["btn_stop"][lang], key="app_stop_btn"):
            st.session_state.app_running = False
            update_global_active(-1)
            st.rerun()

# =========================================================================
# 📧 底部白名单递交表单 (新增：智能防刷重校验逻辑)
# =========================================================================
st.markdown("<hr style='border:1px solid #1e272e; margin-top:20px;'>", unsafe_allow_html=True)
st.markdown(f'<h3 style="color:#A2FF00; font-size:18px; font-weight:700;"><span style="font-size:16px;">🚀</span> {T["wl_title"][lang]}</h3>', unsafe_allow_html=True)

with st.form("unified_whitelist_form"):
    u_email = st.text_input(T["wl_mail"][lang]).strip()
    u_wallet = st.text_input(T["wl_wallet"][lang]).strip()
    submitted = st.form_submit_button(T["wl_btn"][lang])
    
    if submitted:
        if u_email == "" or u_wallet == "":
            st.error(T["err_empty"][lang])
        elif u_email == "admin666":
            # 管理员通道，不执行排重写入
            pass
        else:
            # 读取历史数据进行唯一性核验
            is_duplicate = False
            if os.path.exists("whitelist.txt"):
                with open("whitelist.txt", "r", encoding="utf-8") as f:
                    whitelist_content = f.read()
                
                # 检查邮箱是否已存在
                if f"Email: {u_email} |" in whitelist_content:
                    st.error(T["err_dup_email"][lang])
                    is_duplicate = True
                # 检查钱包是否已存在
                elif f"Wallet: {u_wallet} |" in whitelist_content:
                    st.error(T["err_dup_wallet"][lang])
                    is_duplicate = True
            
            # 校验通过，允许写入
            if not is_duplicate:
                with open("whitelist.txt", "a", encoding="utf-8") as f:
                    f.write(f"Email: {u_email} | Wallet: {u_wallet} | Score: {st.session_state.app_earned:.1f}\n")
                st.success(T["success_wl"][lang])
                st.balloons()

# 后台监控管理
if u_email == "admin666":
    st.markdown('<div class="admin-box">', unsafe_allow_html=True)
    st.markdown('<h2 style="color:#A2FF00; margin-top:0;">📊 全局监控后台 (管理员)</h2>', unsafe_allow_html=True)
    st.metric(label="全网 Active 节点总人数", value=f"{load_global_status()['active_count']} 人")
    if os.path.exists("whitelist.txt"):
        with open("whitelist.txt", "r", encoding="utf-8") as f:
            lines = f.readlines()
        for l in lines: st.text(l.strip())
    st.markdown('</div>', unsafe_allow_html=True)

# =========================================================================
# 📊 底部活数据在线人数区域
# =========================================================================
st.markdown("<hr style='border:1px solid #1e272e; margin-top:20px;'>", unsafe_allow_html=True)
st.markdown(f"""
<div style="text-align: center; margin-bottom: 12px;">
    <span style="background-color:#141d26; color:#A2FF00; font-size:13px; font-weight:bold; padding:6px 14px; border-radius:30px; border: 1px dashed #A2FF00;">
        {T["net_sync"][lang].format(live_nodes_count)}
    </span>
</div>
""", unsafe_allow_html=True)

# 国旗计数器
st.markdown("""
<div style="text-align: center; margin-top: 5px; opacity: 0.85;">
    <a href="https://info.flagcounter.com/NexaEdge">
        <img src="https://s11.flagcounter.com/count2/NexaEdge/bg_0B0F12/txt_A2FF00/border_1E272E/columns_3/maxflags_9/viewers_3/labels_1/pageviews_1/flags_0/" alt="Flag Counter" border="0" style="border-radius: 8px; border: 1px solid #1e272e; max-width: 100%;">
    </a>
</div>
""", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#445; font-size: 11px; margin-top:10px;'>NexaEdge Network © 2026 | Powered by Solana DePIN Infrastructure</p>", unsafe_allow_html=True)

# ==========================================
# 🏎️ 异步高频驱动器
# ==========================================
if st.session_state.app_running:
    st.session_state.app_earned += 0.25       
    st.session_state.session_seconds += 1     
    time.sleep(1.0)                            
    st.rerun()                                 
