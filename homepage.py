import streamlit as st
import time
import random
import pandas as pd
import hashlib
import os
from streamlit_autorefresh import st_autorefresh

st.set_page_config(
    page_title="NexaEdge Network — Investor Terminal",
    page_icon="🟢",
    layout="centered"
)

DEFAULT_CA = "D7h9MvFDkVxPYeJwSTcE7VkKXo6mygCHYph36P8oeic2"

# ── 终极熔炼版 CSS ──
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Syne:wght@400;600;700;800&display=swap');

.main .block-container {
    padding-top: 1rem !important;
    padding-bottom: 2rem !important;
    max-width: 860px !important;
}
.stApp { background-color: #080c0f; }
#MainMenu, footer, header, [data-testid="stHeader"],
[data-testid="manage-app-button"], .styles_viewerBadge__FUChv { display: none !important; }

.stApp::before {
    content: '';
    position: fixed;
    inset: 0;
    background-image:
        linear-gradient(rgba(162,255,0,0.02) 1px, transparent 1px),
        linear-gradient(90deg, rgba(162,255,0,0.02) 1px, transparent 1px);
    background-size: 40px 40px;
    pointer-events: none;
    z-index: 0;
}

h1, h2, h3, h4, p, div, span, label { font-family: 'Syne', sans-serif !important; }

/* 物理防跳自定义 Radio 导航栏 */
div[data-testid="stRadio"] > label { display: none !important; }
div[data-testid="stRadio"] > div {
    flex-direction: row !important;
    gap: 6px !important;
    border-bottom: 1px solid #1a2530 !important;
    padding-bottom: 8px;
    margin-bottom: 20px;
}
div[data-testid="stRadio"] label[data-baseweb="radio"] {
    background-color: #0e1419 !important;
    color: #556070 !important;
    border-radius: 6px 6px 0 0 !important;
    border: 1px solid #1a2530 !important;
    padding: 8px 16px !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 11px !important;
    font-weight: 700 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.05em !important;
    margin: 0 !important;
}
div[data-testid="stRadio"] label[data-baseweb="radio"]:has(input:checked) {
    color: #a2ff00 !important;
    border-color: #1a2530 !important;
    border-bottom-color: #0e1419 !important;
    background-color: #0e1419 !important;
}
div[data-testid="stRadio"] input { display: none !important; }

[data-testid="stMetric"] { background: #0e1419; border: 1px solid #1a2530; border-radius: 10px; padding: 14px !important; }
[data-testid="stMetricLabel"] { font-family: 'Space Mono', monospace !important; font-size: 9px !important; color: #556070 !important; text-transform: uppercase !important; }
[data-testid="stMetricValue"] { font-size: 22px !important; font-weight: 800 !important; color: #e8edf2 !important; }

div.stButton > button {
    background-color: #a2ff00 !important;
    color: #080c0f !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 11px !important;
    font-weight: 700 !important;
    text-transform: uppercase !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 10px 20px !important;
    width: 100% !important;
}
div.stButton > button:hover { background-color: #b5ff33 !important; }

.nx-card { background: #0e1419; border: 1px solid #1a2530; border-radius: 12px; padding: 18px 20px; margin-bottom: 14px; }
.nx-card-title { font-family: 'Space Mono', monospace; font-size: 10px; color: #556070; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 14px; }
.nx-card-title span { color: #a2ff00; margin-right: 6px; }

.nx-feature { background: #060a0d; border: 1px solid #1a2530; border-left: 3px solid #a2ff00; border-radius: 8px; padding: 14px; margin-bottom: 10px; }
.nx-feature-title { font-size: 12px; font-weight: 700; color: #e8edf2; margin-bottom: 5px; }
.nx-feature-body { font-size: 11px; color: #556070; line-height: 1.6; }

.tag-bad { display: inline-block; background: rgba(244,63,94,0.12); color: #f43f5e; font-family: 'Space Mono'; font-size: 9px; padding: 2px 6px; border-radius: 3px; }
.tag-good { display: inline-block; background: rgba(162,255,0,0.1); color: #a2ff00; font-family: 'Space Mono'; font-size: 9px; padding: 2px 6px; border-radius: 3px; }

.nx-node-grid { display: grid; grid-template-columns: repeat(8, 1fr); gap: 5px; margin: 12px 0; }
.nx-node { aspect-ratio: 1; border-radius: 4px; background: #1a2530; }
.nx-node.active { background: #a2ff00; box-shadow: 0 0 6px rgba(162,255,0,0.4); }
.nx-node.processing { background: #00e5ff; box-shadow: 0 0 6px rgba(0,229,255,0.4); animation: blink 0.8s infinite; }
@keyframes blink { 0%,100%{opacity:1} 50%{opacity:0.3} }

.nx-table { width: 100%; border-collapse: collapse; font-size: 11px; }
.nx-table th { text-align: left; padding: 8px 10px; font-family: 'Space Mono'; font-size: 9px; color: #556070; border-bottom: 1px solid #1a2530; }
.nx-table td { padding: 10px; border-bottom: 1px solid rgba(26,37,48,0.5); color: #556070; }
.nx-table tr:last-child td { border-bottom: none; }

.nx-roadmap-item { border-left: 2px solid #1a2530; padding-left: 16px; padding-bottom: 20px; position: relative; }
.nx-roadmap-item::before { content: ''; position: absolute; left: -5px; top: 4px; width: 8px; height: 8px; border-radius: 50%; background: #1a2530; }
.nx-roadmap-item.current::before { background: #00e5ff; box-shadow: 0 0 6px #00e5ff; }
.nx-roadmap-phase { font-family: 'Space Mono'; font-size: 9px; color: #556070; }
.nx-roadmap-title { font-size: 13px; font-weight: 700; color: #e8edf2; }
.nx-roadmap-body { font-size: 11px; color: #556070; line-height: 1.6; }

.nx-log { background: #040709; border: 1px solid #1a2530; border-radius: 8px; padding: 12px; font-family: 'Space Mono'; font-size: 10px; color: #556070; max-height: 120px; overflow-y: auto; }
.log-success { color: #a2ff00; }
.log-info { color: #00e5ff; }

.social-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(75px, 1fr)); gap: 6px; margin: 10px 0; }
.social-btn { display: block; text-align: center; padding: 7px; background: #0e1419; border: 1px solid #1a2530; border-radius: 8px; color: #556070 !important; font-size: 11px; text-decoration: none; font-weight: bold; }
.social-btn:hover { border-color: #a2ff00; color: #a2ff00 !important; }
</style>
""", unsafe_allow_html=True)

# ── 服务器内存锁与状态初始化 ──
@st.cache_resource
def init_global_server_core():
    return {
        "active_device_set": set(),
        "total_online_viewers": random.randint(142, 168),
        "user_db": {
            "contact@nexaedge.org": {
                "password_hash": hashlib.sha256("nexa2026".encode()).hexdigest(),
                "score": 1479.0,
                "reg_time": "2026-05-18 14:22:05",
                "referral_code": "NX-GLOBAL"
            }
        },
        "whitelist_records": []
    }

global_server = init_global_server_core()

if 'sim_running' not in st.session_state: st.session_state.sim_running = False
if 'sim_tasks' not in st.session_state: st.session_state.sim_tasks = 0
if 'sim_log' not in st.session_state: st.session_state.sim_log = []
if 'sim_nodes' not in st.session_state: st.session_state.sim_nodes = [0] * 64
if 'current_user' not in st.session_state: st.session_state.current_user = None
if 'app_earned' not in st.session_state: st.session_state.app_earned = 0.0

TASK_TYPES = [
    ("SLM inference (Phi-3 mini)", "success"),
    ("RLHF label validation", "info"),
    ("ZK proof generation", "success"),
    ("BFT consensus round", "info"),
    ("Thermal check: 36.8°C ✓", "success")
]

# 高频刷新内核挂载
if st.session_state.sim_running:
    st_autorefresh(interval=1000, key="nexa_refresh_pulse")
    # 数据步进
    st.session_state.sim_tasks += 1
    st.session_state.app_earned += 0.01
    
    # 日志追加
    task, cls = random.choice(TASK_TYPES)
    ts = time.strftime("%H:%M:%S")
    st.session_state.sim_log.append((f"[{ts}] Node #{random.randint(1,64)} → {task}", cls))
    if len(st.session_state.sim_log) > 15: st.session_state.sim_log.pop(0)
    
    # 随机节点高亮
    st.session_state.sim_nodes = [random.choice([0, 1, 2]) for _ in range(64)]
    if st.session_state.current_user:
        global_server["user_db"][st.session_state.current_user]["score"] = st.session_state.app_earned

# ── Header ──
col_logo, col_lang = st.columns([3, 1])
with col_logo:
    st.markdown("""
    <div style="display:flex; align-items:center; gap:10px;">
        <div style="width:10px;height:10px;background:#a2ff00;border-radius:50%;box-shadow:0 0 12px #a2ff00;"></div>
        <div style="font-family:'Syne';font-size:22px;font-weight:800;color:#e8edf2;">
            Nexa<span style="color:#a2ff00;">Edge</span> Network
        </div>
    </div>
    """, unsafe_allow_html=True)
with col_lang:
    lang = st.selectbox("Language", ["English", "中文", "Admin Portal 🔒"], index=0, label_visibility="collapsed")

# ── 绝对受控导航栏（真物理防御） ──
nav_options = ["Market", "Network Console", "Moat & Synergy", "Roadmap & Auth"]
current_tab = st.radio("Nav", nav_options, horizontal=True, label_visibility="collapsed")

# ══════════════════════════════════════
# TAB 1: MARKET & POSTURING
# ══════════════════════════════════════
if current_tab == "Market":
    c1, c2, c3 = st.columns(3)
    with c1: st.metric("Global Idle Devices", "6.8B", "Smartphone NPU cluster")
    with c2: st.metric("Settlement Layer", "Solana SPL", "High TPS / Low Gas")
    with c3: st.metric("Thermal Cap Limit", "39°C", "Hardcoded Protection")

    st.markdown(f"""
    <div class="nx-card">
        <div class="nx-card-title"><span>▸</span> CA Smart Contract Address</div>
        <code style="color:#00e5ff; background:rgba(0,229,255,0.05); padding:6px 12px; border-radius:6px; display:block; border:1px dashed rgba(0,229,255,0.2); font-family:'Space Mono'; font-size:11px;">{DEFAULT_CA}</code>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="nx-card">
        <div class="nx-card-title"><span>▸</span> {"Competitive Landscape" if lang=="English" else "全球竞争格局定位"}</div>
        <table class="nx-table">
            <thead>
                <tr>
                    <th>Dimension</th>
                    <th>Centralized Cloud</th>
                    <th>Grass (Bandwidth)</th>
                    <th style="color:#a2ff00;">NexaEdge</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>Primary Resource</td>
                    <td>Server H100 GPUs</td>
                    <td>Residential IP Proxy</td>
                    <td style="color:#e8edf2; font-weight:bold;">Device NPU + CPU Compute</td>
                </tr>
                <tr>
                    <td>Sybil Resistance</td>
                    <td>KYC / Centralized</td>
                    <td><span class="tag-bad">Low</span> Spoofed via VPN</td>
                    <td><span class="tag-good">High</span> Hardware ID + PoC</td>
                </tr>
                <tr>
                    <td>Thermal Defense</td>
                    <td>Industrial AC</td>
                    <td>N/A</td>
                    <td><span class="tag-good">Active</span> 39°C Hardware Lock</td>
                </tr>
            </tbody>
        </table>
    </div>
    """, unsafe_allow_html=True)

    # 创世白名单申领表单
    with st.form("whitelist_genesis_form"):
        st.markdown(f'<div style="font-size:12px; font-weight:bold; color:#a2ff00; margin-bottom:6px;">🎁 {"CLAIM GENESIS WHITELIST REWARDS" if lang=="English" else "申领创世节点白名单与独家加速"}</div>', unsafe_allow_html=True)
        wl_email = st.text_input("Email:", placeholder="node_operator@domain.com")
        wl_wallet = st.text_input("Solana SPL Wallet Address:", placeholder="Enter public key key for airdrops")
        
        if st.form_submit_button("LOCK GENESIS SEAT ⚡"):
            if wl_email and wl_wallet:
                global_server["whitelist_records"].append({"email": wl_email, "wallet": wl_wallet, "time": time.strftime("%Y-%m-%d %H:%M:%S")})
                st.success("🎉 Genesis allocation locked! Notifications will follow before snapshot." if lang=="English" else "🎉 创世白名单席位成功锁定！快照前将定向发放邮件。")
            else:
                st.error("Fields cannot be empty!" if lang=="English" else "输入框不能为空！")

    st.markdown("""
    <div class="social-grid">
        <a class="social-btn" href="https://x.com/nexaedge_" target="_blank">🐦 X / Twitter</a>
        <a class="social-btn" href="https://t.me/NexaEdge7" target="_blank">📢 Telegram</a>
        <a class="social-btn" href="https://www.instagram.com/nexaedge__" target="_blank">📸 Instagram</a>
        <a class="social-btn" href="mailto:contact@nexaedge.org" style="border-color:#00e5ff; color:#00e5ff !important;">📧 Email US</a>
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════
# TAB 2: NETWORK CONSOLE (RERUN SAFE)
# ══════════════════════════════════════
elif current_tab == "Network Console":
    if st.session_state.current_user:
        st.markdown(f'<div style="background:rgba(0,229,255,0.06); border-left:3px solid #00e5ff; padding:8px 12px; border-radius:4px; font-size:11px; font-family:\'Space Mono\'; margin-bottom:12px; color:#e8edf2;">🟢 LINKED ACCOUNT: {st.session_state.current_user}</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div style="background:rgba(255,179,0,0.06); border-left:3px solid #ffb300; padding:8px 12px; border-radius:4px; font-size:11px; margin-bottom:12px; color:#ffb300;">⚠️ VISITOR MODE: Data cached locally. Register profile to cloud sync.</div>', unsafe_allow_html=True)

    cc1, cc2 = st.columns(2)
    with cc1:
        if st.button("▶ ACTIVATE EDGE NODE", disabled=st.session_state.sim_running):
            st.session_state.sim_running = True
            st.rerun()
    with cc2:
        if st.button("■ PAUSE COMPUTE NODE", disabled=not st.session_state.sim_running):
            st.session_state.sim_running = False
            st.rerun()

    # 绘制拓扑网格
    nodes = st.session_state.sim_nodes
    grid_html = '<div class="nx-card"><div class="nx-card-title"><span>▸</span> Live Decoupled Matrix (64 Simulated Devices)</div><div class="nx-node-grid">'
    for v in nodes:
        cls = {0: "", 1: " active", 2: " processing"}.get(v, "")
        grid_html += f'<div class="nx-node{cls}"></div>'
    grid_html += '</div></div>'
    st.markdown(grid_html, unsafe_allow_html=True)

    # 数据大盘
    s1, s2, s3 = st.columns(3)
    with s1: st.metric("Tasks Completed", st.session_state.sim_tasks)
    with s2: st.metric("Aggregated Yield", f"{st.session_state.app_earned:,.2f} NEXA")
    with s3: st.metric("Core Temp Status", "36.8 °C" if st.session_state.sim_running else "31.2 °C", "SAFE Barrier")

    # 实时的任务输出日志
    st.markdown('<div class="nx-card"><div class="nx-card-title"><span>▸</span> Cryptographic Task Pipeline Logs</div>', unsafe_allow_html=True)
    if st.session_state.sim_log:
        log_html = '<div class="nx-log">'
        for line, cls in st.session_state.sim_log[-6:]:
            log_html += f'<div class="log-{cls}">{line}</div>'
        log_html += '</div>'
        st.markdown(log_html, unsafe_allow_html=True)
    else:
        st.markdown('<div class="nx-log">// Toggle activation switch above to feed decentralized data stream.</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════
# TAB 3: MOAT & SYNERGY
# ══════════════════════════════════════
elif current_tab == "Moat & Synergy":
    st.markdown("""
    <div class="nx-card">
        <div class="nx-card-title"><span>▸</span> Solana Mobile System Synergy</div>
        <div style="font-size:12px; color:#bdc3c7; line-height:1.8;">
            NexaEdge acts as an un-evictable system background daemon tailored specifically for the <strong>Solana Seeker & Saga hardware series</strong>. 
            By natively tapping into the mobile system layer during overnight charging sequences, it creates a risk-adjusted asset yield flywheel, turning consumer electronics into direct economic production tools.
        </div>
    </div>
    """, unsafe_allow_html=True)

    m1, m2 = st.columns(2)
    with m1:
        st.markdown("""
        <div class="nx-feature">
            <div class="nx-feature-title">🧠 NPU-Native Framework</div>
            <div class="nx-feature-body">Optimized explicitly for Snapdragon & Apple A-series Neural Processing Units. Executes SLM parameter checking efficiently without battery degradation.</div>
        </div>
        """, unsafe_allow_html=True)
    with m2:
        st.markdown("""
        <div class="nx-feature">
            <div class="nx-feature-title">🔗 Lightweight BFT Tech</div>
            <div class="nx-feature-body">Proprietary Byzantine Fault Tolerant architecture. Implements 2:1 decentralized redundant validation arrays ensuring falsified calculations are discarded instantly.</div>
        </div>
        """, unsafe_allow_html=True)

# ══════════════════════════════════════
# TAB 4: ROADMAP & CLOUD AUTH
# ══════════════════════════════════════
elif current_tab == "Roadmap & Auth":
    # 投资人重点审查： Roadmap
    st.markdown("""
    <div class="nx-card">
        <div class="nx-card-title"><span>▸</span> STRATEGIC ROADMAP 2026</div>
        <div class="nx-roadmap-item current">
            <div class="nx-roadmap-phase">Q2 2026 · ACTIVE PIPELINE</div>
            <div class="nx-roadmap-title">Institutional Ecosystem Acceleration</div>
            <div class="nx-roadmap-body">Architecture blueprints locked. Comprehensive whitepaper finalized. Joint pipeline enrollment matching: <strong>Solana Grant</strong> (Ecosystem capital), <strong>Alliance DAO</strong> (Web3 scale accelerator), and <strong>Y Combinator</strong> (Deep core infrastructure validation).</div>
        </div>
        <div class="nx-roadmap-item">
            <div class="nx-roadmap-phase">Q3 2026</div>
            <div class="nx-roadmap-title">Lightweight WASM Sandbox Testbed</div>
            <div class="nx-roadmap-body">Deployment of native iOS/Android background runtime sandboxes. Proof-of-concept testing execution layer for distributed ML tokenization datasets.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 登录/注册模块组件
    st.markdown('<div class="nx-card"><div class="nx-card-title"><span>▸</span> Cloud Sync Account Hub</div>', unsafe_allow_html=True)
    if st.session_state.current_user:
        st.markdown(f"🔓 Identity confirmed: **{st.session_state.current_user}**")
        if st.button("LOGOUT ARCHIVE"):
            st.session_state.current_user = None
            st.rerun()
    else:
        auth_choice = st.radio("AuthMode", ["Login Terminal", "Register Node"], horizontal=True, label_visibility="collapsed")
        with st.form("auth_cloud_form"):
            in_email = st.text_input("Identity Email:")
            in_password = st.text_input("Secret Token / Password:", type="password")
            
            if auth_choice == "Register Node":
                if st.form_submit_button("CREATE UNIFIED PIPELINE ACCOUNT"):
                    if in_email and in_password:
                        global_server["user_db"][in_email] = {
                            "password_hash": hashlib.sha256(in_password.encode()).hexdigest(),
                            "score": st.session_state.app_earned,
                            "reg_time": time.strftime("%Y-%m-%d %H:%M:%S")
                        }
                        st.session_state.current_user = in_email
                        st.success("Registration success! Cloud profile mounted.")
                        st.rerun()
            else:
                if st.form_submit_button("AUTHENTICATE & LOAD CLOUD ASSETS"):
                    h_pass = hashlib.sha256(in_password.encode()).hexdigest()
                    if in_email in global_server["user_db"] and global_server["user_db"][in_email]["password_hash"] == h_pass:
                        st.session_state.current_user = in_email
                        st.session_state.app_earned = global_server["user_db"][in_email]["score"]
                        st.success("Assets synchronized successfully.")
                        st.rerun()
                    else:
                        st.error("Invalid cloud credential identity matching failure.")
    st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════
# OPTIONAL: ADMIN INTERNAL AUDIT PANEL
# ══════════════════════════════════════
if lang == "Admin Portal 🔒":
    st.markdown("---")
    st.markdown('<h3 style="color:#f43f5e; font-size:14px;">🔒 INTERNAL SECURITY AUDIT TELEMETRY</h3>', unsafe_allow_html=True)
    backdoor_pass = st.text_input("Enter Root Master Authentication Key:", type="password")
    
    if backdoor_pass == "NexaAdmin2026":
        st.toast("Internal accounting logs completely decrypted.", icon="🔓")
        
        ad1, ad2 = st.columns(2)
        ad1.metric("Registered Accounts", len(global_server["user_db"]))
        ad2.metric("Total Whitelist Claims", len(global_server["whitelist_records"]))
        
        st.markdown("**User Database Registry:**")
        st.json(global_server["user_db"])
        
        st.markdown("**Genesis Whitelist Submissions:**")
        st.write(global_server["whitelist_records"])
    elif backdoor_pass != "":
        st.error("Access Denied: Malicious tampering vector blocked.")

# ── Footer ──
st.markdown(f"""
<div style="display:flex; gap:10px; margin-top:20px;">
    <div style="flex:1; background:#0e1419; border:1px dashed #a2ff00; border-radius:8px; padding:10px; text-align:center;">
        <div style="font-family:'Space Mono'; font-size:9px; color:#556070;">LIVE AUDIENCE VIEWERS</div>
        <div style="font-family:'Space Mono'; font-size:14px; font-weight:bold; color:#a2ff00;">{global_server["total_online_viewers"]} Online</div>
    </div>
    <div style="flex:1; background:#0e1419; border:1px dashed #00e5ff; border-radius:8px; padding:10px; text-align:center;">
        <div style="font-family:'Space Mono'; font-size:9px; color:#556070;">GLOBAL NETWORK BASE</div>
        <div style="font-family:'Space Mono'; font-size:14px; font-weight:bold; color:#00e5ff;">{len(global_server["active_device_set"])} ACTIVE</div>
    </div>
</div>
<div class="nx-footer" style="text-align:center; font-family:'Space Mono'; font-size:9px; color:#2a3540; margin-top:30px; border-top:1px solid #1a2530; padding-top:15px;">
    NexaEdge Terminal Framework · Project Pitch Mock Environment · © 2026 NexaEdge.
</div>
""", unsafe_allow_html=True)
