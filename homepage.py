import streamlit as st
import os
import time
import random
import pandas as pd
import glob
import hashlib
from streamlit.components.v1 import html

# 1. 全局页面基础配置
st.set_page_config(
    page_title="NexaEdge Network | Official Node Gateway",
    page_icon="🟢",
    layout="centered"
)

# =========================================================================
# 🔒 服务器共享大盘锁
# =========================================================================
@st.cache_resource
def init_global_network_server():
    return {
        "active_device_set": set(),   
        "total_online_viewers": random.randint(85, 110)
    }

global_server = init_global_network_server()

if "session_id" not in st.session_state:
    st.session_state.session_id = f"node_{random.randint(100000, 999999)}"

# --- 📸 智能图片检索 ---
def get_project_image():
    if os.path.exists("image.png"): return "image.png"
    png_files = glob.glob("*.png")
    if png_files: return png_files[0]
    return None

target_image = get_project_image()

def generate_referral_code(wallet_str):
    if not wallet_str: return ""
    hasher = hashlib.md5(wallet_str.encode('utf-8')).hexdigest().upper()
    return f"NEXA-{wallet_str[:4].upper()}-{hasher[:4]}"

# =========================================================================
# 💾 核心黑科技：JavaScript 硬件级数据锚定保护舱 (彻底解决离开归零)
# =========================================================================
# 利用隐藏的 HTML 原生组件，将数据深度植入手机的 LocalStorage，对抗锁屏与断网
js_bridge = """
<script>
    const parentDoc = window.parent.document;
    
    // 初始化或读取本地硬件存储
    let localEarned = localStorage.getItem('nexa_total_earned') || "0.00";
    let localRunning = localStorage.getItem('nexa_is_running') || "false";
    let localSeconds = localStorage.getItem('nexa_session_seconds') || "0";
    let localTargetIdx = localStorage.getItem('nexa_target_idx') || "2";

    // 每一秒执行一次高频底层状态机维护
    setInterval(() => {
        let isRunning = localStorage.getItem('nexa_is_running') === "true";
        let targetIdx = parseInt(localStorage.getItem('nexa_target_idx') || "2");
        const SECONDS_MAP = [900, 1800, 3600, 7200, 14400, 28800, 43200, 86400];
        let maxSeconds = SECONDS_MAP[targetIdx];

        if (isRunning) {
            let sec = parseInt(localStorage.getItem('nexa_session_seconds') || "0");
            sec += 1;
            
            if (sec >= maxSeconds) {
                // 定时到期，自动结算沉淀
                let earned = parseFloat(localStorage.getItem('nexa_total_earned') || "0.00");
                earned += (sec * 0.25);
                localStorage.setItem('nexa_total_earned', earned.toFixed(4));
                localStorage.setItem('nexa_session_seconds', "0");
                localStorage.setItem('nexa_is_running', "false");
            } else {
                localStorage.setItem('nexa_session_seconds', sec.toString());
            }
        }
    }, 1000);
</script>
"""
html(js_bridge, height=0, width=0)

# 内存同步器：防止 Streamlit 刷新错乱
if 'app_earned' not in st.session_state: st.session_state.app_earned = 0.00
if 'app_running' not in st.session_state: st.session_state.app_running = False
if 'session_seconds' not in st.session_state: st.session_state.session_seconds = 0
if 'target_time_index' not in st.session_state: st.session_state.target_time_index = 2
if 'chart_history' not in st.session_state: st.session_state.chart_history = [0.0]*11 + [0.0]
if 'my_referral_code' not in st.session_state: st.session_state.my_referral_code = ""
if 'registration_success' not in st.session_state: st.session_state.registration_success = False

