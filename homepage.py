import streamlit as st
import time
import random
import pandas as pd

st.set_page_config(
    page_title="NexaEdge Network — Investor Demo",
    page_icon="🟢",
    layout="centered"
)

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

/* Grid background */
.stApp::before {
    content: '';
    position: fixed;
    inset: 0;
    background-image:
        linear-gradient(rgba(162,255,0,0.025) 1px, transparent 1px),
        linear-gradient(90deg, rgba(162,255,0,0.025) 1px, transparent 1px);
    background-size: 40px 40px;
    pointer-events: none;
    z-index: 0;
}

/* Typography */
h1, h2, h3, h4, p, div, span, label {
    font-family: 'Syne', sans-serif !important;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    gap: 6px;
    background-color: transparent !important;
    border-bottom: 1px solid #1a2530 !important;
    margin-bottom: 20px;
}
.stTabs [data-baseweb="tab"] {
    background-color: #0e1419 !important;
    color: #556070 !important;
    border-radius: 6px 6px 0 0 !important;
    border: 1px solid #1a2530 !important;
    border-bottom: none !important;
    padding: 8px 16px !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 11px !important;
    font-weight: 700 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.05em !important;
}
.stTabs [aria-selected="true"] {
    color: #a2ff00 !important;
    background-color: #0e1419 !important;
    border-bottom-color: #0e1419 !important;
}
.stTabs [data-baseweb="tab-highlight"] { display: none !important; }

/* Metrics */
[data-testid="stMetric"] {
    background: #0e1419;
    border: 1px solid #1a2530;
    border-radius: 10px;
    padding: 14px !important;
}
[data-testid="stMetricLabel"] {
    font-family: 'Space Mono', monospace !important;
    font-size: 9px !important;
    color: #556070 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.08em !important;
}
[data-testid="stMetricValue"] {
    font-size: 22px !important;
    font-weight: 800 !important;
    color: #e8edf2 !important;
}
[data-testid="stMetricDelta"] { font-size: 10px !important; }

