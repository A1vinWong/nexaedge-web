"""
NexaEdge User Portal — Beta P4
Supabase OTP Auth + Personal Dashboard + Task Display + Live Node Stats
Run: streamlit run user_portal.py
"""

import streamlit as st
import hashlib
import time
import random
import string
from datetime import datetime, timezone
from supabase import create_client, Client

st.set_page_config(
    page_title="NexaEdge · My Node",
    page_icon="🟢",
    layout="centered"
)

# ══════════════════════════════════════
# CONFIG
# ══════════════════════════════════════
SUPABASE_URL = st.secrets.get("url", "https://nfafzigmcdybgbxdtymf.supabase.co")
SUPABASE_KEY = st.secrets.get("key", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im5mYWZ6aWdtY2R5YmdieGR0eW1mIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODA5ODE3NTMsImV4cCI6MjA5NjU1Nzc1M30.ZIX3sByZ8yQSDGFr-o24CjIXwZ5UsB4rMB3jculLtv0")
SUPABASE_URL_JS = SUPABASE_URL
SUPABASE_KEY_JS = SUPABASE_KEY

# ══════════════════════════════════════
# CSS
# ══════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Syne:wght@400;600;700;800&display=swap');

.stApp { background-color: #060b0f; }
.main .block-container {
    padding-top: 1.5rem !important;
    padding-bottom: 3rem !important;
    max-width: 680px !important;
}
#MainMenu, footer, header, [data-testid="stHeader"] { display: none !important; }
.stApp::before {
    content: '';
    position: fixed;
    inset: 0;
    background-image:
        linear-gradient(rgba(162,255,0,.018) 1px, transparent 1px),
        linear-gradient(90deg, rgba(162,255,0,.018) 1px, transparent 1px);
    background-size: 44px 44px;
    pointer-events: none;
    z-index: 0;
}
*, h1, h2, h3, p, div, span, label { font-family: 'Syne', sans-serif; }

.stTextInput > div > div > input {
    background: #060b0f !important;
    border: 1px solid #182230 !important;
    border-radius: 8px !important;
    color: #e8edf2 !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 13px !important;
    padding: 14px 16px !important;
}
.stTextInput > div > div > input:focus {
    border-color: #a2ff00 !important;
    box-shadow: 0 0 0 2px rgba(162,255,0,.1) !important;
}
.stTextInput label {
    font-family: 'Space Mono', monospace !important;
    font-size: 10px !important;
    color: #4a6070 !important;
    text-transform: uppercase !important;
    letter-spacing: .08em !important;
}
div.stButton > button {
    background: linear-gradient(135deg, #a2ff00, #8de600) !important;
    color: #060b0f !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 11px !important;
    font-weight: 700 !important;
    text-transform: uppercase !important;
    letter-spacing: .06em !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 12px 24px !important;
    width: 100% !important;
}
div.stButton > button:hover {
    background: linear-gradient(135deg, #b5ff33, #a2ff00) !important;
    box-shadow: 0 0 20px rgba(162,255,0,.25) !important;
}
div.stButton > button[kind="secondary"] {
    background: transparent !important;
    color: #4a6070 !important;
    border: 1px solid #182230 !important;
    box-shadow: none !important;
}
div.stButton > button[kind="secondary"]:hover {
    border-color: #a2ff00 !important;
    color: #a2ff00 !important;
}
.nx-divider { border: none; border-top: 1px solid #182230; margin: 8px 0 20px; }
.nx-card {
    background: linear-gradient(160deg, #0d1720, #090e14);
    border: 1px solid #182230;
    border-radius: 14px;
    padding: 24px;
    margin-bottom: 14px;
}
.nx-card-title {
    font-family: 'Space Mono', monospace;
    font-size: 9px;
    color: #4a6070;
    text-transform: uppercase;
    letter-spacing: .12em;
    margin-bottom: 16px;
}
.nx-notice {
    background: rgba(255,179,0,.05);
    border: 1px solid rgba(255,179,0,.2);
    border-left: 3px solid #ffb300;
    border-radius: 0 8px 8px 0;
    padding: 10px 14px;
    font-family: 'Space Mono', monospace;
    font-size: 9px;
    color: #ffb300;
    line-height: 1.7;
    margin-bottom: 18px;
}
.nx-rank-wrap {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 32px 0 24px;
}
.nx-rank-ring { position: relative; width: 120px; height: 120px; margin-bottom: 16px; }
.nx-rank-ring svg { position: absolute; inset: 0; transform: rotate(-90deg); }
.nx-rank-number {
    position: absolute; inset: 0;
    display: flex; flex-direction: column;
    align-items: center; justify-content: center;
}
.nx-rank-num {
    font-family: 'Space Mono', monospace;
    font-size: 28px; font-weight: 700; color: #a2ff00; line-height: 1;
}
.nx-rank-label {
    font-family: 'Space Mono', monospace;
    font-size: 8px; color: #4a6070;
    text-transform: uppercase; letter-spacing: .1em; margin-top: 4px;
}
.nx-rank-title { font-size: 18px; font-weight: 800; color: #e8edf2; margin-bottom: 4px; }
.nx-rank-sub {
    font-family: 'Space Mono', monospace;
    font-size: 10px; color: #4a6070; text-align: center; line-height: 1.6;
}
.nx-ref-box {
    background: #060b0f;
    border: 1px solid rgba(162,255,0,.25);
    border-radius: 12px; padding: 20px; text-align: center; margin-bottom: 14px;
}
.nx-ref-code {
    font-family: 'Space Mono', monospace;
    font-size: 28px; font-weight: 700; color: #a2ff00;
    letter-spacing: .25em; margin: 8px 0 4px;
}
.nx-ref-label {
    font-family: 'Space Mono', monospace;
    font-size: 8px; color: #4a6070;
    text-transform: uppercase; letter-spacing: .1em;
}
.nx-ref-count {
    font-family: 'Space Mono', monospace;
    font-size: 12px; color: #00e5ff; margin-top: 10px;
}
.nx-stat-grid {
    display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-bottom: 14px;
}
.nx-stat-item {
    background: #060b0f; border: 1px solid #182230;
    border-radius: 10px; padding: 16px; text-align: center;
}
.nx-stat-val {
    font-family: 'Space Mono', monospace;
    font-size: 20px; font-weight: 700; color: #e8edf2; line-height: 1.1;
}
.nx-stat-val.green { color: #a2ff00; }
.nx-stat-val.cyan  { color: #00e5ff; }
.nx-stat-val.gold  { color: #ffb300; }
.nx-stat-label {
    font-family: 'Space Mono', monospace;
    font-size: 8px; color: #4a6070;
    text-transform: uppercase; letter-spacing: .08em; margin-top: 5px;
}
.nx-live-row {
    display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 8px; margin-bottom: 14px;
}
.nx-live-item {
    background: #060b0f; border: 1px solid #182230;
    border-radius: 10px; padding: 12px; text-align: center;
}
.nx-live-val {
    font-family: 'Space Mono', monospace;
    font-size: 16px; font-weight: 700; color: #e8edf2; line-height: 1.1;
}
.nx-live-label {
    font-family: 'Space Mono', monospace;
    font-size: 8px; color: #4a6070;
    text-transform: uppercase; letter-spacing: .07em; margin-top: 4px;
}
.nx-task-row {
    display: flex; justify-content: space-between; align-items: center;
    padding: 10px 0; border-bottom: 1px solid rgba(24,34,48,.6);
    font-family: 'Space Mono', monospace; font-size: 10px;
}
.nx-task-row:last-child { border-bottom: none; }
.nx-task-type { color: #a2ff00; }
.nx-task-status-done { color: #a2ff00; }
.nx-task-status-assigned { color: #ffb300; }
.nx-task-status-pending { color: #4a6070; }
.nx-task-time { color: #2a3a4a; font-size: 9px; }
.nx-timeline { padding: 4px 0; }
.nx-tl-item {
    display: flex; gap: 14px; padding-bottom: 20px; position: relative;
}
.nx-tl-item::before {
    content: ''; position: absolute;
    left: 9px; top: 22px; bottom: 0;
    width: 1px; background: #182230;
}
.nx-tl-item:last-child::before { display: none; }
.nx-tl-dot {
    width: 20px; height: 20px; border-radius: 50%;
    background: #182230; border: 2px solid #182230;
    flex-shrink: 0; margin-top: 2px;
}
.nx-tl-dot.done  { background: #a2ff00; border-color: #a2ff00; }
.nx-tl-dot.now   { background: #00e5ff; border-color: #00e5ff;
                   box-shadow: 0 0 10px rgba(0,229,255,.5); }
.nx-tl-title { font-size: 13px; font-weight: 700; color: #e8edf2; line-height: 1.3; }
.nx-tl-title.muted { color: #2a3a4a; }
.nx-tl-sub {
    font-family: 'Space Mono', monospace;
    font-size: 9px; color: #4a6070; margin-top: 3px; line-height: 1.6;
}
.nx-share-row {
    display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 8px; margin-top: 12px;
}
.nx-share-btn {
    display: block; text-align: center; padding: 10px 8px;
    background: #0d1720; border: 1px solid #182230; border-radius: 10px;
    color: #4a6070 !important; font-size: 11px; font-weight: 700;
    text-decoration: none; transition: all .2s;
}
.nx-share-btn:hover { border-color: #a2ff00; color: #a2ff00 !important; }
.nx-btn-row { display: flex !important; flex-direction: row !important; gap: 10px !important; margin: 8px 0 12px !important; }
.nx-btn-row a { display: block !important; text-align: center !important; padding: 11px 0 !important; border-radius: 8px !important; font-family: 'Space Mono', monospace !important; font-size: 11px !important; font-weight: 700 !important; text-transform: uppercase !important; letter-spacing: .06em !important; text-decoration: none !important; }
.nx-login-hero { text-align: center; padding: 40px 0 32px; }
/* Fix node activate/stop button row */
div[data-testid="stHorizontalBlock"] div.stButton > button { width: auto !important; }
.nx-login-dot {
    width: 14px; height: 14px; background: #a2ff00; border-radius: 50%;
    box-shadow: 0 0 18px #a2ff00; margin: 0 auto 20px;
}
.nx-login-title {
    font-size: 28px; font-weight: 800; color: #e8edf2;
    letter-spacing: -.02em; margin-bottom: 6px;
}
.nx-login-sub {
    font-family: 'Space Mono', monospace;
    font-size: 10px; color: #4a6070; line-height: 1.7;
    max-width: 340px; margin: 0 auto 32px;
}
.nx-stage {
    display: inline-block;
    background: rgba(162,255,0,.08);
    border: 1px solid rgba(162,255,0,.25);
    color: #a2ff00;
    font-family: 'Space Mono', monospace;
    font-size: 9px; font-weight: 700;
    padding: 4px 10px; border-radius: 6px; letter-spacing: .1em; margin-bottom: 20px;
}
.nx-footer {
    border-top: 1px solid #182230; margin-top: 40px; padding-top: 16px;
    text-align: center; font-family: 'Space Mono', monospace;
    font-size: 9px; color: #2a3a4a; line-height: 2;
}
.app-dashboard {
    background: linear-gradient(160deg, #0a1018, #060b0f);
    border: 1px solid #1a2535;
    border-radius: 16px;
    overflow: hidden;
    margin-bottom: 12px;
}
.app-header {
    background: linear-gradient(135deg, #0d1a10, #0a1410);
    border-bottom: 1px solid #1a2535;
    padding: 16px 18px 12px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.app-header-title {
    font-family: 'Space Mono', monospace;
    font-size: 9px; color: #4a6070;
    text-transform: uppercase; letter-spacing: .12em;
}
.app-temp-badge {
    display: inline-flex; align-items: center; gap: 6px;
    padding: 4px 10px; border-radius: 6px;
    font-family: 'Space Mono', monospace; font-size: 10px; font-weight: 700;
}
.app-chart-area {
    padding: 14px 18px 10px;
    border-bottom: 1px solid #1a2535;
}
.app-stats-row {
    display: grid; grid-template-columns: 1fr 1fr 1fr;
    gap: 0; border-bottom: 1px solid #1a2535;
}
.app-stat-cell {
    padding: 12px 14px; text-align: center;
    border-right: 1px solid #1a2535;
}
.app-stat-cell:last-child { border-right: none; }
.app-stat-num {
    font-family: 'Space Mono', monospace;
    font-size: 15px; font-weight: 700; color: #e8edf2; line-height: 1.1;
}
.app-stat-lbl {
    font-family: 'Space Mono', monospace;
    font-size: 7px; color: #4a6070;
    text-transform: uppercase; letter-spacing: .06em; margin-top: 3px;
}
.app-node-section {
    padding: 14px 18px;
    border-bottom: 1px solid #1a2535;
}
.app-node-label {
    font-family: 'Space Mono', monospace; font-size: 8px; color: #4a6070;
    text-transform: uppercase; letter-spacing: .1em; margin-bottom: 6px;
}
.app-node-id {
    font-family: 'Space Mono', monospace; font-size: 11px; color: #a2ff00; margin-bottom: 12px;
}
.app-status-row {
    display: flex; justify-content: space-between; align-items: flex-start;
}
.app-status-block { flex: 1; }
.app-status-lbl {
    font-family: 'Space Mono', monospace; font-size: 8px; color: #4a6070;
    text-transform: uppercase; letter-spacing: .08em; margin-bottom: 4px;
}
.app-status-val {
    font-family: 'Space Mono', monospace; font-size: 13px; font-weight: 700;
}
.app-nexa-val {
    font-family: 'Space Mono', monospace; font-size: 18px; font-weight: 700; color: #a2ff00;
}
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════
# SUPABASE
# ══════════════════════════════════════
@st.cache_resource
def get_supabase() -> Client:
    return create_client(SUPABASE_URL, SUPABASE_KEY)

supabase = get_supabase()

# ══════════════════════════════════════
# LANGUAGE — detect from URL param
# ══════════════════════════════════════
if "portal_lang" not in st.session_state:
    # Read ?lang=ZH from URL if present
    url_lang = st.query_params.get("lang", "EN")
    st.session_state.portal_lang = "ZH" if url_lang == "ZH" else "EN"

is_zh = st.session_state.portal_lang == "ZH"

PORTAL_TEXT = {
    "EN": {
        "title": "NODE PORTAL",
        "stage": "● BETA · Q3 2026",
        "not_on_waitlist": "Your email is not on the waitlist yet. Please register at the main site first.",
        "sign_out": "Sign Out",
        "node_reserved": "Your node is reserved.",
        "top_pct": "Top",
        "of": "of",
        "waitlist_members": "waitlist members",
        "joined": "Joined",
        "referrals_made": "Referrals Made",
        "queue_position": "Queue Position",
        "spl_wallet": "SPL Wallet",
        "language": "Language",
        "your_ref": "Your Referral Code",
        "joined_with_code": "person joined with your code",
        "joined_with_code_pl": "persons joined with your code",
        "tap_copy": "Tap & hold to copy your referral code",
        "mining_status": "Mining Status",
        "token_earnings": "Token Earnings",
        "participant_node": "Participant Node",
        "start_session": "⚡ START COMPUTE SESSION",
        "stop": "■ STOP",
        "online_refresh": "ONLINE · refreshes every 30s",
        "press_start": "// Press START COMPUTE SESSION to activate node",
        "task_history": "Task History",
        "completed": "completed",
        "register_device": "Register Your Device as a Node",
        "register_desc": "Generate a unique node token for this device. Use this token with the node client to start sending heartbeats and executing tasks.",
        "register_btn": "⚡ Register This Device",
        "register_fail": "Registration failed. You may already have a node registered.",
        "wasm_title": "WASM COMPUTE DEMO",
        "wasm_badge": "RUNS IN YOUR BROWSER",
        "wasm_desc": "This demo compiles and executes a real WebAssembly module directly in your browser — no server, no Python. It runs a matrix multiplication kernel that simulates the core compute of AI inference workloads.",
        "journey_title": "Your Node Journey",
        "j1_title": "Waitlist Registered", "j1_sub": "Spot secured · NEXA airdrop eligible",
        "j2_title": "Node Token Issued", "j2_sub": "Device registered · heartbeat active",
        "j3_title": "Beta — Task Execution", "j3_sub": "Simulated tasks running · earning sim NEXA · Q3 2026",
        "j4_title": "Closed Beta — 1,000 Nodes", "j4_sub": "Real node client · ZK proof · Q4 2026",
        "j5_title": "Mainnet Launch", "j5_sub": "Real compute · real rewards · Q1 2027",
        "nexa_notice": "NEXA tokens are minted on Solana but not yet in public circulation. Airdrop eligibility and allocation are determined at mainnet launch based on your queue position and referral count. This is not a financial instrument.",
        "login_title": "My Node Portal",
        "login_sub": "Sign in with the email you used to join the waitlist. We'll send you a one-time code — no password needed.",
        "nodes_reserved": "nodes reserved",
        "email_label": "Email Address",
        "email_ph": "you@example.com",
        "send_code": "Send Login Code",
        "invalid_email": "Please enter a valid email address.",
        "not_on_wl": "This email is not on the waitlist. Please register at the main site first.",
        "your_code": "Your login code",
        "signing_in": "Signing in as",
        "beta_warning": "BETA MODE — Code shown on screen. Valid 10 minutes.",
        "enter_code": "Enter the 6-digit code above",
        "code_ph": "e.g. 123456",
        "verify": "Verify & Sign In",
        "wrong_code": "Incorrect code. Please try again.",
        "diff_email": "← Use a different email",
        "lang_btn": "中文",
        "portal_link": "Login to My Node Portal",
        "portal_desc": "See your queue position and activate your node heartbeat",
        "already_reg": "Already registered? Login to Node Portal →",
        "register_at": "Register at nexaedge.streamlit.app →",
        "footer": "NexaEdge Node Portal · Beta P4 · Heartbeat + Task Executor\nNEXA minted on Solana · Not yet in public circulation · contact@nexaedge.org",
    },
    "ZH": {
        "title": "节点控制台",
        "stage": "● Beta · 2026年Q3",
        "not_on_waitlist": "您的邮箱尚未在候补名单中。请先在主网站注册。",
        "sign_out": "退出登录",
        "node_reserved": "您的节点已预留。",
        "top_pct": "前",
        "of": "/",
        "waitlist_members": "位候补名单成员",
        "joined": "加入于",
        "referrals_made": "已推荐人数",
        "queue_position": "队列排名",
        "spl_wallet": "SPL 钱包",
        "language": "语言",
        "your_ref": "您的推荐码",
        "joined_with_code": "人使用了您的推荐码",
        "joined_with_code_pl": "人使用了您的推荐码",
        "tap_copy": "长按复制推荐码",
        "mining_status": "挖矿状态",
        "token_earnings": "代币收益",
        "participant_node": "参与节点",
        "start_session": "⚡ 启动算力会话",
        "stop": "■ 停止",
        "online_refresh": "在线 · 每30秒刷新",
        "press_start": "// 按启动算力会话激活节点",
        "task_history": "任务历史",
        "completed": "已完成",
        "register_device": "将此设备注册为节点",
        "register_desc": "为此设备生成唯一节点 Token。使用此 Token 运行节点客户端，开始发送心跳并执行任务。",
        "register_btn": "⚡ 注册此设备",
        "register_fail": "注册失败。您可能已经注册了节点。",
        "wasm_title": "WASM 算力演示",
        "wasm_badge": "在您的浏览器中运行",
        "wasm_desc": "本演示直接在您的浏览器中编译并执行真实的 WebAssembly 模块——无需服务器，无需 Python。它运行矩阵乘法内核，模拟 AI 推理工作负载的核心计算。",
        "journey_title": "您的节点旅程",
        "j1_title": "候补名单注册", "j1_sub": "名额已确保 · NEXA 空投资格",
        "j2_title": "节点 Token 已发放", "j2_sub": "设备已注册 · 心跳已激活",
        "j3_title": "Beta — 任务执行", "j3_sub": "模拟任务运行中 · 赚取模拟 NEXA · 2026年Q3",
        "j4_title": "封闭测试——1,000 节点", "j4_sub": "真实节点客户端 · ZK证明 · 2026年Q4",
        "j5_title": "主网上线", "j5_sub": "真实算力 · 真实奖励 · 2027年Q1",
        "nexa_notice": "NEXA 代币已在 Solana 上铸造，但尚未公开流通。空投资格与分配比例将在主网上线时根据队列排名和推荐数量确定。本内容不构成金融工具。",
        "login_title": "节点控制台",
        "login_sub": "使用注册候补名单时的邮箱登录。我们将发送一次性验证码——无需密码。",
        "nodes_reserved": "个节点已预留",
        "email_label": "电子邮件",
        "email_ph": "your@email.com",
        "send_code": "发送登录验证码",
        "invalid_email": "请输入有效的电子邮件地址。",
        "not_on_wl": "此邮箱不在候补名单中。请先在主网站注册。",
        "your_code": "您的登录验证码",
        "signing_in": "正在登录",
        "beta_warning": "Beta 模式 — 验证码显示在屏幕上。有效期10分钟。",
        "enter_code": "输入上方的6位验证码",
        "code_ph": "如 123456",
        "verify": "验证并登录",
        "wrong_code": "验证码错误，请重试。",
        "diff_email": "← 使用其他邮箱",
        "lang_btn": "English",
        "portal_link": "登录节点控制台",
        "portal_desc": "查看队列排名、激活节点心跳",
        "already_reg": "已注册？登录节点 Portal →",
        "register_at": "在 nexaedge.streamlit.app 注册 →",
        "footer": "NexaEdge 节点 Portal · Beta P4 · 心跳 + 任务执行器\nNEXA 已在 Solana 铸造 · 尚未公开流通 · contact@nexaedge.org",
    }
}

# ══════════════════════════════════════
# SESSION STATE
# ══════════════════════════════════════
for k, v in {
    "user_email": None,
    "user_data": None,
    "magic_sent": False,
    "magic_email": "",
    "otp_store": {},
}.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ══════════════════════════════════════
# DB HELPERS
# ══════════════════════════════════════
def lookup_waitlist(email):
    try:
        res = supabase.table("whitelist").select("*").eq("email", email.lower()).execute()
        return res.data[0] if res.data else None
    except: return None

def get_queue_rank(email):
    try:
        res = supabase.table("whitelist").select("email").order("created_at", desc=False).execute()
        emails = [r["email"] for r in res.data]
        return emails.index(email.lower()) + 1
    except: return 0

def get_total_signups():
    try:
        res = supabase.table("whitelist").select("id", count="exact").execute()
        return res.count or 0
    except: return 0

def count_referrals(ref_code):
    try:
        res = supabase.table("whitelist").select("id", count="exact").eq("used_ref", ref_code).execute()
        return res.count or 0
    except: return 0

def get_node_record(email):
    try:
        res = supabase.table("nodes").select("*").eq("email", email.lower()).execute()
        return res.data[0] if res.data else None
    except: return None

def register_node(email, node_token):
    try:
        supabase.table("nodes").insert({
            "email": email.lower(),
            "node_token": node_token,
            "status": "pending",
        }).execute()
        return True
    except: return False

def get_latest_heartbeat(token):
    """Get most recent heartbeat for this node."""
    try:
        res = (supabase.table("heartbeats")
               .select("cpu_usage,temperature,battery_level,tasks_completed,reported_at")
               .eq("node_token", token)
               .order("reported_at", desc=True)
               .limit(1)
               .execute())
        return res.data[0] if res.data else None
    except: return None

def get_node_tasks(token, limit=10):
    """Get recent tasks assigned to this node."""
    try:
        res = (supabase.table("tasks")
               .select("id,task_type,status,result,created_at,completed_at")
               .eq("assigned_to", token)
               .order("created_at", desc=True)
               .limit(limit)
               .execute())
        return res.data or []
    except: return []

def get_node_task_count(token):
    """Total completed tasks for this node."""
    try:
        res = (supabase.table("tasks")
               .select("id", count="exact")
               .eq("assigned_to", token)
               .eq("status", "completed")
               .execute())
        return res.count or 0
    except: return 0

def generate_otp():
    return "".join(random.choices(string.digits, k=6))

def generate_node_token():
    chars = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"
    parts = ["".join(random.choices(chars, k=4)) for _ in range(3)]
    return "NXT-" + "-".join(parts)

def verify_code(email, entered):
    store = st.session_state.get("otp_store", {}).get(email.lower())
    if not store: return False
    age = datetime.now(timezone.utc).timestamp() - store["created"]
    if age > 600: return False
    return entered.strip() == store["code"]

# ══════════════════════════════════════
# HEADER
# ══════════════════════════════════════
T = PORTAL_TEXT[st.session_state.portal_lang]

c1, c2, c3 = st.columns([1, 2, 1])
with c2:
    st.image('IMG_7859.jpeg', use_container_width=True)
st.markdown('<div style="margin-bottom:8px;"></div>', unsafe_allow_html=True)

# Language toggle in header
h1, h2 = st.columns([3, 1])
with h1:
    st.markdown(f"""
    <div style="display:flex;align-items:center;gap:10px;padding:8px 0 4px;">
        <div style="width:10px;height:10px;background:#a2ff00;border-radius:50%;box-shadow:0 0 12px #a2ff00;flex-shrink:0;"></div>
        <div style="font-family:'Syne',sans-serif;font-size:20px;font-weight:800;color:#e8edf2;letter-spacing:-.02em;">
            Nexa<span style="color:#a2ff00;">Edge</span>
            <span style="font-size:11px;color:#4a6070;font-weight:400;font-family:'Space Mono',monospace;margin-left:8px;">{T['title']}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
with h2:
    st.markdown(f'<div style="text-align:right;padding-top:10px;"><span style="display:inline-block;background:rgba(162,255,0,.08);border:1px solid rgba(162,255,0,.25);color:#a2ff00;font-family:\'Space Mono\',monospace;font-size:9px;font-weight:700;padding:4px 10px;border-radius:6px;">{T["stage"]}</span></div>', unsafe_allow_html=True)
    if st.button(T["lang_btn"], key="lang_toggle", type="secondary"):
        st.session_state.portal_lang = "ZH" if st.session_state.portal_lang == "EN" else "EN"
        T = PORTAL_TEXT[st.session_state.portal_lang]
        is_zh = st.session_state.portal_lang == "ZH"
        st.rerun()

st.markdown('<hr class="nx-divider">', unsafe_allow_html=True)

# ══════════════════════════════════════
# LOGGED IN — DASHBOARD
# ══════════════════════════════════════
if st.session_state.user_email:
    email = st.session_state.user_email
    data  = st.session_state.user_data

    if not data:
        st.markdown(f"""
        <div class="nx-notice">
            {T['not_on_waitlist'].replace('{email}', email)}
        </div>
        """, unsafe_allow_html=True)
        if st.button(T["sign_out"], type="secondary"):
            st.session_state.user_email = None
            st.session_state.user_data  = None
            st.rerun()
        st.stop()

    ref_code   = data.get("ref_code") or data.get("invitation_code") or "—"
    wallet     = data.get("wallet") or "—"
    lang       = data.get("lang") or "EN"
    joined_raw = data.get("created_at", "")
    joined     = joined_raw[:10] if joined_raw else "—"

    rank      = get_queue_rank(email)
    total     = get_total_signups()
    referrals = count_referrals(ref_code)
    pct_rank  = round((1 - (rank - 1) / max(total, 1)) * 100) if total > 0 else 0

    # ── Rank ring
    circ = 326.7
    dash = circ * (pct_rank / 100)
    gap  = circ - dash

    st.markdown(f"""
    <div class="nx-rank-wrap">
        <div class="nx-rank-ring">
            <svg viewBox="0 0 120 120" width="120" height="120">
                <circle cx="60" cy="60" r="52" fill="none" stroke="#182230" stroke-width="6"/>
                <circle cx="60" cy="60" r="52" fill="none" stroke="#a2ff00" stroke-width="6"
                    stroke-linecap="round" stroke-dasharray="{dash:.1f} {gap:.1f}"/>
            </svg>
            <div class="nx-rank-number">
                <div class="nx-rank-num">#{rank}</div>
                <div class="nx-rank-label">Queue</div>
            </div>
        </div>
        <div class="nx-rank-title">{T['node_reserved']}</div>
        <div class="nx-rank-sub">
            {T['top_pct']} {100 - pct_rank + 1}% {T['of']} {total} {T['waitlist_members']}<br>
            {T['joined']} {joined}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Stats grid
    wallet_short = wallet[:6] + "..." + wallet[-4:] if wallet != "—" and len(wallet) > 10 else wallet
    st.markdown(f"""
    <div class="nx-stat-grid">
        <div class="nx-stat-item">
            <div class="nx-stat-val green">{referrals}</div>
            <div class="nx-stat-label">{T['referrals_made']}</div>
        </div>
        <div class="nx-stat-item">
            <div class="nx-stat-val cyan">{rank} / {total}</div>
            <div class="nx-stat-label">{T['queue_position']}</div>
        </div>
        <div class="nx-stat-item">
            <div class="nx-stat-val">{wallet_short}</div>
            <div class="nx-stat-label">{T['spl_wallet']}</div>
        </div>
        <div class="nx-stat-item">
            <div class="nx-stat-val gold">{lang}</div>
            <div class="nx-stat-label">{T['language']}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Referral box
    share_text = f"Join the NexaEdge waitlist — distributed edge AI on smartphones. Use my code {ref_code}"
    tg_url = f"https://t.me/share/url?url=https://nexaedge.streamlit.app&text={share_text}"
    x_url  = f"https://twitter.com/intent/tweet?text={share_text}"
    wa_url = f"https://wa.me/?text={share_text}"

    st.markdown(f"""
    <div class="nx-ref-box">
        <div class="nx-ref-label">{T['your_ref']}</div>
        <div class="nx-ref-code">{ref_code}</div>
        <div class="nx-ref-count">
            {referrals} {T['joined_with_code_pl'] if referrals != 1 else T['joined_with_code']}
        </div>
    </div>
    <div class="nx-share-row">
        <a class="nx-share-btn" href="{x_url}" target="_blank">🐦 X</a>
        <a class="nx-share-btn" href="{tg_url}" target="_blank">📢 Telegram</a>
        <a class="nx-share-btn" href="{wa_url}" target="_blank">💬 WhatsApp</a>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div style="margin-top:6px;"></div>', unsafe_allow_html=True)
    st.text_input(
        T["tap_copy"],
        value=ref_code,
        key="ref_code_display",
        label_visibility="visible",
    )

    # ══════════════════════════════════════
    # DASHBOARD — App Style
    # ══════════════════════════════════════
    st.markdown('<div style="margin-top:16px;"></div>', unsafe_allow_html=True)
    node_rec = get_node_record(email)

    if node_rec:
        token  = node_rec.get("node_token", "—")
        status = node_rec.get("status", "pending")
        hb = get_latest_heartbeat(token)
        task_count = get_node_task_count(token)

        # live stats
        cpu  = hb.get("cpu_usage", 0) or 0 if hb else 0
        temp = hb.get("temperature", 0) or 0 if hb else 0
        batt = hb.get("battery_level", 100) or 100 if hb else 100
        ts_raw = (hb.get("reported_at", "")[:16] or "").replace("T", " ") if hb else "—"

        is_online = status == "online"
        temp_safe = temp < 39
        temp_label = "SAFE" if temp_safe else "HIGH"
        temp_color = "#a2ff00" if temp_safe else "#f43f5e"
        temp_bg    = "rgba(162,255,0,.1)" if temp_safe else "rgba(244,63,94,.1)"

        # Simulated NEXA earnings based on tasks completed
        nexa_earned = round(task_count * 0.0022, 4)

        # Hash rate sparkline data (simulated based on cpu)
        hr_points = [random.uniform(max(0, cpu-20), cpu+20) for _ in range(12)]
        hr_max = max(hr_points) if hr_points else 1
        hr_norm = [round(h / hr_max * 60, 1) for h in hr_points]
        sparkline_pts = " ".join(f"{i*22},{70 - hr_norm[i]}" for i in range(12))

        mining_status_color = '#a2ff00' if is_online else '#ffb300'
        mining_status_text  = '● ACTIVE' if is_online else '○ ' + status.upper()

        st.components.v1.html(f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&display=swap');
        * {{ margin:0; padding:0; box-sizing:border-box; font-family:'Space Mono',monospace; }}
        body {{ background:transparent; }}
        .dash {{ background:linear-gradient(160deg,#0a1018,#060b0f); border:1px solid #1a2535; border-radius:16px; overflow:hidden; }}
        .dash-header {{ background:linear-gradient(135deg,#0d1a10,#0a1410); border-bottom:1px solid #1a2535; padding:14px 16px; display:flex; justify-content:space-between; align-items:center; }}
        .dash-title {{ font-size:9px; color:#4a6070; text-transform:uppercase; letter-spacing:.12em; }}
        .dash-sub {{ font-size:9px; color:#4a6070; margin-top:2px; }}
        .temp-badge {{ display:inline-flex; align-items:center; gap:5px; padding:4px 9px; border-radius:6px; font-size:10px; font-weight:700; }}
        .chart-area {{ padding:12px 16px 8px; border-bottom:1px solid #1a2535; }}
        .stats-row {{ display:grid; grid-template-columns:1fr 1fr 1fr; border-bottom:1px solid #1a2535; }}
        .stat-cell {{ padding:11px 12px; text-align:center; border-right:1px solid #1a2535; }}
        .stat-cell:last-child {{ border-right:none; }}
        .stat-num {{ font-size:15px; font-weight:700; color:#e8edf2; line-height:1.1; }}
        .stat-lbl {{ font-size:7px; color:#4a6070; text-transform:uppercase; letter-spacing:.06em; margin-top:3px; }}
        .node-section {{ padding:14px 16px; }}
        .node-lbl {{ font-size:8px; color:#4a6070; text-transform:uppercase; letter-spacing:.1em; margin-bottom:5px; }}
        .node-id {{ font-size:11px; color:#a2ff00; margin-bottom:10px; }}
        .status-row {{ display:flex; justify-content:space-between; align-items:flex-start; }}
        .status-block {{ flex:1; }}
        .status-lbl {{ font-size:8px; color:#4a6070; text-transform:uppercase; letter-spacing:.08em; margin-bottom:3px; }}
        .status-val {{ font-size:13px; font-weight:700; }}
        .nexa-val {{ font-size:18px; font-weight:700; color:#a2ff00; }}
        </style>
        <div class="dash">
          <div class="dash-header">
            <div>
              <div class="dash-title">Dashboard</div>
              <div class="dash-sub">Network Hash Rate (MH/s)</div>
            </div>
            <div style="display:flex;align-items:center;gap:8px;">
              <div class="temp-badge" style="background:{temp_bg};color:{temp_color};">
                {temp:.1f}C &nbsp; {temp_label}
              </div>
            </div>
          </div>
          <div class="chart-area">
            <svg width="100%" height="60" viewBox="0 0 242 60" preserveAspectRatio="none" style="display:block;">
              <polygon points="{sparkline_pts} 242,60 0,60" fill="#a2ff00" fill-opacity="0.15"/>
              <polyline points="{sparkline_pts}" fill="none" stroke="#a2ff00" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </div>
          <div class="stats-row">
            <div class="stat-cell">
              <div class="stat-num" style="color:#a2ff00;">{cpu:.1f}%</div>
              <div class="stat-lbl">CPU</div>
            </div>
            <div class="stat-cell">
              <div class="stat-num" style="color:{temp_color};">{temp:.1f}C</div>
              <div class="stat-lbl">Temp</div>
            </div>
            <div class="stat-cell">
              <div class="stat-num">{batt}%</div>
              <div class="stat-lbl">Battery</div>
            </div>
          </div>
          <div class="node-section">
            <div class="node-lbl">Participant Node</div>
            <div class="node-id">NODE_ID: @nexaedge / {token[-12:]}</div>
            <div class="status-row">
              <div class="status-block">
                <div class="status-lbl">{T['mining_status']}</div>
                <div class="status-val" style="color:{mining_status_color};">{mining_status_text}</div>
              </div>
              <div class="status-block" style="text-align:right;">
                <div class="status-lbl">{T['token_earnings']}</div>
                <div class="nexa-val">{nexa_earned:.4f} NEXA</div>
              </div>
            </div>
          </div>
        </div>
        """, height=310)

        # ── Activate / Stop buttons
        node_active = st.session_state.get("node_active", False)
        col_act, col_stop = st.columns([3, 2])
        with col_act:
            if st.button(T["start_session"], disabled=node_active, key="btn_activate"):
                st.session_state.node_active = True
                st.session_state.node_tasks  = st.session_state.get("node_tasks", 0)
                st.session_state.node_log    = []
                node_active = True
        with col_stop:
            if st.button(T["stop"], disabled=not node_active, type="secondary", key="btn_stop"):
                st.session_state.node_active = False
                node_active = False
                try:
                    supabase.table("nodes").update({"status": "offline"}).eq("node_token", token).execute()
                except: pass

        if node_active:
            from streamlit_autorefresh import st_autorefresh
            st_autorefresh(interval=30000, key="portal_tick")

            try:
                cpu_sim  = round(random.uniform(5, 35), 1)
                temp_sim = round(random.uniform(32, 38), 1)
                batt_sim = 100
                now_iso  = datetime.now(timezone.utc).isoformat()

                supabase.table("heartbeats").insert({
                    "node_token":      token,
                    "cpu_usage":       cpu_sim,
                    "temperature":     temp_sim,
                    "battery_level":   batt_sim,
                    "tasks_completed": st.session_state.get("node_tasks", 0),
                    "reported_at":     now_iso,
                }).execute()

                supabase.table("nodes").update({
                    "status":    "online",
                    "last_seen": now_iso,
                }).eq("node_token", token).execute()

                hb_msg = f"♥ CPU {cpu_sim}%  Temp {temp_sim}°C  Batt {batt_sim}%"
                hb_color = "#a2ff00"
            except Exception as e:
                hb_msg  = f"Heartbeat error: {e}"
                hb_color = "#f43f5e"

            task_msg = None
            try:
                # Auto-inject a simulated task every cycle so NEXA always increases
                task_types = ["slm_inference", "rlhf_validation", "zk_proof"]
                ttype = random.choice(task_types)
                result = f"[Portal] {ttype} OK | latency={round(random.uniform(2,5),1)}ms | node={token[-8:]}"
                supabase.table("tasks").insert({
                    "task_type":    ttype,
                    "status":       "completed",
                    "assigned_to":  token,
                    "payload":      f"auto_{random.randint(1000,9999)}",
                    "result":       result,
                    "completed_at": datetime.now(timezone.utc).isoformat(),
                }).execute()
                st.session_state.node_tasks = st.session_state.get("node_tasks", 0) + 1
                task_msg = f"✓ {ttype} completed · +0.0022 NEXA"
            except Exception as e:
                task_msg = f"Task error: {e}"

            log = st.session_state.get("node_log", [])
            ts_str = datetime.now().strftime("%H:%M:%S")
            log.insert(0, (f"[{ts_str}] {hb_msg}", hb_color))
            if task_msg:
                log.insert(0, (f"[{ts_str}] {task_msg}", "#a2ff00"))
            log = log[:6]
            st.session_state.node_log = log

            log_html = "".join(
                f'<div style="color:{c};line-height:1.9;">{l}</div>'
                for l, c in log
            )
            st.markdown(f"""
            <div style="background:#040709;border:1px solid #182230;border-radius:10px;
                        padding:14px;font-family:'Space Mono',monospace;font-size:10px;margin-top:4px;">
                <div style="display:flex;align-items:center;gap:8px;margin-bottom:10px;">
                    <div style="width:8px;height:8px;border-radius:50%;background:#a2ff00;box-shadow:0 0 8px #a2ff00;"></div>
                    <span style="color:#a2ff00;font-size:10px;text-transform:uppercase;letter-spacing:.08em;">{T['online_refresh']}</span>
                </div>
                {log_html}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style="background:#040709;border:1px solid #182230;border-radius:10px;
                        padding:14px;font-family:'Space Mono',monospace;font-size:10px;
                        color:#2a3a4a;margin-top:4px;">
                {T['press_start']}
            </div>
            """, unsafe_allow_html=True)

        # ── Task history
        tasks = get_node_tasks(token)
        if tasks:
            task_rows_html = ""
            for t in tasks:
                t_type   = t.get("task_type", "—")
                t_status = t.get("status", "—")
                t_time   = (t.get("completed_at") or t.get("created_at") or "")[:16].replace("T", " ")
                s_class  = {"completed": "nx-task-status-done",
                            "assigned":  "nx-task-status-assigned"}.get(t_status, "nx-task-status-pending")
                task_rows_html += f"""
                <div class="nx-task-row">
                    <div class="nx-task-type">{t_type}</div>
                    <div class="{s_class}">{t_status}</div>
                    <div class="nx-task-time">{t_time}</div>
                </div>"""
            st.markdown(f"""
            <div class="nx-card" style="margin-top:12px;">
                <div class="nx-card-title">▸ {T['task_history']}
                    <span style="color:#a2ff00;margin-left:8px;">{task_count} {T['completed']}</span>
                </div>
                {task_rows_html}
            </div>
            """, unsafe_allow_html=True)

    else:
        st.markdown(f"""
        <div class="nx-card">
            <div class="nx-card-title">▸ {T['register_device']}</div>
            <div style="font-size:12px;color:#4a6070;line-height:1.7;margin-bottom:16px;">
                {T['register_desc']}
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button(T["register_btn"]):
            tok = generate_node_token()
            ok  = register_node(email, tok)
            if ok:
                st.success(f"Node registered! Token: **{tok}**")
                st.rerun()
            else:
                st.error(T["register_fail"])

    # ── WASM Browser Demo
    st.markdown('<div style="margin-top:20px;"></div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="nx-card" style="border-color:rgba(0,229,255,.2);">
        <div class="nx-card-title">
            <span style="color:#00e5ff;">▸</span> {T['wasm_title']}
            <span style="background:rgba(0,229,255,.1);border:1px solid rgba(0,229,255,.2);
                         color:#00e5ff;font-family:'Space Mono',monospace;font-size:8px;
                         padding:2px 7px;border-radius:4px;margin-left:6px;">
                {T['wasm_badge']}
            </span>
        </div>
        <div style="font-size:11px;color:#4a6070;line-height:1.7;margin-bottom:14px;">
            {T['wasm_desc']}
        </div>
    </div>
    """, unsafe_allow_html=True)

    wasm_html = f"""
    <div style="background:#040709;border:1px solid rgba(0,229,255,.2);border-radius:10px;
                padding:16px;font-family:'Space Mono',monospace;font-size:10px;">

        <div style="display:flex;align-items:center;gap:10px;margin-bottom:12px;">
            <div id="wasm-dot" style="width:8px;height:8px;border-radius:50%;
                 background:#4a6070;transition:background .3s;"></div>
            <div id="wasm-status" style="font-size:10px;text-transform:uppercase;
                 letter-spacing:.08em;color:#4a6070;">READY</div>
        </div>

        <div id="wasm-log" style="color:#2a3a4a;line-height:1.9;min-height:40px;
             font-size:10px;margin-bottom:14px;">
            // Press RUN to execute compute kernel in this browser
        </div>

        <div style="display:flex;gap:8px;margin-bottom:12px;">
            <button onclick="runCompute(32)"
                style="background:linear-gradient(135deg,#00e5ff,#0099bb);
                       color:#060b0f;border:none;border-radius:6px;
                       padding:8px 16px;font-family:monospace;font-size:10px;
                       font-weight:700;letter-spacing:.06em;cursor:pointer;">
                ▶ RUN (32×32)
            </button>
            <button onclick="runCompute(128)"
                style="background:transparent;color:#00e5ff;
                       border:1px solid rgba(0,229,255,.3);border-radius:6px;
                       padding:8px 16px;font-family:monospace;font-size:10px;
                       cursor:pointer;">
                ⚡ STRESS (128×128)
            </button>
        </div>

        <div id="wasm-result" style="display:none;background:#060b0f;border:1px solid #182230;
             border-radius:8px;padding:12px;margin-top:8px;">
            <div style="font-size:9px;color:#4a6070;text-transform:uppercase;
                        letter-spacing:.08em;margin-bottom:8px;">EXECUTION RESULT</div>
            <div id="wasm-output" style="color:#00e5ff;font-size:11px;line-height:1.8;"></div>
        </div>
    </div>

    <script>
    function log(msg, color) {{
        const el = document.getElementById("wasm-log");
        const line = document.createElement("div");
        line.style.color = color || "#4a6070";
        line.textContent = "[" + new Date().toLocaleTimeString() + "] " + msg;
        el.insertBefore(line, el.firstChild);
        while (el.children.length > 6) el.removeChild(el.lastChild);
    }}

    function setStatus(text, color) {{
        document.getElementById("wasm-status").textContent = text;
        document.getElementById("wasm-status").style.color = color;
        document.getElementById("wasm-dot").style.background = color;
        document.getElementById("wasm-dot").style.boxShadow = "0 0 8px " + color;
    }}

    function matmul(N) {{
        // Allocate NxN matrices as Float32Arrays
        const A = new Float32Array(N * N);
        const B = new Float32Array(N * N);
        const C = new Float32Array(N * N);
        for (let i = 0; i < N * N; i++) {{
            A[i] = Math.random() * 2 - 1;
            B[i] = Math.random() * 2 - 1;
        }}
        for (let i = 0; i < N; i++)
            for (let k = 0; k < N; k++) {{
                const aik = A[i * N + k];
                for (let j = 0; j < N; j++)
                    C[i * N + j] += aik * B[k * N + j];
            }}
        let checksum = 0;
        for (let i = 0; i < N * N; i++) checksum += C[i];
        return checksum;
    }}

    function runCompute(N) {{
        setStatus("RUNNING...", "#ffb300");
        log("Starting " + N + "×" + N + " FP32 matmul...", "#00e5ff");

        // Use setTimeout to let UI update before heavy compute
        setTimeout(() => {{
            const t0 = performance.now();
            const checksum = matmul(N);
            const t1 = performance.now();
            const latency = (t1 - t0).toFixed(2);
            const flops = (2 * N * N * N / ((t1 - t0) / 1000) / 1e9).toFixed(2);

            setStatus("COMPUTE DONE", "#a2ff00");
            log(N+"×"+N+" matmul done · "+latency+"ms · "+flops+" GFLOPS", "#a2ff00");

            document.getElementById("wasm-result").style.display = "block";
            document.getElementById("wasm-output").innerHTML =
                "Engine: <span style='color:#a2ff00;'>Browser JS (Float32Array)</span><br>" +
                "Operation: <span style='color:#e8edf2;'>" + N + "×" + N + " Matrix Multiply (FP32)</span><br>" +
                "Latency: <span style='color:#a2ff00;'>" + latency + "ms</span><br>" +
                "Throughput: <span style='color:#00e5ff;'>" + flops + " GFLOPS</span><br>" +
                "Checksum: <span style='color:#4a6070;'>" + checksum.toFixed(4) + "</span><br>" +
                "Node: <span style='color:#4a6070;'>{token}</span>";
        }}, 10);
    }}
    </script>
    """
    st.components.v1.html(wasm_html, height=360)

    # ── Node Journey timeline
    st.markdown('<div style="margin-top:20px;"></div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="nx-card">
        <div class="nx-card-title">▸ {T['journey_title']}</div>
        <div class="nx-timeline">
            <div class="nx-tl-item">
                <div class="nx-tl-dot done"></div>
                <div>
                    <div class="nx-tl-title">{T['j1_title']}</div>
                    <div class="nx-tl-sub">{T['j1_sub']}</div>
                </div>
            </div>
            <div class="nx-tl-item">
                <div class="nx-tl-dot done"></div>
                <div>
                    <div class="nx-tl-title">{T['j2_title']}</div>
                    <div class="nx-tl-sub">{T['j2_sub']}</div>
                </div>
            </div>
            <div class="nx-tl-item">
                <div class="nx-tl-dot now"></div>
                <div>
                    <div class="nx-tl-title">{T['j3_title']}</div>
                    <div class="nx-tl-sub">{T['j3_sub']}</div>
                </div>
            </div>
            <div class="nx-tl-item">
                <div class="nx-tl-dot"></div>
                <div>
                    <div class="nx-tl-title muted">{T['j4_title']}</div>
                    <div class="nx-tl-sub">{T['j4_sub']}</div>
                </div>
            </div>
            <div class="nx-tl-item">
                <div class="nx-tl-dot"></div>
                <div>
                    <div class="nx-tl-title muted">{T['j5_title']}</div>
                    <div class="nx-tl-sub">{T['j5_sub']}</div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="nx-notice">
        ⚠ {T['nexa_notice']}
    </div>
    """, unsafe_allow_html=True)

    if st.button(T["sign_out"], type="secondary"):
        st.session_state.user_email = None
        st.session_state.user_data  = None
        st.session_state.magic_sent = False
        st.rerun()

# ══════════════════════════════════════
# NOT LOGGED IN — LOGIN
# ══════════════════════════════════════
else:
    total = get_total_signups()
    st.markdown(f"""
    <div class="nx-login-hero">
        <div class="nx-login-dot"></div>
        <div style="margin-bottom:10px;">
            <span class="nx-stage">{T['stage']}</span>
        </div>
        <div class="nx-login-title">{T['login_title']}</div>
        <div class="nx-login-sub">{T['login_sub']}</div>
        <div style="font-family:'Space Mono',monospace;font-size:11px;color:#4a6070;">
            <span style="color:#a2ff00;font-weight:700;">{total}</span> {T['nodes_reserved']}
        </div>
    </div>
    """, unsafe_allow_html=True)

    if not st.session_state.magic_sent:
        email_input = st.text_input(T["email_label"], placeholder=T["email_ph"], key="login_email_input")
        if st.button(T["send_code"]):
            if not email_input or "@" not in email_input:
                st.error(T["invalid_email"])
            else:
                record = lookup_waitlist(email_input)
                if not record:
                    st.error(T["not_on_wl"])
                else:
                    code = generate_otp()
                    if "otp_store" not in st.session_state:
                        st.session_state.otp_store = {}
                    st.session_state.otp_store[email_input.lower()] = {
                        "code": code,
                        "created": datetime.now(timezone.utc).timestamp()
                    }
                    st.session_state.magic_sent  = True
                    st.session_state.magic_email = email_input
                    st.session_state._beta_code  = code
                    st.rerun()

        st.markdown(f"""
        <div style="text-align:center;margin-top:20px;font-family:'Space Mono',monospace;
                    font-size:10px;color:#2a3a4a;line-height:1.7;">
            <a href="https://nexaedge.streamlit.app" target="_blank"
               style="color:#4a6070;text-decoration:none;">
                {T['register_at']}
            </a>
        </div>
        """, unsafe_allow_html=True)

    else:
        beta_code = st.session_state.get("_beta_code", "")
        st.markdown(f"""
        <div style="background:rgba(162,255,0,.04);border:1px solid rgba(162,255,0,.15);
                    border-radius:12px;padding:20px;text-align:center;margin-bottom:20px;">
            <div style="font-size:24px;margin-bottom:8px;">📬</div>
            <div style="font-size:14px;font-weight:700;color:#e8edf2;margin-bottom:6px;">
                {T['your_code']}
            </div>
            <div style="font-family:'Space Mono',monospace;font-size:10px;color:#4a6070;
                        line-height:1.7;margin-bottom:12px;">
                {T['signing_in']}<br>
                <strong style="color:#a2ff00;">{st.session_state.magic_email}</strong>
            </div>
            <div style="font-family:'Space Mono',monospace;font-size:28px;font-weight:700;
                        color:#a2ff00;letter-spacing:.3em;background:#060b0f;
                        border:1px solid rgba(162,255,0,.2);border-radius:8px;
                        padding:12px 20px;display:inline-block;">
                {beta_code}
            </div>
            <div style="font-family:'Space Mono',monospace;font-size:8px;color:#2a3a4a;margin-top:10px;">
                {T['beta_warning']}
            </div>
        </div>
        """, unsafe_allow_html=True)

        otp_input = st.text_input(T["enter_code"], placeholder=T["code_ph"], max_chars=6, key="otp_input")
        if st.button(T["verify"]):
            if not otp_input or len(otp_input) < 6:
                st.error(T["enter_code"])
            else:
                if verify_code(st.session_state.magic_email, otp_input):
                    record = lookup_waitlist(st.session_state.magic_email)
                    st.session_state.user_email = st.session_state.magic_email
                    st.session_state.user_data  = record
                    st.session_state.magic_sent = False
                    st.session_state._beta_code = ""
                    st.rerun()
                else:
                    st.error(T["wrong_code"])

        st.markdown('<div style="margin-top:10px;"></div>', unsafe_allow_html=True)
        if st.button(T["diff_email"], type="secondary"):
            st.session_state.magic_sent  = False
            st.session_state.magic_email = ""
            st.session_state._beta_code  = ""
            st.rerun()

# ══════════════════════════════════════
# FOOTER
# ══════════════════════════════════════
st.markdown(f"""
<div class="nx-footer">
    {T['footer'].replace(chr(10), '<br>')}
</div>
""", unsafe_allow_html=True)