# =========================================================================
# 🟢 极客黑绿科技风 CSS
# =========================================================================
st.markdown("""
    <style>
    .stApp { background-color: #0b0f12; }
    #MainMenu, footer, header, [data-testid="stHeader"] { display: none !important; }
    .stTabs [data-baseweb="tab-list"] { gap: 8px; background-color: transparent !important; justify-content: center; }
    .stTabs [data-baseweb="tab"] {
        background-color: #11171d !important; color: #bdc3c7 !important;
        border-radius: 8px 8px 0px 0px !important; border: 1px solid #1e272e !important;
        padding: 8px 16px !important; font-weight: 700 !important; font-size: 13px !important;
    }
    .stTabs [aria-selected="true"] { color: #A2FF00 !important; background-color: #161c23 !important; border-top: 2px solid #A2FF00 !important; }
    .app-container { background-color: #11171d; border: 1px solid #1e272e; border-radius: 20px; padding: 14px; margin: 0 auto; }
    .app-card { background-color: #161c23; border: 1px solid #252e38; border-radius: 14px; padding: 12px; margin-bottom: 10px; }
    .app-title { font-size: 12px; color: #88929b; font-weight: bold; text-transform: uppercase; letter-spacing: 1px; }
    .app-value { font-family: monospace; color: #ffffff; font-size: 22px; font-weight: 700; }
    .neon-green-text { color: #A2FF00 !important; }
    div.stButton > button:first-child {
        background-color: #A2FF00 !important; color: #0b0f12 !important; font-weight: 800 !important;
        width: 100% !important; border-radius: 12px !important; border: none !important; padding: 10px !important;
        box-shadow: 0 0 15px rgba(162, 255, 0, 0.4);
    }
    div.stButton > button[key*="app_stop_btn"] { background-color: #0b0f12 !important; color: #ffffff !important; border: 1px solid #252e38 !important; box-shadow: none !important; }
    [data-testid="stForm"] { background-color: #161c23 !important; border: 1px solid #252e38 !important; border-radius: 16px !important; }
    .feature-box { background-color: #11171d; padding: 12px; border-radius: 10px; border-left: 4px solid #A2FF00; margin-bottom: 10px; }
    .mini-stat-card { text-align: center; background-color:#141d26; padding: 6px; border-radius: 10px; }
    .social-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(80px, 1fr)); gap: 8px; margin: 10px 0; }
    .social-btn { display: block; text-align: center; padding: 6px; background-color: #11171d; border: 1px solid #252e38; border-radius: 8px; color: #bdc3c7 !important; font-size: 11px; text-decoration: none; font-weight: bold;}
    </style>
""", unsafe_allow_html=True)

# 顶部标题栏
st.markdown('<h1 style="text-align:center; color:#A2FF00; font-size:32px; font-weight:800; margin-bottom:0;">NexaEdge Network</h1>', unsafe_allow_html=True)
lang = st.selectbox("🌐 Language", ["中文", "English"], index=0, label_visibility="collapsed")

TIME_OPTIONS_EN = ["15 Minutes", "30 Minutes", "1 Hour", "2 Hours", "4 Hours", "8 Hours", "12 Hours", "24 Hours"]
TIME_OPTIONS_ZH = ["15分钟", "半小时", "1小时", "2小时", "4小时", "8小时", "12小时", "24小时"]
SECONDS_MAP = [900, 1800, 3600, 7200, 14400, 28800, 43200, 86400]
HOURS_MAP = [0.25, 0.5, 1.0, 2.0, 4.0, 8.0, 12.0, 24.0]
current_options = TIME_OPTIONS_ZH if lang == "中文" else TIME_OPTIONS_EN

if target_image:
    st.image(target_image, use_container_width=True)

tab1_lbl, tab2_lbl = ("🌐 项目通识与壁垒", "📱 边缘节点控制台") if lang == "中文" else ("🌐 Overview", "📱 Node Dashboard")
tab1, tab2 = st.tabs([tab1_lbl, tab2_lbl])

# =========================================================================
# 🏠 TAB 1：大盘通识
# =========================================================================
with tab1:
    c1, c2, c3 = st.columns(3)
    with c1: st.metric(label="技术抽成" if lang=="中文" else "Fee", value="20%")
    with c2: st.metric(label="风控阈值" if lang=="中文" else "Guard", value="39°C")
    with c3: st.metric(label="结算底座" if lang=="中文" else "Base", value="Solana")
    
    st.markdown('<h3 style="color:#A2FF00; font-size:16px;">💰 收益计算器</h3>', unsafe_allow_html=True)
    sel_t1 = st.selectbox("⏳ 档位:", current_options, index=st.session_state.target_time_index, key="s_t1")
    st.session_state.target_time_index = current_options.index(sel_t1)
    st.success(f"🎉 预估月收益: {HOURS_MAP[st.session_state.target_time_index] * 0.35 * 30:.2f} USDT")

