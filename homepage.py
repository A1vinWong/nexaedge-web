import streamlit as st
import time
import random
import re
import hashlib
from streamlit_autorefresh import st_autorefresh
from supabase import create_client, Client

st.set_page_config(
    page_title="NexaEdge Network — Investor Demo",
    page_icon="🟢",
    layout="centered"
)

# ══════════════════════════════════════
# Supabase 连接
# ══════════════════════════════════════
SUPABASE_URL = "https://nfafzigmcdybgbxdtymf.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im5mYWZ6aWdtY2R5YmdieGR0eW1mIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODA5ODE3NTMsImV4cCI6MjA5NjU1Nzc1M30.ZIX3sByZ8yQSDGFr-o24CjIXwZ5UsB4rMB3jculLtv0"

@st.cache_resource
def get_supabase() -> Client:
    return create_client(SUPABASE_URL, SUPABASE_KEY)

supabase = get_supabase()

def db_count():
    try:
        res = supabase.table("whitelist").select("id", count="exact").execute()
        return res.count or 0
    except:
        return 0

def db_email_exists(email):
    try:
        res = supabase.table("whitelist").select("id").eq("email", email.lower()).execute()
        return len(res.data) > 0
    except:
        return False

def db_insert(email, wallet, ref_code, used_ref, lang):
    try:
        supabase.table("whitelist").insert({
            "email": email.lower(),
            "wallet": wallet,
            "ref_code": ref_code,
            "used_ref": used_ref or None,
            "referred_by": used_ref or None,
            "invitation_code": ref_code,
            "lang": lang,
        }).execute()
        return True
    except:
        return False

def db_get_registrations():
    try:
        res = supabase.table("whitelist").select("*").order("created_at", desc=False).execute()
        return res.data or []
    except:
        return []