/* Buttons */
div.stButton > button {
    background-color: #a2ff00 !important;
    color: #080c0f !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 11px !important;
    font-weight: 700 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.05em !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 10px 20px !important;
    width: 100% !important;
}
div.stButton > button:hover { background-color: #b5ff33 !important; }
div.stButton > button[kind="secondary"] {
    background-color: transparent !important;
    color: #556070 !important;
    border: 1px solid #1a2530 !important;
}
div.stButton > button[kind="secondary"]:hover {
    border-color: #556070 !important;
    color: #e8edf2 !important;
}

/* Cards */
.nx-card {
    background: #0e1419;
    border: 1px solid #1a2530;
    border-radius: 12px;
    padding: 18px 20px;
    margin-bottom: 14px;
}
.nx-card-title {
    font-family: 'Space Mono', monospace;
    font-size: 10px;
    color: #556070;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-bottom: 14px;
}
.nx-card-title span { color: #a2ff00; margin-right: 6px; }

/* Warning notice */
.nx-notice {
    background: rgba(255,179,0,0.07);
    border: 1px solid rgba(255,179,0,0.2);
    border-radius: 8px;
    padding: 10px 14px;
    font-family: 'Space Mono', monospace;
    font-size: 10px;
    color: #ffb300;
    line-height: 1.6;
    margin-bottom: 18px;
}

/* Stage badge */
.nx-stage-badge {
    display: inline-block;
    background: rgba(255,179,0,0.1);
    border: 1px solid rgba(255,179,0,0.3);
    color: #ffb300;
    font-family: 'Space Mono', monospace;
    font-size: 10px;
    font-weight: 700;
    padding: 4px 10px;
    border-radius: 4px;
    letter-spacing: 0.08em;
}

/* Feature box */
.nx-feature {
    background: #060a0d;
    border: 1px solid #1a2530;
    border-left: 3px solid #a2ff00;
    border-radius: 8px;
    padding: 14px;
    margin-bottom: 10px;
}
.nx-feature-title {
    font-size: 12px;
    font-weight: 700;
    color: #e8edf2;
    margin-bottom: 5px;
}
.nx-feature-body {
    font-size: 11px;
    color: #556070;
    line-height: 1.6;
}
.nx-feature-buyer {
    margin-top: 7px;
    font-family: 'Space Mono', monospace;
    font-size: 10px;
    color: #00e5ff;
}

/* Tags */
.tag-bad {
    display: inline-block;
    background: rgba(244,63,94,0.12);
    color: #f43f5e;
    font-family: 'Space Mono', monospace;
    font-size: 9px;
    padding: 2px 6px;
    border-radius: 3px;
    font-weight: 700;
}
.tag-good {
    display: inline-block;
    background: rgba(162,255,0,0.1);
    color: #a2ff00;
    font-family: 'Space Mono', monospace;
    font-size: 9px;
    padding: 2px 6px;
    border-radius: 3px;
    font-weight: 700;
}

/* Node grid */
.nx-node-grid {
    display: grid;
    grid-template-columns: repeat(8, 1fr);
    gap: 5px;
    margin: 12px 0;
}
.nx-node {
    aspect-ratio: 1;
    border-radius: 4px;
    background: #1a2530;
}
.nx-node.active { background: #a2ff00; box-shadow: 0 0 6px rgba(162,255,0,0.4); }
.nx-node.processing {
    background: #00e5ff;
    box-shadow: 0 0 6px rgba(0,229,255,0.4);
    animation: blink 0.8s ease-in-out infinite;
}
@keyframes blink { 0%,100%{opacity:1} 50%{opacity:0.3} }

/* Sim stats */
.nx-sim-stat {
    background: #060a0d;
    border: 1px solid #1a2530;
    border-radius: 8px;
    padding: 12px;
    text-align: center;
}
.nx-sim-val {
    font-family: 'Space Mono', monospace;
    font-size: 20px;
    font-weight: 700;
    color: #a2ff00;
}
.nx-sim-label {
    font-family: 'Space Mono', monospace;
    font-size: 9px;
    color: #556070;
    margin-top: 4px;
    text-transform: uppercase;
    letter-spacing: 0.06em;
}

/* Task log */
.nx-log {
    background: #040709;
    border: 1px solid #1a2530;
    border-radius: 8px;
    padding: 12px;
    font-family: 'Space Mono', monospace;
    font-size: 10px;
    color: #556070;
    line-height: 1.8;
    max-height: 140px;
    overflow-y: auto;
}
.log-success { color: #a2ff00; }
.log-info { color: #00e5ff; }
.log-warn { color: #ffb300; }

/* Roadmap */
.nx-roadmap-item {
    border-left: 2px solid #1a2530;
    padding-left: 16px;
    padding-bottom: 20px;
    position: relative;
}
.nx-roadmap-item::before {
    content: '';
    position: absolute;
    left: -5px; top: 4px;
    width: 8px; height: 8px;
    border-radius: 50%;
    background: #1a2530;
    border: 1px solid #1a2530;
}
.nx-roadmap-item.current::before {
    background: #00e5ff;
    border-color: #00e5ff;
    box-shadow: 0 0 6px rgba(0,229,255,0.5);
}
.nx-roadmap-phase {
    font-family: 'Space Mono', monospace;
    font-size: 9px;
    color: #556070;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-bottom: 3px;
}
.nx-roadmap-title {
    font-size: 13px;
    font-weight: 700;
    color: #e8edf2;
    margin-bottom: 4px;
}
.nx-roadmap-body {
    font-size: 11px;
    color: #556070;
    line-height: 1.6;
}

/* Table */
.nx-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 11px;
}
.nx-table th {
    text-align: left;
    padding: 8px 10px;
    font-family: 'Space Mono', monospace;
    font-size: 9px;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: #556070;
    border-bottom: 1px solid #1a2530;
}
.nx-table th.hl { color: #a2ff00; }
.nx-table td {
    padding: 10px;
    border-bottom: 1px solid rgba(26,37,48,0.5);
    color: #556070;
    vertical-align: top;
    line-height: 1.5;
}
.nx-table td:first-child { color: #e8edf2; font-weight: 600; width: 150px; }
.nx-table td.hl { color: #e8edf2; }
.nx-table tr:last-child td { border-bottom: none; }

/* Progress */
.nx-prog-label {
    display: flex;
    justify-content: space-between;
    font-family: 'Space Mono', monospace;
    font-size: 10px;
    color: #556070;
    margin-bottom: 5px;
}
.nx-prog-bar {
    height: 4px;
    background: #1a2530;
    border-radius: 2px;
    overflow: hidden;
    margin-bottom: 12px;
}
.nx-prog-fill { height: 100%; background: #a2ff00; border-radius: 2px; }
.nx-prog-fill.blue { background: #00e5ff; }

/* Moat */
.nx-moat {
    background: #060a0d;
    border: 1px solid #1a2530;
    border-radius: 8px;
    padding: 14px;
}
.nx-moat-icon { font-size: 20px; margin-bottom: 8px; }
.nx-moat-title { font-size: 12px; font-weight: 700; color: #e8edf2; margin-bottom: 5px; }
.nx-moat-body { font-size: 11px; color: #556070; line-height: 1.6; }

/* Footer */
.nx-footer {
    border-top: 1px solid #1a2530;
    margin-top: 40px;
    padding-top: 16px;
    text-align: center;
    font-family: 'Space Mono', monospace;
    font-size: 10px;
    color: #2a3540;
    line-height: 1.8;
}

/* Social links */
.nx-social-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(70px, 1fr));
    gap: 6px;
    margin: 10px 0;
}
.nx-social-btn {
    display: block;
    text-align: center;
    padding: 7px;
    background: #0e1419;
    border: 1px solid #1a2530;
    border-radius: 8px;
    color: #556070 !important;
    font-size: 11px;
    font-weight: bold;
    text-decoration: none;
    transition: all 0.2s;
}
.nx-social-btn:hover { border-color: #a2ff00; color: #a2ff00 !important; }
</style>
""", unsafe_allow_html=True)

# ── Session state init ──
if 'sim_running' not in st.session_state: st.session_state.sim_running = False
if 'sim_tasks' not in st.session_state: st.session_state.sim_tasks = 0
if 'sim_log' not in st.session_state: st.session_state.sim_log = []
if 'sim_nodes' not in st.session_state: st.session_state.sim_nodes = [0] * 64  # 0=idle, 1=active, 2=processing
if 'sim_start_time' not in st.session_state: st.session_state.sim_start_time = 0.0
if 'prog1' not in st.session_state: st.session_state.prog1 = 0
if 'prog2' not in st.session_state: st.session_state.prog2 = 0
if 'prog3' not in st.session_state: st.session_state.prog3 = 0

TASK_TYPES = [
    ("SLM inference (Phi-3 mini)", "success"),
    ("RLHF label validation", "info"),
    ("ZK proof generation", "success"),
    ("BFT consensus round", "info"),
    ("Thermal check: 36.4°C ✓", "success"),
    ("Dataset chunk checksum", "info"),
    ("Node fingerprint verified", "success"),
    ("Cross-node result agreement", "info"),
]

def tick_simulation():
    """Advance simulation state by one tick."""
    nodes = st.session_state.sim_nodes
    # activate ~48 nodes if not already
    idle = [i for i, v in enumerate(nodes) if v == 0]
    if len([v for v in nodes if v > 0]) < 48 and idle:
        for _ in range(min(4, len(idle))):
            idx = random.choice(idle)
            nodes[idx] = 1
            idle.remove(idx)

    # random active node becomes processing, then back
    active = [i for i, v in enumerate(nodes) if v == 1]
    if active:
        pick = random.choice(active)
        nodes[pick] = 2
        # revert a few processing ones back to active
        processing = [i for i, v in enumerate(nodes) if v == 2]
        for p in random.sample(processing, min(2, len(processing))):
            nodes[p] = 1

    st.session_state.sim_nodes = nodes

    # log entry
    task, cls = random.choice(TASK_TYPES)
    node_id = random.randint(1, 64)
    ts = time.strftime("%H:%M:%S")
    entry = (f"[{ts}] Node #{node_id} → {task}", cls)
    st.session_state.sim_log.append(entry)
    if len(st.session_state.sim_log) > 30:
        st.session_state.sim_log = st.session_state.sim_log[-30:]

    st.session_state.sim_tasks += 1
    t = st.session_state.sim_tasks
    st.session_state.prog1 = min(85, int(t * 1.4))
    st.session_state.prog2 = min(72, int(t * 1.1))
    st.session_state.prog3 = min(60, int(t * 0.9))

# ── Header ──
col_logo, col_badge = st.columns([3, 1])
with col_logo:
    st.markdown("""
    <div style="display:flex; align-items:center; gap:10px; padding: 8px 0;">
        <div style="width:10px;height:10px;background:#a2ff00;border-radius:50%;
                    box-shadow:0 0 12px #a2ff00;animation:none;flex-shrink:0;"></div>
        <div style="font-family:'Syne',sans-serif;font-size:22px;font-weight:800;color:#e8edf2;">
            Nexa<span style="color:#a2ff00;">Edge</span> Network
        </div>
    </div>
    <div style="font-family:'Syne',sans-serif;font-size:12px;color:#556070;
                line-height:1.6;padding-bottom:12px;max-width:500px;">
        Aggregating idle smartphone compute into a distributed edge AI inference network —
        turning personal devices into institutional-grade infrastructure.
    </div>
    """, unsafe_allow_html=True)
with col_badge:
    st.markdown("""
    <div style="text-align:right;padding-top:12px;">
        <span class="nx-stage-badge">⚠ PRE-LAUNCH<br>CONCEPT DEMO</span>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<hr style="border-color:#1a2530;margin:4px 0 20px 0;">', unsafe_allow_html=True)

# ── Tabs ──
tab_market, tab_sim, tab_moat, tab_roadmap = st.tabs([
    "Market", "Network Sim", "Differentiation", "Roadmap"
])

# ══════════════════════════════════════
# TAB 1 — MARKET
# ══════════════════════════════════════
with tab_market:

    # Metrics
    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Global Idle Smartphones", "6.8B", "devices with NPU / on-device AI")
    with c2:
        st.metric("Edge AI Market (2028)", "$107B", "projected CAGR 19.2%")
    with c3:
        st.metric("GPU Compute Cost", "$2–4/hr", "H100 spot — volatile & scarce")

    # Competitive table
    st.markdown("""
    <div class="nx-card">
        <div class="nx-card-title"><span>▸</span> Competitive Positioning</div>
        <table class="nx-table">
            <thead>
                <tr>
                    <th>Dimension</th>
                    <th>Centralized GPU Cloud</th>
                    <th>Grass (Bandwidth)</th>
                    <th class="hl">NexaEdge</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>CapEx</td>
                    <td><span class="tag-bad">EXTREME</span> H100 scarce & costly</td>
                    <td>Low (bandwidth proxy)</td>
                    <td class="hl"><span class="tag-good">ZERO</span> User-owned devices</td>
                </tr>
                <tr>
                    <td>Latency</td>
                    <td><span class="tag-bad">50–150ms</span> datacenter roundtrip</td>
                    <td>N/A (not compute)</td>
                    <td class="hl"><span class="tag-good">&lt;5ms</span> On-device edge</td>
                </tr>
                <tr>
                    <td>Privacy</td>
                    <td><span class="tag-bad">Data leaves device</span></td>
                    <td>Partial</td>
                    <td class="hl"><span class="tag-good">GDPR-native</span> Local processing</td>
                </tr>
                <tr>
                    <td>Geographic reach</td>
                    <td>Few datacenters</td>
                    <td>High (IPs)</td>
                    <td class="hl"><span class="tag-good">Global</span> Every city & rural</td>
                </tr>
                <tr>
                    <td>Compute layer</td>
                    <td>GPU (training-grade)</td>
                    <td><span class="tag-bad">Network only</span></td>
                    <td class="hl"><span class="tag-good">NPU + CPU</span> On-device inference</td>
                </tr>
                <tr>
                    <td>Sybil resistance</td>
                    <td>Centralized auth</td>
                    <td><span class="tag-bad">IP spoofable</span></td>
                    <td class="hl"><span class="tag-good">Hardware fingerprint + ZK</span></td>
                </tr>
            </tbody>
        </table>
    </div>
    """, unsafe_allow_html=True)

    # Buyer segments
    st.markdown('<div class="nx-card"><div class="nx-card-title"><span>▸</span> Who Pays — Buyer Segments</div>', unsafe_allow_html=True)
    b1, b2 = st.columns(2)
    with b1:
        st.markdown("""
        <div class="nx-feature">
            <div class="nx-feature-title">🤖 Edge AI Agent Deployers</div>
            <div class="nx-feature-body">Run 1.8B–3.8B parameter SLMs (Phi-3, Gemma) with sub-5ms local inference. No data leaves device — GDPR compliant by architecture.</div>
            <div class="nx-feature-buyer">→ AI app developers, enterprise SaaS</div>
        </div>
        <div class="nx-feature">
            <div class="nx-feature-title">🧹 AI Dataset Cleaning (RLHF)</div>
            <div class="nx-feature-body">Distributed WASM sandbox runs automated labeling and cross-validation of AI training corpora across thousands of nodes simultaneously.</div>
            <div class="nx-feature-buyer">→ AI labs, data pipeline companies</div>
        </div>
        """, unsafe_allow_html=True)
    with b2:
        st.markdown("""
        <div class="nx-feature">
            <div class="nx-feature-title">🔐 ZK-ML Inference Verification</div>
            <div class="nx-feature-body">Fragment AI inference proofs across independent nodes. Redundant verification prevents result tampering — no single point of trust.</div>
            <div class="nx-feature-buyer">→ DeFi protocols, compliance platforms</div>
        </div>
        <div class="nx-feature">
            <div class="nx-feature-title">📡 Sensor-Context AI</div>
            <div class="nx-feature-body">Leverage unique smartphone hardware — GPS, camera, IMU — for context-aware inference unavailable in any datacenter.</div>
            <div class="nx-feature-buyer">→ Location AI, autonomous systems</div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Architecture
    st.markdown("""
    <div class="nx-card">
        <div class="nx-card-title"><span>▸</span> System Architecture</div>
        <div style="display:flex;align-items:stretch;gap:0;">
            <div style="flex:1;background:#060a0d;border:1px solid #1a2530;border-radius:8px;padding:14px;text-align:center;">
                <div style="font-family:'Space Mono',monospace;font-size:9px;color:#556070;text-transform:uppercase;margin-bottom:8px;">Demand Side</div>
                <div style="font-size:22px;margin-bottom:6px;">🏢</div>
                <div style="font-size:12px;font-weight:700;color:#e8edf2;margin-bottom:4px;">AI Buyers</div>
                <div style="font-size:10px;color:#556070;line-height:1.5;">Submit inference tasks via API. Pay in NEXA token per compute unit.</div>
            </div>
            <div style="display:flex;align-items:center;padding:0 8px;color:#a2ff00;font-size:18px;">→</div>
            <div style="flex:1;background:#060a0d;border:1px solid #1a2530;border-radius:8px;padding:14px;text-align:center;">
                <div style="font-family:'Space Mono',monospace;font-size:9px;color:#556070;text-transform:uppercase;margin-bottom:8px;">Coordination</div>
                <div style="font-size:22px;margin-bottom:6px;">⛓</div>
                <div style="font-size:12px;font-weight:700;color:#e8edf2;margin-bottom:4px;">Solana SPL</div>
                <div style="font-size:10px;color:#556070;line-height:1.5;">Task routing, BFT consensus, reward settlement. Low gas, high TPS.</div>
            </div>
            <div style="display:flex;align-items:center;padding:0 8px;color:#a2ff00;font-size:18px;">→</div>
            <div style="flex:1;background:#060a0d;border:1px solid #1a2530;border-radius:8px;padding:14px;text-align:center;">
                <div style="font-family:'Space Mono',monospace;font-size:9px;color:#556070;text-transform:uppercase;margin-bottom:8px;">Supply Side</div>
                <div style="font-size:22px;margin-bottom:6px;">📱</div>
                <div style="font-size:12px;font-weight:700;color:#e8edf2;margin-bottom:4px;">Device Nodes</div>
                <div style="font-size:10px;color:#556070;line-height:1.5;">WASM sandbox on idle devices. NPU executes inference. Proof submitted on-chain.</div>
            </div>
        </div>
    </div>

    <div class="nx-social-grid">
        <a class="nx-social-btn" href="https://www.instagram.com/nexaedge__" target="_blank">📸 Instagram</a>
        <a class="nx-social-btn" href="https://x.com/nexaedge_" target="_blank">🐦 X / Twitter</a>
        <a class="nx-social-btn" href="https://www.facebook.com/share/18eXN6P3Ge/" target="_blank">👥 Facebook</a>
        <a class="nx-social-btn" href="https://www.tiktok.com/@nexaedge7" target="_blank">🎵 TikTok</a>
        <a class="nx-social-btn" href="https://t.me/NexaEdge7" target="_blank">📢 Telegram</a>
        <a class="nx-social-btn" href="mailto:contact@nexaedge.org" style="border-color:#00e5ff;color:#00e5ff !important;">📧 Email Us</a>
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════
# TAB 2 — NETWORK SIM
# ══════════════════════════════════════
with tab_sim:

    st.markdown("""
    <div class="nx-notice">
        ⚠ SIMULATION ONLY — This visualizes the NexaEdge network concept.<br>
        No real compute, tokens, or blockchain transactions occur in this demo.<br>
        All figures are illustrative projections, not performance guarantees.
    </div>
    """, unsafe_allow_html=True)

    # Controls
    col_start, col_stop, col_status = st.columns([2, 2, 3])
    with col_start:
        if st.button("▶ Start Simulation", disabled=st.session_state.sim_running):
            st.session_state.sim_running = True
            st.session_state.sim_tasks = 0
            st.session_state.sim_log = []
            st.session_state.sim_nodes = [0] * 64
            st.session_state.sim_start_time = time.time()
            st.session_state.prog1 = 0
            st.session_state.prog2 = 0
            st.session_state.prog3 = 0
            st.rerun()
    with col_stop:
        if st.button("■ Stop", disabled=not st.session_state.sim_running, type="secondary"):
            st.session_state.sim_running = False
            st.session_state.sim_nodes = [0] * 64
            st.rerun()
    with col_status:
        status_color = "#a2ff00" if st.session_state.sim_running else "#556070"
        status_text = "● RUNNING" if st.session_state.sim_running else "○ IDLE"
        st.markdown(f'<div style="font-family:\'Space Mono\',monospace;font-size:11px;color:{status_color};padding-top:10px;">{status_text}</div>', unsafe_allow_html=True)

    # Tick simulation if running
    if st.session_state.sim_running:
        tick_simulation()

    # Node grid
    nodes = st.session_state.sim_nodes
    node_html = '<div class="nx-card"><div class="nx-card-title"><span>▸</span> Node Network — 64 Simulated Devices</div><div class="nx-node-grid">'
    for v in nodes:
        cls = {0: "", 1: " active", 2: " processing"}.get(v, "")
        node_html += f'<div class="nx-node{cls}"></div>'
    node_html += '</div>'
    node_html += '''
    <div style="display:flex;gap:16px;margin-top:10px;">
        <span style="font-size:10px;color:#556070;font-family:'Space Mono',monospace;display:flex;align-items:center;gap:5px;">
            <span style="width:10px;height:10px;background:#1a2530;border-radius:2px;display:inline-block;"></span> Idle
        </span>
        <span style="font-size:10px;color:#a2ff00;font-family:'Space Mono',monospace;display:flex;align-items:center;gap:5px;">
            <span style="width:10px;height:10px;background:#a2ff00;border-radius:2px;display:inline-block;"></span> Active
        </span>
        <span style="font-size:10px;color:#00e5ff;font-family:'Space Mono',monospace;display:flex;align-items:center;gap:5px;">
            <span style="width:10px;height:10px;background:#00e5ff;border-radius:2px;display:inline-block;"></span> Processing
        </span>
    </div></div>'''
    st.markdown(node_html, unsafe_allow_html=True)

    # Sim stats
    active_count = sum(1 for v in nodes if v > 0)
    latency = f"{random.uniform(2.1, 4.8):.1f}ms" if st.session_state.sim_running else "—"
    consensus = f"{random.uniform(96.5, 99.9):.1f}%" if st.session_state.sim_running else "—"

    s1, s2, s3, s4 = st.columns(4)
    with s1:
        st.markdown(f'<div class="nx-sim-stat"><div class="nx-sim-val">{active_count}</div><div class="nx-sim-label">Active Nodes</div></div>', unsafe_allow_html=True)
    with s2:
        st.markdown(f'<div class="nx-sim-stat"><div class="nx-sim-val">{st.session_state.sim_tasks}</div><div class="nx-sim-label">Tasks Done</div></div>', unsafe_allow_html=True)
    with s3:
        st.markdown(f'<div class="nx-sim-stat"><div class="nx-sim-val">{latency}</div><div class="nx-sim-label">Avg Latency</div></div>', unsafe_allow_html=True)
    with s4:
        st.markdown(f'<div class="nx-sim-stat"><div class="nx-sim-val">{consensus}</div><div class="nx-sim-label">BFT Consensus</div></div>', unsafe_allow_html=True)

    # Task log
    st.markdown('<div class="nx-card" style="margin-top:14px;"><div class="nx-card-title"><span>▸</span> Task Dispatch Log</div>', unsafe_allow_html=True)
    if st.session_state.sim_log:
        log_html = '<div class="nx-log">'
        for line, cls in st.session_state.sim_log[-15:]:
            log_html += f'<div class="log-{cls}">{line}</div>'
        log_html += '</div>'
    else:
        log_html = '<div class="nx-log"><div>// Press ▶ Start Simulation to begin.</div></div>'
    st.markdown(log_html + '</div>', unsafe_allow_html=True)

    # Progress bars
    p1, p2, p3 = st.session_state.prog1, st.session_state.prog2, st.session_state.prog3
    st.markdown(f"""
    <div class="nx-card">
        <div class="nx-card-title"><span>▸</span> Simulated Workload Capacity</div>
        <div class="nx-prog-label"><span>Edge AI Inference (SLM 1.8B)</span><span>{p1}%</span></div>
        <div class="nx-prog-bar"><div class="nx-prog-fill" style="width:{p1}%"></div></div>
        <div class="nx-prog-label"><span>Dataset Validation (RLHF)</span><span>{p2}%</span></div>
        <div class="nx-prog-bar"><div class="nx-prog-fill blue" style="width:{p2}%"></div></div>
        <div class="nx-prog-label"><span>ZK Proof Generation</span><span>{p3}%</span></div>
        <div class="nx-prog-bar"><div class="nx-prog-fill" style="width:{p3}%"></div></div>
    </div>
    """, unsafe_allow_html=True)

    # Auto-refresh only when running
    if st.session_state.sim_running:
        time.sleep(0.9)
        st.rerun()


# ══════════════════════════════════════
# TAB 3 — DIFFERENTIATION / MOAT
# ══════════════════════════════════════
with tab_moat:

    st.markdown("""
    <div class="nx-card">
        <div class="nx-card-title"><span>▸</span> Why NexaEdge vs Grass</div>
        <table class="nx-table">
            <thead>
                <tr>
                    <th>Dimension</th>
                    <th>Grass</th>
                    <th class="hl">NexaEdge</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>Core resource</td>
                    <td>Network bandwidth (residential proxy)</td>
                    <td class="hl">Device compute (CPU + NPU)</td>
                </tr>
                <tr>
                    <td>Primary use case</td>
                    <td>Web scraping / data collection</td>
                    <td class="hl">AI inference, RLHF, ZK-ML verification</td>
                </tr>
                <tr>
                    <td>Sybil resistance</td>
                    <td><span class="tag-bad">HIGH RISK</span> IP spoofed via VPN</td>
                    <td class="hl"><span class="tag-good">LOW RISK</span> Hardware fingerprint + Proof of Compute</td>
                </tr>
                <tr>
                    <td>Compute verification</td>
                    <td>None (bandwidth only)</td>
                    <td class="hl">BFT consensus + ZK proof of inference result</td>
                </tr>
                <tr>
                    <td>Solana Mobile synergy</td>
                    <td>None</td>
                    <td class="hl"><span class="tag-good">NATIVE</span> Seeker / Saga system daemon</td>
                </tr>
            </tbody>
        </table>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="nx-card"><div class="nx-card-title"><span>▸</span> Technical Moat</div>', unsafe_allow_html=True)
    m1, m2 = st.columns(2)
    with m1:
        st.markdown("""
        <div class="nx-moat">
            <div class="nx-moat-icon">🔐</div>
            <div class="nx-moat-title">Proof of Compute (PoC)</div>
            <div class="nx-moat-body">Every node must solve a cryptographic ML inference puzzle to claim rewards. Hardware fingerprint + ZK proof prevents Sybil attacks that plague bandwidth-only networks.</div>
        </div>
        <br>
        <div class="nx-moat">
            <div class="nx-moat-icon">🌍</div>
            <div class="nx-moat-title">Geographic Density</div>
            <div class="nx-moat-body">6.8B smartphones vs. a few thousand datacenters. NexaEdge reaches rural markets, developing economies, and ultra-local inference use cases no cloud can serve.</div>
        </div>
        """, unsafe_allow_html=True)
    with m2:
        st.markdown("""
        <div class="nx-moat">
            <div class="nx-moat-icon">🧠</div>
            <div class="nx-moat-title">NPU-Native Execution</div>
            <div class="nx-moat-body">Modern smartphones (A-series, Snapdragon) have dedicated NPUs. NexaEdge targets these for SLM inference — energy-per-op rivals older server GPUs for small models.</div>
        </div>
        <br>
        <div class="nx-moat">
            <div class="nx-moat-icon">📱</div>
            <div class="nx-moat-title">Solana Mobile Integration</div>
            <div class="nx-moat-body">Solana Seeker / Saga are the only Web3-native phones. NexaEdge becomes the killer app that makes hardware ROI-positive — a structural flywheel for both ecosystems.</div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="nx-card">
        <div class="nx-card-title"><span>▸</span> Hardware Thermal Safety — 39°C Protocol</div>
        <div style="font-size:12px;color:#556070;line-height:1.9;">
            The 39°C thermal ceiling is a hardcoded daemon constraint, not a marketing claim.<br>
            If device temperature ≥ 39°C → task queue paused → passive cooling mode activated.<br>
            Enforced at the WASM sandbox level — not overridable by the user.<br><br>
            <span style="color:#e8edf2;font-weight:600;">Why this matters to buyers:</span>
            Institutional compute buyers need SLA guarantees. A network that destroys user hardware
            cannot maintain supply. The 39°C protocol is the supply-side durability guarantee.
        </div>
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════
# TAB 4 — ROADMAP
# ══════════════════════════════════════
with tab_roadmap:

    st.markdown("""
    <div class="nx-card">
        <div class="nx-card-title"><span>▸</span> Development Roadmap</div>
        <div class="nx-roadmap-item current">
            <div class="nx-roadmap-phase">Q2 2026 · NOW</div>
            <div class="nx-roadmap-title">Concept Validation & Grant Applications</div>
            <div class="nx-roadmap-body">Architecture design finalized. Whitepaper drafted. Applied to Solana Grant, Alliance DAO, Y Combinator. Building community waitlist.</div>
        </div>
        <div class="nx-roadmap-item">
            <div class="nx-roadmap-phase">Q3 2026</div>
            <div class="nx-roadmap-title">WASM Sandbox MVP</div>
            <div class="nx-roadmap-body">Functional WASM execution environment on iOS / Android. First real SLM inference (Phi-3 mini) running on device NPU. Thermal guard daemon implementation. Internal alpha: 50 devices.</div>
        </div>
        <div class="nx-roadmap-item">
            <div class="nx-roadmap-phase">Q4 2026</div>
            <div class="nx-roadmap-title">Closed Beta — 1,000 Nodes</div>
            <div class="nx-roadmap-body">Solana SPL token deployment. BFT consensus testnet. First paying buyer pilot (AI data cleaning use case). Device fingerprint + ZK proof of compute live.</div>
        </div>
        <div class="nx-roadmap-item">
            <div class="nx-roadmap-phase">Q1 2027</div>
            <div class="nx-roadmap-title">Public Mainnet Launch</div>
            <div class="nx-roadmap-body">Open node enrollment. Solana Seeker native integration. Marketplace for buyers to post inference tasks. Target: 100,000 active nodes, 3 enterprise buyers.</div>
        </div>
        <div class="nx-roadmap-item" style="padding-bottom:0;">
            <div class="nx-roadmap-phase">2027+</div>
            <div class="nx-roadmap-title">Scale & Ecosystem</div>
            <div class="nx-roadmap-body">ZK-ML verification product live. Expand to laptop / IoT device classes. Series A fundraise targeting $15M.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    r1, r2, r3 = st.columns(3)
    with r1:
        st.metric("Funding Target (Seed)", "$500K", "for MVP + 1,000-node beta")
    with r2:
        st.metric("Target Node Count (Y1)", "100K", "active devices at mainnet")
    with r3:
        st.metric("Settlement Chain", "Solana SPL", "low gas · high TPS · mobile-native")

# ── Footer ──
st.markdown("""
<div class="nx-footer">
    NexaEdge Network · Pre-Launch Concept Demo · All simulations are illustrative only.<br>
    No tokens issued · No investment contract · contact@nexaedge.org<br>
    © 2026 NexaEdge Network. All rights reserved.
</div>
""", unsafe_allow_html=True)