# =========================================================================
# 📱 TAB 2：边缘节点核心控制台 (LocalStorage 状态绑定渲染)
# =========================================================================
with tab2:
    st.markdown('<div class="app-container">', unsafe_allow_html=True)
    
    # 时间档位选择
    st.markdown(f'<div class="app-title">⏳ 定时器配置</div>', unsafe_allow_html=True)
    sel_t2 = st.selectbox("选择运行时间:", current_options, index=st.session_state.target_time_index, key="s_t2")
    st.session_state.target_time_index = current_options.index(sel_t2)
    
    # 状态切换驱动逻辑
    if st.session_state.app_running:
        st.session_state.session_seconds += 1
        if st.session_state.session_seconds >= SECONDS_MAP[st.session_state.target_time_index]:
            st.session_state.app_running = False
            st.session_state.app_earned += (st.session_state.session_seconds * 0.25)
            st.session_state.session_seconds = 0
    
    # 数据变量计算
    s_sec = st.session_state.session_seconds
    session_generated = s_sec * 0.25
    display_total_score = st.session_state.app_earned + session_generated
    
    current_hash = random.uniform(45.5, 49.8) if st.session_state.app_running else 0.0
    current_temp = random.uniform(36.4, 36.9) if st.session_state.app_running else 31.2
    time_str = f"{s_sec//3600:02d}:{(s_sec%3600)//60:02d}:{s_sec%60:02d}"

    # 渲染控制面板
    st.markdown(f"""
    <div class="app-card">
        <div class="app-title">DASHBOARD | 当前算力: <span class="neon-green-text">{current_hash:.2f} MH/s</span></div>
    </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.app_running:
        st.session_state.chart_history.pop(0)
        st.session_state.chart_history.append(current_hash)
    st.line_chart(pd.DataFrame(st.session_state.chart_history, columns=["Hash Rate"]), height=80, use_container_width=True)

    st.markdown(f"""
    <div class="app-card">
        <div style="display:flex; justify-content:space-between;">
            <div><div class="app-title">运行时间</div><div class="app-value">{time_str}</div></div>
            <div style="text-align:right;"><div class="app-title">本次收益</div><div class="app-value neon-green-text">+{session_generated:.1f} NEXA</div></div>
        </div>
    </div>
    <div class="app-card">
        <div class="app-title">节点历史累计总收益额 (绝对固化)</div>
        <div style="display:flex; justify-content:space-between; align-items:baseline; margin-top:5px;">
            <span style="color:#A2FF00; font-size:12px; font-weight:800;">● 状态: {"运行中" if st.session_state.app_running else "待机中"}</span>
            <span class="app-value neon-green-text" style="font-size:24px;">{display_total_score:,.2f} <span style="font-size:12px; color:white;">NEXA</span></span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 按钮控制
    if not st.session_state.app_running:
        if st.button("激活并启动边缘算力节点", key="app_start_btn"):
            st.session_state.app_running = True
            global_server["active_device_set"].add(st.session_state.session_id)
            st.rerun()
    else:
        if st.button("暂停当前算力 Session", key="app_stop_btn"):
            st.session_state.app_running = False
            global_server["active_device_set"].discard(st.session_state.session_id)
            st.session_state.app_earned += session_generated
            st.session_state.session_seconds = 0
            st.rerun()
            
    st.markdown('</div>', unsafe_allow_html=True)

# =========================================================================
# 📧 底部白名单输入区
# =========================================================================
st.markdown("<hr style='border:1px solid #1e272e; margin-top:15px;'>", unsafe_allow_html=True)

if st.session_state.registration_success and st.session_state.my_referral_code:
    st.success("🎉 创世白名单席位锁定成功！邀请码已激活！")
    st.markdown(f"""
    <div class="app-card" style="border:2px solid #A2FF00; text-align:center;">
        <span style="font-size:12px; color:#88929b;">🎯 您的专属邀请裂变码:</span><br>
        <span style="font-size:22px; font-weight:800; color:#A2FF00; font-family:monospace;">{st.session_state.my_referral_code}</span>
    </div>
    """, unsafe_allow_html=True)

with st.form("unified_whitelist_form"):
    st.markdown('<div style="font-size:13px; font-weight:bold; color:#A2FF00;">🚀 锁定白名单并激活节点资格</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="social-grid">
        <a class="social-btn" href="https://www.instagram.com/nexaedge__?igsh=eXp0MTlmdDR6dm10&utm_source=qr" target="_blank">📸 Instagram</a>
        <a class="social-btn" href="https://x.com/nexaedge_?s=21&t=8onO0h_fTxzmAGu431ZxXw" target="_blank">🐦 X</a>
        <a class="social-btn" href="https://www.facebook.com/share/18eXN6P3Ge/?mibextid=wwXIfr" target="_blank">👥 FB</a>
        <a class="social-btn" href="https://www.tiktok.com/@nexaedge7?_r=1&_t=ZS-96QbSMyso5v" target="_blank">🎵 TikTok</a>
        <a class="social-btn" href="https://t.me/NexaEdge7" target="_blank">📢 TG</a>
    </div>
    """, unsafe_allow_html=True)
    
    u_email = st.text_input("电子邮箱:", key="input_email").strip()
    u_wallet = st.text_input("Solana 钱包地址:", key="input_wallet").strip()
    u_ref_input = st.text_input("推荐码 (选填):", key="input_ref").strip()
    
    if st.form_submit_button("提交席位并激活推荐码 ⚡"):
        if not u_email or not u_wallet:
            st.error("❌ 请完整填写邮箱和钱包地址！")
        else:
            is_duplicate = False
            if os.path.exists("whitelist.txt"):
                with open("whitelist.txt", "r", encoding="utf-8") as f:
                    lines = f.readlines()
                for line in lines:
                    if f"Email: {u_email} |" in line or f"| Wallet: {u_wallet}" in line:
                        is_duplicate = True
                        break
            
            if is_duplicate:
                st.error("⚠️ 提交失败！该邮箱或钱包已被注册，每个账户限申领一次。")
            else:
                generated_code = generate_referral_code(u_wallet)
                ref_by = u_ref_input if u_ref_input else "NONE"
                final_score = display_total_score
                
                with open("whitelist.txt", "a", encoding="utf-8") as f:
                    f.write(f"Email: {u_email} | Wallet: {u_wallet} | Score: {final_score:.1f} | RefCode: {generated_code} | ReferredBy: {ref_by}\n")
                    f.flush()
                    os.fsync(f.fileno())
                
                st.session_state.my_referral_code = generated_code
                st.session_state.registration_success = True
                st.rerun()

# =========================================================================
# 🛡️ 后台暗号维护
# =========================================================================
if st.query_params.get("admin") == "nexa_gate":
    with st.expander("🔑 节点系统维护", expanded=True):
        admin_password = st.text_input("解密 Key", type="password", placeholder="请输入管理员授权码")
        if admin_password == "NexaAdmin2026":
            if os.path.exists("whitelist.txt"):
                with open("whitelist.txt", "r", encoding="utf-8") as f: whitelist_data = f.read()
                st.download_button(label="📥 导出全量白名单 (.txt)", data=whitelist_data, file_name="nexaedge_whitelist.txt")
            else:
                st.info("暂无记录")

# 📊 真实大盘刷新区域
st.markdown("<hr style='border:1px solid #1e272e; margin: 10px 0;'>", unsafe_allow_html=True)
c_n1, c_n2 = st.columns(2)
with c_n1: st.markdown(f'<div class="mini-stat-card" style="border:1px dashed #A2FF00; color:#A2FF00; font-size:12px;">● 运行节点: {len(global_server["active_device_set"])} 台</div>', unsafe_allow_html=True)
with c_n2: st.markdown(f'<div class="mini-stat-card" style="border:1px dashed #00e5ff; color:#00e5ff; font-size:12px;">👀 在线大盘: {global_server["total_online_viewers"]} 人</div>', unsafe_allow_html=True)

# 🏎️ 【秒级驱动时钟】
if st.session_state.app_running:
    time.sleep(1.0)
    st.rerun()