# ══════════════════════════════════════
# 语言配置
# ══════════════════════════════════════
LANGS = {
    "EN": {
        "nav": ["Market", "Network Sim", "Differentiation", "Roadmap", "Whitelist"],
        "tagline": "Aggregating idle smartphone compute into a distributed edge AI inference network — turning personal devices into institutional-grade infrastructure.",
        "stage": "⚠ PRE-LAUNCH · ARCHITECTURE DEMO",
        "sim_only": "⚠ CONCEPT SIMULATION — All metrics are scaling projections, not performance guarantees.",
        "start_sim": "▶ Start Simulation",
        "stop_sim": "■ Stop",
        "running": "● LIVE TELEMETRY ACTIVE",
        "idle": "○ STANDBY",
        "online_now": "🟢 Nodes Online",
        "total_sessions": "Registered",
        "active_nodes": "Active Nodes",
        "tasks_done": "Tasks Done",
        "avg_latency": "Avg Latency",
        "bft_consensus": "Consensus",
        "nexa_earned": "NEXA Earned",
        "nexa_per_task": "NEXA/Task",
        "nexa_proj_title": "NEXA Token Projection",
        "nexa_sim_earned": "Simulated Yield",
        "nexa_est_usd": "Est. USD (@ $0.50)",
        "nexa_supply": "Total Supply",
        "nexa_disclaimer": "⚠ Illustrative only. NEXA reward ~0.0012–0.0038/task based on $50M projected market cap, 100M supply, $0.50 est. price. Actual rates at mainnet.",
        "node_grid_title": "Node Matrix — 64 Simulated Devices",
        "task_log_title": "Task Dispatch Log",
        "log_empty": "// Press ▶ Start to begin.",
        "workload_title": "Compute Pipeline Capacity",
        "wl_inference": "Edge AI Inference (SLM 1.8B / WASM)",
        "wl_rlhf": "Dataset Validation (RLHF)",
        "wl_zk": "ZK Proof Generation",
        "comp_title": "Competitive Positioning",
        "buyer_title": "Who Pays — Buyer Segments",
        "arch_title": "System Architecture",
        "diff_title": "NexaEdge vs. Bandwidth Proxies",
        "moat_title": "Technical Moat",
        "thermal_title": "Hardware Safety — 39°C Thermal Protocol",
        "roadmap_title": "Development Roadmap",
        "wl_title": "Join the Genesis Whitelist",
        "wl_desc": "Register early — lock your node slot before mainnet launch.",
        "wl_email": "Email Address",
        "wl_email_ph": "you@example.com",
        "wl_wallet": "Solana Wallet (SPL)",
        "wl_wallet_ph": "32–44 char public key (e.g. 7xKp...)",
        "wl_ref": "Referral Code (Optional)",
        "wl_ref_ph": "Enter a friend's referral code",
        "wl_submit": "Register for Whitelist",
        "wl_success_title": "✅ Registration Successful!",
        "wl_success_desc": "You're on the NexaEdge whitelist. Share your referral code to earn bonus NEXA at launch.",
        "wl_your_ref": "Your Referral Code",
        "wl_copy": "📋 Copy to Clipboard",
        "wl_copied": "✅ Copied!",
        "wl_reset": "🔄 Register Another Node",
        "wl_total": "Total Registered",
        "err_email": "Please enter a valid email address.",
        "err_wallet": "Solana wallet must be 32–44 characters.",
        "err_dupe": "This email is already registered.",
        "idle_label": "Idle", "active_label": "Active", "processing_label": "Processing",
        "demand_side": "Demand Layer", "coordination": "Settlement Layer", "supply_side": "Supply Cluster",
        "lang_btn": "中文",
        "ledger_title": "🛡️ Genesis Ledger — Registered Nodes",
        "invest_title": "Institutional Seed Round Gateway",
        "invest_desc": "NexaEdge Seed round processed via AngelList Rollups (Post-money SAFE). Institutional allocators may lock intent directly.",
        "invest_btn": "💼 Soft-Circle Allocation",
        "invest_warn": "AngelList compliance audit in progress. Submit via Whitelist or email contact@nexaedge.org.",
    },
    "ZH": {
        "nav": ["核心市场", "网络模拟", "差异化优势", "路线图", "白名单注册"],
        "tagline": "将闲置智能手机算力汇聚成分布式边缘 AI 推理网络——让个人设备变身机构级基础设施。",
        "stage": "⚠ 预发布 · 架构及融资演示",
        "sim_only": "⚠ 概念模拟演示——所有指标均为示意性预测，非性能保证。",
        "start_sim": "▶ 启动模拟网络",
        "stop_sim": "■ 停止",
        "running": "● 实时遥测已激活",
        "idle": "○ 待机中",
        "online_now": "🟢 在线节点",
        "total_sessions": "已注册",
        "active_nodes": "活跃节点",
        "tasks_done": "完成任务",
        "avg_latency": "平均延迟",
        "bft_consensus": "BFT 共识",
        "nexa_earned": "已赚 NEXA",
        "nexa_per_task": "NEXA/任务",
        "nexa_proj_title": "NEXA 代币预测",
        "nexa_sim_earned": "模拟产出",
        "nexa_est_usd": "估值 (@ $0.50)",
        "nexa_supply": "总供应量",
        "nexa_disclaimer": "⚠ 仅供参考。每任务约 0.0012–0.0038 NEXA，基于 1 亿总供应量、5000 万美元预计市值、$0.50 发行价估算。实际比率以主网为准。",
        "node_grid_title": "节点矩阵 — 64 个模拟设备",
        "task_log_title": "任务调度日志",
        "log_empty": "// 点击 ▶ 启动模拟网络以开始。",
        "workload_title": "算力管道负载",
        "wl_inference": "边缘 AI 推理 (SLM 1.8B / WASM)",
        "wl_rlhf": "数据集验证 (RLHF)",
        "wl_zk": "ZK 证明生成",
        "comp_title": "竞争定位",
        "buyer_title": "买家细分",
        "arch_title": "系统架构",
        "diff_title": "NexaEdge vs 带宽代理网络",
        "moat_title": "技术护城河",
        "thermal_title": "硬件安全 — 39°C 热保护协议",
        "roadmap_title": "开发路线图",
        "wl_title": "加入创世白名单",
        "wl_desc": "提前注册——在主网上线前锁定您的节点位置。",
        "wl_email": "电子邮件",
        "wl_email_ph": "your@email.com",
        "wl_wallet": "Solana 钱包 (SPL)",
        "wl_wallet_ph": "32–44 位公钥（如 7xKp...）",
        "wl_ref": "推荐码（可选）",
        "wl_ref_ph": "输入朋友的推荐码",
        "wl_submit": "提交白名单注册",
        "wl_success_title": "✅ 注册成功！",
        "wl_success_desc": "您已加入 NexaEdge 白名单。分享推荐码，在主网上线时获得额外 NEXA 奖励。",
        "wl_your_ref": "您的推荐码",
        "wl_copy": "📋 复制",
        "wl_copied": "✅ 已复制！",
        "wl_reset": "🔄 注册另一个节点",
        "wl_total": "已注册总数",
        "err_email": "请输入有效的电子邮件地址。",
        "err_wallet": "Solana 钱包地址应为 32–44 个字符。",
        "err_dupe": "此邮箱已注册。",
        "idle_label": "空闲", "active_label": "活跃", "processing_label": "处理中",
        "demand_side": "需求方", "coordination": "协调层", "supply_side": "供给方",
        "lang_btn": "English",
        "ledger_title": "🛡️ 创世账本 — 已注册节点",
        "invest_title": "机构种子轮投资入口",
        "invest_desc": "NexaEdge 种子轮通过 AngelList Rollups（Post-money SAFE）架构处理。合格机构可直接锁定意向额度。",
        "invest_btn": "💼 意向锁定",
        "invest_warn": "合规审核处理中。请通过白名单提交或联系 contact@nexaedge.org。",
    }
}

