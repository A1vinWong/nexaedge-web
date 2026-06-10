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
.nx-login-hero { text-align: center; padding: 40px 0 32px; }
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
c1, c2, c3 = st.columns([1, 2, 1])
with c2:
    st.image('IMG_7859.jpeg', use_container_width=True)
st.markdown('<div style="margin-bottom:8px;"></div>', unsafe_allow_html=True)
st.markdown("""
<div style="display:flex;align-items:center;gap:10px;padding:8px 0 4px;">
    <div style="width:10px;height:10px;background:#a2ff00;border-radius:50%;
                box-shadow:0 0 12px #a2ff00;flex-shrink:0;"></div>
    <div style="font-family:'Syne',sans-serif;font-size:20px;font-weight:800;
                color:#e8edf2;letter-spacing:-.02em;">
        Nexa<span style="color:#a2ff00;">Edge</span>
        <span style="font-size:11px;color:#4a6070;font-weight:400;
                     font-family:'Space Mono',monospace;margin-left:8px;">
            NODE PORTAL
        </span>
    </div>
</div>
<hr class="nx-divider">
""", unsafe_allow_html=True)

# ══════════════════════════════════════
# LOGGED IN — DASHBOARD
# ══════════════════════════════════════
if st.session_state.user_email:
    email = st.session_state.user_email
    data  = st.session_state.user_data

    if not data:
        st.markdown(f"""
        <div class="nx-notice">
            ⚠ Your email <strong>{email}</strong> is not on the waitlist yet.
            Please register at the main site first.
        </div>
        """, unsafe_allow_html=True)
        if st.button("Sign Out", type="secondary"):
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
                <circle cx="60" cy="60" r="52"
                    fill="none" stroke="#182230" stroke-width="6"/>
                <circle cx="60" cy="60" r="52"
                    fill="none" stroke="#a2ff00" stroke-width="6"
                    stroke-linecap="round"
                    stroke-dasharray="{dash:.1f} {gap:.1f}"/>
            </svg>
            <div class="nx-rank-number">
                <div class="nx-rank-num">#{rank}</div>
                <div class="nx-rank-label">Queue</div>
            </div>
        </div>
        <div class="nx-rank-title">Your node is reserved.</div>
        <div class="nx-rank-sub">
            Top {100 - pct_rank + 1}% of {total} waitlist members<br>
            Joined {joined}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Stats grid
    wallet_short = wallet[:6] + "…" + wallet[-4:] if wallet != "—" and len(wallet) > 10 else wallet
    st.markdown(f"""
    <div class="nx-stat-grid">
        <div class="nx-stat-item">
            <div class="nx-stat-val green">{referrals}</div>
            <div class="nx-stat-label">Referrals Made</div>
        </div>
        <div class="nx-stat-item">
            <div class="nx-stat-val cyan">{rank} / {total}</div>
            <div class="nx-stat-label">Queue Position</div>
        </div>
        <div class="nx-stat-item">
            <div class="nx-stat-val">{wallet_short}</div>
            <div class="nx-stat-label">SPL Wallet</div>
        </div>
        <div class="nx-stat-item">
            <div class="nx-stat-val gold">{lang}</div>
            <div class="nx-stat-label">Language</div>
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
        <div class="nx-ref-label">Your Referral Code</div>
        <div class="nx-ref-code">{ref_code}</div>
        <div class="nx-ref-count">
            {referrals} person{'s' if referrals != 1 else ''} joined with your code
        </div>
    </div>
    <div class="nx-share-row">
        <a class="nx-share-btn" href="{x_url}" target="_blank">🐦 X</a>
        <a class="nx-share-btn" href="{tg_url}" target="_blank">📢 Telegram</a>
        <a class="nx-share-btn" href="{wa_url}" target="_blank">💬 WhatsApp</a>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div style="margin-top:6px;"></div>', unsafe_allow_html=True)
    if st.button("📋 Copy Referral Code"):
        st.components.v1.html(
            f'<script>navigator.clipboard.writeText("{ref_code}").catch(()=>{{}});</script>',
            height=0, width=0
        )
        st.toast("✅ Code copied!")

    # ══════════════════════════════════════
    # NODE SECTION
    # ══════════════════════════════════════
    st.markdown('<div style="margin-top:20px;"></div>', unsafe_allow_html=True)
    node_rec = get_node_record(email)

    if node_rec:
        token  = node_rec.get("node_token", "—")
        status = node_rec.get("status", "pending")
        status_color = {"online": "#a2ff00", "pending": "#ffb300", "offline": "#4a6070"}.get(status, "#4a6070")

        # ── Live heartbeat stats
        hb = get_latest_heartbeat(token)
        task_count = get_node_task_count(token)

        if hb:
            cpu   = hb.get("cpu_usage", 0) or 0
            temp  = hb.get("temperature", 0) or 0
            batt  = hb.get("battery_level", 0) or 0
            ts_raw = (hb.get("reported_at", "")[:19] or "").replace("T", " ")
            temp_color = "#f43f5e" if temp >= 39 else "#e8edf2"
            st.markdown(f"""
            <div class="nx-card" style="border-color:rgba(162,255,0,.2);">
                <div class="nx-card-title">▸ Live Node Stats</div>
                <div style="display:flex;align-items:center;gap:10px;margin-bottom:14px;">
                    <div style="width:8px;height:8px;border-radius:50%;background:{status_color};
                                box-shadow:0 0 8px {status_color};"></div>
                    <div style="font-family:'Space Mono',monospace;font-size:10px;
                                color:{status_color};text-transform:uppercase;letter-spacing:.08em;">
                        {status}
                    </div>
                    <div style="font-family:'Space Mono',monospace;font-size:9px;
                                color:#2a3a4a;margin-left:auto;">
                        Last seen {ts_raw} UTC
                    </div>
                </div>
                <div class="nx-live-row">
                    <div class="nx-live-item">
                        <div class="nx-live-val">{cpu:.1f}%</div>
                        <div class="nx-live-label">CPU</div>
                    </div>
                    <div class="nx-live-item">
                        <div class="nx-live-val" style="color:{temp_color};">{temp:.1f}°C</div>
                        <div class="nx-live-label">Temp</div>
                    </div>
                    <div class="nx-live-item">
                        <div class="nx-live-val">{batt}%</div>
                        <div class="nx-live-label">Battery</div>
                    </div>
                </div>
                <div style="font-family:'Space Mono',monospace;font-size:9px;color:#4a6070;
                            margin-bottom:6px;text-transform:uppercase;letter-spacing:.08em;">
                    Node Token
                </div>
                <div style="font-family:'Space Mono',monospace;font-size:12px;color:#e8edf2;
                            background:#060b0f;border:1px solid #182230;border-radius:8px;
                            padding:10px 14px;word-break:break-all;">
                    {token}
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="nx-card" style="border-color:rgba(162,255,0,.2);">
                <div class="nx-card-title">▸ Your Node Registration</div>
                <div style="display:flex;align-items:center;gap:10px;margin-bottom:14px;">
                    <div style="width:8px;height:8px;border-radius:50%;background:{status_color};
                                box-shadow:0 0 8px {status_color};"></div>
                    <div style="font-family:'Space Mono',monospace;font-size:10px;
                                color:{status_color};text-transform:uppercase;letter-spacing:.08em;">
                        {status} — no heartbeat yet
                    </div>
                </div>
                <div style="font-family:'Space Mono',monospace;font-size:9px;color:#4a6070;
                            margin-bottom:6px;text-transform:uppercase;letter-spacing:.08em;">
                    Node Token
                </div>
                <div style="font-family:'Space Mono',monospace;font-size:12px;color:#e8edf2;
                            background:#060b0f;border:1px solid #182230;border-radius:8px;
                            padding:10px 14px;word-break:break-all;">
                    {token}
                </div>
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
            <div class="nx-card" style="margin-top:4px;">
                <div class="nx-card-title">▸ Task History
                    <span style="color:#a2ff00;margin-left:8px;">{task_count} completed</span>
                </div>
                {task_rows_html}
            </div>
            """, unsafe_allow_html=True)

        # ── Python-backend heartbeat + task executor (no JS fetch, iOS safe)
        st.markdown('<div style="margin-top:4px;"></div>', unsafe_allow_html=True)

        # Activate / Stop buttons
        node_active = st.session_state.get("node_active", False)
        col_act, col_stop = st.columns([3, 2])
        with col_act:
            if st.button("⚡ ACTIVATE NODE", disabled=node_active, key="btn_activate"):
                st.session_state.node_active = True
                st.session_state.node_tasks  = st.session_state.get("node_tasks", 0)
                st.session_state.node_log    = []
                st.rerun()
        with col_stop:
            if st.button("■ STOP", disabled=not node_active, type="secondary", key="btn_stop"):
                st.session_state.node_active = False
                try:
                    supabase.table("nodes").update({
                        "status": "offline"
                    }).eq("node_token", token).execute()
                except: pass
                st.rerun()

        if node_active:
            from streamlit_autorefresh import st_autorefresh
            st_autorefresh(interval=30000, key="portal_tick")

            # ── Send heartbeat
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

            # ── Poll and execute one task
            task_msg = None
            try:
                res = (supabase.table("tasks")
                       .select("*")
                       .eq("status", "pending")
                       .is_("assigned_to", "null")
                       .limit(1)
                       .execute())
                if res.data:
                    t       = res.data[0]
                    tid     = t["id"]
                    ttype   = t.get("task_type", "slm_inference")

                    supabase.table("tasks").update({
                        "status":      "assigned",
                        "assigned_to": token,
                    }).eq("id", tid).execute()

                    result = f"[Portal] {ttype} OK | latency={round(random.uniform(2,5),1)}ms | node={token[-8:]}"

                    supabase.table("tasks").update({
                        "status":       "completed",
                        "result":       result,
                        "completed_at": datetime.now(timezone.utc).isoformat(),
                    }).eq("id", tid).execute()

                    st.session_state.node_tasks = st.session_state.get("node_tasks", 0) + 1
                    task_msg = f"✓ {ttype} completed"
            except Exception as e:
                task_msg = f"Task error: {e}"

            # ── Log display
            log = st.session_state.get("node_log", [])
            ts_str = datetime.now().strftime("%H:%M:%S")
            log.insert(0, (f"[{ts_str}] {hb_msg}", hb_color))
            if task_msg:
                log.insert(0, (f"[{ts_str}] {task_msg}", "#a2ff00"))
            log = log[:8]
            st.session_state.node_log = log

            log_html = "".join(
                f'<div style="color:{c};line-height:1.9;">{l}</div>'
                for l, c in log
            )
            st.markdown(f"""
            <div style="background:#040709;border:1px solid #182230;border-radius:10px;
                        padding:14px;font-family:'Space Mono',monospace;font-size:10px;
                        margin-top:4px;">
                <div style="display:flex;align-items:center;gap:8px;margin-bottom:10px;">
                    <div style="width:8px;height:8px;border-radius:50%;background:#a2ff00;
                                box-shadow:0 0 8px #a2ff00;"></div>
                    <span style="color:#a2ff00;font-size:10px;text-transform:uppercase;
                                 letter-spacing:.08em;">ONLINE · refreshes every 30s</span>
                </div>
                {log_html}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="background:#040709;border:1px solid #182230;border-radius:10px;
                        padding:14px;font-family:'Space Mono',monospace;font-size:10px;
                        color:#2a3a4a;margin-top:4px;">
                // Press ACTIVATE NODE to start heartbeat + task execution
            </div>
            """, unsafe_allow_html=True)

    else:
        st.markdown("""
        <div class="nx-card">
            <div class="nx-card-title">▸ Register Your Device as a Node</div>
            <div style="font-size:12px;color:#4a6070;line-height:1.7;margin-bottom:16px;">
                Generate a unique node token for this device.
                Use this token with the node client to start sending heartbeats
                and executing tasks.
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("⚡ Register This Device"):
            tok = generate_node_token()
            ok  = register_node(email, tok)
            if ok:
                st.success(f"Node registered! Token: **{tok}**")
                st.rerun()
            else:
                st.error("Registration failed. You may already have a node registered.")

    # ── Node Journey timeline
    st.markdown('<div style="margin-top:20px;"></div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="nx-card">
        <div class="nx-card-title">▸ Your Node Journey</div>
        <div class="nx-timeline">
            <div class="nx-tl-item">
                <div class="nx-tl-dot done"></div>
                <div>
                    <div class="nx-tl-title">Waitlist Registered</div>
                    <div class="nx-tl-sub">Spot secured · NEXA airdrop eligible</div>
                </div>
            </div>
            <div class="nx-tl-item">
                <div class="nx-tl-dot done"></div>
                <div>
                    <div class="nx-tl-title">Node Token Issued</div>
                    <div class="nx-tl-sub">Device registered · heartbeat active</div>
                </div>
            </div>
            <div class="nx-tl-item">
                <div class="nx-tl-dot now"></div>
                <div>
                    <div class="nx-tl-title">Beta — Task Execution</div>
                    <div class="nx-tl-sub">Simulated tasks running · earning sim NEXA · Q3 2026</div>
                </div>
            </div>
            <div class="nx-tl-item">
                <div class="nx-tl-dot"></div>
                <div>
                    <div class="nx-tl-title muted">Closed Beta — 1,000 Nodes</div>
                    <div class="nx-tl-sub">Real node client · ZK proof · Q4 2026</div>
                </div>
            </div>
            <div class="nx-tl-item">
                <div class="nx-tl-dot"></div>
                <div>
                    <div class="nx-tl-title muted">Mainnet Launch</div>
                    <div class="nx-tl-sub">Real compute · real rewards · Q1 2027</div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="nx-notice">
        ⚠ NEXA tokens are minted on Solana but not yet in public circulation.
        Airdrop eligibility and allocation are determined at mainnet launch
        based on your queue position and referral count. This is not a financial instrument.
    </div>
    """, unsafe_allow_html=True)

    if st.button("Sign Out", type="secondary"):
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
            <span class="nx-stage">● BETA · Q3 2026</span>
        </div>
        <div class="nx-login-title">My Node Portal</div>
        <div class="nx-login-sub">
            Sign in with the email you used to join the waitlist.
            We'll send you a one-time code — no password needed.
        </div>
        <div style="font-family:'Space Mono',monospace;font-size:11px;color:#4a6070;">
            <span style="color:#a2ff00;font-weight:700;">{total}</span> nodes reserved
        </div>
    </div>
    """, unsafe_allow_html=True)

    if not st.session_state.magic_sent:
        email_input = st.text_input("Email Address", placeholder="you@example.com", key="login_email_input")
        if st.button("Send Login Code"):
            if not email_input or "@" not in email_input:
                st.error("Please enter a valid email address.")
            else:
                record = lookup_waitlist(email_input)
                if not record:
                    st.error("This email is not on the waitlist. Please register at the main site first.")
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

        st.markdown("""
        <div style="text-align:center;margin-top:20px;font-family:'Space Mono',monospace;
                    font-size:10px;color:#2a3a4a;line-height:1.7;">
            Not on the waitlist yet?<br>
            <a href="https://nexaedge.streamlit.app" target="_blank"
               style="color:#4a6070;text-decoration:none;">
                Register at nexaedge.streamlit.app →
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
                Your login code
            </div>
            <div style="font-family:'Space Mono',monospace;font-size:10px;color:#4a6070;
                        line-height:1.7;margin-bottom:12px;">
                Signing in as<br>
                <strong style="color:#a2ff00;">{st.session_state.magic_email}</strong>
            </div>
            <div style="font-family:'Space Mono',monospace;font-size:28px;font-weight:700;
                        color:#a2ff00;letter-spacing:.3em;background:#060b0f;
                        border:1px solid rgba(162,255,0,.2);border-radius:8px;
                        padding:12px 20px;display:inline-block;">
                {beta_code}
            </div>
            <div style="font-family:'Space Mono',monospace;font-size:8px;color:#2a3a4a;margin-top:10px;">
                ⚠ BETA MODE — Code shown on screen. Valid 10 minutes.
            </div>
        </div>
        """, unsafe_allow_html=True)

        otp_input = st.text_input("Enter the 6-digit code above", placeholder="e.g. 123456", max_chars=6, key="otp_input")
        if st.button("Verify & Sign In"):
            if not otp_input or len(otp_input) < 6:
                st.error("Please enter the 6-digit code.")
            else:
                if verify_code(st.session_state.magic_email, otp_input):
                    record = lookup_waitlist(st.session_state.magic_email)
                    st.session_state.user_email = st.session_state.magic_email
                    st.session_state.user_data  = record
                    st.session_state.magic_sent = False
                    st.session_state._beta_code = ""
                    st.rerun()
                else:
                    st.error("Incorrect code. Please try again.")

        st.markdown('<div style="margin-top:10px;"></div>', unsafe_allow_html=True)
        if st.button("← Use a different email", type="secondary"):
            st.session_state.magic_sent  = False
            st.session_state.magic_email = ""
            st.session_state._beta_code  = ""
            st.rerun()

# ══════════════════════════════════════
# FOOTER
# ══════════════════════════════════════
st.markdown("""
<div class="nx-footer">
    NexaEdge Node Portal · Beta P4 · Heartbeat + Task Executor<br>
    NEXA minted on Solana · Not yet in public circulation · contact@nexaedge.org
</div>
""", unsafe_allow_html=True)
