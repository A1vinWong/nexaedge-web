import streamlit as st
import time
import random
import re
import hashlib
import urllib.parse
from streamlit_autorefresh import st_autorefresh
from supabase import create_client, Client

st.set_page_config(
    page_title="NexaEdge Network — Early Beta",
    page_icon="🟢",
    layout="centered"
)

SUPABASE_URL = st.secrets["supabase"]["url"]
SUPABASE_KEY = st.secrets["supabase"]["key"]


@st.cache_resource
def get_supabase() -> Client:
    return create_client(SUPABASE_URL, SUPABASE_KEY)

supabase = get_supabase()

def db_count():
    try:
        res = supabase.table("whitelist").select("id", count="exact").execute()
        return res.count or 0
    except: return 0

def db_email_exists(email):
    try:
        res = supabase.table("whitelist").select("id").eq("email", email.lower()).execute()
        return len(res.data) > 0
    except: return False

def db_insert(email, wallet, ref_code, used_ref, lang):
    try:
        supabase.table("whitelist").insert({
            "email": email.lower(), "wallet": wallet, "ref_code": ref_code,
            "used_ref": used_ref or None, "referred_by": used_ref or None,
            "invitation_code": ref_code, "lang": lang,
        }).execute()
        return True
    except: return False

def db_get_registrations():
    try:
        res = supabase.table("whitelist").select("*").order("created_at", desc=False).execute()
        return res.data or []
    except: return []

def db_live_nodes():
    try:
        res = supabase.table("nodes").select("status").execute()
        rows = res.data or []
        online = sum(1 for r in rows if r.get("status") == "online")
        return {"online": online, "total": len(rows)}
    except: return {"online": 0, "total": 0}

def db_latest_heartbeat():
    try:
        res = (supabase.table("heartbeats")
               .select("cpu_usage,temperature,battery_level,reported_at")
               .order("reported_at", desc=True).limit(1).execute())
        return res.data[0] if res.data else None
    except: return None

LANGS = {
    "EN": {
        "nav": ["Market", "Network Sim", "Differentiation", "Roadmap", "Waitlist", "Whitepaper"],
        "tagline": "A protocol design to aggregate idle smartphone compute into a distributed edge AI inference network.",
        "stage": "● EARLY BETA · Q3 2026",
        "sim_only": "⚠ SIMULATION ONLY — All nodes, metrics, and NEXA figures are randomly generated for concept illustration. No real compute is running.",
        "start_sim": "▶ Start Simulation", "stop_sim": "■ Stop",
        "running": "● SIMULATION ACTIVE", "idle": "○ STANDBY",
        "registered": "Waitlist Signups", "active_nodes": "Simulated Active Nodes",
        "tasks_done": "Simulated Tasks", "avg_latency": "Sim. Latency",
        "bft_consensus": "Sim. Consensus", "nexa_earned": "Sim. NEXA",
        "nexa_per_task": "Sim. NEXA/Task", "nexa_proj_title": "NEXA Token Model (Illustrative)",
        "nexa_sim_earned": "Simulated Yield", "nexa_est_usd": "Est. USD (@ $0.50 illustrative)",
        "nexa_supply": "Total Supply (Minted)",
        "nexa_disclaimer": "⚠ Simulated NEXA yield figures are illustrative only. 100,000,000 NEXA tokens have been minted on Solana (contract: D7h9MvFDkVxPYeJwSTcE7VkKXo6mygCHYph36P8oeic2) but are not yet in public circulation. The $0.50 price shown is a hypothetical model, not a market rate. Reward rates and distribution rules will be defined at mainnet. This is not a financial instrument or investment offer.",
        "node_grid_title": "Simulated Node Matrix — 64 Virtual Devices",
        "task_log_title": "Simulated Task Dispatch Log",
        "log_empty": "// Press ▶ Start to begin the simulation.",
        "workload_title": "Simulated Compute Pipeline",
        "wl_inference": "Edge AI Inference (SLM 1.8B / WASM) — concept",
        "wl_rlhf": "Dataset Validation (RLHF) — concept",
        "wl_zk": "ZK Proof Generation — concept",
        "comp_title": "Competitive Positioning", "buyer_title": "Target Buyer Segments",
        "arch_title": "Proposed System Architecture", "diff_title": "NexaEdge vs. Bandwidth Proxies",
        "moat_title": "Planned Technical Moat",
        "thermal_title": "Hardware Safety Design — 39°C Thermal Protocol",
        "roadmap_title": "Development Roadmap", "wl_title": "Join the Early Waitlist",
        "wl_desc": "Signal interest in the node program. Early registrants receive priority airdrop eligibility — the earlier you join and the more you refer, the larger your allocation.",
        "wl_email": "Email Address", "wl_email_ph": "you@example.com",
        "wl_wallet": "Solana Wallet (SPL) — for future use",
        "wl_wallet_ph": "32–44 char public key (e.g. 7xKp...)",
        "wl_ref": "Referral Code (Optional)", "wl_ref_ph": "Enter a friend's code",
        "wl_submit": "Join Waitlist", "wl_success_title": "✅ You're on the waitlist!",
        "wl_success_desc": "You're in the priority airdrop pool. Share your referral code — every person you bring moves you up the queue and increases your allocation.",
        "wl_your_ref": "Your Referral Code", "wl_copy": "📋 Copy Code", "wl_copied": "✅ Copied!",
        "wl_reset": "🔄 Register Another", "wl_total": "Waitlist Signups",
        "err_email": "Please enter a valid email address.",
        "err_wallet": "Solana wallet must be 32–44 characters.",
        "err_dupe": "This email is already registered.",
        "idle_label": "Idle", "active_label": "Active", "processing_label": "Processing",
        "demand_side": "Demand Layer", "coordination": "Settlement Layer", "supply_side": "Supply Cluster",
        "lang_btn": "中文", "ledger_title": "📋 Waitlist — Registered Nodes",
    },
    "ZH": {
        "nav": ["核心市场", "网络模拟", "差异化优势", "路线图", "候补名单", "白皮书"],
        "tagline": "一个将闲置智能手机算力汇聚成分布式边缘 AI 推理网络的协议设计方案。",
        "stage": "● 早期 Beta · 2026年Q3",
        "sim_only": "⚠ 仅为模拟演示——所有节点、指标与 NEXA 数字均为随机生成，用于概念说明，并非真实算力运行。",
        "start_sim": "▶ 启动模拟", "stop_sim": "■ 停止",
        "running": "● 模拟运行中", "idle": "○ 待机中",
        "registered": "候补名单注册数", "active_nodes": "模拟活跃节点",
        "tasks_done": "模拟任务数", "avg_latency": "模拟延迟",
        "bft_consensus": "模拟共识", "nexa_earned": "模拟 NEXA",
        "nexa_per_task": "模拟 NEXA/任务", "nexa_proj_title": "NEXA 代币模型（示意）",
        "nexa_sim_earned": "模拟产出", "nexa_est_usd": "估值（@ $0.50 示意价）",
        "nexa_supply": "总供应量（已铸造）",
        "nexa_disclaimer": "⚠ 模拟 NEXA 产出数字仅供示意。1 亿枚 NEXA 代币已在 Solana 上铸造（合约：D7h9MvFDkVxPYeJwSTcE7VkKXo6mygCHYph36P8oeic2），但尚未公开流通。所示 $0.50 价格为假设模型，并非市场价格。奖励比率与分发规则将在主网阶段确定。本内容不构成金融工具或投资要约。",
        "node_grid_title": "模拟节点矩阵 — 64 个虚拟设备",
        "task_log_title": "模拟任务调度日志", "log_empty": "// 点击 ▶ 启动模拟。",
        "workload_title": "模拟算力管道",
        "wl_inference": "边缘 AI 推理（SLM 1.8B / WASM）— 概念",
        "wl_rlhf": "数据集验证（RLHF）— 概念", "wl_zk": "ZK 证明生成 — 概念",
        "comp_title": "竞争定位", "buyer_title": "目标买家细分",
        "arch_title": "拟议系统架构", "diff_title": "NexaEdge vs 带宽代理网络",
        "moat_title": "计划中的技术护城河",
        "thermal_title": "硬件安全设计 — 39°C 热保护协议",
        "roadmap_title": "开发路线图", "wl_title": "加入早期候补名单",
        "wl_desc": "表达对节点计划的兴趣。早期注册成员享有优先空投资格——注册越早、推荐越多，获得的分配比例越高。",
        "wl_email": "电子邮件", "wl_email_ph": "your@email.com",
        "wl_wallet": "Solana 钱包（SPL）— 备用", "wl_wallet_ph": "32–44 位公钥（如 7xKp...）",
        "wl_ref": "推荐码（可选）", "wl_ref_ph": "输入朋友的推荐码",
        "wl_submit": "加入候补名单", "wl_success_title": "✅ 已加入候补名单！",
        "wl_success_desc": "您已进入优先空投池。分享推荐码——每推荐一人，您的排名上升，分配比例也随之提高。",
        "wl_your_ref": "您的推荐码", "wl_copy": "📋 复制", "wl_copied": "✅ 已复制！",
        "wl_reset": "🔄 注册另一个", "wl_total": "候补名单注册数",
        "err_email": "请输入有效的电子邮件地址。",
        "err_wallet": "Solana 钱包地址应为 32–44 个字符。",
        "err_dupe": "此邮箱已注册。",
        "idle_label": "空闲", "active_label": "活跃", "processing_label": "处理中",
        "demand_side": "需求方", "coordination": "协调层", "supply_side": "供给方",
        "lang_btn": "English", "ledger_title": "📋 候补名单 — 已注册节点",
    }
}