TASK_TYPES_EN = [
    ("SLM inference (Phi-3 mini / WASM)", "success"),
    ("RLHF label validation chunk", "info"),
    ("ZK proof chunk verification", "success"),
    ("BFT consensus cluster vote", "info"),
    ("Thermal check: OK ✓", "success"),
    ("Node fingerprint SHA256 verified", "success"),
]
TASK_TYPES_ZH = [
    ("SLM 推理任务执行 (Phi-3 mini / WASM)", "success"),
    ("RLHF 数据标签交叉验证", "info"),
    ("ZK 证明片段生成与校验", "success"),
    ("BFT 共识层节点签名投票", "info"),
    ("本机热指标检查: 正常 ✓", "success"),
    ("节点硬件指纹哈希校验成功", "success"),
]

REWARD_BASE = 0.0022

# ══════════════════════════════════════
# CSS
# ══════════════════════════════════════
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
.nx-online-badge{display:inline-flex;align-items:center;gap:10px;background:#060b0f;border:1px solid #182230;border-radius:8px;padding:7px 14px;font-family:'Space Mono',monospace;font-size:10px;color:#00e5ff;margin-top:8px}
.nx-pulse{width:6px;height:6px;background:#00e5ff;border-radius:50%;animation:pulse-anim 2s ease-in-out infinite}
@keyframes pulse-anim{0%,100%{box-shadow:0 0 0 0 rgba(0,229,255,.4)}50%{box-shadow:0 0 0 5px rgba(0,229,255,0)}}
.nx-stage-badge{display:inline-block;background:rgba(0,229,255,.07);border:1px solid rgba(0,229,255,.2);color:#00e5ff;font-family:'Space Mono',monospace;font-size:9px;font-weight:700;padding:5px 12px;border-radius:6px;letter-spacing:.1em}
.nx-feature{background:#060b0f;border:1px solid #182230;border-left:3px solid #a2ff00;border-radius:0 10px 10px 0;padding:16px 18px;margin-bottom:12px}
.nx-feature-title{font-size:13px;font-weight:700;color:#e8edf2;margin-bottom:6px}
.nx-feature-body{font-size:11px;color:#4a6070;line-height:1.7}
.nx-feature-buyer{margin-top:8px;font-family:'Space Mono',monospace;font-size:10px;color:#00e5ff}
.tag-bad{display:inline-block;background:rgba(244,63,94,.12);color:#f43f5e;font-family:'Space Mono',monospace;font-size:9px;padding:2px 7px;border-radius:4px;font-weight:700}
.tag-good{display:inline-block;background:rgba(162,255,0,.1);color:#a2ff00;font-family:'Space Mono',monospace;font-size:9px;padding:2px 7px;border-radius:4px;font-weight:700}
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
.nx-roadmap-item.current::before{background:#00e5ff;border-color:#00e5ff;box-shadow:0 0 10px rgba(0,229,255,.5)}
.nx-roadmap-phase{font-family:'Space Mono',monospace;font-size:9px;color:#ffb300;text-transform:uppercase;letter-spacing:.1em;margin-bottom:5px}
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

# ══════════════════════════════════════
# Session State
# ══════════════════════════════════════
_defaults = {
    'lang': 'EN',
    'sim_running': False, 'sim_tasks': 0, 'sim_log': [],
    'sim_nodes': [0]*64, 'sim_latency': 3.0, 'sim_consensus': 98.2,
    'prog1': 0, 'prog2': 0, 'prog3': 0,
    'nexa_earned': 0.0, 'nexa_rate': 0.0,
    'wl_success': False, 'wl_ref_code': '',
}
for k, v in _defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

L = LANGS[st.session_state.lang]
TASK_TYPES = TASK_TYPES_EN if st.session_state.lang == "EN" else TASK_TYPES_ZH

# ══════════════════════════════════════
# Sim engine
# ══════════════════════════════════════
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
    st.session_state.sim_log.append((f"[{ts}] Node #{random.randint(1,64)} → {task}", cls))
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

# ══════════════════════════════════════
# HEADER
# ══════════════════════════════════════
total_reg_count = db_count()
active_node_count = len([v for v in st.session_state.sim_nodes if v > 0]) + 12

col_logo, col_right = st.columns([3, 1])
with col_logo:
    st.markdown(f"""
    <div style="display:flex;align-items:center;gap:12px;padding:10px 0 4px;">
        <div style="width:11px;height:11px;background:#a2ff00;border-radius:50%;box-shadow:0 0 14px #a2ff00;flex-shrink:0;"></div>
        <div style="font-family:'Syne',sans-serif;font-size:24px;font-weight:800;color:#e8edf2;letter-spacing:-.02em;">
            Nexa<span style="color:#a2ff00;">Edge</span> Network
        </div>
    </div>
    <div style="font-size:12px;color:#4a6070;line-height:1.65;max-width:500px;padding-bottom:8px;">{L['tagline']}</div>
    <div class="nx-online-badge">
        <div class="nx-pulse"></div>
        {L['online_now']}: <strong style="color:#a2ff00;">{active_node_count}</strong>
        &nbsp;·&nbsp;
        {L['total_sessions']}: <strong style="color:#e8edf2;">{total_reg_count}</strong>
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
    with c3: st.metric("GPU Spot Cost" if st.session_state.lang=="EN" else "GPU即时价", "$2–4/hr", "H100 volatile" if st.session_state.lang=="EN" else "H100波动")

    if st.session_state.lang == "EN":
        st.markdown(f"""<div class="nx-card"><div class="nx-card-title"><span class="dot">▸</span> {L['comp_title']}</div>
        <table class="nx-table"><thead><tr><th>Dimension</th><th>GPU Cloud</th><th>Grass</th><th class="hl">NexaEdge</th></tr></thead><tbody>
        <tr><td>CapEx</td><td><span class="tag-bad">EXTREME</span></td><td>Low</td><td class="hl"><span class="tag-good">ZERO</span></td></tr>
        <tr><td>Latency</td><td><span class="tag-bad">50–150ms</span></td><td>N/A</td><td class="hl"><span class="tag-good">&lt;5ms</span></td></tr>
        <tr><td>Privacy</td><td><span class="tag-bad">Data leaves</span></td><td>Partial</td><td class="hl"><span class="tag-good">GDPR-native</span></td></tr>
        <tr><td>Geo Reach</td><td>Few DCs</td><td>High IPs</td><td class="hl"><span class="tag-good">Global</span></td></tr>
        <tr><td>Compute</td><td>GPU only</td><td><span class="tag-bad">Network only</span></td><td class="hl"><span class="tag-good">NPU + CPU</span></td></tr>
        <tr><td>Sybil Resist.</td><td>Central auth</td><td><span class="tag-bad">IP spoofable</span></td><td class="hl"><span class="tag-good">HW fingerprint+ZK</span></td></tr>
        </tbody></table></div>""", unsafe_allow_html=True)
    else:
        st.markdown(f"""<div class="nx-card"><div class="nx-card-title"><span class="dot">▸</span> {L['comp_title']}</div>
        <table class="nx-table"><thead><tr><th>维度</th><th>GPU云</th><th>Grass</th><th class="hl">NexaEdge</th></tr></thead><tbody>
        <tr><td>资本支出</td><td><span class="tag-bad">极高</span></td><td>低</td><td class="hl"><span class="tag-good">零</span></td></tr>
        <tr><td>延迟</td><td><span class="tag-bad">50–150ms</span></td><td>不适用</td><td class="hl"><span class="tag-good">&lt;5ms</span></td></tr>
        <tr><td>隐私</td><td><span class="tag-bad">数据离设备</span></td><td>部分</td><td class="hl"><span class="tag-good">GDPR原生</span></td></tr>
        <tr><td>地理覆盖</td><td>少量DC</td><td>高IP</td><td class="hl"><span class="tag-good">全球</span></td></tr>
        <tr><td>算力</td><td>GPU</td><td><span class="tag-bad">仅网络</span></td><td class="hl"><span class="tag-good">NPU+CPU</span></td></tr>
        <tr><td>女巫抵抗</td><td>中心化</td><td><span class="tag-bad">IP可伪造</span></td><td class="hl"><span class="tag-good">硬件指纹+ZK</span></td></tr>
        </tbody></table></div>""", unsafe_allow_html=True)

    st.markdown(f'<div class="nx-card"><div class="nx-card-title"><span class="dot">▸</span> {L["buyer_title"]}</div>', unsafe_allow_html=True)
    b1, b2 = st.columns(2)
    if st.session_state.lang == "EN":
        with b1:
            st.markdown("""<div class="nx-feature"><div class="nx-feature-title">🤖 Edge AI Agent Deployers</div><div class="nx-feature-body">Run 1.8B–3.8B SLMs with sub-5ms local inference. GDPR compliant by architecture.</div><div class="nx-feature-buyer">→ AI developers, enterprise SaaS</div></div>
            <div class="nx-feature"><div class="nx-feature-title">🧹 AI Dataset Cleaning (RLHF)</div><div class="nx-feature-body">Distributed WASM sandbox runs automated labeling across thousands of nodes simultaneously.</div><div class="nx-feature-buyer">→ AI labs, data pipeline companies</div></div>""", unsafe_allow_html=True)
        with b2:
            st.markdown("""<div class="nx-feature"><div class="nx-feature-title">🔐 ZK-ML Inference Verification</div><div class="nx-feature-body">Fragment AI inference proofs across independent nodes. No single point of trust.</div><div class="nx-feature-buyer">→ DeFi protocols, compliance platforms</div></div>
            <div class="nx-feature"><div class="nx-feature-title">📡 Sensor-Context AI</div><div class="nx-feature-body">Leverage GPS, camera, IMU — context-aware inference unavailable in any datacenter.</div><div class="nx-feature-buyer">→ Location AI, autonomous systems</div></div>""", unsafe_allow_html=True)
    else:
        with b1:
            st.markdown("""<div class="nx-feature"><div class="nx-feature-title">🤖 边缘AI代理部署者</div><div class="nx-feature-body">运行1.8B–3.8B SLM，延迟低于5ms，架构层面符合GDPR。</div><div class="nx-feature-buyer">→ AI开发者、企业SaaS</div></div>
            <div class="nx-feature"><div class="nx-feature-title">🧹 AI数据集清洗（RLHF）</div><div class="nx-feature-body">分布式WASM沙箱在数千节点上同步运行自动标注与交叉验证。</div><div class="nx-feature-buyer">→ AI实验室、数据管道公司</div></div>""", unsafe_allow_html=True)
        with b2:
            st.markdown("""<div class="nx-feature"><div class="nx-feature-title">🔐 ZK-ML推理验证</div><div class="nx-feature-body">将AI推理证明分散到独立节点，冗余验证防止结果篡改。</div><div class="nx-feature-buyer">→ DeFi协议、合规平台</div></div>
            <div class="nx-feature"><div class="nx-feature-title">📡 传感器上下文AI</div><div class="nx-feature-body">利用GPS、摄像头、IMU实现数据中心无法提供的上下文感知推理。</div><div class="nx-feature-buyer">→ 位置AI、自主系统</div></div>""", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    d, c, s = L["demand_side"], L["coordination"], L["supply_side"]
    arch_body = (["Submit tasks via API. Pay in NEXA.", "BFT consensus & reward settlement.", "WASM sandbox. NPU executes inference."]
                 if st.session_state.lang=="EN" else ["通过API提交任务，支付NEXA。","BFT共识与奖励结算。","WASM沙箱，NPU执行推理。"])
    arch_titles = ["AI Buyers" if st.session_state.lang=="EN" else "AI买家","Solana SPL","Device Nodes" if st.session_state.lang=="EN" else "设备节点"]
    arch_html = '<div style="display:flex;align-items:stretch;">'
    for i,(icon,lbl,title,body) in enumerate(zip(["🏢","⛓","📱"],[d,c,s],arch_titles,arch_body)):
        arch_html += f'<div class="arch-box"><div class="arch-label">{lbl}</div><div class="arch-icon">{icon}</div><div class="arch-title">{title}</div><div class="arch-body">{body}</div></div>'
        if i<2: arch_html += '<div class="arch-arrow">→</div>'
    arch_html += '</div>'
    st.markdown(f'<div class="nx-card"><div class="nx-card-title"><span class="dot">▸</span> {L["arch_title"]}</div>{arch_html}</div>', unsafe_allow_html=True)

    st.markdown(f"""<div class="nx-card" style="border-color:rgba(0,229,255,.2);background:rgba(0,229,255,.02);">
    <div class="nx-card-title"><span style="color:#00e5ff;">◈</span> {L['invest_title']}</div>
    <div style="font-size:12px;color:#4a6070;line-height:1.7;margin-bottom:14px;">{L['invest_desc']}</div></div>""", unsafe_allow_html=True)
    if st.button(L["invest_btn"], key="invest_btn"):
        st.warning(L["invest_warn"])

    st.markdown("""<div class="nx-social-grid">
    <a class="nx-social-btn" href="https://www.instagram.com/nexaedge__" target="_blank">📸 Instagram</a>
    <a class="nx-social-btn" href="https://x.com/nexaedge_" target="_blank">🐦 X / Twitter</a>
    <a class="nx-social-btn" href="https://www.facebook.com/share/18eXN6P3Ge/" target="_blank">👥 Facebook</a>
    <a class="nx-social-btn" href="https://www.tiktok.com/@nexaedge7" target="_blank">🎵 TikTok</a>
    <a class="nx-social-btn" href="https://t.me/NexaEdge7" target="_blank">📢 Telegram</a>
    <a class="nx-social-btn" href="mailto:contact@nexaedge.org" style="border-color:rgba(0,229,255,.3);color:#00e5ff!important;">📧 Email</a>
    </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════
# TAB 2 — NETWORK SIM
# ══════════════════════════════════════
elif current_tab == L["nav"][1]:
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
        sc,st_txt = ("#a2ff00",L["running"]) if st.session_state.sim_running else ("#4a6070",L["idle"])
        st.markdown(f'<div style="font-family:\'Space Mono\',monospace;font-size:10px;color:{sc};padding-top:12px;font-weight:700;">{st_txt}</div>', unsafe_allow_html=True)

    nodes = st.session_state.sim_nodes
    node_html = f'<div class="nx-card"><div class="nx-card-title"><span class="dot">▸</span> {L["node_grid_title"]}</div><div class="nx-node-grid">'
    for v in nodes:
        cls={0:"",1:" active",2:" processing"}.get(v,"")
        node_html += f'<div class="nx-node{cls}"></div>'
    node_html += f"""</div><div class="nx-legend">
    <div class="nx-legend-item"><div class="nx-legend-dot" style="background:#182230;"></div>{L['idle_label']}</div>
    <div class="nx-legend-item" style="color:#a2ff00;"><div class="nx-legend-dot" style="background:#a2ff00;"></div>{L['active_label']}</div>
    <div class="nx-legend-item" style="color:#00e5ff;"><div class="nx-legend-dot" style="background:#00e5ff;"></div>{L['processing_label']}</div>
    </div></div>"""
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

    st.markdown(f'<div class="nx-card" style="margin-top:14px;"><div class="nx-card-title"><span class="dot">▸</span> {L["task_log_title"]}</div>', unsafe_allow_html=True)
    if st.session_state.sim_log:
        log_html='<div class="nx-log">'
        for line,cls in st.session_state.sim_log:
            log_html+=f'<div class="log-{cls}">{line}</div>'
        log_html+='</div>'
    else:
        log_html=f'<div class="nx-log"><div>{L["log_empty"]}</div></div>'
    st.markdown(log_html+'</div>', unsafe_allow_html=True)

    p1,p2,p3 = st.session_state.prog1,st.session_state.prog2,st.session_state.prog3
    st.markdown(f"""<div class="nx-card"><div class="nx-card-title"><span class="dot">▸</span> {L['workload_title']}</div>
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
        st.markdown(f"""<div class="nx-card"><div class="nx-card-title"><span class="dot">▸</span> {L['diff_title']}</div>
        <table class="nx-table"><thead><tr><th>Dimension</th><th>Grass</th><th class="hl">NexaEdge</th></tr></thead><tbody>
        <tr><td>Core resource</td><td>Residential bandwidth</td><td class="hl">Device compute (CPU+NPU)</td></tr>
        <tr><td>Primary use</td><td>Web scraping</td><td class="hl">AI inference, RLHF, ZK-ML</td></tr>
        <tr><td>Sybil resistance</td><td><span class="tag-bad">HIGH RISK</span> VPN spoofed</td><td class="hl"><span class="tag-good">LOW RISK</span> HW fingerprint</td></tr>
        <tr><td>Compute verify</td><td>None</td><td class="hl">BFT + ZK proof</td></tr>
        <tr><td>Solana Mobile</td><td>None</td><td class="hl"><span class="tag-good">NATIVE</span> Seeker/Saga</td></tr>
        </tbody></table></div>""", unsafe_allow_html=True)
    else:
        st.markdown(f"""<div class="nx-card"><div class="nx-card-title"><span class="dot">▸</span> {L['diff_title']}</div>
        <table class="nx-table"><thead><tr><th>维度</th><th>Grass</th><th class="hl">NexaEdge</th></tr></thead><tbody>
        <tr><td>核心资源</td><td>住宅带宽</td><td class="hl">设备算力（CPU+NPU）</td></tr>
        <tr><td>主要用途</td><td>网页抓取</td><td class="hl">AI推理、RLHF、ZK-ML</td></tr>
        <tr><td>女巫抵抗</td><td><span class="tag-bad">高风险</span> VPN伪造</td><td class="hl"><span class="tag-good">低风险</span> 硬件指纹</td></tr>
        <tr><td>算力验证</td><td>无</td><td class="hl">BFT + ZK证明</td></tr>
        <tr><td>Solana Mobile</td><td>无</td><td class="hl"><span class="tag-good">原生</span> Seeker/Saga</td></tr>
        </tbody></table></div>""", unsafe_allow_html=True)

    st.markdown(f'<div class="nx-card"><div class="nx-card-title"><span class="dot">▸</span> {L["moat_title"]}</div>', unsafe_allow_html=True)
    m1,m2=st.columns(2)
    if st.session_state.lang=="EN":
        with m1:
            st.markdown("""<div class="nx-moat"><div class="nx-moat-icon">🔐</div><div class="nx-moat-title">Proof of Compute (PoC)</div><div class="nx-moat-body">Every node solves a cryptographic ML inference puzzle to claim rewards. HW fingerprint + ZK proof prevents Sybil attacks.</div></div>
            <div class="nx-moat"><div class="nx-moat-icon">🌍</div><div class="nx-moat-title">Geographic Density</div><div class="nx-moat-body">6.8B smartphones vs. a few thousand datacenters. NexaEdge reaches rural markets no cloud can serve.</div></div>""", unsafe_allow_html=True)
        with m2:
            st.markdown("""<div class="nx-moat"><div class="nx-moat-icon">🧠</div><div class="nx-moat-title">NPU-Native Execution</div><div class="nx-moat-body">Modern smartphones (A-series, Snapdragon) have dedicated NPUs. NexaEdge targets these for SLM inference.</div></div>
            <div class="nx-moat"><div class="nx-moat-icon">📱</div><div class="nx-moat-title">Solana Mobile Integration</div><div class="nx-moat-body">Solana Seeker/Saga are the only Web3-native phones. NexaEdge becomes the killer app making hardware ROI-positive.</div></div>""", unsafe_allow_html=True)
    else:
        with m1:
            st.markdown("""<div class="nx-moat"><div class="nx-moat-icon">🔐</div><div class="nx-moat-title">算力证明（PoC）</div><div class="nx-moat-body">每个节点必须解决加密ML推理难题才能领取奖励。硬件指纹+ZK证明防止女巫攻击。</div></div>
            <div class="nx-moat"><div class="nx-moat-icon">🌍</div><div class="nx-moat-title">地理密度</div><div class="nx-moat-body">68亿部智能手机对比数千个数据中心。NexaEdge覆盖任何云端无法服务的超本地场景。</div></div>""", unsafe_allow_html=True)
        with m2:
            st.markdown("""<div class="nx-moat"><div class="nx-moat-icon">🧠</div><div class="nx-moat-title">NPU原生执行</div><div class="nx-moat-body">现代智能手机（A系列、骁龙）配备专用NPU。NexaEdge将其用于SLM推理。</div></div>
            <div class="nx-moat"><div class="nx-moat-icon">📱</div><div class="nx-moat-title">Solana Mobile集成</div><div class="nx-moat-body">Solana Seeker/Saga是唯一的Web3原生手机。NexaEdge成为使硬件投资回报为正的杀手级应用。</div></div>""", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    thermal_en="The 39°C thermal ceiling is a hardcoded daemon constraint.<br>If device ≥ 39°C → task queue paused → passive cooling activated.<br>Enforced at WASM sandbox level — not overridable by user.<br><br><strong style='color:#d0d8e4;'>Why it matters:</strong> Institutional buyers need SLA guarantees. The 39°C protocol is the supply-side durability guarantee."
    thermal_zh="39°C 热限是硬编码的守护进程约束。<br>设备温度 ≥ 39°C → 任务队列暂停 → 激活被动散热模式。<br>在 WASM 沙箱层面强制执行——用户不可覆盖。<br><br><strong style='color:#d0d8e4;'>对买家的意义：</strong>机构算力买家需要SLA保证。39°C协议是供给侧的耐久性保障。"
    st.markdown(f"""<div class="nx-card"><div class="nx-card-title"><span class="dot">▸</span> {L['thermal_title']}</div>
    <div style="font-size:12px;color:#4a6070;line-height:1.9;">{thermal_en if st.session_state.lang=="EN" else thermal_zh}</div></div>""", unsafe_allow_html=True)

# ══════════════════════════════════════
# TAB 4 — ROADMAP
# ══════════════════════════════════════
elif current_tab == L["nav"][3]:
    if st.session_state.lang=="EN":
        st.markdown(f"""<div class="nx-card"><div class="nx-card-title"><span class="dot">▸</span> {L['roadmap_title']}</div>
        <div class="nx-roadmap-item current"><div class="nx-roadmap-phase">Q2 2026 · NOW</div><div class="nx-roadmap-title">Concept Validation & Institutional Acceleration</div><div class="nx-roadmap-body">Architecture finalized. Whitepaper drafted. <strong>Solana Grant</strong>, <strong>Alliance DAO</strong>, <strong>Y Combinator</strong> in pipeline. AngelList SAFE ($5M cap) initialized. Global node waitlist open.</div></div>
        <div class="nx-roadmap-item"><div class="nx-roadmap-phase">Q3 2026</div><div class="nx-roadmap-title">WASM Sandbox MVP</div><div class="nx-roadmap-body">Functional WASM on iOS/Android. First SLM inference (Phi-3 mini) on device NPU. Thermal guard daemon. Internal alpha: 50 devices.</div></div>
        <div class="nx-roadmap-item"><div class="nx-roadmap-phase">Q4 2026</div><div class="nx-roadmap-title">Closed Beta — 1,000 Nodes</div><div class="nx-roadmap-body">Solana SPL token deployment. BFT testnet. First paying buyer pilot. ZK proof of compute live.</div></div>
        <div class="nx-roadmap-item"><div class="nx-roadmap-phase">Q1 2027</div><div class="nx-roadmap-title">Public Mainnet Launch</div><div class="nx-roadmap-body">Open enrollment. Solana Seeker integration. Marketplace live. Target: 100K active nodes, 3 enterprise buyers.</div></div>
        <div class="nx-roadmap-item" style="padding-bottom:0;"><div class="nx-roadmap-phase">2027+</div><div class="nx-roadmap-title">Scale & Ecosystem</div><div class="nx-roadmap-body">ZK-ML verification live. Expand to laptop/IoT. Series A targeting $15M.</div></div>
        </div>""", unsafe_allow_html=True)
    else:
        st.markdown(f"""<div class="nx-card"><div class="nx-card-title"><span class="dot">▸</span> {L['roadmap_title']}</div>
        <div class="nx-roadmap-item current"><div class="nx-roadmap-phase">2026年Q2 · 当前</div><div class="nx-roadmap-title">概念验证与机构加速</div><div class="nx-roadmap-body">架构设计定稿。白皮书起草完成。<strong>Solana Grant</strong>、<strong>Alliance DAO</strong>、<strong>Y Combinator</strong> 积极推进中。AngelList SAFE（$500万上限）初始化。全球节点候补名单开放。</div></div>
        <div class="nx-roadmap-item"><div class="nx-roadmap-phase">2026年Q3</div><div class="nx-roadmap-title">WASM 沙箱 MVP</div><div class="nx-roadmap-body">iOS/Android WASM 执行环境。首个 SLM 推理（Phi-3 mini）在设备 NPU 上运行。热保护守护进程。内部 alpha：50 台设备。</div></div>
        <div class="nx-roadmap-item"><div class="nx-roadmap-phase">2026年Q4</div><div class="nx-roadmap-title">封闭测试——1,000 节点</div><div class="nx-roadmap-body">Solana SPL 代币部署。BFT 测试网。首个付费买家试点。ZK 算力证明上线。</div></div>
        <div class="nx-roadmap-item"><div class="nx-roadmap-phase">2027年Q1</div><div class="nx-roadmap-title">公开主网上线</div><div class="nx-roadmap-body">开放节点注册。Solana Seeker 集成。市场上线。目标：10万活跃节点、3个企业买家。</div></div>
        <div class="nx-roadmap-item" style="padding-bottom:0;"><div class="nx-roadmap-phase">2027年+</div><div class="nx-roadmap-title">规模扩张与生态</div><div class="nx-roadmap-body">ZK-ML 验证上线。扩展至笔记本/IoT。A轮融资目标 1500 万美元。</div></div>
        </div>""", unsafe_allow_html=True)

    r1,r2,r3=st.columns(3)
    if st.session_state.lang=="EN":
        with r1: st.metric("Seed Target","$500K","MVP + 1,000-node beta")
        with r2: st.metric("Target Nodes (Y1)","100K","at mainnet")
        with r3: st.metric("Settlement Chain","Solana SPL","low gas · high TPS")
    else:
        with r1: st.metric("种子轮目标","$500K","MVP+1000节点测试")
        with r2: st.metric("目标节点数","100K","主网活跃")
        with r3: st.metric("结算链","Solana SPL","低gas·高TPS")

    st.markdown(f"""<div class="nx-card" style="margin-top:8px;border-color:rgba(255,179,0,.2);background:rgba(255,179,0,.02);">
    <div class="nx-card-title"><span style="color:#ffb300;">◈</span> {L['nexa_proj_title']}</div>
    <div style="font-size:11px;color:#4a6070;line-height:1.8;">{L['nexa_disclaimer']}</div></div>""", unsafe_allow_html=True)

# ══════════════════════════════════════
# TAB 5 — WHITELIST（写入 Supabase）
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
        st.markdown(f"""<div class="nx-success-banner">
        <div style="font-size:20px;font-weight:800;color:#a2ff00;margin-bottom:6px;">{L['wl_success_title']}</div>
        <div style="font-size:12px;color:#4a6070;line-height:1.7;margin-bottom:20px;">{L['wl_success_desc']}</div>
        <div class="nx-ref-display">
            <div class="nx-ref-label">{L['wl_your_ref']}</div>
            <div class="nx-ref-code">{ref}</div>
        </div></div>""", unsafe_allow_html=True)
        cb1,cb2=st.columns(2)
        with cb1:
            if st.button(L["wl_copy"], key="copy_ref_btn"):
                st.components.v1.html(f'<script>navigator.clipboard.writeText("{ref}").catch(()=>{{}});</script>', height=0, width=0)
                st.toast(L["wl_copied"])
        with cb2:
            if st.button(L["wl_reset"], type="secondary", key="wl_reset_btn"):
                st.session_state.wl_success=False; st.session_state.wl_ref_code=''; st.rerun()
    else:
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
        disclaimer="By registering you confirm this is a concept demo. No tokens issued. No investment contract formed." if st.session_state.lang=='EN' else "注册即表明您了解这是概念演示。不发行代币，不构成投资合同。"
        st.markdown(f'<div style="font-family:\'Space Mono\',monospace;font-size:9px;color:#2a3a4a;text-align:center;line-height:1.7;margin-top:10px;">{disclaimer}</div>', unsafe_allow_html=True)

    if total_reg > 0:
        regs = db_get_registrations()
        if regs:
            st.markdown(f'<div style="margin-top:24px;font-family:\'Space Mono\',monospace;font-size:10px;color:#4a6070;text-transform:uppercase;letter-spacing:.1em;margin-bottom:10px;">{L["ledger_title"]}</div>', unsafe_allow_html=True)
            ledger_rows=[{"Timestamp":r["created_at"][:19].replace("T"," "),"Node Hash":hashlib.sha256(r["email"].encode()).hexdigest()[:22]+"... @SPL"} for r in regs]
            st.dataframe(ledger_rows, use_container_width=True, hide_index=True)

st.markdown("""<div class="nx-footer">
NexaEdge Network &nbsp;·&nbsp; Pre-Launch Concept Demo &nbsp;·&nbsp; All simulations illustrative only<br>
No tokens issued &nbsp;·&nbsp; No investment contract &nbsp;·&nbsp; contact@nexaedge.org<br>
© 2026 NexaEdge Network. All rights reserved.
</div>""", unsafe_allow_html=True)
