import streamlit as st
import time
import random
import re
import hashlib
import psutil
from streamlit_autorefresh import st_autorefresh

st.set_page_config(
    page_title="NexaEdge Network — Investor Demo",
    page_icon="🟢",
    layout="centered"
)

# ══════════════════════════════════════
# 全局持久化层（跨 Session 共享，刷新不丢失）
# ══════════════════════════════════════
@st.cache_resource
def get_global_db():
    return {
        "registrations": [],
        "whitelisted_emails": set(),
        "base_sessions": 142,
    }

global_db = get_global_db()

# ══════════════════════════════════════
# 语言配置
# ══════════════════════════════════════
LANGS = {
    "EN": {
        "nav": ["Market", "Network Sim", "Differentiation", "Roadmap", "Whitelist"],
        "tagline": "Aggregating idle smartphone compute into a distributed edge AI inference network — turning personal devices into institutional-grade infrastructure.",
        "stage": "⚠ PRE-LAUNCH · ARCHITECTURE DEMO",
        "sim_only": "⚠ CONCEPT SIMULATION — Visualizing the NexaEdge engine deployment. Telemetry syncs real host load mixed with simulated nodes. All metrics are scaling projections.",
        "start_sim": "▶ Start Telemetry Simulation",
        "stop_sim": "■ Stop Protocol",
        "running": "● LIVE TELEMETRY ACTIVE",
        "idle": "○ STANDBY PROTOCOL",
        "online_now": "🟢 Nodes Online Now",
        "total_sessions": "Total Node Sessions",
        "active_nodes": "Active Nodes",
        "tasks_done": "Tasks Dispatched",
        "avg_latency": "Network Latency",
        "bft_consensus": "Consensus Rate",
        "nexa_earned": "Simulated $NEXA",
        "nexa_per_task": "NEXA / Task",
        "nexa_proj_title": "NEXA Token Ledger",
        "nexa_sim_earned": "Earned Yield",
        "nexa_est_usd": "Est. Value (@ $0.50)",
        "nexa_supply": "Total Supply",
        "nexa_disclaimer": "⚠ Illustrative only. NEXA reward ~0.0012–0.0038/task based on $50M projected market cap, 100M supply, $0.50 est. price. Actual rates set at mainnet.",
        "node_grid_title": "Distributed Node Matrix — Hardware Telemetry",
        "task_log_title": "Cryptographic Verification & Task Pipeline",
        "log_empty": "// Execute 'Start Telemetry Simulation' to pipe node streams.",
        "workload_title": "Compute Layer Pipeline Capacity",
        "wl_inference": "Edge AI Inference (SLM 1.8B / WASM)",
        "wl_rlhf": "Dataset Validation Ledger (RLHF)",
        "wl_zk": "ZK Proof Fragment Generation",
        "comp_title": "Competitive Matrix & Infrastructure Paradigm",
        "buyer_title": "Value Capture — Node Monetization Pipeline",
        "arch_title": "Distributed Network Topology",
        "diff_title": "Structural Moat: NexaEdge vs. Bandwidth Proxies",
        "moat_title": "Core Technological Anchors",
        "thermal_title": "Hardware Integrity — 39°C Thermal Sandboxing",
        "roadmap_title": "Ecosystem Rollout Roadmap",
        "wl_title": "Secure Genesis Whitelist Allocation",
        "wl_desc": "Register node signature early access — locked to Solana SPL verification parameters.",
        "wl_email": "Operator Email",
        "wl_email_ph": "you@example.com",
        "wl_wallet": "Solana Wallet (SPL)",
        "wl_wallet_ph": "Enter 32–44 char public key (e.g., 7xKp...)",
        "wl_ref": "Referral Code (Optional)",
        "wl_ref_ph": "Enter a referral code",
        "wl_submit": "Commit Node Signature to Ledger",
        "wl_success_title": "✅ RECORD LOCKED SUCCESSFULLY",
        "wl_success_desc": "Your node configuration has been appended to the global ledger database.",
        "wl_your_ref": "Your Referral Code",
        "wl_copy": "📋 Copy",
        "wl_copied": "✅ Copied!",
        "wl_total": "Total Registered",
        "err_email": "Invalid email address.",
        "err_wallet": "Solana wallet must be 32–44 characters.",
        "err_dupe": "This email is already registered.",
        "idle_label": "Standby",
        "active_label": "Node Ready",
        "processing_label": "WASM Executing",
        "demand_side": "Demand Layer",
        "coordination": "Settlement & Coordination",
        "supply_side": "Supply Cluster",
        "lang_btn": "中文",
        "ledger_title": "Genesis Ledger Secure Footprints",
        "invest_title": "Seed Round Institutional Investment Gateway",
        "invest_desc": "NexaEdge Seed round infrastructure is processed through AngelList Rollups (Post-money SAFE). Qualified institutional allocators can lock intent queues directly.",
        "invest_btn": "💼 Soft-Circle Seed Allocation",
        "invest_warn": "AngelList infrastructure is processing compliance audit. Please use the Whitelist Ledger or email contact@nexaedge.org directly.",
        "admin_title": "⚙️ System Root Audit Console",
        "admin_pw_ph": "Enter admin password",
        "admin_login": "Unlock Console",
        "admin_wrong": "Authentication failed.",
        "admin_header": "📊 LIVE BACKEND DATABASE",
        "admin_export": "💾 Export Node Registry CSV",
        "admin_empty": "Global ledger is currently empty.",
        "admin_logout": "Relock Console",
        "tag_bad_extreme": "EXTREME",
        "tag_bad_spoof": "IP Spoof Risk",
        "tag_good_zero": "ZERO",
        "tag_good_zk": "ZK Proof + PoC",
        "tag_good_local": "100% Local WASM",
    },
    "ZH": {
        "nav": ["核心市场", "网络节点模拟", "架构差异化", "路线图 & 融资", "白名单注册"],
        "tagline": "将闲置智能手机算力汇聚成分布式边缘 AI 推理网络——让个人设备变身机构级基础设施。",
        "stage": "⚠ 预发布 · 架构及融资演示",
        "sim_only": "⚠ 概念监控层——本页面同步抓取演示机真实硬件状态并混合模拟节点拓扑。所有计算指标均为网络规模化后的示意性预测。",
        "start_sim": "▶ 启动物理与模拟网络流",
        "stop_sim": "■ 终止网络调度",
        "running": "● 实时遥测网络已激活",
        "idle": "○ 调度层处于就绪休眠状态",
        "online_now": "🟢 实时在线节点",
        "total_sessions": "累计节点会话",
        "active_nodes": "活跃算力单元",
        "tasks_done": "已分发验证任务",
        "avg_latency": "边缘网络延迟",
        "bft_consensus": "BFT 共识率",
        "nexa_earned": "模拟积累 $NEXA",
        "nexa_per_task": "单任务 NEXA 奖励",
        "nexa_proj_title": "NEXA 代币账本",
        "nexa_sim_earned": "模拟挖矿产出",
        "nexa_est_usd": "预估价值 (@ $0.50)",
        "nexa_supply": "总供应量",
        "nexa_disclaimer": "⚠ 仅供参考。每任务约 0.0012–0.0038 NEXA，基于 1 亿总供应量、5000 万美元预计市值、$0.50 发行价估算。实际比率以主网为准。",
        "node_grid_title": "分布式节点矩阵 — 物理与模拟设备混合流",
        "task_log_title": "密码学验证与任务分发异步日志",
        "log_empty": "// 点击 '启动物理与模拟网络流' 导入实时遥测管道。",
        "workload_title": "算力管道实时吞吐负载",
        "wl_inference": "边缘 AI 推理任务 (SLM 1.8B / WASM 沙箱)",
        "wl_rlhf": "数据集自动化清洗与标注验证 (RLHF)",
        "wl_zk": "分布式 ZK 证明片段生成",
        "comp_title": "竞争定位与去中心化基础设施范式对比",
        "buyer_title": "价值捕获 — 算力买家与变现管道",
        "arch_title": "分布式网络拓扑流",
        "diff_title": "技术护城河：NexaEdge 对比纯带宽代理网络（如 Grass）",
        "moat_title": "核心技术锚点",
        "thermal_title": "硬件耐久保障 — 39°C 严格热沙箱协议",
        "roadmap_title": "生态落地与融资路线图",
        "wl_title": "锁定创世白名单节点分配额度",
        "wl_desc": "提早注册节点设备特征码——直接锁定基于 Solana SPL 的创世奖励权重。",
        "wl_email": "运营商联络邮箱",
        "wl_email_ph": "your@email.com",
        "wl_wallet": "目标 Solana 接收钱包 (SPL)",
        "wl_wallet_ph": "请输入 32-44 位公钥地址（例如: 7xKp...）",
        "wl_ref": "推荐码（可选）",
        "wl_ref_ph": "请输入推荐人哈希特征码",
        "wl_submit": "向全局分布式账本提交签名",
        "wl_success_title": "✅ 数据记录已成功写入",
        "wl_success_desc": "您的节点配置和设备特征已成功写入全局持久化缓存，刷新不丢失。",
        "wl_your_ref": "您的专属推荐码",
        "wl_copy": "📋 复制",
        "wl_copied": "✅ 已复制！",
        "wl_total": "全球累计注册节点",
        "err_email": "格式校验错误：邮箱字符串校验失败。",
        "err_wallet": "格式校验错误：Solana SPL 地址长度不符合规范（应为 32–44 字符）。",
        "err_dupe": "冲突错误：此邮箱已存在于创世账本记录中。",
        "idle_label": "休眠备用",
        "active_label": "节点就绪",
        "processing_label": "WASM正在执行",
        "demand_side": "需求方集群",
        "coordination": "结算与共识协调层",
        "supply_side": "供给方集群",
        "lang_btn": "English",
        "ledger_title": "🛡️ 创世账本安全特征指纹",
        "invest_title": "机构种子轮投资入口",
        "invest_desc": "NexaEdge 种子轮通过 AngelList Rollups（Post-money SAFE）架构处理。合格机构分配方可直接锁定意向额度。",
        "invest_btn": "💼 意向锁定种子轮额度",
        "invest_warn": "AngelList 基础架构目前在后台合规审核中。请通过白名单提交或直接联系 contact@nexaedge.org。",
        "admin_title": "⚙️ 系统根权限审计控制台",
        "admin_pw_ph": "请输入管理员密码",
        "admin_login": "解锁控制台",
        "admin_wrong": "认证失败，密码错误。",
        "admin_header": "📊 实时后台数据库（持久化）",
        "admin_export": "💾 导出注册节点 CSV",
        "admin_empty": "全局账本当前为空。",
        "admin_logout": "重新锁定控制台",
        "tag_bad_extreme": "极高",
        "tag_bad_spoof": "IP可伪造",
        "tag_good_zero": "零成本",
        "tag_good_zk": "ZK证明 + PoC",
        "tag_good_local": "100% 本地WASM",
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
    ("SLM 推理任务执行 (Phi-3 mini / WASM 沙箱)", "success"),
    ("RLHF 数据标签自动化交叉验证", "info"),
    ("ZK 证明片段生成与校验", "success"),
    ("BFT 共识层节点签名投票", "info"),
    ("本机热指标检查: 正常 ✓", "success"),
    ("节点硬件指纹哈希校验成功", "success"),
]

ADMIN_PASSWORD = "nexaedge2026admin"
REWARD_BASE = 0.0022

# ══════════════════════════════════════
# CSS
# ══════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Syne:wght@400;600;700;800&display=swap');

.main .block-container { padding-top: 1rem !important; padding-bottom: 2rem !important; max-width: 860px !important; }
.stApp { background-color: #080c0f; }
#MainMenu, footer, header, [data-testid="stHeader"] { display: none !important; }

.stApp::before {
    content: ''; position: fixed; inset: 0;
    background-image: linear-gradient(rgba(162,255,0,0.018) 1px, transparent 1px), linear-gradient(90deg, rgba(162,255,0,0.018) 1px, transparent 1px);
    background-size: 40px 40px; pointer-events: none; z-index: 0;
}

h1, h2, h3, h4, p, div, span, label { font-family: 'Syne', sans-serif !important; }

div[data-testid="stRadio"] > label { display: none !important; }
div[data-testid="stRadio"] > div { flex-direction: row !important; gap: 6px !important; border-bottom: 1px solid #1a2530 !important; padding-bottom: 8px; margin-bottom: 20px; flex-wrap: wrap !important; }
div[data-testid="stRadio"] label[data-baseweb="radio"] {
    background-color: #0e1419 !important; color: #556070 !important; border-radius: 6px 6px 0 0 !important;
    border: 1px solid #1a2530 !important; padding: 8px 14px !important; font-family: 'Space Mono', monospace !important;
    font-size: 10px !important; font-weight: 700 !important; text-transform: uppercase !important;
    letter-spacing: 0.05em !important; margin: 0 !important;
}
div[data-testid="stRadio"] label[data-baseweb="radio"]:has(input:checked) {
    color: #a2ff00 !important; border-bottom-color: #0e1419 !important; background-color: #0e1419 !important;
}
div[data-testid="stRadio"] input { display: none !important; }
div[data-testid="stRadio"] div[data-testid="stMarkdownContainer"] p { font-size: 10px !important; font-weight: 700 !important; }

[data-testid="stMetric"] { background: #0e1419; border: 1px solid #1a2530; border-radius: 10px; padding: 14px !important; }
[data-testid="stMetricLabel"] { font-family: 'Space Mono', monospace !important; font-size: 9px !important; color: #556070 !important; text-transform: uppercase !important; letter-spacing: 0.08em !important; }
[data-testid="stMetricValue"] { font-size: 20px !important; font-weight: 800 !important; color: #e8edf2 !important; }
[data-testid="stMetricDelta"] { font-size: 10px !important; }

div.stButton > button {
    background-color: #a2ff00 !important; color: #080c0f !important; font-family: 'Space Mono', monospace !important;
    font-size: 11px !important; font-weight: 700 !important; text-transform: uppercase !important;
    letter-spacing: 0.05em !important; border: none !important; border-radius: 8px !important;
    padding: 10px 20px !important; width: 100% !important;
}
div.stButton > button:hover { background-color: #b5ff33 !important; }
div.stButton > button[kind="secondary"] { background-color: transparent !important; color: #556070 !important; border: 1px solid #1a2530 !important; }
div.stButton > button[kind="secondary"]:hover { border-color: #556070 !important; color: #e8edf2 !important; }

.stTextInput > div > div > input {
    background: #060a0d !important; border: 1px solid #1a2530 !important; border-radius: 8px !important;
    color: #e8edf2 !important; font-family: 'Space Mono', monospace !important; font-size: 12px !important;
}
.stTextInput > div > div > input:focus { border-color: #a2ff00 !important; box-shadow: none !important; }
.stTextInput label { font-family: 'Space Mono', monospace !important; font-size: 10px !important; color: #556070 !important; text-transform: uppercase !important; letter-spacing: 0.08em !important; }

.nx-card { background: #0e1419; border: 1px solid #1a2530; border-radius: 12px; padding: 18px 20px; margin-bottom: 14px; }
.nx-card-title { font-family: 'Space Mono', monospace; font-size: 10px; color: #556070; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 14px; }
.nx-card-title span { color: #a2ff00; margin-right: 6px; }

.nx-notice { background: rgba(255,179,0,0.04); border: 1px solid rgba(255,179,0,0.15); border-radius: 8px; padding: 10px 14px; font-family: 'Space Mono', monospace; font-size: 10px; color: #ffb300; line-height: 1.6; margin-bottom: 18px; }
.nx-online-badge { display: inline-flex; align-items: center; gap: 8px; background: #060a0d; border: 1px solid #1a2530; border-radius: 6px; padding: 6px 12px; font-family: 'Space Mono', monospace; font-size: 10px; color: #00e5ff; margin-top: 6px; }
.nx-stage-badge { display: inline-block; background: rgba(0,229,255,0.08); border: 1px solid rgba(0,229,255,0.25); color: #00e5ff; font-family: 'Space Mono', monospace; font-size: 10px; font-weight: 700; padding: 4px 10px; border-radius: 4px; letter-spacing: 0.08em; }

.nx-feature { background: #060a0d; border: 1px solid #1a2530; border-left: 3px solid #a2ff00; border-radius: 8px; padding: 14px; margin-bottom: 10px; }
.nx-feature-title { font-size: 12px; font-weight: 700; color: #e8edf2; margin-bottom: 5px; }
.nx-feature-body { font-size: 11px; color: #556070; line-height: 1.6; }
.nx-feature-buyer { margin-top: 7px; font-family: 'Space Mono', monospace; font-size: 10px; color: #00e5ff; }

.tag-bad { display: inline-block; background: rgba(244,63,94,0.12); color: #f43f5e; font-family: 'Space Mono', monospace; font-size: 9px; padding: 2px 6px; border-radius: 3px; font-weight: 700; }
.tag-good { display: inline-block; background: rgba(162,255,0,0.1); color: #a2ff00; font-family: 'Space Mono', monospace; font-size: 9px; padding: 2px 6px; border-radius: 3px; font-weight: 700; }

.nx-node-grid { display: grid; grid-template-columns: repeat(8, 1fr); gap: 5px; margin: 12px 0; }
.nx-node { aspect-ratio: 1; border-radius: 4px; background: #1a2530; }
.nx-node.active { background: #a2ff00; box-shadow: 0 0 6px rgba(162,255,0,0.3); }
.nx-node.processing { background: #00e5ff; box-shadow: 0 0 6px rgba(0,229,255,0.3); animation: blink 1s ease-in-out infinite; }
@keyframes blink { 0%,100%{opacity:1} 50%{opacity:0.35} }

.nx-sim-stat { background: #060a0d; border: 1px solid #1a2530; border-radius: 8px; padding: 12px; text-align: center; }
.nx-sim-val { font-family: 'Space Mono', monospace; font-size: 16px; font-weight: 700; color: #a2ff00; }
.nx-sim-val.cyan { color: #00e5ff; }
.nx-sim-val.gold { color: #ffb300; }
.nx-sim-label { font-family: 'Space Mono', monospace; font-size: 8px; color: #556070; margin-top: 4px; text-transform: uppercase; letter-spacing: 0.06em; }

.nx-log { background: #040709; border: 1px solid #1a2530; border-radius: 8px; padding: 12px; font-family: 'Space Mono', monospace; font-size: 10px; color: #556070; line-height: 1.8; max-height: 140px; overflow-y: auto; }
.log-success { color: #a2ff00; }
.log-info { color: #00e5ff; }

.nx-roadmap-item { border-left: 2px solid #1a2530; padding-left: 16px; padding-bottom: 20px; position: relative; }
.nx-roadmap-item::before { content: ''; position: absolute; left: -5px; top: 4px; width: 8px; height: 8px; border-radius: 50%; background: #1a2530; border: 1px solid #1a2530; }
.nx-roadmap-item.current::before { background: #00e5ff; border-color: #00e5ff; box-shadow: 0 0 6px rgba(0,229,255,0.5); }
.nx-roadmap-phase { font-family: 'Space Mono', monospace; font-size: 9px; color: #ffb300; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 3px; }
.nx-roadmap-title { font-size: 13px; font-weight: 700; color: #e8edf2; margin-bottom: 4px; }
.nx-roadmap-body { font-size: 11px; color: #556070; line-height: 1.6; }

.nx-prog-label { display: flex; justify-content: space-between; font-family: 'Space Mono', monospace; font-size: 10px; color: #556070; margin-bottom: 5px; }
.nx-prog-bar { height: 4px; background: #1a2530; border-radius: 2px; overflow: hidden; margin-bottom: 12px; }
.nx-prog-fill { height: 100%; background: #a2ff00; border-radius: 2px; transition: width 0.6s ease; }
.nx-prog-fill.blue { background: #00e5ff; }

.nx-table { width: 100%; border-collapse: collapse; font-size: 11px; }
.nx-table th { text-align: left; padding: 8px 10px; font-family: 'Space Mono', monospace; font-size: 9px; text-transform: uppercase; letter-spacing: 0.08em; color: #556070; border-bottom: 1px solid #1a2530; }
.nx-table th.hl { color: #a2ff00; }
.nx-table td { padding: 10px; border-bottom: 1px solid rgba(26,37,48,0.5); color: #556070; vertical-align: top; line-height: 1.5; }
.nx-table td:first-child { color: #e8edf2; font-weight: 600; width: 150px; }
.nx-table td.hl { color: #e8edf2; }
.nx-table tr:last-child td { border-bottom: none; }

.nx-moat { background: #060a0d; border: 1px solid #1a2530; border-radius: 8px; padding: 14px; margin-bottom: 10px; }
.nx-moat-icon { font-size: 20px; margin-bottom: 8px; }
.nx-moat-title { font-size: 12px; font-weight: 700; color: #e8edf2; margin-bottom: 5px; }
.nx-moat-body { font-size: 11px; color: #556070; line-height: 1.6; }

.nx-social-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(70px, 1fr)); gap: 6px; margin: 10px 0; }
.nx-social-btn { display: block; text-align: center; padding: 7px; background: #0e1419; border: 1px solid #1a2530; border-radius: 8px; color: #556070 !important; font-size: 11px; font-weight: bold; text-decoration: none; transition: all 0.2s; }
.nx-social-btn:hover { border-color: #a2ff00; color: #a2ff00 !important; }

.nx-ref-code { font-family: 'Space Mono', monospace; font-size: 22px; font-weight: 700; color: #a2ff00; letter-spacing: 0.15em; margin: 10px 0; }
.nx-success-box { background: rgba(162,255,0,0.04); border: 1px solid rgba(162,255,0,0.2); border-radius: 12px; padding: 24px; text-align: center; }

.nx-footer { border-top: 1px solid #1a2530; margin-top: 40px; padding-top: 16px; text-align: center; font-family: 'Space Mono', monospace; font-size: 10px; color: #2a3540; line-height: 1.8; }
.admin-table { width: 100%; border-collapse: collapse; font-size: 11px; }
.admin-table th { text-align: left; padding: 8px 10px; font-family: 'Space Mono', monospace; font-size: 9px; color: #556070; text-transform: uppercase; border-bottom: 1px solid #1a2530; }
.admin-table td { padding: 10px; border-bottom: 1px solid rgba(26,37,48,0.4); color: #e8edf2; font-family: 'Space Mono', monospace; font-size: 10px; word-break: break-all; }
.admin-table tr:last-child td { border-bottom: none; }
.admin-badge { display: inline-block; background: rgba(162,255,0,0.1); color: #a2ff00; border-radius: 3px; padding: 2px 6px; font-size: 9px; }
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════
# Session State 初始化
# ══════════════════════════════════════
_defaults = {
    'lang': 'ZH',
    'sim_running': False,
    'sim_tasks': 0,
    'sim_log': [],
    'sim_nodes': [0] * 64,
    'sim_latency': 3.0,
    'sim_consensus': 98.2,
    'prog1': 0, 'prog2': 0, 'prog3': 0,
    'nexa_earned': 0.0,
    'nexa_rate': 0.0,
    'wl_success': False,
    'wl_ref_code': '',
    'wl_copied': False,
    'admin_logged_in': False,
    'admin_error': False,
}
for k, v in _defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

if 'session_counted' not in st.session_state:
    st.session_state.session_counted = True
    global_db['base_sessions'] += 1

L = LANGS[st.session_state.lang]
TASK_TYPES = TASK_TYPES_EN if st.session_state.lang == "EN" else TASK_TYPES_ZH

# ══════════════════════════════════════
# 遥测 tick（真实CPU混合模拟）
# ══════════════════════════════════════
if st.session_state.sim_running:
    st_autorefresh(interval=1200, key="nexa_telemetry_tick")

    real_cpu = psutil.cpu_percent()
    nodes = st.session_state.sim_nodes
    active_target = int(10 + (real_cpu / 100) * 40)
    for i in range(64):
        if i < active_target:
            nodes[i] = 2 if random.random() > 0.4 else 1
        else:
            nodes[i] = 0
    st.session_state.sim_nodes = nodes

    task, cls = random.choice(TASK_TYPES)
    node_id = random.randint(1, 64)
    ts = time.strftime("%H:%M:%S")
    st.session_state.sim_log.append((f"[{ts}] Node #{node_id} → {task}", cls))
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
col_logo, col_right = st.columns([3, 1])
total_sessions_display = global_db['base_sessions'] + len(global_db['registrations'])
active_node_count = len([v for v in st.session_state.sim_nodes if v > 0]) + 12

with col_logo:
    st.markdown(f"""
    <div style="display:flex;align-items:center;gap:10px;padding:8px 0;">
        <div style="width:10px;height:10px;background:#a2ff00;border-radius:50%;box-shadow:0 0 12px #a2ff00;flex-shrink:0;"></div>
        <div style="font-family:'Syne',sans-serif;font-size:22px;font-weight:800;color:#e8edf2;">
            Nexa<span style="color:#a2ff00;">Edge</span> Network
        </div>
    </div>
    <div style="font-size:12px;color:#556070;line-height:1.6;padding-bottom:6px;max-width:520px;">{L['tagline']}</div>
    <div class="nx-online-badge">
        <span style="width:6px;height:6px;background:#00e5ff;border-radius:50%;display:inline-block;"></span>
        {L['online_now']}: <strong style="color:#a2ff00;">{active_node_count}</strong>
        &nbsp;·&nbsp;
        {L['total_sessions']}: <strong style="color:#e8edf2;">{total_sessions_display}</strong>
    </div>
    """, unsafe_allow_html=True)

with col_right:
    st.markdown(f'<div style="text-align:right;padding-top:8px;"><span class="nx-stage-badge">{L["stage"]}</span></div>', unsafe_allow_html=True)
    if st.button(L["lang_btn"], key="lang_toggle"):
        st.session_state.lang = "ZH" if st.session_state.lang == "EN" else "EN"
        st.rerun()

st.markdown('<hr style="border-color:#1a2530;margin:8px 0 10px 0;">', unsafe_allow_html=True)

current_tab = st.radio("Nav", L["nav"], horizontal=True, label_visibility="collapsed")

# ══════════════════════════════════════
# TAB 1 — MARKET
# ══════════════════════════════════════
if current_tab == L["nav"][0]:
    real_cpu = psutil.cpu_percent()
    c1, c2, c3 = st.columns(3)
    with c1: st.metric("Local Node CPU Load", f"{real_cpu}%", "Real-time Telemetry")
    with c2: st.metric("6.8B" if st.session_state.lang=="EN" else "全球闲置智能手机", "6.8B" if st.session_state.lang=="EN" else "68亿", "NPU Target Market" if st.session_state.lang=="EN" else "NPU目标市场")
    with c3: st.metric("Edge AI Market (2028)", "$107B", "CAGR 19.2%")

    if st.session_state.lang == "EN":
        st.markdown(f"""
        <div class="nx-card">
            <div class="nx-card-title"><span>▸</span> {L['comp_title']}</div>
            <table class="nx-table">
                <thead><tr><th>Dimension</th><th>Centralized GPU Cloud</th><th>Grass (Bandwidth)</th><th class="hl">NexaEdge</th></tr></thead>
                <tbody>
                    <tr><td>CapEx</td><td><span class="tag-bad">EXTREME</span> H100 scarce &amp; costly</td><td>Low (bandwidth proxy)</td><td class="hl"><span class="tag-good">ZERO</span> User-owned devices</td></tr>
                    <tr><td>Latency</td><td><span class="tag-bad">50–150ms</span> datacenter roundtrip</td><td>N/A (not compute)</td><td class="hl"><span class="tag-good">&lt;5ms</span> On-device edge</td></tr>
                    <tr><td>Privacy</td><td><span class="tag-bad">Data leaves device</span></td><td>Partial</td><td class="hl"><span class="tag-good">GDPR-native</span> Local processing</td></tr>
                    <tr><td>Geographic reach</td><td>Few datacenters</td><td>High (IPs)</td><td class="hl"><span class="tag-good">Global</span> Every city &amp; rural</td></tr>
                    <tr><td>Compute layer</td><td>GPU (training-grade)</td><td><span class="tag-bad">Network only</span></td><td class="hl"><span class="tag-good">NPU + CPU</span> On-device inference</td></tr>
                    <tr><td>Sybil resistance</td><td>Centralized auth</td><td><span class="tag-bad">IP spoofable</span></td><td class="hl"><span class="tag-good">Hardware fingerprint + ZK</span></td></tr>
                </tbody>
            </table>
        </div>""", unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="nx-card">
            <div class="nx-card-title"><span>▸</span> {L['comp_title']}</div>
            <table class="nx-table">
                <thead><tr><th>维度</th><th>中心化GPU云</th><th>Grass（带宽）</th><th class="hl">NexaEdge</th></tr></thead>
                <tbody>
                    <tr><td>资本支出</td><td><span class="tag-bad">极高</span> H100 稀缺且昂贵</td><td>低（带宽代理）</td><td class="hl"><span class="tag-good">零</span> 用户自有设备</td></tr>
                    <tr><td>延迟</td><td><span class="tag-bad">50–150ms</span> 数据中心往返</td><td>不适用</td><td class="hl"><span class="tag-good">&lt;5ms</span> 设备本地</td></tr>
                    <tr><td>隐私</td><td><span class="tag-bad">数据离开设备</span></td><td>部分</td><td class="hl"><span class="tag-good">GDPR原生</span> 本地处理</td></tr>
                    <tr><td>地理覆盖</td><td>少数数据中心</td><td>高（IP数量）</td><td class="hl"><span class="tag-good">全球</span> 城市与农村全覆盖</td></tr>
                    <tr><td>算力层</td><td>GPU（训练级）</td><td><span class="tag-bad">仅网络</span></td><td class="hl"><span class="tag-good">NPU + CPU</span> 设备端推理</td></tr>
                    <tr><td>女巫攻击抵抗</td><td>中心化认证</td><td><span class="tag-bad">IP可伪造</span></td><td class="hl"><span class="tag-good">硬件指纹 + ZK</span></td></tr>
                </tbody>
            </table>
        </div>""", unsafe_allow_html=True)

    st.markdown(f'<div class="nx-card"><div class="nx-card-title"><span>▸</span> {L["buyer_title"]}</div>', unsafe_allow_html=True)
    b1, b2 = st.columns(2)
    if st.session_state.lang == "EN":
        with b1:
            st.markdown("""
            <div class="nx-feature"><div class="nx-feature-title">🤖 Edge AI Agent Deployers</div><div class="nx-feature-body">Run 1.8B–3.8B parameter SLMs (Phi-3, Gemma) with sub-5ms local inference. No data leaves device — GDPR compliant by architecture.</div><div class="nx-feature-buyer">→ AI app developers, enterprise SaaS</div></div>
            <div class="nx-feature"><div class="nx-feature-title">🧹 AI Dataset Cleaning (RLHF)</div><div class="nx-feature-body">Distributed WASM sandbox runs automated labeling and cross-validation of AI training corpora across thousands of nodes simultaneously.</div><div class="nx-feature-buyer">→ AI labs, data pipeline companies</div></div>
            """, unsafe_allow_html=True)
        with b2:
            st.markdown("""
            <div class="nx-feature"><div class="nx-feature-title">🔐 ZK-ML Inference Verification</div><div class="nx-feature-body">Fragment AI inference proofs across independent nodes. Redundant verification prevents result tampering — no single point of trust.</div><div class="nx-feature-buyer">→ DeFi protocols, compliance platforms</div></div>
            <div class="nx-feature"><div class="nx-feature-title">📡 Sensor-Context AI</div><div class="nx-feature-body">Leverage unique smartphone hardware — GPS, camera, IMU — for context-aware inference unavailable in any datacenter.</div><div class="nx-feature-buyer">→ Location AI, autonomous systems</div></div>
            """, unsafe_allow_html=True)
    else:
        with b1:
            st.markdown("""
            <div class="nx-feature"><div class="nx-feature-title">🤖 边缘AI代理部署者</div><div class="nx-feature-body">运行1.8B–3.8B参数SLM，本地推理延迟低于5ms。数据不离开设备，架构层面符合GDPR。</div><div class="nx-feature-buyer">→ AI应用开发者、企业SaaS</div></div>
            <div class="nx-feature"><div class="nx-feature-title">🧹 AI数据集清洗（RLHF）</div><div class="nx-feature-body">分布式WASM沙箱在数千节点上同步运行自动标注与交叉验证。</div><div class="nx-feature-buyer">→ AI实验室、数据管道公司</div></div>
            """, unsafe_allow_html=True)
        with b2:
            st.markdown("""
            <div class="nx-feature"><div class="nx-feature-title">🔐 ZK-ML推理验证</div><div class="nx-feature-body">将AI推理证明分散到独立节点，冗余验证防止结果篡改，无单点信任风险。</div><div class="nx-feature-buyer">→ DeFi协议、合规平台</div></div>
            <div class="nx-feature"><div class="nx-feature-title">📡 传感器上下文AI</div><div class="nx-feature-body">利用智能手机独有硬件——GPS、摄像头、IMU——实现数据中心无法提供的上下文感知推理。</div><div class="nx-feature-buyer">→ 位置AI、自主系统</div></div>
            """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    d, c, s = L["demand_side"], L["coordination"], L["supply_side"]
    arch_body_en = ["Submit inference tasks via API. Pay in NEXA per compute unit.", "Task routing, BFT consensus, reward settlement. Low gas, high TPS.", "WASM sandbox on idle devices. NPU executes inference. Proof submitted on-chain."]
    arch_body_zh = ["通过API提交推理任务，按算力单位支付NEXA代币。", "任务路由、BFT共识、奖励结算。低gas，高TPS。", "闲置设备上的WASM沙箱，NPU执行推理，证明上链。"]
    arch_body = arch_body_en if st.session_state.lang == "EN" else arch_body_zh
    arch_titles = (["AI Buyers", "Solana SPL", "Device Nodes"] if st.session_state.lang == "EN" else ["AI买家", "Solana SPL", "设备节点"])
    arch_icons = ["🏢", "⛓", "📱"]
    arch_labels = [d, c, s]
    arch_html = '<div style="display:flex;align-items:stretch;gap:0;">'
    for i in range(3):
        arch_html += f'<div style="flex:1;background:#060a0d;border:1px solid #1a2530;border-radius:8px;padding:14px;text-align:center;"><div style="font-family:\'Space Mono\',monospace;font-size:9px;color:#556070;text-transform:uppercase;margin-bottom:8px;">{arch_labels[i]}</div><div style="font-size:22px;margin-bottom:6px;">{arch_icons[i]}</div><div style="font-size:12px;font-weight:700;color:#e8edf2;margin-bottom:4px;">{arch_titles[i]}</div><div style="font-size:10px;color:#556070;line-height:1.5;">{arch_body[i]}</div></div>'
        if i < 2:
            arch_html += '<div style="display:flex;align-items:center;padding:0 8px;color:#a2ff00;font-size:18px;">→</div>'
    arch_html += '</div>'
    st.markdown(f'<div class="nx-card"><div class="nx-card-title"><span>▸</span> {L["arch_title"]}</div>{arch_html}</div>', unsafe_allow_html=True)

    # 投资入口
    st.markdown(f"### 🏛️ {L['invest_title']}")
    ci1, ci2 = st.columns([2, 1])
    with ci1:
        st.markdown(f'<div style="font-size:12px;color:#556070;line-height:1.6;">{L["invest_desc"]}</div>', unsafe_allow_html=True)
    with ci2:
        if st.button(L["invest_btn"], key="invest_btn"):
            st.warning(L["invest_warn"])

    st.markdown("""
    <div class="nx-social-grid">
        <a class="nx-social-btn" href="https://www.instagram.com/nexaedge__" target="_blank">📸 Instagram</a>
        <a class="nx-social-btn" href="https://x.com/nexaedge_" target="_blank">🐦 X / Twitter</a>
        <a class="nx-social-btn" href="https://www.facebook.com/share/18eXN6P3Ge/" target="_blank">👥 Facebook</a>
        <a class="nx-social-btn" href="https://www.tiktok.com/@nexaedge7" target="_blank">🎵 TikTok</a>
        <a class="nx-social-btn" href="https://t.me/NexaEdge7" target="_blank">📢 Telegram</a>
        <a class="nx-social-btn" href="mailto:contact@nexaedge.org" style="border-color:#00e5ff;color:#00e5ff !important;">📧 Email</a>
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════
# TAB 2 — NETWORK SIM
# ══════════════════════════════════════
elif current_tab == L["nav"][1]:
    st.markdown(f'<div class="nx-notice">{L["sim_only"]}</div>', unsafe_allow_html=True)

    b_start, b_stop, col_status = st.columns([2, 2, 3])
    with b_start:
        if st.button(L["start_sim"], disabled=st.session_state.sim_running):
            st.session_state.sim_running = True
            st.session_state.sim_tasks = 0
            st.session_state.sim_log = []
            st.session_state.sim_nodes = [0] * 64
            st.session_state.nexa_earned = 0.0
            st.session_state.nexa_rate = 0.0
            st.session_state.prog1 = 0
            st.session_state.prog2 = 0
            st.session_state.prog3 = 0
            st.rerun()
    with b_stop:
        if st.button(L["stop_sim"], disabled=not st.session_state.sim_running, type="secondary"):
            st.session_state.sim_running = False
            st.session_state.sim_nodes = [0] * 64
            st.rerun()
    with col_status:
        status_color = "#a2ff00" if st.session_state.sim_running else "#556070"
        status_text = L["running"] if st.session_state.sim_running else L["idle"]
        st.markdown(f'<div style="font-family:\'Space Mono\',monospace;font-size:10px;color:{status_color};padding-top:10px;">{status_text}</div>', unsafe_allow_html=True)

    nodes = st.session_state.sim_nodes
    node_html = f'<div class="nx-card"><div class="nx-card-title"><span>▸</span> {L["node_grid_title"]}</div><div class="nx-node-grid">'
    for v in nodes:
        cls = {0: "", 1: " active", 2: " processing"}.get(v, "")
        node_html += f'<div class="nx-node{cls}"></div>'
    node_html += f"""</div>
    <div style="display:flex;gap:16px;margin-top:10px;">
        <span style="font-size:10px;color:#556070;font-family:'Space Mono',monospace;display:flex;align-items:center;gap:5px;"><span style="width:10px;height:10px;background:#1a2530;border-radius:2px;display:inline-block;"></span> {L['idle_label']}</span>
        <span style="font-size:10px;color:#a2ff00;font-family:'Space Mono',monospace;display:flex;align-items:center;gap:5px;"><span style="width:10px;height:10px;background:#a2ff00;border-radius:2px;display:inline-block;"></span> {L['active_label']}</span>
        <span style="font-size:10px;color:#00e5ff;font-family:'Space Mono',monospace;display:flex;align-items:center;gap:5px;"><span style="width:10px;height:10px;background:#00e5ff;border-radius:2px;display:inline-block;"></span> {L['processing_label']}</span>
    </div></div>"""
    st.markdown(node_html, unsafe_allow_html=True)

    active_count = sum(1 for v in nodes if v > 0)
    latency_val = f"{st.session_state.sim_latency:.1f}ms" if st.session_state.sim_running else "—"
    consensus_val = f"{st.session_state.sim_consensus:.1f}%" if st.session_state.sim_running else "—"
    nexa_val = f"{st.session_state.nexa_earned:.4f}" if (st.session_state.sim_running or st.session_state.nexa_earned > 0) else "—"
    nexa_rate_val = f"{st.session_state.nexa_rate:.4f}" if st.session_state.sim_running else "—"

    s1,s2,s3,s4,s5,s6 = st.columns(6)
    for col, val, lbl, cls in [
        (s1, active_count, L["active_nodes"], ""),
        (s2, st.session_state.sim_tasks, L["tasks_done"], ""),
        (s3, latency_val, L["avg_latency"], " cyan"),
        (s4, consensus_val, L["bft_consensus"], " cyan"),
        (s5, nexa_val, L["nexa_earned"], " gold"),
        (s6, nexa_rate_val, L["nexa_per_task"], " gold"),
    ]:
        with col:
            st.markdown(f'<div class="nx-sim-stat"><div class="nx-sim-val{cls}">{val}</div><div class="nx-sim-label">{lbl}</div></div>', unsafe_allow_html=True)

    if st.session_state.sim_running or st.session_state.nexa_earned > 0:
        usd_val = st.session_state.nexa_earned * 0.50
        st.markdown(f"""
        <div class="nx-card" style="border-color:rgba(255,179,0,0.2);background:rgba(255,179,0,0.02);">
            <div class="nx-card-title"><span style="color:#ffb300;">◈</span> {L['nexa_proj_title']}</div>
            <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:10px;">
                <div style="background:#060a0d;border:1px solid #1a2530;border-radius:8px;padding:12px;text-align:center;">
                    <div style="font-family:'Space Mono',monospace;font-size:9px;color:#556070;text-transform:uppercase;margin-bottom:4px;">{L['nexa_sim_earned']}</div>
                    <div style="font-family:'Space Mono',monospace;font-size:14px;font-weight:700;color:#ffb300;">{st.session_state.nexa_earned:.4f} NEXA</div>
                </div>
                <div style="background:#060a0d;border:1px solid #1a2530;border-radius:8px;padding:12px;text-align:center;">
                    <div style="font-family:'Space Mono',monospace;font-size:9px;color:#556070;text-transform:uppercase;margin-bottom:4px;">{L['nexa_est_usd']}</div>
                    <div style="font-family:'Space Mono',monospace;font-size:14px;font-weight:700;color:#ffb300;">${usd_val:.4f}</div>
                </div>
                <div style="background:#060a0d;border:1px solid #1a2530;border-radius:8px;padding:12px;text-align:center;">
                    <div style="font-family:'Space Mono',monospace;font-size:9px;color:#556070;text-transform:uppercase;margin-bottom:4px;">{L['nexa_supply']}</div>
                    <div style="font-family:'Space Mono',monospace;font-size:14px;font-weight:700;color:#ffb300;">100,000,000</div>
                </div>
            </div>
            <div style="font-family:'Space Mono',monospace;font-size:9px;color:#556070;margin-top:10px;line-height:1.7;">{L['nexa_disclaimer']}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown(f'<div class="nx-card"><div class="nx-card-title"><span>▸</span> {L["task_log_title"]}</div>', unsafe_allow_html=True)
    if st.session_state.sim_log:
        log_html = '<div class="nx-log">'
        for line, cls in st.session_state.sim_log:
            log_html += f'<div class="log-{cls}">{line}</div>'
        log_html += '</div>'
    else:
        log_html = f'<div class="nx-log"><div>{L["log_empty"]}</div></div>'
    st.markdown(log_html + '</div>', unsafe_allow_html=True)

    p1, p2, p3 = st.session_state.prog1, st.session_state.prog2, st.session_state.prog3
    st.markdown(f"""
    <div class="nx-card">
        <div class="nx-card-title"><span>▸</span> {L['workload_title']}</div>
        <div class="nx-prog-label"><span>{L['wl_inference']}</span><span>{p1}%</span></div>
        <div class="nx-prog-bar"><div class="nx-prog-fill" style="width:{p1}%"></div></div>
        <div class="nx-prog-label"><span>{L['wl_rlhf']}</span><span>{p2}%</span></div>
        <div class="nx-prog-bar"><div class="nx-prog-fill blue" style="width:{p2}%"></div></div>
        <div class="nx-prog-label"><span>{L['wl_zk']}</span><span>{p3}%</span></div>
        <div class="nx-prog-bar"><div class="nx-prog-fill" style="width:{p3}%"></div></div>
    </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════
# TAB 3 — DIFFERENTIATION
# ══════════════════════════════════════
elif current_tab == L["nav"][2]:
    if st.session_state.lang == "EN":
        st.markdown(f"""
        <div class="nx-card">
            <div class="nx-card-title"><span>▸</span> {L['diff_title']}</div>
            <table class="nx-table">
                <thead><tr><th>Dimension</th><th>Grass</th><th class="hl">NexaEdge</th></tr></thead>
                <tbody>
                    <tr><td>Core resource</td><td>Network bandwidth (residential proxy)</td><td class="hl">Device compute (CPU + NPU)</td></tr>
                    <tr><td>Primary use case</td><td>Web scraping / data collection</td><td class="hl">AI inference, RLHF, ZK-ML verification</td></tr>
                    <tr><td>Sybil resistance</td><td><span class="tag-bad">HIGH RISK</span> IP spoofed via VPN</td><td class="hl"><span class="tag-good">LOW RISK</span> Hardware fingerprint + PoC</td></tr>
                    <tr><td>Compute verification</td><td>None (bandwidth only)</td><td class="hl">BFT consensus + ZK proof of inference</td></tr>
                    <tr><td>Solana Mobile synergy</td><td>None</td><td class="hl"><span class="tag-good">NATIVE</span> Seeker / Saga system daemon</td></tr>
                </tbody>
            </table>
        </div>""", unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="nx-card">
            <div class="nx-card-title"><span>▸</span> {L['diff_title']}</div>
            <table class="nx-table">
                <thead><tr><th>维度</th><th>Grass</th><th class="hl">NexaEdge</th></tr></thead>
                <tbody>
                    <tr><td>核心资源</td><td>网络带宽（住宅代理）</td><td class="hl">设备算力（CPU + NPU）</td></tr>
                    <tr><td>主要用途</td><td>网页抓取 / 数据采集</td><td class="hl">AI推理、RLHF、ZK-ML验证</td></tr>
                    <tr><td>女巫攻击抵抗</td><td><span class="tag-bad">高风险</span> VPN伪造IP</td><td class="hl"><span class="tag-good">低风险</span> 硬件指纹 + PoC</td></tr>
                    <tr><td>算力验证</td><td>无（仅带宽）</td><td class="hl">BFT共识 + ZK推理结果证明</td></tr>
                    <tr><td>Solana Mobile协同</td><td>无</td><td class="hl"><span class="tag-good">原生</span> Seeker / Saga 守护进程</td></tr>
                </tbody>
            </table>
        </div>""", unsafe_allow_html=True)

    st.markdown(f'<div class="nx-card"><div class="nx-card-title"><span>▸</span> {L["moat_title"]}</div>', unsafe_allow_html=True)
    m1, m2 = st.columns(2)
    if st.session_state.lang == "EN":
        with m1:
            st.markdown("""
            <div class="nx-moat"><div class="nx-moat-icon">🔐</div><div class="nx-moat-title">Proof of Compute (PoC)</div><div class="nx-moat-body">Every node must solve a cryptographic ML inference puzzle to claim rewards. Hardware fingerprint + ZK proof prevents Sybil attacks.</div></div>
            <div class="nx-moat" style="margin-top:10px;"><div class="nx-moat-icon">🌍</div><div class="nx-moat-title">Geographic Density</div><div class="nx-moat-body">6.8B smartphones vs. a few thousand datacenters. NexaEdge reaches rural markets and ultra-local use cases no cloud can serve.</div></div>
            """, unsafe_allow_html=True)
        with m2:
            st.markdown("""
            <div class="nx-moat"><div class="nx-moat-icon">🧠</div><div class="nx-moat-title">NPU-Native Execution</div><div class="nx-moat-body">Modern smartphones (A-series, Snapdragon) have dedicated NPUs. NexaEdge targets these for SLM inference — energy rivals server GPUs for small models.</div></div>
            <div class="nx-moat" style="margin-top:10px;"><div class="nx-moat-icon">📱</div><div class="nx-moat-title">Solana Mobile Integration</div><div class="nx-moat-body">Solana Seeker / Saga are the only Web3-native phones. NexaEdge becomes the killer app that makes hardware ROI-positive.</div></div>
            """, unsafe_allow_html=True)
    else:
        with m1:
            st.markdown("""
            <div class="nx-moat"><div class="nx-moat-icon">🔐</div><div class="nx-moat-title">算力证明（PoC）</div><div class="nx-moat-body">每个节点必须解决加密ML推理难题才能领取奖励。硬件指纹+ZK证明防止女巫攻击。</div></div>
            <div class="nx-moat" style="margin-top:10px;"><div class="nx-moat-icon">🌍</div><div class="nx-moat-title">地理密度</div><div class="nx-moat-body">68亿部智能手机对比数千个数据中心。NexaEdge覆盖农村市场及任何云端无法服务的超本地场景。</div></div>
            """, unsafe_allow_html=True)
        with m2:
            st.markdown("""
            <div class="nx-moat"><div class="nx-moat-icon">🧠</div><div class="nx-moat-title">NPU原生执行</div><div class="nx-moat-body">现代智能手机（A系列、骁龙）配备专用NPU。NexaEdge将其用于SLM推理，小模型能耗媲美旧款服务器GPU。</div></div>
            <div class="nx-moat" style="margin-top:10px;"><div class="nx-moat-icon">📱</div><div class="nx-moat-title">Solana Mobile集成</div><div class="nx-moat-body">Solana Seeker/Saga是唯一的Web3原生手机。NexaEdge成为使硬件投资回报为正的杀手级应用。</div></div>
            """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    thermal_en = """The 39°C thermal ceiling is a hardcoded daemon constraint, not a marketing claim.<br>
        If device temperature ≥ 39°C → task queue paused → passive cooling mode activated.<br>
        Enforced at the WASM sandbox level — not overridable by the user.<br><br>
        <span style="color:#e8edf2;font-weight:600;">Why this matters to buyers:</span>
        Institutional compute buyers need SLA guarantees. A network that destroys user hardware cannot maintain supply. The 39°C protocol is the supply-side durability guarantee."""
    thermal_zh = """39°C 热限是硬编码的守护进程约束，而非营销口号。<br>
        设备温度 ≥ 39°C → 任务队列暂停 → 激活被动散热模式。<br>
        在 WASM 沙箱层面强制执行——用户不可覆盖。<br><br>
        <span style="color:#e8edf2;font-weight:600;">对买家的意义：</span>
        机构算力买家需要SLA保证。损毁用户硬件的网络无法维持供给。39°C协议是供给侧的耐久性保障。"""
    st.markdown(f"""
    <div class="nx-card">
        <div class="nx-card-title"><span>▸</span> {L['thermal_title']}</div>
        <div style="font-size:12px;color:#556070;line-height:1.9;">{thermal_en if st.session_state.lang=="EN" else thermal_zh}</div>
    </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════
# TAB 4 — ROADMAP & FUNDING
# ══════════════════════════════════════
elif current_tab == L["nav"][3]:
    if st.session_state.lang == "EN":
        st.markdown(f"""
        <div class="nx-card">
            <div class="nx-card-title"><span>▸</span> {L['roadmap_title']}</div>
            <div class="nx-roadmap-item current">
                <div class="nx-roadmap-phase">Q2 2026 · NOW · IN REVIEW</div>
                <div class="nx-roadmap-title">Concept Validation & Institutional Acceleration</div>
                <div class="nx-roadmap-body">Architecture design finalized. Whitepaper drafted. Accelerating: <strong>Solana Grant</strong>, <strong>Alliance DAO</strong>, <strong>Y Combinator</strong> in active pipeline. Building global node waitlist. Post-money SAFE ($5M cap) framework initialized via AngelList Rollup.</div>
            </div>
            <div class="nx-roadmap-item">
                <div class="nx-roadmap-phase">Q3 2026</div>
                <div class="nx-roadmap-title">WASM Sandbox MVP</div>
                <div class="nx-roadmap-body">Functional WASM execution on iOS / Android. First real SLM inference (Phi-3 mini) on device NPU. Thermal guard daemon. Internal alpha: 50 devices.</div>
            </div>
            <div class="nx-roadmap-item">
                <div class="nx-roadmap-phase">Q4 2026</div>
                <div class="nx-roadmap-title">Closed Beta — 1,000 Nodes</div>
                <div class="nx-roadmap-body">Solana SPL token deployment. BFT consensus testnet. First paying buyer pilot. ZK proof of compute live.</div>
            </div>
            <div class="nx-roadmap-item">
                <div class="nx-roadmap-phase">Q1 2027</div>
                <div class="nx-roadmap-title">Public Mainnet Launch</div>
                <div class="nx-roadmap-body">Open node enrollment. Solana Seeker native integration. Marketplace live. Target: 100,000 active nodes, 3 enterprise buyers.</div>
            </div>
            <div class="nx-roadmap-item" style="padding-bottom:0;">
                <div class="nx-roadmap-phase">2027+</div>
                <div class="nx-roadmap-title">Scale & Ecosystem</div>
                <div class="nx-roadmap-body">ZK-ML verification product live. Expand to laptop / IoT. Series A targeting $15M.</div>
            </div>
        </div>""", unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="nx-card">
            <div class="nx-card-title"><span>▸</span> {L['roadmap_title']}</div>
            <div class="nx-roadmap-item current">
                <div class="nx-roadmap-phase">2026年Q2 · 当前 · 审核中</div>
                <div class="nx-roadmap-title">概念验证与机构加速</div>
                <div class="nx-roadmap-body">架构设计定稿。白皮书起草完成。<strong>Solana Grant</strong>、<strong>Alliance DAO</strong>、<strong>Y Combinator</strong> 积极推进中。全球节点候补名单建设中。AngelList Rollup Post-money SAFE（$500万估值上限）框架已初始化。</div>
            </div>
            <div class="nx-roadmap-item">
                <div class="nx-roadmap-phase">2026年Q3</div>
                <div class="nx-roadmap-title">WASM 沙箱 MVP</div>
                <div class="nx-roadmap-body">iOS/Android 上的 WASM 执行环境。首个真实 SLM 推理（Phi-3 mini）在设备 NPU 上运行。热保护守护进程实现。内部 alpha：50 台设备。</div>
            </div>
            <div class="nx-roadmap-item">
                <div class="nx-roadmap-phase">2026年Q4</div>
                <div class="nx-roadmap-title">封闭测试——1,000 节点</div>
                <div class="nx-roadmap-body">Solana SPL 代币部署。BFT 共识测试网。首个付费买家试点。设备指纹 + ZK 算力证明上线。</div>
            </div>
            <div class="nx-roadmap-item">
                <div class="nx-roadmap-phase">2027年Q1</div>
                <div class="nx-roadmap-title">公开主网上线</div>
                <div class="nx-roadmap-body">开放节点注册。Solana Seeker 原生集成。市场上线。目标：10万活跃节点、3个企业买家。</div>
            </div>
            <div class="nx-roadmap-item" style="padding-bottom:0;">
                <div class="nx-roadmap-phase">2027年+</div>
                <div class="nx-roadmap-title">规模扩张与生态</div>
                <div class="nx-roadmap-body">ZK-ML 验证产品上线。扩展至笔记本/IoT。A轮融资目标 1500 万美元。</div>
            </div>
        </div>""", unsafe_allow_html=True)

    r1, r2, r3 = st.columns(3)
    if st.session_state.lang == "EN":
        with r1: st.metric("Funding Target (Seed)", "$500K", "for MVP + 1,000-node beta")
        with r2: st.metric("Target Nodes (Y1)", "100K", "active devices at mainnet")
        with r3: st.metric("Settlement Chain", "Solana SPL", "low gas · high TPS")
    else:
        with r1: st.metric("融资目标（种子轮）", "$500K", "用于MVP+1000节点测试")
        with r2: st.metric("目标节点数（第1年）", "100K", "主网活跃设备")
        with r3: st.metric("结算链", "Solana SPL", "低gas · 高TPS")

    st.markdown(f"""
    <div class="nx-card" style="border-color:rgba(255,179,0,0.2);background:rgba(255,179,0,0.02);">
        <div class="nx-card-title"><span style="color:#ffb300;">◈</span> {L['nexa_proj_title']}</div>
        <div style="font-size:11px;color:#556070;line-height:1.7;">{L['nexa_disclaimer']}</div>
    </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════
# TAB 5 — WHITELIST（全局持久化存储）
# ══════════════════════════════════════
elif current_tab == L["nav"][4]:
    total_reg = len(global_db["registrations"])

    st.markdown(f"""
    <div class="nx-card">
        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:16px;">
            <div>
                <div style="font-size:18px;font-weight:800;color:#e8edf2;margin-bottom:4px;">{L['wl_title']}</div>
                <div style="font-size:12px;color:#556070;line-height:1.6;">{L['wl_desc']}</div>
            </div>
            <div style="background:#060a0d;border:1px solid #1a2530;border-radius:8px;padding:10px 16px;text-align:center;min-width:110px;">
                <div style="font-family:'Space Mono',monospace;font-size:8px;color:#556070;text-transform:uppercase;">{L['wl_total']}</div>
                <div style="font-family:'Space Mono',monospace;font-size:28px;font-weight:700;color:#a2ff00;">{total_reg}</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    if st.session_state.wl_success:
        ref = st.session_state.wl_ref_code
        st.markdown(f"""
        <div class="nx-success-box">
            <div style="font-size:18px;font-weight:800;color:#a2ff00;margin-bottom:8px;">{L['wl_success_title']}</div>
            <div style="font-size:12px;color:#556070;line-height:1.7;margin-bottom:16px;">{L['wl_success_desc']}</div>
            <div style="background:#060a0d;border:1px solid rgba(162,255,0,0.3);border-radius:8px;padding:16px;">
                <div style="font-family:'Space Mono',monospace;font-size:9px;color:#556070;text-transform:uppercase;margin-bottom:6px;">{L['wl_your_ref']}</div>
                <div class="nx-ref-code">{ref}</div>
            </div>
        </div>""", unsafe_allow_html=True)
        copy_lbl = L["wl_copied"] if st.session_state.wl_copied else L["wl_copy"]
        if st.button(copy_lbl, key="copy_ref_btn"):
            st.session_state.wl_copied = True
            st.rerun()
    else:
        with st.form("wl_form_secure"):
            email_in = st.text_input(L["wl_email"], placeholder=L["wl_email_ph"])
            wallet_in = st.text_input(L["wl_wallet"], placeholder=L["wl_wallet_ph"])
            ref_in = st.text_input(L["wl_ref"], placeholder=L["wl_ref_ph"])
            submitted = st.form_submit_button(L["wl_submit"])

            if submitted:
                errors = []
                if not email_in or not re.match(r'^[^\s@]+@[^\s@]+\.[^\s@]+$', email_in):
                    errors.append(L["err_email"])
                if not wallet_in or not (32 <= len(wallet_in) <= 44):
                    errors.append(L["err_wallet"])
                if email_in.lower() in global_db["whitelisted_emails"]:
                    errors.append(L["err_dupe"])
                if errors:
                    for e in errors:
                        st.error(e)
                else:
                    chars = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"
                    ref_code = "NX-" + "".join(random.choices(chars, k=6))
                    entry = {
                        "email": email_in.lower(),
                        "wallet": wallet_in,
                        "ref_code": ref_code,
                        "used_ref": ref_in or "—",
                        "lang": st.session_state.lang,
                        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                    }
                    global_db["registrations"].append(entry)
                    global_db["whitelisted_emails"].add(email_in.lower())
                    st.session_state.wl_success = True
                    st.session_state.wl_ref_code = ref_code
                    st.rerun()

        st.markdown(f"""
        <div style="font-family:'Space Mono',monospace;font-size:9px;color:#2a3540;text-align:center;line-height:1.6;margin-top:10px;">
            {"By registering you confirm this is a concept demo. No tokens are issued. No investment contract is formed." if st.session_state.lang=='EN' else "注册即表明您了解这是概念演示。不发行代币，不构成投资合同。"}
        </div>""", unsafe_allow_html=True)

    # 显示已哈希的账本指纹（增强现场感）
    if global_db["registrations"]:
        st.markdown(f"### {L['ledger_title']}")
        ledger_rows = [
            {"Timestamp": r["timestamp"],
             "Node Hash Identity": hashlib.sha256(r["email"].encode()).hexdigest()[:20] + "... @SPL"}
            for r in global_db["registrations"]
        ]
        st.dataframe(ledger_rows, use_container_width=True, hide_index=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════
# FOOTER + 隐藏后台管理（折叠入口）
# ══════════════════════════════════════
st.markdown("""
<div class="nx-footer">
    NexaEdge Network · Pre-Launch Concept Demo · All simulations are illustrative only.<br>
    No tokens issued · No investment contract · contact@nexaedge.org<br>
    © 2026 NexaEdge Network. All rights reserved.
</div>
""", unsafe_allow_html=True)

with st.expander(L["admin_title"], expanded=False):
    if not st.session_state.admin_logged_in:
        pw = st.text_input("", type="password", placeholder=L["admin_pw_ph"], key="admin_pw_input", label_visibility="collapsed")
        if st.button(L["admin_login"], key="admin_login_btn"):
            if pw == ADMIN_PASSWORD:
                st.session_state.admin_logged_in = True
                st.session_state.admin_error = False
                st.rerun()
            else:
                st.session_state.admin_error = True
        if st.session_state.admin_error:
            st.error(L["admin_wrong"])
    else:
        st.markdown(f'<div style="color:#a2ff00;font-family:\'Space Mono\',monospace;font-size:12px;font-weight:700;margin-bottom:14px;">{L["admin_header"]}</div>', unsafe_allow_html=True)

        regs = global_db["registrations"]
        ac1, ac2, ac3 = st.columns(3)
        with ac1: st.metric("Total Registrations", len(regs))
        with ac2: st.metric("Online Nodes (Est.)", active_node_count)
        with ac3: st.metric("Total Sessions", total_sessions_display)

        if regs:
            rows_html = ""
            for i, r in enumerate(regs):
                rows_html += f"""<tr>
                    <td>{i+1}</td><td>{r['email']}</td>
                    <td style="max-width:130px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">{r['wallet']}</td>
                    <td><span class="admin-badge">{r['ref_code']}</span></td>
                    <td>{r.get('used_ref','—')}</td>
                    <td>{r.get('lang','')}</td>
                    <td style="color:#556070;">{r['timestamp']}</td>
                </tr>"""
            st.markdown(f"""
            <div class="nx-card" style="overflow-x:auto;">
                <div class="nx-card-title"><span>▸</span> Whitelist Registrations</div>
                <table class="admin-table">
                    <thead><tr><th>#</th><th>Email</th><th>Solana Wallet</th><th>Ref Code</th><th>Used Ref</th><th>Lang</th><th>Timestamp</th></tr></thead>
                    <tbody>{rows_html}</tbody>
                </table>
            </div>""", unsafe_allow_html=True)

            csv_lines = ["#,Email,Wallet,RefCode,UsedRef,Lang,Timestamp"]
            for i, r in enumerate(regs):
                csv_lines.append(f"{i+1},{r['email']},{r['wallet']},{r['ref_code']},{r.get('used_ref','')},{r.get('lang','')},{r['timestamp']}")
            st.download_button(
                label=L["admin_export"],
                data="\n".join(csv_lines),
                file_name="nexaedge_whitelist.csv",
                mime="text/csv",
                key="dl_csv"
            )
        else:
            st.info(L["admin_empty"])

        if st.button(L["admin_logout"], key="admin_logout_btn"):
            st.session_state.admin_logged_in = False
            st.rerun()