TASK_TYPES_EN = [
    ("[SIM] SLM inference (Phi-3 mini / WASM)", "success"),
    ("[SIM] RLHF label validation chunk", "info"),
    ("[SIM] ZK proof chunk verification", "success"),
    ("[SIM] BFT consensus cluster vote", "info"),
    ("[SIM] Thermal check: OK ✓", "success"),
    ("[SIM] Node fingerprint SHA256 verified", "success"),
]
TASK_TYPES_ZH = [
    ("[模拟] SLM 推理任务执行 (Phi-3 mini / WASM)", "success"),
    ("[模拟] RLHF 数据标签交叉验证", "info"),
    ("[模拟] ZK 证明片段生成与校验", "success"),
    ("[模拟] BFT 共识层节点签名投票", "info"),
    ("[模拟] 本机热指标检查: 正常 ✓", "success"),
    ("[模拟] 节点硬件指纹哈希校验成功", "success"),
]
REWARD_BASE = 0.0022

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Syne:wght@400;600;700;800&display=swap');
.main .block-container{padding-top:1.2rem!important;padding-bottom:3rem!important;max-width:880px!important}
.stApp{background-color:#060b0f}
#MainMenu,footer,header,[data-testid="stHeader"]{display:none!important}
.stApp::before{content:'';position:fixed;inset:0;background-image:linear-gradient(rgba(162,255,0,.022) 1px,transparent 1px),linear-gradient(90deg,rgba(162,255,0,.022) 1px,transparent 1px);background-size:44px 44px;pointer-events:none;z-index:0}
*,h1,h2,h3,h4,p,div,span,label{font-family:'Syne',sans-serif}
div[data-testid="stRadio"]>label{display:none!important}
div[data-testid="stRadio"]>div{flex-direction:row!important;gap:4px!important;border-bottom:1px solid #182230!important;padding-bottom:0!important;margin-bottom:24px;flex-wrap:wrap!important}
div[data-testid="stRadio"] label[data-baseweb="radio"]{background:#0d1720!important;color:#4a6070!important;border-radius:8px 8px 0 0!important;border:1px solid #182230!important;border-bottom:none!important;padding:9px 18px!important;font-family:'Space Mono',monospace!important;font-size:10px!important;font-weight:700!important;text-transform:uppercase!important;letter-spacing:.06em!important;margin:0!important;cursor:pointer!important}
div[data-testid="stRadio"] label[data-baseweb="radio"]:hover{color:#a2ff00!important}
div[data-testid="stRadio"] label[data-baseweb="radio"]:has(input:checked){color:#a2ff00!important;background:#0d1720!important}
div[data-testid="stRadio"] input{display:none!important}
div[data-testid="stRadio"] div[data-testid="stMarkdownContainer"] p{font-size:10px!important;font-weight:700!important}
[data-testid="stMetric"]{background:linear-gradient(135deg,#0d1720,#0a1118)!important;border:1px solid #182230!important;border-radius:12px!important;padding:18px!important}
[data-testid="stMetricLabel"]{font-family:'Space Mono',monospace!important;font-size:9px!important;color:#4a6070!important;text-transform:uppercase!important;letter-spacing:.1em!important}
[data-testid="stMetricValue"]{font-size:24px!important;font-weight:800!important;color:#e8edf2!important}
[data-testid="stMetricDelta"]{font-size:10px!important;color:#a2ff00!important}
div.stButton>button{background:linear-gradient(135deg,#a2ff00,#8de600)!important;color:#060b0f!important;font-family:'Space Mono',monospace!important;font-size:11px!important;font-weight:700!important;text-transform:uppercase!important;letter-spacing:.06em!important;border:none!important;border-radius:8px!important;padding:11px 22px!important;width:100%!important}
div.stButton>button:hover{background:linear-gradient(135deg,#b5ff33,#a2ff00)!important;box-shadow:0 0 20px rgba(162,255,0,.25)!important}
div.stButton>button[kind="secondary"]{background:transparent!important;color:#4a6070!important;border:1px solid #182230!important;box-shadow:none!important}
div.stButton>button[kind="secondary"]:hover{border-color:#a2ff00!important;color:#a2ff00!important}
.stTextInput>div>div>input{background:#060b0f!important;border:1px solid #182230!important;border-radius:8px!important;color:#e8edf2!important;font-family:'Space Mono',monospace!important;font-size:12px!important;padding:12px 14px!important}
.stTextInput>div>div>input:focus{border-color:#a2ff00!important;box-shadow:0 0 0 2px rgba(162,255,0,.1)!important}
.stTextInput label{font-family:'Space Mono',monospace!important;font-size:10px!important;color:#4a6070!important;text-transform:uppercase!important;letter-spacing:.08em!important}
.nx-card{background:linear-gradient(160deg,#0d1720,#090e14);border:1px solid #182230;border-radius:14px;padding:22px 24px;margin-bottom:16px}
.nx-card-title{font-family:'Space Mono',monospace;font-size:10px;color:#4a6070;text-transform:uppercase;letter-spacing:.12em;margin-bottom:18px;display:flex;align-items:center;gap:8px}
.nx-card-title .dot{color:#a2ff00}
.nx-notice{background:rgba(255,179,0,.05);border:1px solid rgba(255,179,0,.2);border-left:3px solid #ffb300;border-radius:0 8px 8px 0;padding:12px 16px;font-family:'Space Mono',monospace;font-size:10px;color:#ffb300;line-height:1.7;margin-bottom:20px}
.nx-online-badge{display:inline-flex;align-items:center;gap:10px;background:#060b0f;border:1px solid #182230;border-radius:8px;padding:7px 14px;font-family:'Space Mono',monospace;font-size:10px;color:#4a6070;margin-top:8px}
.nx-stage-badge{display:inline-block;background:rgba(162,255,0,.08);border:1px solid rgba(162,255,0,.25);color:#a2ff00;font-family:'Space Mono',monospace;font-size:9px;font-weight:700;padding:5px 12px;border-radius:6px;letter-spacing:.1em}
.nx-feature{background:#060b0f;border:1px solid #182230;border-left:3px solid #a2ff00;border-radius:0 10px 10px 0;padding:16px 18px;margin-bottom:12px}
.nx-feature-title{font-size:13px;font-weight:700;color:#e8edf2;margin-bottom:6px}
.nx-feature-body{font-size:11px;color:#4a6070;line-height:1.7}
.nx-feature-buyer{margin-top:8px;font-family:'Space Mono',monospace;font-size:10px;color:#00e5ff}
.tag-bad{display:inline-block;background:rgba(244,63,94,.12);color:#f43f5e;font-family:'Space Mono',monospace;font-size:9px;padding:2px 7px;border-radius:4px;font-weight:700}
.tag-good{display:inline-block;background:rgba(162,255,0,.1);color:#a2ff00;font-family:'Space Mono',monospace;font-size:9px;padding:2px 7px;border-radius:4px;font-weight:700}
.tag-plan{display:inline-block;background:rgba(0,229,255,.08);color:#00e5ff;font-family:'Space Mono',monospace;font-size:9px;padding:2px 7px;border-radius:4px;font-weight:700}
.nx-node-grid{display:grid;grid-template-columns:repeat(8,1fr);gap:6px;margin:14px 0}
.nx-node{aspect-ratio:1;border-radius:5px;background:#182230}
.nx-node.active{background:#a2ff00;box-shadow:0 0 8px rgba(162,255,0,.35)}
.nx-node.processing{background:#00e5ff;box-shadow:0 0 8px rgba(0,229,255,.35);animation:blink 1.1s ease-in-out infinite}
@keyframes blink{0%,100%{opacity:1}50%{opacity:.3}}
.nx-legend{display:flex;gap:20px;margin-top:12px}
.nx-legend-item{display:flex;align-items:center;gap:6px;font-family:'Space Mono',monospace;font-size:10px;color:#4a6070}
.nx-legend-dot{width:10px;height:10px;border-radius:3px}
.nx-sim-stat{background:#060b0f;border:1px solid #182230;border-radius:10px;padding:14px 10px;text-align:center}
.nx-sim-val{font-family:'Space Mono',monospace;font-size:17px;font-weight:700;color:#a2ff00}
.nx-sim-val.cyan{color:#00e5ff}
.nx-sim-val.gold{color:#ffb300}
.nx-sim-label{font-family:'Space Mono',monospace;font-size:8px;color:#4a6070;margin-top:5px;text-transform:uppercase;letter-spacing:.07em}
.nx-log{background:#040709;border:1px solid #182230;border-radius:10px;padding:14px;font-family:'Space Mono',monospace;font-size:10px;color:#4a6070;line-height:1.9;max-height:150px;overflow-y:auto}
.log-success{color:#a2ff00}
.log-info{color:#00e5ff}
.nx-prog-row{display:flex;justify-content:space-between;font-family:'Space Mono',monospace;font-size:10px;color:#4a6070;margin-bottom:6px}
.nx-prog-bar{height:5px;background:#182230;border-radius:3px;overflow:hidden;margin-bottom:14px}
.nx-prog-fill{height:100%;background:linear-gradient(90deg,#a2ff00,#7acc00);border-radius:3px;transition:width .7s ease}
.nx-prog-fill.blue{background:linear-gradient(90deg,#00e5ff,#0099bb)}
.nx-table{width:100%;border-collapse:collapse;font-size:11px}
.nx-table th{text-align:left;padding:10px 12px;font-family:'Space Mono',monospace;font-size:9px;text-transform:uppercase;letter-spacing:.08em;color:#4a6070;border-bottom:1px solid #182230}
.nx-table th.hl{color:#a2ff00}
.nx-table td{padding:11px 12px;border-bottom:1px solid rgba(24,34,48,.6);color:#4a6070;vertical-align:top;line-height:1.5}
.nx-table td:first-child{color:#d0d8e4;font-weight:600;width:140px}
.nx-table td.hl{color:#d0d8e4}
.nx-table tr:last-child td{border-bottom:none}
.nx-table tr:hover td{background:rgba(24,34,48,.3)}
.nx-roadmap-item{border-left:2px solid #182230;padding-left:20px;padding-bottom:24px;position:relative}
.nx-roadmap-item::before{content:'';position:absolute;left:-6px;top:5px;width:10px;height:10px;border-radius:50%;background:#182230;border:2px solid #182230}
.nx-roadmap-item.current::before{background:#a2ff00;border-color:#a2ff00;box-shadow:0 0 10px rgba(162,255,0,.5)}
.nx-roadmap-item.done::before{background:#a2ff00;border-color:#a2ff00}
.nx-roadmap-phase{font-family:'Space Mono',monospace;font-size:9px;color:#ffb300;text-transform:uppercase;letter-spacing:.1em;margin-bottom:5px}
.nx-roadmap-phase.done{color:#a2ff00}
.nx-roadmap-title{font-size:14px;font-weight:700;color:#e8edf2;margin-bottom:6px}
.nx-roadmap-body{font-size:11px;color:#4a6070;line-height:1.7}
.nx-moat{background:#060b0f;border:1px solid #182230;border-radius:10px;padding:18px;margin-bottom:12px}
.nx-moat-icon{font-size:22px;margin-bottom:10px}
.nx-moat-title{font-size:13px;font-weight:700;color:#e8edf2;margin-bottom:6px}
.nx-moat-body{font-size:11px;color:#4a6070;line-height:1.7}
.nx-social-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(80px,1fr));gap:8px;margin:16px 0 0}
.nx-social-btn{display:block;text-align:center;padding:9px 8px;background:#0d1720;border:1px solid #182230;border-radius:10px;color:#4a6070!important;font-size:11px;font-weight:700;text-decoration:none;transition:all .2s}
.nx-social-btn:hover{border-color:#a2ff00;color:#a2ff00!important}
.nx-ref-display{background:#060b0f;border:1px solid rgba(162,255,0,.3);border-radius:10px;padding:20px;text-align:center;margin-bottom:16px}
.nx-ref-code{font-family:'Space Mono',monospace;font-size:26px;font-weight:700;color:#a2ff00;letter-spacing:.2em;margin:8px 0}
.nx-ref-label{font-family:'Space Mono',monospace;font-size:9px;color:#4a6070;text-transform:uppercase;letter-spacing:.1em}
.nx-success-banner{background:rgba(162,255,0,.05);border:1px solid rgba(162,255,0,.2);border-radius:14px;padding:28px;text-align:center;margin-bottom:16px}
.arch-box{flex:1;background:#060b0f;border:1px solid #182230;border-radius:10px;padding:18px 14px;text-align:center}
.arch-label{font-family:'Space Mono',monospace;font-size:8px;color:#4a6070;text-transform:uppercase;letter-spacing:.1em;margin-bottom:10px}
.arch-icon{font-size:26px;margin-bottom:8px}
.arch-title{font-size:13px;font-weight:700;color:#e8edf2;margin-bottom:6px}
.arch-body{font-size:10px;color:#4a6070;line-height:1.6}
.arch-arrow{display:flex;align-items:center;padding:0 10px;color:#a2ff00;font-size:20px}
.nx-nexa-mini{background:#060b0f;border:1px solid #182230;border-radius:10px;padding:14px;text-align:center}
.nx-nexa-mini-label{font-family:'Space Mono',monospace;font-size:9px;color:#4a6070;text-transform:uppercase;letter-spacing:.08em;margin-bottom:5px}
.nx-nexa-mini-val{font-family:'Space Mono',monospace;font-size:15px;font-weight:700;color:#ffb300}
.nx-footer{border-top:1px solid #182230;margin-top:50px;padding-top:20px;text-align:center;font-family:'Space Mono',monospace;font-size:10px;color:#2a3a4a;line-height:2}
.nx-divider{border:none;border-top:1px solid #182230;margin:6px 0 12px}
</style>
""", unsafe_allow_html=True)

_defaults = {
    'lang': 'EN', 'sim_running': False, 'sim_tasks': 0, 'sim_log': [],
    'sim_nodes': [0]*64, 'sim_latency': 3.0, 'sim_consensus': 98.2,
    'prog1': 0, 'prog2': 0, 'prog3': 0, 'nexa_earned': 0.0, 'nexa_rate': 0.0,
    'wl_success': False, 'wl_ref_code': '',
}
for k, v in _defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

L = LANGS[st.session_state.lang]
TASK_TYPES = TASK_TYPES_EN if st.session_state.lang == "EN" else TASK_TYPES_ZH

if st.session_state.sim_running:
    st_autorefresh(interval=1200, key="nexa_tick")
    real_cpu = random.randint(15, 85)
    nodes = st.session_state.sim_nodes
    active_target = int(10 + (real_cpu / 100) * 40)
    for i in range(64):
        nodes[i] = (2 if random.random() > 0.4 else 1) if i < active_target else 0
    st.session_state.sim_nodes = nodes
    task, cls = random.choice(TASK_TYPES)
    ts = time.strftime("%H:%M:%S")
    st.session_state.sim_log.append((f"[{ts}] Node #{random.randint(1,64)} -> {task}", cls))
    if len(st.session_state.sim_log) > 15:
        st.session_state.sim_log = st.session_state.sim_log[-15:]
    st.session_state.sim_tasks += 1
    t = st.session_state.sim_tasks
    st.session_state.prog1 = min(85, int(t * 1.4))
    st.session_state.prog2 = min(72, int(t * 1.1))
    st.session_state.prog3 = min(60, int(t * 0.9))
    st.session_state.sim_latency = max(2.2, min(4.5, st.session_state.sim_latency + random.uniform(-0.3, 0.3)))
    st.session_state.sim_consensus = max(95.0, min(99.9, st.session_state.sim_consensus + random.uniform(-0.2, 0.2)))
    reward = max(0, REWARD_BASE + random.uniform(-0.0005, 0.001))
    st.session_state.nexa_rate = reward
    st.session_state.nexa_earned += reward

total_reg_count = 0
live = {"online": 0, "total": 0}

c1, c2, c3 = st.columns([1, 2, 1])
with c2:
    st.image('IMG_7859.jpeg', use_container_width=True)
st.markdown('<div style="margin-bottom:8px;"></div>', unsafe_allow_html=True)
col_logo, col_right = st.columns([3, 1])
with col_logo:
    live_dot = '<span style="display:inline-block;width:7px;height:7px;border-radius:50%;background:#a2ff00;box-shadow:0 0 6px #a2ff00;margin-right:5px;"></span>' if live["online"] > 0 else ''
    node_color = "a2ff00" if live["online"] > 0 else "4a6070"
    st.markdown(f"""
    <div style="display:flex;align-items:center;gap:12px;padding:10px 0 4px;">
        <div style="width:11px;height:11px;background:#a2ff00;border-radius:50%;box-shadow:0 0 14px #a2ff00;flex-shrink:0;"></div>
        <div style="font-family:'Syne',sans-serif;font-size:24px;font-weight:800;color:#e8edf2;letter-spacing:-.02em;">
            Nexa<span style="color:#a2ff00;">Edge</span> Network
        </div>
    </div>
    <div style="font-size:12px;color:#4a6070;line-height:1.65;max-width:500px;padding-bottom:8px;">{L['tagline']}</div>
    <div style="display:flex;gap:8px;flex-wrap:wrap;margin-top:4px;">
        <div class="nx-online-badge">{L['registered']}: <strong style="color:#e8edf2;">{total_reg_count}</strong></div>
        <div class="nx-online-badge">{live_dot}<strong style="color:#{node_color};">{live['online']}</strong>&nbsp;node{'s' if live['online']!=1 else ''} online</div>
    </div>
    <div style="margin-top:10px;">
        <a href="https://portal.nexaedge.org?lang={st.session_state.lang}" target="_blank" style="display:inline-flex;align-items:center;gap:8px;background:linear-gradient(135deg,#a2ff00,#8de600);color:#060b0f;font-family:'Space Mono',monospace;font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:.06em;padding:8px 16px;border-radius:8px;text-decoration:none;">
            &#9889; {'登录我的节点' if is_zh else 'My Node Portal'}
        </a>
    </div>
    """, unsafe_allow_html=True)

with col_right:
    st.markdown(f'<div style="text-align:right;padding-top:14px;margin-bottom:8px;"><span class="nx-stage-badge">{L["stage"]}</span></div>', unsafe_allow_html=True)
    if st.button(L["lang_btn"], key="lang_toggle", type="secondary"):
        st.session_state.lang = "ZH" if st.session_state.lang == "EN" else "EN"
        st.rerun()

st.markdown('<hr class="nx-divider">', unsafe_allow_html=True)
current_tab = st.radio("Nav", L["nav"], horizontal=True, label_visibility="collapsed")

# ══════════════════════════════════════
# TAB 1 — MARKET
# ══════════════════════════════════════
if current_tab == L["nav"][0]:
    c1, c2, c3 = st.columns(3)
    with c1: st.metric("Global Idle Smartphones" if st.session_state.lang=="EN" else "全球闲置智能手机", "6.8B", "NPU-capable" if st.session_state.lang=="EN" else "配备NPU")
    with c2: st.metric("Edge AI Market 2028" if st.session_state.lang=="EN" else "边缘AI市场 2028", "$107B", "CAGR 19.2%")
    with c3: st.metric("GPU Spot Cost" if st.session_state.lang=="EN" else "GPU即时价", "$2-4/hr", "H100 volatile" if st.session_state.lang=="EN" else "H100波动")

    if st.session_state.lang == "EN":
        st.markdown(f"""<div class="nx-card"><div class="nx-card-title"><span class="dot">></span> {L['comp_title']}</div>
        <table class="nx-table"><thead><tr><th>Dimension</th><th>GPU Cloud</th><th>Grass</th><th class="hl">NexaEdge (Planned)</th></tr></thead><tbody>
        <tr><td>CapEx</td><td><span class="tag-bad">EXTREME</span></td><td>Low</td><td class="hl"><span class="tag-plan">ZERO (design)</span></td></tr>
        <tr><td>Latency</td><td><span class="tag-bad">50-150ms</span></td><td>N/A</td><td class="hl"><span class="tag-plan">&lt;5ms (target)</span></td></tr>
        <tr><td>Privacy</td><td><span class="tag-bad">Data leaves</span></td><td>Partial</td><td class="hl"><span class="tag-plan">GDPR-native (design)</span></td></tr>
        <tr><td>Geo Reach</td><td>Few DCs</td><td>High IPs</td><td class="hl"><span class="tag-plan">Global (design)</span></td></tr>
        <tr><td>Compute</td><td>GPU only</td><td><span class="tag-bad">Network only</span></td><td class="hl"><span class="tag-plan">NPU + CPU (design)</span></td></tr>
        <tr><td>Sybil Resist.</td><td>Central auth</td><td><span class="tag-bad">IP spoofable</span></td><td class="hl"><span class="tag-plan">HW fingerprint+ZK (design)</span></td></tr>
        </tbody></table></div>""", unsafe_allow_html=True)
    else:
        st.markdown(f"""<div class="nx-card"><div class="nx-card-title"><span class="dot">></span> {L['comp_title']}</div>
        <table class="nx-table"><thead><tr><th>维度</th><th>GPU云</th><th>Grass</th><th class="hl">NexaEdge（计划中）</th></tr></thead><tbody>
        <tr><td>资本支出</td><td><span class="tag-bad">极高</span></td><td>低</td><td class="hl"><span class="tag-plan">零（设计目标）</span></td></tr>
        <tr><td>延迟</td><td><span class="tag-bad">50-150ms</span></td><td>不适用</td><td class="hl"><span class="tag-plan">&lt;5ms（目标）</span></td></tr>
        <tr><td>隐私</td><td><span class="tag-bad">数据离设备</span></td><td>部分</td><td class="hl"><span class="tag-plan">GDPR原生（设计）</span></td></tr>
        <tr><td>地理覆盖</td><td>少量DC</td><td>高IP</td><td class="hl"><span class="tag-plan">全球（设计）</span></td></tr>
        <tr><td>算力</td><td>GPU</td><td><span class="tag-bad">仅网络</span></td><td class="hl"><span class="tag-plan">NPU+CPU（设计）</span></td></tr>
        <tr><td>女巫抵抗</td><td>中心化</td><td><span class="tag-bad">IP可伪造</span></td><td class="hl"><span class="tag-plan">硬件指纹+ZK（设计）</span></td></tr>
        </tbody></table></div>""", unsafe_allow_html=True)

    st.markdown(f'<div class="nx-card"><div class="nx-card-title"><span class="dot">></span> {L["buyer_title"]}</div>', unsafe_allow_html=True)
    b1, b2 = st.columns(2)
    if st.session_state.lang == "EN":
        with b1:
            st.markdown("""<div class="nx-feature"><div class="nx-feature-title">Edge AI Agent Deployers</div><div class="nx-feature-body">Run 1.8B-3.8B SLMs with sub-5ms local inference. GDPR compliant by architecture.</div><div class="nx-feature-buyer">-> AI developers, enterprise SaaS</div></div>
            <div class="nx-feature"><div class="nx-feature-title">AI Dataset Cleaning (RLHF)</div><div class="nx-feature-body">Distributed WASM sandbox runs automated labeling across thousands of nodes simultaneously.</div><div class="nx-feature-buyer">-> AI labs, data pipeline companies</div></div>""", unsafe_allow_html=True)
        with b2:
            st.markdown("""<div class="nx-feature"><div class="nx-feature-title">ZK-ML Inference Verification</div><div class="nx-feature-body">Fragment AI inference proofs across independent nodes. No single point of trust.</div><div class="nx-feature-buyer">-> DeFi protocols, compliance platforms</div></div>
            <div class="nx-feature"><div class="nx-feature-title">Sensor-Context AI</div><div class="nx-feature-body">Leverage GPS, camera, IMU -- context-aware inference unavailable in any datacenter.</div><div class="nx-feature-buyer">-> Location AI, autonomous systems</div></div>""", unsafe_allow_html=True)
    else:
        with b1:
            st.markdown("""<div class="nx-feature"><div class="nx-feature-title">边缘AI代理部署者</div><div class="nx-feature-body">运行1.8B-3.8B SLM，延迟低于5ms，架构层面符合GDPR。</div><div class="nx-feature-buyer">-> AI开发者、企业SaaS</div></div>
            <div class="nx-feature"><div class="nx-feature-title">AI数据集清洗（RLHF）</div><div class="nx-feature-body">分布式WASM沙箱在数千节点上同步运行自动标注与交叉验证。</div><div class="nx-feature-buyer">-> AI实验室、数据管道公司</div></div>""", unsafe_allow_html=True)
        with b2:
            st.markdown("""<div class="nx-feature"><div class="nx-feature-title">ZK-ML推理验证</div><div class="nx-feature-body">将AI推理证明分散到独立节点，冗余验证防止结果篡改。</div><div class="nx-feature-buyer">-> DeFi协议、合规平台</div></div>
            <div class="nx-feature"><div class="nx-feature-title">传感器上下文AI</div><div class="nx-feature-body">利用GPS、摄像头、IMU实现数据中心无法提供的上下文感知推理。</div><div class="nx-feature-buyer">-> 位置AI、自主系统</div></div>""", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    d, c, s = L["demand_side"], L["coordination"], L["supply_side"]
    arch_body = (["Submit tasks via API. Pay in NEXA.", "BFT consensus & reward settlement.", "WASM sandbox. NPU executes inference."]
                 if st.session_state.lang=="EN" else ["通过API提交任务，支付NEXA。","BFT共识与奖励结算。","WASM沙箱，NPU执行推理。"])
    arch_titles = ["AI Buyers" if st.session_state.lang=="EN" else "AI买家","Solana SPL","Device Nodes" if st.session_state.lang=="EN" else "设备节点"]
    arch_html = '<div style="display:flex;align-items:stretch;">'
    for i,(icon,lbl,title,body) in enumerate(zip(["🏢","⛓","📱"],[d,c,s],arch_titles,arch_body)):
        arch_html += f'<div class="arch-box"><div class="arch-label">{lbl}</div><div class="arch-icon">{icon}</div><div class="arch-title">{title}</div><div class="arch-body">{body}</div></div>'
        if i<2: arch_html += '<div class="arch-arrow">-></div>'
    arch_html += '</div>'
    st.markdown(f'<div class="nx-card"><div class="nx-card-title"><span class="dot">></span> {L["arch_title"]}</div>{arch_html}</div>', unsafe_allow_html=True)

    if st.session_state.lang == "EN":
        st.markdown("""<div class="nx-card" style="border-color:rgba(0,229,255,.15);background:rgba(0,229,255,.02);">
        <div class="nx-card-title"><span style="color:#00e5ff;">◈</span> INVESTOR CONTACT</div>
        <div style="font-size:12px;color:#4a6070;line-height:1.8;">NexaEdge is raising a pre-seed round. If you are an accredited investor or grant committee interested in the concept, please reach out directly.<br><br>
        <strong style="color:#d0d8e4;">contact@nexaedge.org</strong><br>
        <span style="font-family:'Space Mono',monospace;font-size:9px;color:#2a3a4a;">No SAFE or investment contract has been formed. All commitments are subject to formal due diligence.</span>
        </div></div>""", unsafe_allow_html=True)
    else:
        st.markdown("""<div class="nx-card" style="border-color:rgba(0,229,255,.15);background:rgba(0,229,255,.02);">
        <div class="nx-card-title"><span style="color:#00e5ff;">◈</span> 投资方联系</div>
        <div style="font-size:12px;color:#4a6070;line-height:1.8;">NexaEdge 正在进行种子前融资。如果您是对本概念感兴趣的合格投资人或资助委员会，请直接联系我们。<br><br>
        <strong style="color:#d0d8e4;">contact@nexaedge.org</strong><br>
        <span style="font-family:'Space Mono',monospace;font-size:9px;color:#2a3a4a;">目前尚未签署任何 SAFE 或投资合同。所有承诺须经正式尽职调查后方可生效。</span>
        </div></div>""", unsafe_allow_html=True)

    st.markdown("""<div class="nx-social-grid">
    <a class="nx-social-btn" href="https://www.instagram.com/nexaedge__" target="_blank">Instagram</a>
    <a class="nx-social-btn" href="https://x.com/nexaedge_" target="_blank">X / Twitter</a>
    <a class="nx-social-btn" href="https://www.facebook.com/share/18eXN6P3Ge/" target="_blank">Facebook</a>
    <a class="nx-social-btn" href="https://www.tiktok.com/@nexaedge7" target="_blank">TikTok</a>
    <a class="nx-social-btn" href="https://t.me/NexaEdge7" target="_blank">Telegram</a>
    <a class="nx-social-btn" href="mailto:contact@nexaedge.org" style="border-color:rgba(0,229,255,.3);color:#00e5ff!important;">Email</a>
    </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════
# TAB 2 — NETWORK SIM
# ══════════════════════════════════════
elif current_tab == L["nav"][1]:
    live2 = db_live_nodes()
    hb2   = db_latest_heartbeat()
    if live2["online"] > 0 and hb2:
        cpu  = hb2.get("cpu_usage", 0) or 0
        temp = hb2.get("temperature", 0) or 0
        batt = hb2.get("battery_level", 0) or 0
        ts_raw = (hb2.get("reported_at", "")[:19] or "").replace("T", " ")
        temp_color = "f43f5e" if temp >= 39 else "e8edf2"
        st.markdown(f"""<div style="background:rgba(162,255,0,.04);border:1px solid rgba(162,255,0,.2);border-left:3px solid #a2ff00;border-radius:0 10px 10px 0;padding:12px 16px;font-family:'Space Mono',monospace;font-size:10px;color:#4a6070;line-height:1.8;margin-bottom:14px;">
            <span style="color:#a2ff00;font-weight:700;">LIVE NODE DATA</span>
            &nbsp;·&nbsp; {live2['online']} node{'s' if live2['online']!=1 else ''} online
            &nbsp;·&nbsp; CPU <span style="color:#e8edf2;">{cpu:.1f}%</span>
            &nbsp;·&nbsp; Temp <span style="color:#{temp_color};">{temp:.1f}C</span>
            &nbsp;·&nbsp; Batt <span style="color:#e8edf2;">{batt}%</span>
            &nbsp;·&nbsp; {ts_raw} UTC
        </div>""", unsafe_allow_html=True)
    elif live2["total"] > 0:
        st.markdown(f"""<div style="background:rgba(74,96,112,.05);border:1px solid #182230;border-left:3px solid #4a6070;border-radius:0 10px 10px 0;padding:10px 16px;font-family:'Space Mono',monospace;font-size:10px;color:#4a6070;margin-bottom:14px;">
            {live2['total']} node{'s' if live2['total']!=1 else ''} registered · None online now ·
            <a href="https://portal.nexaedge.org?lang={st.session_state.lang}" target="_blank" style="color:#4a6070;">Activate yours -></a>
        </div>""", unsafe_allow_html=True)

    st.markdown(f'<div class="nx-notice">{L["sim_only"]}</div>', unsafe_allow_html=True)
    b_start, b_stop, col_status = st.columns([2,2,3])
    with b_start:
        if st.button(L["start_sim"], disabled=st.session_state.sim_running):
            st.session_state.sim_running=True; st.session_state.sim_tasks=0; st.session_state.sim_log=[]
            st.session_state.sim_nodes=[0]*64; st.session_state.nexa_earned=0.0; st.session_state.nexa_rate=0.0
            st.session_state.prog1=0; st.session_state.prog2=0; st.session_state.prog3=0; st.rerun()
    with b_stop:
        if st.button(L["stop_sim"], disabled=not st.session_state.sim_running, type="secondary"):
            st.session_state.sim_running=False; st.session_state.sim_nodes=[0]*64; st.rerun()
    with col_status:
        sc,st_txt = ("#ffb300",L["running"]) if st.session_state.sim_running else ("#4a6070",L["idle"])
        st.markdown(f'<div style="font-family:\'Space Mono\',monospace;font-size:10px;color:{sc};padding-top:12px;font-weight:700;">{st_txt}</div>', unsafe_allow_html=True)

    nodes = st.session_state.sim_nodes
    node_html = f'<div class="nx-card"><div class="nx-card-title"><span class="dot">></span> {L["node_grid_title"]}</div><div class="nx-node-grid">'
    for v in nodes:
        cls={0:"",1:" active",2:" processing"}.get(v,"")
        node_html += f'<div class="nx-node{cls}"></div>'
    node_html += f'</div><div class="nx-legend"><div class="nx-legend-item"><div class="nx-legend-dot" style="background:#182230;"></div>{L["idle_label"]}</div><div class="nx-legend-item" style="color:#a2ff00;"><div class="nx-legend-dot" style="background:#a2ff00;"></div>{L["active_label"]}</div><div class="nx-legend-item" style="color:#00e5ff;"><div class="nx-legend-dot" style="background:#00e5ff;"></div>{L["processing_label"]}</div></div></div>'
    st.markdown(node_html, unsafe_allow_html=True)

    active_count = sum(1 for v in nodes if v > 0)
    latency_val = f"{st.session_state.sim_latency:.1f}ms" if st.session_state.sim_running else "—"
    consensus_val = f"{st.session_state.sim_consensus:.1f}%" if st.session_state.sim_running else "—"
    nexa_val = f"{st.session_state.nexa_earned:.4f}" if (st.session_state.sim_running or st.session_state.nexa_earned>0) else "—"
    nexa_rate_val = f"{st.session_state.nexa_rate:.4f}" if st.session_state.sim_running else "—"

    s1,s2,s3,s4,s5,s6 = st.columns(6)
    for col,val,lbl,cls in [(s1,active_count,L["active_nodes"],""),(s2,st.session_state.sim_tasks,L["tasks_done"],""),(s3,latency_val,L["avg_latency"]," cyan"),(s4,consensus_val,L["bft_consensus"]," cyan"),(s5,nexa_val,L["nexa_earned"]," gold"),(s6,nexa_rate_val,L["nexa_per_task"]," gold")]:
        with col:
            st.markdown(f'<div class="nx-sim-stat"><div class="nx-sim-val{cls}">{val}</div><div class="nx-sim-label">{lbl}</div></div>', unsafe_allow_html=True)

    if st.session_state.sim_running or st.session_state.nexa_earned>0:
        usd_val = st.session_state.nexa_earned*0.50
        st.markdown('<div style="margin-top:14px;"></div>', unsafe_allow_html=True)
        n1,n2,n3 = st.columns(3)
        with n1: st.markdown(f'<div class="nx-nexa-mini"><div class="nx-nexa-mini-label">{L["nexa_sim_earned"]}</div><div class="nx-nexa-mini-val">{st.session_state.nexa_earned:.4f} NEXA</div></div>', unsafe_allow_html=True)
        with n2: st.markdown(f'<div class="nx-nexa-mini"><div class="nx-nexa-mini-label">{L["nexa_est_usd"]}</div><div class="nx-nexa-mini-val">${usd_val:.4f}</div></div>', unsafe_allow_html=True)
        with n3: st.markdown(f'<div class="nx-nexa-mini"><div class="nx-nexa-mini-label">{L["nexa_supply"]}</div><div class="nx-nexa-mini-val">100,000,000</div></div>', unsafe_allow_html=True)
        st.markdown(f'<div style="font-family:\'Space Mono\',monospace;font-size:9px;color:#2a3a4a;margin-top:10px;line-height:1.7;">{L["nexa_disclaimer"]}</div>', unsafe_allow_html=True)

    st.markdown(f'<div class="nx-card" style="margin-top:14px;"><div class="nx-card-title"><span class="dot">></span> {L["task_log_title"]}</div>', unsafe_allow_html=True)
    if st.session_state.sim_log:
        log_html='<div class="nx-log">'
        for line,cls in st.session_state.sim_log:
            log_html+=f'<div class="log-{cls}">{line}</div>'
        log_html+='</div>'
    else:
        log_html=f'<div class="nx-log"><div>{L["log_empty"]}</div></div>'
    st.markdown(log_html+'</div>', unsafe_allow_html=True)

    p1,p2,p3 = st.session_state.prog1,st.session_state.prog2,st.session_state.prog3
    st.markdown(f"""<div class="nx-card"><div class="nx-card-title"><span class="dot">></span> {L['workload_title']}</div>
    <div class="nx-prog-row"><span>{L['wl_inference']}</span><span style="color:#a2ff00;">{p1}%</span></div>
    <div class="nx-prog-bar"><div class="nx-prog-fill" style="width:{p1}%"></div></div>
    <div class="nx-prog-row"><span>{L['wl_rlhf']}</span><span style="color:#00e5ff;">{p2}%</span></div>
    <div class="nx-prog-bar"><div class="nx-prog-fill blue" style="width:{p2}%"></div></div>
    <div class="nx-prog-row"><span>{L['wl_zk']}</span><span style="color:#a2ff00;">{p3}%</span></div>
    <div class="nx-prog-bar"><div class="nx-prog-fill" style="width:{p3}%"></div></div></div>""", unsafe_allow_html=True)

# ══════════════════════════════════════
# TAB 3 — DIFFERENTIATION
# ══════════════════════════════════════
elif current_tab == L["nav"][2]:
    if st.session_state.lang=="EN":
        st.markdown(f"""<div class="nx-card"><div class="nx-card-title"><span class="dot">></span> {L['diff_title']}</div>
        <table class="nx-table"><thead><tr><th>Dimension</th><th>Grass</th><th class="hl">NexaEdge (Planned)</th></tr></thead><tbody>
        <tr><td>Core resource</td><td>Residential bandwidth</td><td class="hl">Device compute (CPU+NPU)</td></tr>
        <tr><td>Primary use</td><td>Web scraping</td><td class="hl">AI inference, RLHF, ZK-ML</td></tr>
        <tr><td>Sybil resistance</td><td><span class="tag-bad">HIGH RISK</span> VPN spoofed</td><td class="hl"><span class="tag-plan">PLANNED</span> HW fingerprint</td></tr>
        <tr><td>Compute verify</td><td>None</td><td class="hl"><span class="tag-plan">PLANNED</span> BFT + ZK proof</td></tr>
        <tr><td>Solana Mobile</td><td>None</td><td class="hl"><span class="tag-plan">PLANNED</span> Seeker/Saga</td></tr>
        </tbody></table></div>""", unsafe_allow_html=True)
    else:
        st.markdown(f"""<div class="nx-card"><div class="nx-card-title"><span class="dot">></span> {L['diff_title']}</div>
        <table class="nx-table"><thead><tr><th>维度</th><th>Grass</th><th class="hl">NexaEdge（计划中）</th></tr></thead><tbody>
        <tr><td>核心资源</td><td>住宅带宽</td><td class="hl">设备算力（CPU+NPU）</td></tr>
        <tr><td>主要用途</td><td>网页抓取</td><td class="hl">AI推理、RLHF、ZK-ML</td></tr>
        <tr><td>女巫抵抗</td><td><span class="tag-bad">高风险</span> VPN伪造</td><td class="hl"><span class="tag-plan">计划中</span> 硬件指纹</td></tr>
        <tr><td>算力验证</td><td>无</td><td class="hl"><span class="tag-plan">计划中</span> BFT + ZK证明</td></tr>
        <tr><td>Solana Mobile</td><td>无</td><td class="hl"><span class="tag-plan">计划中</span> Seeker/Saga</td></tr>
        </tbody></table></div>""", unsafe_allow_html=True)

    st.markdown(f'<div class="nx-card"><div class="nx-card-title"><span class="dot">></span> {L["moat_title"]}</div>', unsafe_allow_html=True)
    m1,m2=st.columns(2)
    if st.session_state.lang=="EN":
        with m1:
            st.markdown("""<div class="nx-moat"><div class="nx-moat-icon">🔐</div><div class="nx-moat-title">Proof of Compute (PoC) — Planned</div><div class="nx-moat-body">Every node will solve a cryptographic ML inference puzzle to claim rewards. HW fingerprint + ZK proof designed to prevent Sybil attacks.</div></div>
            <div class="nx-moat"><div class="nx-moat-icon">🌍</div><div class="nx-moat-title">Geographic Density — Design Thesis</div><div class="nx-moat-body">6.8B smartphones vs. a few thousand datacenters. NexaEdge is designed to reach markets no cloud can serve.</div></div>""", unsafe_allow_html=True)
        with m2:
            st.markdown("""<div class="nx-moat"><div class="nx-moat-icon">🧠</div><div class="nx-moat-title">NPU-Native Execution — Planned</div><div class="nx-moat-body">Modern smartphones (A-series, Snapdragon) have dedicated NPUs. The protocol targets these for SLM inference workloads.</div></div>
            <div class="nx-moat"><div class="nx-moat-icon">📱</div><div class="nx-moat-title">Solana Mobile Integration — Planned</div><div class="nx-moat-body">Solana Seeker/Saga are Web3-native phones. NexaEdge is designed to become a native node client on these devices.</div></div>""", unsafe_allow_html=True)
    else:
        with m1:
            st.markdown("""<div class="nx-moat"><div class="nx-moat-icon">🔐</div><div class="nx-moat-title">算力证明（PoC）— 计划中</div><div class="nx-moat-body">每个节点将通过加密ML推理难题领取奖励。设计上采用硬件指纹+ZK证明防止女巫攻击。</div></div>
            <div class="nx-moat"><div class="nx-moat-icon">🌍</div><div class="nx-moat-title">地理密度 — 设计论点</div><div class="nx-moat-body">68亿部智能手机对比数千个数据中心，协议设计覆盖任何云端无法服务的超本地场景。</div></div>""", unsafe_allow_html=True)
        with m2:
            st.markdown("""<div class="nx-moat"><div class="nx-moat-icon">🧠</div><div class="nx-moat-title">NPU原生执行 — 计划中</div><div class="nx-moat-body">现代智能手机（A系列、骁龙）配备专用NPU。协议针对这些硬件运行SLM推理工作负载。</div></div>
            <div class="nx-moat"><div class="nx-moat-icon">📱</div><div class="nx-moat-title">Solana Mobile集成 — 计划中</div><div class="nx-moat-body">NexaEdge 计划成为 Solana Seeker/Saga 设备上的原生节点客户端。</div></div>""", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    thermal_en="The 39C thermal ceiling is a planned daemon constraint in the protocol design. If device >= 39C task queue paused, passive cooling activated. Enforced at WASM sandbox level — not overridable by the user.<br><br><strong style='color:#d0d8e4;'>Design rationale:</strong> Institutional buyers require SLA guarantees. The 39C protocol is the planned supply-side durability guarantee — to be validated in hardware alpha."
    thermal_zh="39C 热限是协议设计中计划的守护进程约束。设备温度 >= 39C 任务队列暂停，激活被动散热模式。在 WASM 沙箱层面强制执行——用户不可覆盖。<br><br><strong style='color:#d0d8e4;'>设计依据：</strong>机构买家需要SLA保证。39C协议是计划中的供给侧耐久性保障——将在硬件 alpha 阶段验证。"
    st.markdown(f"""<div class="nx-card"><div class="nx-card-title"><span class="dot">></span> {L['thermal_title']}</div>
    <div style="font-size:12px;color:#4a6070;line-height:1.9;">{thermal_en if st.session_state.lang=="EN" else thermal_zh}</div></div>""", unsafe_allow_html=True)

# ══════════════════════════════════════
# TAB 4 — ROADMAP
# ══════════════════════════════════════
elif current_tab == L["nav"][3]:
    if st.session_state.lang=="EN":
        st.markdown(f"""<div class="nx-card"><div class="nx-card-title"><span class="dot">></span> {L['roadmap_title']}</div>
        <div class="nx-roadmap-item done"><div class="nx-roadmap-phase done">Q2 2026 · COMPLETE</div><div class="nx-roadmap-title">Concept Validation & Early Community</div><div class="nx-roadmap-body">Architecture finalized. Whitepaper live. Waitlist, node registration, heartbeat system, and task queue all deployed. Real data flowing into Supabase.</div></div>
        <div class="nx-roadmap-item current"><div class="nx-roadmap-phase">Q3 2026 · NOW — EARLY BETA</div><div class="nx-roadmap-title">Early Beta — Simulated Task Execution</div><div class="nx-roadmap-body">Task queue live. Node portal active. Heartbeat + simulated task execution running. iOS developer recruitment in progress for native app. Infrastructure validated.</div></div>
        <div class="nx-roadmap-item"><div class="nx-roadmap-phase">Q4 2026 · TARGET</div><div class="nx-roadmap-title">Closed Beta — 1,000 Nodes</div><div class="nx-roadmap-body">Native iOS/Android node client. Solana SPL token deployment. BFT testnet. First paying buyer pilot. ZK proof of compute live.</div></div>
        <div class="nx-roadmap-item"><div class="nx-roadmap-phase">Q1 2027 · TARGET</div><div class="nx-roadmap-title">Public Mainnet Launch</div><div class="nx-roadmap-body">Open enrollment. Solana Seeker integration. Marketplace live. Target: 100K active nodes, 3 enterprise buyers.</div></div>
        <div class="nx-roadmap-item" style="padding-bottom:0;"><div class="nx-roadmap-phase">2027+ · VISION</div><div class="nx-roadmap-title">Scale & Ecosystem</div><div class="nx-roadmap-body">ZK-ML verification live. Expand to laptop/IoT. Series A exploration.</div></div>
        </div>""", unsafe_allow_html=True)
    else:
        st.markdown(f"""<div class="nx-card"><div class="nx-card-title"><span class="dot">></span> {L['roadmap_title']}</div>
        <div class="nx-roadmap-item done"><div class="nx-roadmap-phase done">2026年Q2 · 已完成</div><div class="nx-roadmap-title">概念验证与早期社区</div><div class="nx-roadmap-body">架构定稿。白皮书上线。候补名单、节点注册、心跳系统和任务队列全部部署完成。真实数据写入 Supabase。</div></div>
        <div class="nx-roadmap-item current"><div class="nx-roadmap-phase">2026年Q3 · 当前 — 早期 Beta</div><div class="nx-roadmap-title">早期 Beta — 模拟任务执行</div><div class="nx-roadmap-body">任务队列上线。节点 Portal 运行中。心跳与模拟任务执行已验证。iOS 开发者招募中。</div></div>
        <div class="nx-roadmap-item"><div class="nx-roadmap-phase">2026年Q4 · 目标</div><div class="nx-roadmap-title">封闭测试——1,000 节点</div><div class="nx-roadmap-body">iOS/Android 原生节点客户端。Solana SPL 代币部署。BFT 测试网。首个付费买家试点。</div></div>
        <div class="nx-roadmap-item"><div class="nx-roadmap-phase">2027年Q1 · 目标</div><div class="nx-roadmap-title">公开主网上线</div><div class="nx-roadmap-body">开放节点注册。Solana Seeker 集成。市场上线。目标：10万活跃节点、3个企业买家。</div></div>
        <div class="nx-roadmap-item" style="padding-bottom:0;"><div class="nx-roadmap-phase">2027年+ · 愿景</div><div class="nx-roadmap-title">规模扩张与生态</div><div class="nx-roadmap-body">ZK-ML 验证上线。扩展至笔记本/IoT。探索 A 轮融资。</div></div>
        </div>""", unsafe_allow_html=True)

    r1,r2,r3=st.columns(3)
    if st.session_state.lang=="EN":
        with r1: st.metric("Beta Stage","Early Beta","Infrastructure live")
        with r2: st.metric("Target Nodes (Y1)","100K","at mainnet launch")
        with r3: st.metric("Settlement Chain","Solana SPL","low gas · high TPS")
    else:
        with r1: st.metric("当前阶段","早期 Beta","基础设施已上线")
        with r2: st.metric("目标节点数","100K","主网上线时")
        with r3: st.metric("结算链","Solana SPL","低gas·高TPS")

    st.markdown(f"""<div class="nx-card" style="margin-top:8px;border-color:rgba(255,179,0,.2);background:rgba(255,179,0,.02);">
    <div class="nx-card-title"><span style="color:#ffb300;">◈</span> {L['nexa_proj_title']}</div>
    <div style="font-size:11px;color:#4a6070;line-height:1.8;">{L['nexa_disclaimer']}</div></div>""", unsafe_allow_html=True)

# ══════════════════════════════════════
# TAB 5 — WAITLIST
# ══════════════════════════════════════
elif current_tab == L["nav"][4]:
    total_reg = db_count()
    wl_h1, wl_h2 = st.columns([3,1])
    with wl_h1:
        st.markdown(f"""<div style="margin-bottom:6px;">
        <div style="font-size:20px;font-weight:800;color:#e8edf2;margin-bottom:6px;">{L['wl_title']}</div>
        <div style="font-size:12px;color:#4a6070;line-height:1.7;">{L['wl_desc']}</div></div>""", unsafe_allow_html=True)
    with wl_h2:
        st.markdown(f"""<div style="background:#060b0f;border:1px solid #182230;border-radius:10px;padding:14px 18px;text-align:center;margin-top:4px;">
        <div style="font-family:'Space Mono',monospace;font-size:8px;color:#4a6070;text-transform:uppercase;letter-spacing:.1em;">{L['wl_total']}</div>
        <div style="font-family:'Space Mono',monospace;font-size:32px;font-weight:700;color:#a2ff00;line-height:1.1;">{total_reg}</div></div>""", unsafe_allow_html=True)

    st.markdown('<div style="margin-bottom:16px;"></div>', unsafe_allow_html=True)

    if st.session_state.wl_success:
        ref = st.session_state.wl_ref_code
        site_url = "https://nexaedge.org"

        if is_zh:
            share_text_only = f"加入 NexaEdge 候补名单 🟢\n将闲置手机算力变成分布式 AI 网络，赚取 NEXA 代币。\n推荐码：{ref}"
            share_msg       = f"{share_text_only}\n{site_url}"
            wa_msg          = f"加入 NexaEdge 候补名单 — 将闲置手机算力变成分布式 AI 网络。使用我的推荐码 {ref} . nexaedge.org"
        else:
            share_text_only = f"Join the NexaEdge waitlist 🟢\nDistributed edge AI on smartphones — earn NEXA tokens.\nReferral code: {ref}"
            share_msg       = f"{share_text_only}\n{site_url}"
        wa_msg = f"Join the NexaEdge waitlist — distributed edge AI on smartphones. Use my code {ref} . nexaedge.org"

        x_url  = "https://twitter.com/intent/tweet?url=" + urllib.parse.quote(site_url) + "&text=" + urllib.parse.quote(share_text_only)
        tg_url = "https://telegram.me/share/url?url=" + urllib.parse.quote(site_url) + "&text=" + urllib.parse.quote(share_msg)
        wa_url = "https://wa.me/?text=" + urllib.parse.quote(wa_msg)

        st.markdown(f"""<div class="nx-success-banner">
        <div style="font-size:20px;font-weight:800;color:#a2ff00;margin-bottom:6px;">{L['wl_success_title']}</div>
        <div style="font-size:12px;color:#4a6070;line-height:1.7;margin-bottom:20px;">{L['wl_success_desc']}</div>
        <div class="nx-ref-display"><div class="nx-ref-label">{L['wl_your_ref']}</div><div class="nx-ref-code">{ref}</div></div></div>""", unsafe_allow_html=True)

        portal_label = "Login to My Node Portal" if not is_zh else "登录节点控制台"
        portal_desc  = "See your queue position and activate your node heartbeat" if not is_zh else "查看队列排名、激活节点心跳"
        st.markdown(f"""<a href="https://portal.nexaedge.org?lang={st.session_state.lang}" target="_blank" style="display:block;background:rgba(162,255,0,.06);border:1px solid rgba(162,255,0,.25);border-radius:12px;padding:16px 20px;text-decoration:none;margin-bottom:14px;">
        <div style="font-family:'Space Mono',monospace;font-size:11px;font-weight:700;color:#a2ff00;margin-bottom:4px;">{portal_label}</div>
        <div style="font-size:11px;color:#4a6070;">{portal_desc}</div></a>""", unsafe_allow_html=True)

        # Share message preview
        share_label = "分享给朋友（含注册链接）" if is_zh else "Share with friends (includes signup link)"
        st.markdown(f"""
        <div style="display:flex;gap:8px;margin-bottom:8px;">
            <a href="{tg_url}" target="_blank" style="flex:1;text-align:center;padding:10px;
               background:#0d1720;border:1px solid #182230;border-radius:8px;
               color:#4a6070;text-decoration:none;font-family:'Space Mono',monospace;font-size:10px;">
               📢 Telegram
            </a>
            <a href="{wa_url}" target="_blank" style="flex:1;text-align:center;padding:10px;
               background:#0d1720;border:1px solid #182230;border-radius:8px;
               color:#4a6070;text-decoration:none;font-family:'Space Mono',monospace;font-size:10px;">
               💬 WhatsApp
            </a>
        </div>
        """, unsafe_allow_html=True)

        copy_label = "长按复制完整分享信息（X / WhatsApp）" if is_zh else "Tap & hold to copy full message (X / WhatsApp)"
        st.text_input(copy_label, value=share_msg, key="share_msg_copy", label_visibility="visible")

        cb1,cb2=st.columns(2)
        with cb1:
            if st.button(L["wl_copy"], key="copy_ref_btn"):
                st.components.v1.html(f'<script>navigator.clipboard.writeText("{share_msg}").catch(()=>{{}});</script>', height=0, width=0)
                st.toast(L["wl_copied"])
        with cb2:
            if st.button(L["wl_reset"], type="secondary", key="wl_reset_btn"):
                st.session_state.wl_success=False; st.session_state.wl_ref_code=''; st.rerun()
    else:
        already_label = "Already registered? Login to Node Portal ->" if not is_zh else "已注册？登录节点 Portal ->"
        st.markdown(f'<div style="text-align:right;margin-bottom:10px;"><a href="https://portal.nexaedge.org?lang={st.session_state.lang}" target="_blank" style="font-family:\'Space Mono\',monospace;font-size:10px;color:#a2ff00;text-decoration:none;">{already_label}</a></div>', unsafe_allow_html=True)
        st.markdown('<div class="nx-card">', unsafe_allow_html=True)
        with st.form("wl_form"):
            f1,f2=st.columns(2)
            with f1: email_in=st.text_input(L["wl_email"], placeholder=L["wl_email_ph"])
            with f2: ref_in=st.text_input(L["wl_ref"], placeholder=L["wl_ref_ph"])
            wallet_in=st.text_input(L["wl_wallet"], placeholder=L["wl_wallet_ph"])
            submitted=st.form_submit_button(L["wl_submit"])
            if submitted:
                errors=[]
                if not email_in or not re.match(r'^[^\s@]+@[^\s@]+\.[^\s@]+$', email_in):
                    errors.append(L["err_email"])
                if not wallet_in or not (32<=len(wallet_in)<=44):
                    errors.append(L["err_wallet"])
                if not errors and db_email_exists(email_in):
                    errors.append(L["err_dupe"])
                if errors:
                    for e in errors: st.error(e)
                else:
                    chars="ABCDEFGHJKLMNPQRSTUVWXYZ23456789"
                    ref_code="NX-"+"".join(random.choices(chars,k=6))
                    ok=db_insert(email_in, wallet_in, ref_code, ref_in, st.session_state.lang)
                    if ok:
                        st.session_state.wl_success=True; st.session_state.wl_ref_code=ref_code; st.rerun()
                    else:
                        st.error("Database error. Please try again." if st.session_state.lang=="EN" else "数据库错误，请重试。")
        st.markdown('</div>', unsafe_allow_html=True)
        disclaimer=("By registering, you confirm you understand this is an early beta. NEXA tokens are minted on Solana but not yet in public circulation. Wallet address is collected for future node airdrop eligibility only. No investment contract is formed by registering."
                    if st.session_state.lang=='EN' else
                    "注册即表明您了解这是早期 Beta 阶段。NEXA 代币已在 Solana 上铸造，但尚未公开流通。空投资格与分配比例将在主网上线时根据队列排名和推荐数量确定。注册不构成投资合同。")
        st.markdown(f'<div style="font-family:\'Space Mono\',monospace;font-size:9px;color:#2a3a4a;text-align:center;line-height:1.7;margin-top:10px;">{disclaimer}</div>', unsafe_allow_html=True)

    if total_reg > 0:
        regs = db_get_registrations()
        if regs:
            st.markdown(f'<div style="margin-top:24px;font-family:\'Space Mono\',monospace;font-size:10px;color:#4a6070;text-transform:uppercase;letter-spacing:.1em;margin-bottom:10px;">{L["ledger_title"]}</div>', unsafe_allow_html=True)
            ledger_rows=[{"Timestamp":r["created_at"][:19].replace("T"," "),"Node Hash":hashlib.sha256(r["email"].encode()).hexdigest()[:22]+"... @SPL"} for r in regs]
            st.dataframe(ledger_rows, use_container_width=True, hide_index=True)

# ══════════════════════════════════════
# TAB 6 — WHITEPAPER (Full 10 sections)
# ══════════════════════════════════════
elif current_tab in ["Whitepaper", "白皮书"]:
    is_zh = st.session_state.lang == "ZH"
    wp_cover_title = "技术白皮书 · V0.2 · 2026年Q3" if is_zh else "TECHNICAL WHITEPAPER · V0.2 · Q3 2026"
    wp_tagline = "将全球闲置智能手机算力汇聚成分布式边缘 AI 推理网络" if is_zh else "Aggregating Idle Smartphone Compute into a Distributed Edge AI Inference Network"
    wp_warn = "早期 Beta 阶段 · 非投资建议" if is_zh else "EARLY BETA · NOT AN INVESTMENT OFFER"

    st.markdown(f"""
<style>
.wp-cover{{background:linear-gradient(135deg,#0f172a,#1e293b);border-radius:14px;padding:40px 24px;text-align:center;margin-bottom:20px}}
.wp-dot{{font-size:36px;color:#22c55e;text-shadow:0 0 16px #22c55e;margin-bottom:12px}}
.wp-title{{font-family:'Syne',sans-serif;font-size:28px;font-weight:800;color:#e8edf2;margin-bottom:6px}}
.wp-title span{{color:#22c55e}}
.wp-sub{{font-family:'Space Mono',monospace;font-size:10px;color:#64748b;letter-spacing:.1em;margin-bottom:20px}}
.wp-tagline{{font-size:13px;color:#94a3b8;font-style:italic;margin-bottom:20px}}
.wp-warn{{display:inline-block;background:rgba(162,255,0,.1);border:1px solid rgba(162,255,0,.3);color:#a2ff00;font-family:'Space Mono',monospace;font-size:9px;padding:5px 12px;border-radius:6px;letter-spacing:.05em}}
.wp-stats{{display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin:20px 0}}
.wp-stat{{background:#f0fdf4;border:1px solid #bbf7d0;border-radius:10px;padding:14px 8px;text-align:center}}
.wp-stat-val{{font-family:'Space Mono',monospace;font-size:18px;font-weight:700;color:#16a34a;line-height:1.1}}
.wp-stat-lbl{{font-size:9px;color:#64748b;text-transform:uppercase;letter-spacing:.05em;margin-top:4px}}
.wp-section{{background:white;border:1px solid #e2e8f0;border-radius:12px;padding:24px;margin-bottom:14px}}
.wp-h2{{font-size:18px;font-weight:800;color:#0f172a;margin-bottom:4px;padding-bottom:8px;border-bottom:3px solid #22c55e;display:inline-block}}
.wp-h3{{font-size:13px;font-weight:700;color:#166534;margin:16px 0 6px}}
.wp-body{{font-size:12px;color:#475569;line-height:1.75;margin-bottom:10px}}
.wp-hl{{background:#f0fdf4;border-left:4px solid #22c55e;padding:12px 16px;border-radius:0 8px 8px 0;margin:12px 0;font-style:italic;color:#166534;font-size:12px}}
.wp-note{{background:#fffbeb;border-left:4px solid #f59e0b;padding:10px 14px;border-radius:0 8px 8px 0;margin:10px 0;font-size:11px;color:#92400e}}
.wp-table{{width:100%;border-collapse:collapse;font-size:11px;margin:12px 0}}
.wp-table th{{background:#0f172a;color:white;padding:8px 12px;text-align:left;font-family:'Space Mono',monospace;font-size:9px;text-transform:uppercase;letter-spacing:.05em}}
.wp-table th.g{{background:#166534}}
.wp-table td{{padding:8px 12px;border-bottom:1px solid #f1f5f9;color:#475569}}
.wp-table tr:last-child td{{border-bottom:none}}
.wp-table tr:nth-child(even) td{{background:#f8fafc}}
.wp-table td.hl{{color:#16a34a;font-weight:600}}
.wp-table td.dk{{color:#0f172a;font-weight:600}}
.wp-rm{{padding-left:24px;border-left:2px solid #e2e8f0;margin:12px 0}}
.wp-rm-item{{padding-bottom:20px;position:relative}}
.wp-rm-item::before{{content:'';position:absolute;left:-29px;top:5px;width:10px;height:10px;border-radius:50%;background:#e2e8f0}}
.wp-rm-item.done::before{{background:#22c55e;box-shadow:0 0 8px rgba(34,197,94,.5)}}
.wp-rm-item.now::before{{background:#a2ff00;box-shadow:0 0 8px rgba(162,255,0,.5)}}
.wp-rm-phase{{font-family:'Space Mono',monospace;font-size:10px;color:#f59e0b;text-transform:uppercase;letter-spacing:.06em;margin-bottom:3px}}
.wp-rm-phase.done{{color:#22c55e}}
.wp-rm-phase.active{{color:#a2ff00}}
.wp-rm-title{{font-size:14px;font-weight:700;color:#0f172a;margin-bottom:3px}}
.wp-rm-body{{font-size:11px;color:#64748b;line-height:1.6}}
</style>
<div class="wp-cover">
  <div class="wp-dot">●</div>
  <div class="wp-title">Nexa<span>Edge</span> Network</div>
  <div class="wp-sub">{wp_cover_title}</div>
  <div class="wp-tagline">{wp_tagline}</div>
  <div class="wp-warn">{wp_warn}</div>
  <div class="wp-stats">
    <div class="wp-stat"><div class="wp-stat-val">6.8B</div><div class="wp-stat-lbl">{'闲置手机' if is_zh else 'Idle Phones'}</div></div>
    <div class="wp-stat"><div class="wp-stat-val">$107B</div><div class="wp-stat-lbl">{'边缘AI 2028' if is_zh else 'Edge AI 2028'}</div></div>
    <div class="wp-stat"><div class="wp-stat-val">19.2%</div><div class="wp-stat-lbl">CAGR</div></div>
    <div class="wp-stat"><div class="wp-stat-val">100M</div><div class="wp-stat-lbl">{'NEXA 已铸造' if is_zh else 'NEXA Minted'}</div></div>
  </div>
</div>
    """, unsafe_allow_html=True)

    if is_zh:
        st.markdown("""
<div class="wp-section"><div class="wp-h2">1. 执行摘要</div><div class="wp-body" style="margin-top:12px">NexaEdge 是一个将闲置智能手机算力汇聚成无需许可的分布式边缘 AI 推理网络的协议设计。现代智能手机内置专用神经处理单元（NPU），每天有超过 95% 的时间处于闲置状态。NexaEdge 旨在利用这些潜在算力，以低于 5ms 的延迟、接近零边际成本提供 AI 推理服务，并原生支持 GDPR 合规。</div><div class="wp-hl">全球边缘 AI 市场预计到 2028 年将达到 1070 亿美元（CAGR 19.2%）。目前尚无协议能够在规模上聚合智能手机 NPU 算力。NexaEdge 的设计目标是成为第一个。</div><div class="wp-body">项目目前处于早期 Beta 阶段（2026年Q3）。候补名单、节点注册、心跳系统和任务队列已全部上线并验证。1亿枚 NEXA 代币已在 Solana 上铸造，但尚未公开流通。</div><div class="wp-note">本文件仅供资助委员会、加速器项目及合格投资人参考，不构成证券发行或投资合同。</div></div>
<div class="wp-section"><div class="wp-h2">2. 问题陈述</div><div class="wp-h3">2.1 边缘 AI 算力缺口</div><div class="wp-body">AI 推理需求增长速度已超过中心化 GPU 供给能力。H100 即时价格在每小时 $2-$4 之间波动。与此同时：</div><div class="wp-body">• 68亿部智能手机内置可运行 1.8B-3.8B 参数 SLM 的 NPU<br>• 这些设备每天有 12-20 小时处于闲置状态<br>• 它们分布在全球每个地区，紧邻终端用户<br>• 其算力完全未被更广泛的 AI 生态系统利用</div><div class="wp-h3">2.2 竞争格局</div><table class="wp-table"><tr><th></th><th>GPU 云</th><th>Grass.io</th><th class="g">NexaEdge（设计目标）</th></tr><tr><td class="dk">资本支出</td><td>极高</td><td>低</td><td class="hl">零</td></tr><tr><td class="dk">延迟</td><td>50-150ms</td><td>不适用</td><td class="hl">&lt;5ms 目标</td></tr><tr><td class="dk">隐私</td><td>数据离设备</td><td>部分</td><td class="hl">GDPR 原生</td></tr><tr><td class="dk">算力</td><td>仅GPU</td><td>仅网络</td><td class="hl">NPU + CPU</td></tr><tr><td class="dk">女巫抵抗</td><td>中心化认证</td><td>IP可伪造</td><td class="hl">硬件指纹+ZK</td></tr></table></div>
<div class="wp-section"><div class="wp-h2">3. NexaEdge 协议</div><div class="wp-hl">将每一部闲置智能手机变成经过验证的边缘计算节点，通过执行 AI 推理任务赚取 NEXA 代币。</div><div class="wp-h3">3.1 三层架构</div><table class="wp-table"><tr><th>层级</th><th>组件</th><th>功能</th></tr><tr><td class="dk">需求层</td><td>AI买家 API</td><td>提交任务，用 NEXA 支付</td></tr><tr><td class="dk">协调层</td><td>Solana SPL</td><td>BFT 共识、ZK 验证、奖励分发</td></tr><tr><td class="dk">供给层</td><td>设备节点</td><td>WASM 沙箱、NPU 执行、热保护</td></tr></table><div class="wp-h3">3.2 算力证明（PoC）</div><div class="wp-body">• 硬件指纹 — 设备专属、不可伪造的标识符<br>• ZK 推理证明 — 无需暴露模型权重即可验证<br>• BFT 交叉验证 — 需要最小法定数量的独立节点确认</div><div class="wp-h3">3.3 39°C 热保护协议</div><div class="wp-body">设备温度达到 39°C 时，任务队列自动暂停。在 WASM 沙箱层面强制执行——节点运营者不可覆盖。为机构买家提供 SLA 保证。</div></div>
<div class="wp-section"><div class="wp-h2">4. NEXA 代币模型</div><div class="wp-stats" style="margin-top:12px"><div class="wp-stat"><div class="wp-stat-val">1亿</div><div class="wp-stat-lbl">总供应量（固定）</div></div><div class="wp-stat"><div class="wp-stat-val" style="font-size:13px">Solana SPL</div><div class="wp-stat-lbl">区块链</div></div><div class="wp-stat"><div class="wp-stat-val">$0.50</div><div class="wp-stat-lbl">示意价格</div></div><div class="wp-stat"><div class="wp-stat-val" style="font-size:13px">2026年Q4</div><div class="wp-stat-lbl">目标分发</div></div></div><div class="wp-body" style="margin-top:12px">合约地址：<code style="background:#f1f5f9;padding:2px 5px;border-radius:3px;font-size:10px">D7h9MvFDkVxPYeJwSTcE7VkKXo6mygCHYph36P8oeic2</code></div><div class="wp-h3">计划分配（示意）</div><table class="wp-table"><tr><th>类别</th><th>分配比例</th><th>归属规则</th></tr><tr><td class="dk">节点运营者奖励</td><td class="hl">40%</td><td>按任务获得，无锁定期</td></tr><tr><td class="dk">生态系统与资助</td><td class="hl">20%</td><td>3年线性归属</td></tr><tr><td class="dk">团队与顾问</td><td class="hl">15%</td><td>1年锁定，3年归属</td></tr><tr><td class="dk">储备金</td><td class="hl">15%</td><td>DAO 控制，4年锁定</td></tr><tr><td class="dk">早期候补名单空投</td><td class="hl">10%</td><td>主网上线时快照</td></tr></table><div class="wp-note">代币分配仅供示意，可能调整。本内容不构成金融工具或投资要约。</div></div>
<div class="wp-section"><div class="wp-h2">5. 市场机会</div><div class="wp-stats" style="margin-top:12px"><div class="wp-stat"><div class="wp-stat-val">$107B</div><div class="wp-stat-lbl">边缘AI 2028</div></div><div class="wp-stat"><div class="wp-stat-val">$28B</div><div class="wp-stat-lbl">AI推理 2026</div></div><div class="wp-stat"><div class="wp-stat-val">68亿</div><div class="wp-stat-lbl">NPU手机</div></div><div class="wp-stat"><div class="wp-stat-val">19.2%</div><div class="wp-stat-lbl">CAGR</div></div></div><div class="wp-h3">目标买家细分</div><div class="wp-body"><b>边缘AI代理部署者</b> — 运行 1.8B-3.8B SLM，延迟低于 5ms，架构层面符合 GDPR。→ AI开发者、企业SaaS</div><div class="wp-body"><b>AI数据集清洗（RLHF）</b> — 分布式 WASM 沙箱在数千节点上同步运行自动标注。→ AI实验室、数据管道公司</div><div class="wp-body"><b>ZK-ML推理验证</b> — 无需中心化预言机的可信推理验证。→ DeFi协议、合规平台</div><div class="wp-body"><b>传感器上下文AI</b> — GPS、摄像头、IMU实现数据中心无法提供的上下文感知推理。→ 位置AI、自主系统</div></div>
<div class="wp-section"><div class="wp-h2">6. 开发路线图</div><div class="wp-rm" style="margin-top:16px"><div class="wp-rm-item done"><div class="wp-rm-phase done">2026年Q2 · 已完成</div><div class="wp-rm-title">概念验证与早期社区</div><div class="wp-rm-body">架构定稿。白皮书上线。候补名单、节点注册、心跳和任务队列全部部署。</div></div><div class="wp-rm-item now"><div class="wp-rm-phase active">2026年Q3 · 当前 — 早期 Beta</div><div class="wp-rm-title">早期 Beta — 模拟任务执行</div><div class="wp-rm-body">任务队列上线。节点 Portal 运行中。iOS 开发者招募中。</div></div><div class="wp-rm-item"><div class="wp-rm-phase">2026年Q4 · 目标</div><div class="wp-rm-title">封闭测试——1,000 节点</div><div class="wp-rm-body">iOS/Android 原生节点客户端。Solana SPL 部署。BFT 测试网。首个付费买家。</div></div><div class="wp-rm-item"><div class="wp-rm-phase">2027年Q1 · 目标</div><div class="wp-rm-title">公开主网上线</div><div class="wp-rm-body">开放注册。Solana Seeker 集成。目标：10万活跃节点。</div></div><div class="wp-rm-item"><div class="wp-rm-phase">2027年+ · 愿景</div><div class="wp-rm-title">规模扩张与生态</div><div class="wp-rm-body">ZK-ML 验证上线。扩展至笔记本/IoT。探索 A 轮融资。</div></div></div></div>
<div class="wp-section"><div class="wp-h2">7. 技术护城河</div><div class="wp-h3">NPU 原生执行</div><div class="wp-body">苹果 A17 Pro NPU：35 TOPS。高通骁龙 8 Gen 3：45 TOPS。NexaEdge 通过 WASM 运行时直接调用 Core ML（iOS）和 NNAPI（Android）。</div><div class="wp-h3">Solana Mobile 集成</div><div class="wp-body">Solana Seeker 和 Saga 具备硬件级密钥存储（Seed Vault）。NexaEdge 设计与这些设备原生集成，支持节点注册和设备端 NEXA 钱包管理。</div><div class="wp-h3">地理密度优势</div><div class="wp-body">68亿部智能手机遍布全球每个城市和农村地区——数据中心在结构上无法复制。随着边缘 AI 普及，贴近终端用户的地理优势将成为核心护城河。</div></div>
<div class="wp-section"><div class="wp-h2">8. 融资与资金用途</div><div class="wp-stats" style="margin-top:12px"><div class="wp-stat"><div class="wp-stat-val">$50万</div><div class="wp-stat-lbl">种子前目标</div></div><div class="wp-stat"><div class="wp-stat-val" style="font-size:14px">SAFE</div><div class="wp-stat-lbl">融资工具</div></div><div class="wp-stat"><div class="wp-stat-val" style="font-size:14px">2026年Q3</div><div class="wp-stat-lbl">目标完成</div></div><div class="wp-stat"><div class="wp-stat-val">50</div><div class="wp-stat-lbl">Alpha设备数</div></div></div><table class="wp-table" style="margin-top:12px"><tr><th>类别</th><th>金额</th><th>占比</th></tr><tr><td class="dk">WASM 运行时开发</td><td>$20万</td><td class="hl">40%</td></tr><tr><td class="dk">节点运营者激励</td><td>$10万</td><td class="hl">20%</td></tr><tr><td class="dk">Solana 集成与智能合约</td><td>$10万</td><td class="hl">20%</td></tr><tr><td class="dk">法律与合规</td><td>$5万</td><td class="hl">10%</td></tr><tr><td class="dk">市场营销与社区建设</td><td>$5万</td><td class="hl">10%</td></tr></table><div class="wp-body" style="margin-top:10px">联系方式：<a href="mailto:contact@nexaedge.org" style="color:#16a34a">contact@nexaedge.org</a></div><div class="wp-note">目前尚未签署任何 SAFE 或投资合同。所有承诺须经正式尽职调查后方可生效。</div></div>
<div class="wp-section"><div class="wp-h2">9. 风险因素</div><div class="wp-h3">技术风险</div><div class="wp-body">移动 NPU 上的 WASM 运行时性能在规模上尚未经过验证。设备端 SLM 推理延迟可能高于预期。</div><div class="wp-h3">监管风险</div><div class="wp-body">加密货币代币分发受各司法管辖区不断演变的证券法规约束。NEXA 代币分类可能需要在公开分发前进行法律重构。</div><div class="wp-h3">采用风险</div><div class="wp-body">节点运营者获取需要足够的 NEXA 奖励率。AI 买家获取需要在企业承诺前展示可靠性和 SLA 合规性。</div><div class="wp-h3">竞争风险</div><div class="wp-body">Akash、Render、io.net 等资金充裕的协议可能转向移动算力。苹果和谷歌可能在未来 OS 更新中限制移动端 WASM 执行。</div><div class="wp-hl">NexaEdge 处于早期 Beta 阶段。所有预测、时间表和技术主张均为设计目标，不构成保证。</div></div>
<div class="wp-section"><div class="wp-h2">10. 法律免责声明</div><div class="wp-body">本白皮书仅供参考。不构成招股说明书、出售要约或购买任何证券或金融工具的邀请。NEXA 代币是设计用于 NexaEdge 协议内部的功能代币，尚未在任何司法管辖区依据证券法进行注册。所有前瞻性陈述均基于当前设计意图，可能随时更改。加入候补名单不产生任何法律权利或代币、股权、金融工具的权益。</div><div style="margin-top:16px;font-family:'Space Mono',monospace;font-size:9px;color:#94a3b8;text-align:center;line-height:2">contact@nexaedge.org · @nexaedge_ · t.me/NexaEdge7<br>© 2026 NexaEdge Network. 保留所有权利。</div></div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
<div class="wp-section"><div class="wp-h2">1. Executive Summary</div><div class="wp-body" style="margin-top:12px">NexaEdge is a protocol design to aggregate idle smartphone compute into a permissionless, distributed edge AI inference network. Modern smartphones contain dedicated Neural Processing Units (NPUs) that sit idle for 95%+ of the day. NexaEdge proposes to harness this latent compute to serve AI inference tasks at sub-5ms latency, at near-zero marginal cost, with native GDPR compliance.</div><div class="wp-hl">The global edge AI market is projected to reach $107B by 2028 (CAGR 19.2%). Today, no protocol exists that aggregates smartphone NPU compute at scale. NexaEdge is designed to be the first.</div><div class="wp-body">The project is at Early Beta stage (Q3 2026). Waitlist, node registration, heartbeat system, and task queue are all live and validated. 100,000,000 NEXA tokens have been minted on Solana but are not yet in public circulation.</div><div class="wp-note">This document is for grant committees, accelerators, and accredited investors only. It does not constitute a securities offering or investment contract.</div></div>
<div class="wp-section"><div class="wp-h2">2. The Problem</div><div class="wp-h3">2.1 The Edge AI Compute Gap</div><div class="wp-body">AI inference demand is growing faster than centralized GPU supply. H100 spot prices fluctuate between $2-4/hour. Meanwhile:</div><div class="wp-body">• 6.8 billion smartphones contain NPUs capable of running 1.8B-3.8B parameter SLMs<br>• These devices are idle for 12-20 hours per day<br>• They are distributed across every geography, close to end users<br>• Their compute goes entirely unused by the broader AI ecosystem</div><div class="wp-h3">2.2 Competitive Landscape</div><table class="wp-table"><tr><th></th><th>GPU Cloud</th><th>Grass.io</th><th class="g">NexaEdge (Design)</th></tr><tr><td class="dk">CapEx</td><td>Extreme</td><td>Low</td><td class="hl">Zero</td></tr><tr><td class="dk">Latency</td><td>50-150ms</td><td>N/A</td><td class="hl">&lt;5ms target</td></tr><tr><td class="dk">Privacy</td><td>Data leaves</td><td>Partial</td><td class="hl">GDPR-native</td></tr><tr><td class="dk">Compute</td><td>GPU only</td><td>Network only</td><td class="hl">NPU + CPU</td></tr><tr><td class="dk">Sybil Resist.</td><td>Central auth</td><td>IP spoofable</td><td class="hl">HW fingerprint+ZK</td></tr></table></div>
<div class="wp-section"><div class="wp-h2">3. The NexaEdge Protocol</div><div class="wp-hl">Turn every idle smartphone into a verified edge compute node that earns NEXA tokens for executing AI inference tasks.</div><div class="wp-h3">3.1 Three-Layer Architecture</div><table class="wp-table"><tr><th>Layer</th><th>Component</th><th>Function</th></tr><tr><td class="dk">Demand</td><td>AI Buyers API</td><td>Submit tasks, pay in NEXA</td></tr><tr><td class="dk">Coordination</td><td>Solana SPL</td><td>BFT consensus, ZK verification, rewards</td></tr><tr><td class="dk">Supply</td><td>Device Nodes</td><td>WASM sandbox, NPU execution, thermal guard</td></tr></table><div class="wp-h3">3.2 Proof of Compute (PoC)</div><div class="wp-body">• Hardware fingerprint — device-specific, non-spoofable identifier<br>• ZK proof of inference — verifiable without revealing model weights<br>• BFT cross-validation — minimum quorum of independent nodes required</div><div class="wp-h3">3.3 39C Thermal Protocol</div><div class="wp-body">If device temperature reaches 39C, the task queue pauses automatically. Enforced at WASM sandbox level — not overridable by node operators. Enables institutional SLA guarantees.</div></div>
<div class="wp-section"><div class="wp-h2">4. NEXA Token Model</div><div class="wp-stats" style="margin-top:12px"><div class="wp-stat"><div class="wp-stat-val">100M</div><div class="wp-stat-lbl">Supply (Fixed)</div></div><div class="wp-stat"><div class="wp-stat-val" style="font-size:13px">Solana SPL</div><div class="wp-stat-lbl">Blockchain</div></div><div class="wp-stat"><div class="wp-stat-val">$0.50</div><div class="wp-stat-lbl">Illustrative</div></div><div class="wp-stat"><div class="wp-stat-val" style="font-size:13px">Q4 2026</div><div class="wp-stat-lbl">Distribution</div></div></div><div class="wp-body" style="margin-top:12px">Contract: <code style="background:#f1f5f9;padding:2px 5px;border-radius:3px;font-size:10px">D7h9MvFDkVxPYeJwSTcE7VkKXo6mygCHYph36P8oeic2</code></div><div class="wp-h3">Planned Allocation (Illustrative)</div><table class="wp-table"><tr><th>Category</th><th>Allocation</th><th>Vesting</th></tr><tr><td class="dk">Node Operator Rewards</td><td class="hl">40%</td><td>Earned per task</td></tr><tr><td class="dk">Ecosystem & Grants</td><td class="hl">20%</td><td>3-year linear vest</td></tr><tr><td class="dk">Team & Advisors</td><td class="hl">15%</td><td>1-year cliff, 3-year vest</td></tr><tr><td class="dk">Reserve</td><td class="hl">15%</td><td>DAO-controlled, 4-year lock</td></tr><tr><td class="dk">Early Waitlist Airdrop</td><td class="hl">10%</td><td>Snapshot at mainnet launch</td></tr></table><div class="wp-note">Token allocation is illustrative. This is not a financial instrument or investment offer.</div></div>
<div class="wp-section"><div class="wp-h2">5. Market Opportunity</div><div class="wp-stats" style="margin-top:12px"><div class="wp-stat"><div class="wp-stat-val">$107B</div><div class="wp-stat-lbl">Edge AI 2028</div></div><div class="wp-stat"><div class="wp-stat-val">$28B</div><div class="wp-stat-lbl">Inference 2026</div></div><div class="wp-stat"><div class="wp-stat-val">6.8B</div><div class="wp-stat-lbl">NPU Phones</div></div><div class="wp-stat"><div class="wp-stat-val">19.2%</div><div class="wp-stat-lbl">CAGR</div></div></div><div class="wp-h3">Target Buyer Segments</div><div class="wp-body"><b>Edge AI Agent Deployers</b> — Run 1.8B-3.8B SLMs with sub-5ms local inference. GDPR compliant by architecture. → AI developers, enterprise SaaS</div><div class="wp-body"><b>AI Dataset Cleaning (RLHF)</b> — Distributed WASM sandbox runs automated labeling across thousands of nodes simultaneously. → AI labs, data pipeline companies</div><div class="wp-body"><b>ZK-ML Inference Verification</b> — Trustless inference verification without centralized oracles. → DeFi protocols, compliance platforms</div><div class="wp-body"><b>Sensor-Context AI</b> — GPS, camera, IMU enable tasks structurally impossible in datacenters. → Location AI, autonomous systems</div></div>
<div class="wp-section"><div class="wp-h2">6. Development Roadmap</div><div class="wp-rm" style="margin-top:16px"><div class="wp-rm-item done"><div class="wp-rm-phase done">Q2 2026 · COMPLETE</div><div class="wp-rm-title">Concept Validation & Early Community</div><div class="wp-rm-body">Architecture finalized. Whitepaper live. Waitlist, node registration, heartbeat, and task queue all deployed. Real data flowing into Supabase.</div></div><div class="wp-rm-item now"><div class="wp-rm-phase active">Q3 2026 · NOW — EARLY BETA</div><div class="wp-rm-title">Early Beta — Simulated Task Execution</div><div class="wp-rm-body">Task queue live. Node portal active. Heartbeat and simulated task execution running. iOS developer recruitment in progress.</div></div><div class="wp-rm-item"><div class="wp-rm-phase">Q4 2026 · TARGET</div><div class="wp-rm-title">Closed Beta — 1,000 Nodes</div><div class="wp-rm-body">Native iOS/Android node client. Solana SPL deployment. BFT testnet. First paying buyer pilot. ZK proof of compute live.</div></div><div class="wp-rm-item"><div class="wp-rm-phase">Q1 2027 · TARGET</div><div class="wp-rm-title">Public Mainnet Launch</div><div class="wp-rm-body">Open enrollment. Solana Seeker integration. Marketplace live. Target: 100K active nodes, 3 enterprise buyers.</div></div><div class="wp-rm-item"><div class="wp-rm-phase">2027+ · VISION</div><div class="wp-rm-title">Scale & Ecosystem</div><div class="wp-rm-body">ZK-ML verification live. Expand to laptop/IoT. Series A exploration.</div></div></div></div>
<div class="wp-section"><div class="wp-h2">7. Technical Moat</div><div class="wp-h3">NPU-Native Execution</div><div class="wp-body">Apple A17 Pro NPU: 35 TOPS. Qualcomm Snapdragon 8 Gen 3: 45 TOPS. NexaEdge targets these directly via Core ML (iOS) and NNAPI (Android) through the WASM runtime.</div><div class="wp-h3">Solana Mobile Integration</div><div class="wp-body">Solana Seeker and Saga feature hardware-level key storage (Seed Vault). NexaEdge is designed to integrate natively for seamless node enrollment and on-device NEXA wallet management.</div><div class="wp-h3">Geographic Density Advantage</div><div class="wp-body">6.8 billion smartphones in every city and rural area on Earth — structurally impossible to replicate with datacenters. Proximity to end users becomes a competitive moat as edge AI adoption grows.</div></div>
<div class="wp-section"><div class="wp-h2">8. Funding & Use of Proceeds</div><div class="wp-stats" style="margin-top:12px"><div class="wp-stat"><div class="wp-stat-val">$500K</div><div class="wp-stat-lbl">Pre-Seed Target</div></div><div class="wp-stat"><div class="wp-stat-val" style="font-size:14px">SAFE</div><div class="wp-stat-lbl">Instrument</div></div><div class="wp-stat"><div class="wp-stat-val" style="font-size:14px">Q3 2026</div><div class="wp-stat-lbl">Target Close</div></div><div class="wp-stat"><div class="wp-stat-val">50</div><div class="wp-stat-lbl">Alpha Devices</div></div></div><table class="wp-table" style="margin-top:12px"><tr><th>Category</th><th>Amount</th><th>%</th></tr><tr><td class="dk">WASM Runtime Development</td><td>$200K</td><td class="hl">40%</td></tr><tr><td class="dk">Node Operator Incentives</td><td>$100K</td><td class="hl">20%</td></tr><tr><td class="dk">Solana Integration</td><td>$100K</td><td class="hl">20%</td></tr><tr><td class="dk">Legal & Compliance</td><td>$50K</td><td class="hl">10%</td></tr><tr><td class="dk">Marketing & Community</td><td>$50K</td><td class="hl">10%</td></tr></table><div class="wp-body" style="margin-top:10px">Contact: <a href="mailto:contact@nexaedge.org" style="color:#16a34a">contact@nexaedge.org</a></div><div class="wp-note">No SAFE or investment contract has been formed. All commitments subject to formal due diligence.</div></div>
<div class="wp-section"><div class="wp-h2">9. Risk Factors</div><div class="wp-h3">Technical Risk</div><div class="wp-body">WASM runtime performance on mobile NPUs is unproven at scale. SLM inference may exhibit higher latency than projected.</div><div class="wp-h3">Regulatory Risk</div><div class="wp-body">Token distribution is subject to evolving securities law. NEXA classification may require legal restructuring before public distribution.</div><div class="wp-h3">Adoption Risk</div><div class="wp-body">Node operator acquisition requires sufficient NEXA reward rates. AI buyer acquisition requires demonstrated SLA compliance.</div><div class="wp-h3">Competition Risk</div><div class="wp-body">Akash, Render, io.net may pivot to mobile compute. Apple/Google may restrict WASM on mobile in future OS updates.</div><div class="wp-hl">NexaEdge is at Early Beta stage. All projections and technical claims are design targets, not guarantees.</div></div>
<div class="wp-section"><div class="wp-h2">10. Legal Disclaimer</div><div class="wp-body">This whitepaper is for informational purposes only. It does not constitute a prospectus, an offer to sell, or a solicitation to purchase any securities or financial instruments. NEXA tokens are utility tokens for use within the NexaEdge protocol. They have not been registered under the securities laws of any jurisdiction. All forward-looking statements are subject to change. Participation in the waitlist does not create any legal right or entitlement to tokens, equity, or financial instruments.</div><div style="margin-top:16px;font-family:'Space Mono',monospace;font-size:9px;color:#94a3b8;text-align:center;line-height:2">contact@nexaedge.org · @nexaedge_ · t.me/NexaEdge7<br>© 2026 NexaEdge Network. All rights reserved.</div></div>
        """, unsafe_allow_html=True)

st.markdown("""<div class="nx-footer">
NexaEdge Network &nbsp;·&nbsp; Early Beta · Q3 2026 &nbsp;·&nbsp; Infrastructure live · Simulated task execution · iOS app in development<br>
NEXA minted on Solana · Not yet in public circulation &nbsp;·&nbsp; No investment contract formed &nbsp;·&nbsp; contact@nexaedge.org<br>
© 2026 NexaEdge Network. All rights reserved.
</div>""", unsafe_allow_html=True)

