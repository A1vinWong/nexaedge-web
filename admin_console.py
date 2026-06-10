"""
NexaEdge Admin Dashboard — Beta P1
Run: streamlit run admin_dashboard.py
Access via password — set ADMIN_PASSWORD in Streamlit secrets or .env
"""

import streamlit as st
import pandas as pd
import hashlib
import io
from datetime import datetime, timedelta, timezone
from collections import Counter
from supabase import create_client, Client

st.set_page_config(
    page_title="NexaEdge · Admin",
    page_icon="🛡",
    layout="wide"
)

# ══════════════════════════════════════
# CONFIG — change these or move to st.secrets
# ══════════════════════════════════════
SUPABASE_URL = "https://nfafzigmcdybgbxdtymf.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im5mYWZ6aWdtY2R5YmdieGR0eW1mIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODA5ODE3NTMsImV4cCI6MjA5NjU1Nzc1M30.ZIX3sByZ8yQSDGFr-o24CjIXwZ5UsB4rMB3jculLtv0"

# ⚠️ Change this password before deploying
ADMIN_PASSWORD = "nexaedge2026"

# ══════════════════════════════════════
# CSS — matches NexaEdge dark theme
# ══════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Syne:wght@400;600;700;800&display=swap');

.stApp { background-color: #060b0f; }
.main .block-container { padding-top: 1.5rem !important; padding-bottom: 3rem !important; max-width: 1400px !important; }
#MainMenu, footer, header, [data-testid="stHeader"] { display: none !important; }

.stApp::before {
    content: '';
    position: fixed;
    inset: 0;
    background-image:
        linear-gradient(rgba(162,255,0,.015) 1px, transparent 1px),
        linear-gradient(90deg, rgba(162,255,0,.015) 1px, transparent 1px);
    background-size: 44px 44px;
    pointer-events: none;
    z-index: 0;
}

*, h1, h2, h3, p, div, span, label { font-family: 'Syne', sans-serif; }

/* Metrics */
[data-testid="stMetric"] {
    background: linear-gradient(135deg, #0d1720, #0a1118) !important;
    border: 1px solid #182230 !important;
    border-radius: 12px !important;
    padding: 20px !important;
}
[data-testid="stMetricLabel"] {
    font-family: 'Space Mono', monospace !important;
    font-size: 9px !important;
    color: #4a6070 !important;
    text-transform: uppercase !important;
    letter-spacing: .1em !important;
}
[data-testid="stMetricValue"] {
    font-size: 28px !important;
    font-weight: 800 !important;
    color: #e8edf2 !important;
}
[data-testid="stMetricDelta"] { font-size: 10px !important; color: #a2ff00 !important; }

/* Buttons */
div.stButton > button {
    background: linear-gradient(135deg, #a2ff00, #8de600) !important;
    color: #060b0f !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 10px !important;
    font-weight: 700 !important;
    text-transform: uppercase !important;
    letter-spacing: .06em !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 10px 20px !important;
}
div.stButton > button[kind="secondary"] {
    background: transparent !important;
    color: #4a6070 !important;
    border: 1px solid #182230 !important;
}
div.stButton > button[kind="secondary"]:hover {
    border-color: #a2ff00 !important;
    color: #a2ff00 !important;
}

/* Inputs */
.stTextInput > div > div > input {
    background: #060b0f !important;
    border: 1px solid #182230 !important;
    border-radius: 8px !important;
    color: #e8edf2 !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 12px !important;
    padding: 12px 14px !important;
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

/* Dataframe */
[data-testid="stDataFrame"] {
    border: 1px solid #182230 !important;
    border-radius: 10px !important;
    overflow: hidden !important;
}

/* Selectbox */
.stSelectbox label {
    font-family: 'Space Mono', monospace !important;
    font-size: 10px !important;
    color: #4a6070 !important;
    text-transform: uppercase !important;
    letter-spacing: .08em !important;
}

/* Charts */
[data-testid="stVegaLiteChart"] { background: transparent !important; }

/* Cards */
.nx-card {
    background: linear-gradient(160deg, #0d1720, #090e14);
    border: 1px solid #182230;
    border-radius: 14px;
    padding: 22px 24px;
    margin-bottom: 16px;
}
.nx-card-title {
    font-family: 'Space Mono', monospace;
    font-size: 10px;
    color: #4a6070;
    text-transform: uppercase;
    letter-spacing: .12em;
    margin-bottom: 18px;
    display: flex;
    align-items: center;
    gap: 8px;
}
.nx-notice {
    background: rgba(255,179,0,.05);
    border: 1px solid rgba(255,179,0,.2);
    border-left: 3px solid #ffb300;
    border-radius: 0 8px 8px 0;
    padding: 10px 16px;
    font-family: 'Space Mono', monospace;
    font-size: 9px;
    color: #ffb300;
    line-height: 1.7;
    margin-bottom: 20px;
}
.nx-stat-row {
    display: flex;
    gap: 12px;
    margin-bottom: 12px;
    flex-wrap: wrap;
}
.nx-mini-stat {
    background: #060b0f;
    border: 1px solid #182230;
    border-radius: 10px;
    padding: 14px 18px;
    min-width: 140px;
    flex: 1;
}
.nx-mini-val {
    font-family: 'Space Mono', monospace;
    font-size: 22px;
    font-weight: 700;
    color: #a2ff00;
    line-height: 1.1;
}
.nx-mini-val.cyan { color: #00e5ff; }
.nx-mini-val.gold { color: #ffb300; }
.nx-mini-label {
    font-family: 'Space Mono', monospace;
    font-size: 8px;
    color: #4a6070;
    text-transform: uppercase;
    letter-spacing: .08em;
    margin-top: 5px;
}
.nx-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 11px;
}
.nx-table th {
    text-align: left;
    padding: 10px 12px;
    font-family: 'Space Mono', monospace;
    font-size: 9px;
    text-transform: uppercase;
    letter-spacing: .08em;
    color: #4a6070;
    border-bottom: 1px solid #182230;
}
.nx-table td {
    padding: 10px 12px;
    border-bottom: 1px solid rgba(24,34,48,.6);
    color: #4a6070;
    line-height: 1.5;
    font-family: 'Space Mono', monospace;
    font-size: 10px;
}
.nx-table td:first-child { color: #d0d8e4; }
.nx-table tr:hover td { background: rgba(24,34,48,.4); }
.nx-badge {
    display: inline-block;
    padding: 2px 8px;
    border-radius: 4px;
    font-family: 'Space Mono', monospace;
    font-size: 9px;
    font-weight: 700;
}
.badge-en { background: rgba(162,255,0,.1); color: #a2ff00; }
.badge-zh { background: rgba(0,229,255,.1); color: #00e5ff; }
.badge-ref { background: rgba(255,179,0,.1); color: #ffb300; }
.badge-no-ref { background: rgba(74,96,112,.1); color: #4a6070; }
.nx-divider { border: none; border-top: 1px solid #182230; margin: 6px 0 20px; }
.login-wrap {
    max-width: 380px;
    margin: 80px auto 0;
    background: linear-gradient(160deg, #0d1720, #090e14);
    border: 1px solid #182230;
    border-radius: 16px;
    padding: 36px 32px;
    text-align: center;
}
.login-title {
    font-size: 22px;
    font-weight: 800;
    color: #e8edf2;
    margin-bottom: 6px;
}
.login-sub {
    font-family: 'Space Mono', monospace;
    font-size: 9px;
    color: #4a6070;
    text-transform: uppercase;
    letter-spacing: .12em;
    margin-bottom: 28px;
}
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════
# AUTH — simple password gate
# ══════════════════════════════════════
if "admin_authed" not in st.session_state:
    st.session_state.admin_authed = False

if not st.session_state.admin_authed:
    st.markdown("""
    <div class="login-wrap">
        <div style="width:12px;height:12px;background:#a2ff00;border-radius:50%;
                    box-shadow:0 0 14px #a2ff00;margin:0 auto 16px;"></div>
        <div class="login-title">NexaEdge</div>
        <div class="login-sub">Admin Dashboard · Restricted Access</div>
    </div>
    """, unsafe_allow_html=True)

    col_c, col_m, col_c2 = st.columns([1, 2, 1])
    with col_m:
        pw = st.text_input("Password", type="password", label_visibility="collapsed",
                           placeholder="Enter admin password")
        if st.button("Unlock Dashboard"):
            if pw == ADMIN_PASSWORD:
                st.session_state.admin_authed = True
                st.rerun()
            else:
                st.error("Incorrect password.")
    st.stop()

# ══════════════════════════════════════
# SUPABASE
# ══════════════════════════════════════
@st.cache_resource
def get_supabase() -> Client:
    return create_client(SUPABASE_URL, SUPABASE_KEY)

supabase = get_supabase()

@st.cache_data(ttl=60)
def load_all():
    try:
        res = supabase.table("whitelist").select("*").order("created_at", desc=False).execute()
        return res.data or []
    except Exception as e:
        st.error(f"Supabase error: {e}")
        return []

@st.cache_data(ttl=30)
def load_nodes():
    try:
        res = supabase.table("nodes").select("*").order("created_at", desc=False).execute()
        return res.data or []
    except:
        return []

@st.cache_data(ttl=30)
def load_heartbeats(limit=100):
    try:
        res = (supabase.table("heartbeats")
               .select("*")
               .order("reported_at", desc=True)
               .limit(limit)
               .execute())
        return res.data or []
    except:
        return []

# ══════════════════════════════════════
# HEADER
# ══════════════════════════════════════
st.image('IMG_7859.jpeg', width=100)
st.markdown('<div style="margin-top:-10px;"></div>', unsafe_allow_html=True)
h_left, h_right = st.columns([4, 1])
with h_left:
    st.markdown("""
    <div style="display:flex;align-items:center;gap:12px;padding:6px 0 2px;">
        <div style="width:11px;height:11px;background:#a2ff00;border-radius:50%;
                    box-shadow:0 0 14px #a2ff00;flex-shrink:0;"></div>
        <div style="font-family:'Syne',sans-serif;font-size:22px;font-weight:800;
                    color:#e8edf2;letter-spacing:-.02em;">
            Nexa<span style="color:#a2ff00;">Edge</span>
            <span style="font-size:13px;color:#4a6070;font-weight:400;
                         font-family:'Space Mono',monospace;margin-left:10px;">
                ADMIN · BETA P1
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)
with h_right:
    if st.button("Refresh Data", type="secondary"):
        st.cache_data.clear()
        st.rerun()
    if st.button("Sign Out", type="secondary"):
        st.session_state.admin_authed = False
        st.rerun()

st.markdown('<hr class="nx-divider">', unsafe_allow_html=True)

# ══════════════════════════════════════
# LOAD DATA
# ══════════════════════════════════════
raw = load_all()

if not raw:
    st.markdown("""
    <div style="text-align:center;padding:60px 0;font-family:'Space Mono',monospace;
                font-size:12px;color:#4a6070;">
        No registrations found. The waitlist is empty.
    </div>
    """, unsafe_allow_html=True)
    st.stop()

df = pd.DataFrame(raw)

# Parse timestamps
df["created_at"] = pd.to_datetime(df["created_at"], utc=True)
df["date"] = df["created_at"].dt.date
df["hour"] = df["created_at"].dt.hour

now_utc = datetime.now(timezone.utc)
today = now_utc.date()
yesterday = today - timedelta(days=1)
last_7 = today - timedelta(days=6)
last_30 = today - timedelta(days=29)

count_total   = len(df)
count_today   = len(df[df["date"] == today])
count_7d      = len(df[df["date"] >= last_7])
count_30d     = len(df[df["date"] >= last_30])
count_ref     = df["used_ref"].notna().sum() if "used_ref" in df.columns else 0
ref_rate      = f"{(count_ref / count_total * 100):.1f}%" if count_total > 0 else "—"
count_zh      = len(df[df.get("lang", pd.Series(dtype=str)) == "ZH"]) if "lang" in df.columns else 0
count_en      = count_total - count_zh

# ══════════════════════════════════════
# KPI ROW
# ══════════════════════════════════════
k1, k2, k3, k4, k5, k6 = st.columns(6)
with k1: st.metric("Total Signups",   f"{count_total:,}")
with k2: st.metric("Today",           f"{count_today:,}")
with k3: st.metric("Last 7 Days",     f"{count_7d:,}")
with k4: st.metric("Last 30 Days",    f"{count_30d:,}")
with k5: st.metric("Referred",        f"{count_ref:,}", ref_rate)
with k6: st.metric("EN / ZH",         f"{count_en} / {count_zh}")

st.markdown('<div style="margin-top:8px;"></div>', unsafe_allow_html=True)

# ══════════════════════════════════════
# CHARTS ROW
# ══════════════════════════════════════
ch1, ch2 = st.columns([3, 2])

with ch1:
    st.markdown("""
    <div class="nx-card-title" style="margin-bottom:10px;">
        <span style="color:#a2ff00;">▸</span> Daily Signups (Last 30 Days)
    </div>""", unsafe_allow_html=True)

    daily = (
        df[df["date"] >= last_30]
        .groupby("date")
        .size()
        .reset_index(name="signups")
    )
    daily["date"] = daily["date"].astype(str)

    if not daily.empty:
        st.bar_chart(
            daily.set_index("date")["signups"],
            color="#a2ff00",
            height=220,
        )
    else:
        st.markdown('<div style="font-family:\'Space Mono\',monospace;font-size:10px;color:#4a6070;padding:20px 0;">No data in last 30 days.</div>', unsafe_allow_html=True)

with ch2:
    st.markdown("""
    <div class="nx-card-title" style="margin-bottom:10px;">
        <span style="color:#00e5ff;">▸</span> Cumulative Growth
    </div>""", unsafe_allow_html=True)

    cum = (
        df.groupby("date")
        .size()
        .reset_index(name="n")
        .sort_values("date")
    )
    cum["cumulative"] = cum["n"].cumsum()
    cum["date"] = cum["date"].astype(str)

    if not cum.empty:
        st.line_chart(
            cum.set_index("date")["cumulative"],
            color="#00e5ff",
            height=220,
        )

# ══════════════════════════════════════
# REFERRAL LEADERBOARD
# ══════════════════════════════════════
st.markdown('<hr class="nx-divider">', unsafe_allow_html=True)

ref_left, ref_right = st.columns([3, 2])

with ref_left:
    st.markdown("""
    <div class="nx-card-title">
        <span style="color:#ffb300;">▸</span> Referral Leaderboard
    </div>""", unsafe_allow_html=True)

    if "used_ref" in df.columns:
        ref_counts = (
            df[df["used_ref"].notna()]
            .groupby("used_ref")
            .size()
            .reset_index(name="referred")
            .sort_values("referred", ascending=False)
            .head(15)
        )
        ref_counts.columns = ["Referral Code", "Signups Brought"]

        if not ref_counts.empty:
            # Build HTML table
            rows_html = ""
            for i, row in ref_counts.iterrows():
                rank = ref_counts.index.get_loc(i) + 1
                medal = {1: "🥇", 2: "🥈", 3: "🥉"}.get(rank, f"#{rank}")
                rows_html += f"""
                <tr>
                    <td style="color:#4a6070;font-size:11px;">{medal}</td>
                    <td style="color:#a2ff00;">{row['Referral Code']}</td>
                    <td style="color:#e8edf2;text-align:right;">{row['Signups Brought']}</td>
                </tr>"""
            st.markdown(f"""
            <table class="nx-table">
                <thead><tr>
                    <th>#</th>
                    <th>Code</th>
                    <th style="text-align:right;">Signups</th>
                </tr></thead>
                <tbody>{rows_html}</tbody>
            </table>""", unsafe_allow_html=True)
        else:
            st.markdown('<div style="font-family:\'Space Mono\',monospace;font-size:10px;color:#4a6070;padding:12px 0;">No referrals yet.</div>', unsafe_allow_html=True)

with ref_right:
    st.markdown("""
    <div class="nx-card-title">
        <span style="color:#a2ff00;">▸</span> Breakdown
    </div>""", unsafe_allow_html=True)

    # Referred vs organic
    organic = count_total - count_ref
    st.markdown(f"""
    <div class="nx-mini-stat" style="margin-bottom:10px;">
        <div class="nx-mini-val">{count_ref}</div>
        <div class="nx-mini-label">Referred Signups</div>
    </div>
    <div class="nx-mini-stat" style="margin-bottom:10px;">
        <div class="nx-mini-val cyan">{organic}</div>
        <div class="nx-mini-label">Organic (No Referral)</div>
    </div>
    <div class="nx-mini-stat">
        <div class="nx-mini-val gold">{ref_rate}</div>
        <div class="nx-mini-label">Referral Conversion Rate</div>
    </div>""", unsafe_allow_html=True)

    # Language split
    if "lang" in df.columns:
        st.markdown('<div style="margin-top:16px;"></div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="nx-card-title">
            <span style="color:#4a6070;">▸</span> Language Split
        </div>""", unsafe_allow_html=True)

        lang_counts = df["lang"].value_counts().reset_index()
        lang_counts.columns = ["Language", "Count"]
        st.bar_chart(
            lang_counts.set_index("Language")["Count"],
            color="#a2ff00",
            height=120,
        )

# ══════════════════════════════════════
# REGISTRANT TABLE WITH SEARCH / FILTER
# ══════════════════════════════════════
st.markdown('<hr class="nx-divider">', unsafe_allow_html=True)
st.markdown("""
<div class="nx-card-title">
    <span style="color:#a2ff00;">▸</span> All Registrants
</div>""", unsafe_allow_html=True)

f1, f2, f3 = st.columns([3, 2, 2])
with f1:
    search = st.text_input("Search", placeholder="Search email hash, wallet, ref code…")
with f2:
    lang_filter = st.selectbox("Language", ["All", "EN", "ZH"])
with f3:
    ref_filter = st.selectbox("Referral", ["All", "Has referral", "No referral"])

# Build display dataframe
display_df = df.copy()

# Mask email with hash (privacy)
display_df["email_hash"] = display_df["email"].apply(
    lambda e: hashlib.sha256(str(e).encode()).hexdigest()[:14] + "…"
)

# Wallet truncated
display_df["wallet_short"] = display_df["wallet"].apply(
    lambda w: str(w)[:6] + "…" + str(w)[-4:] if w and len(str(w)) > 10 else str(w)
) if "wallet" in display_df.columns else "—"

# Ref code
display_df["ref_code_show"] = display_df.get("ref_code", pd.Series(dtype=str)).fillna("—")
display_df["used_ref_show"] = display_df.get("used_ref", pd.Series(dtype=str)).fillna("—")

# Filters
if search:
    mask = (
        display_df["email_hash"].str.contains(search, case=False, na=False)
        | display_df["wallet_short"].str.contains(search, case=False, na=False)
        | display_df["ref_code_show"].str.contains(search, case=False, na=False)
        | display_df["used_ref_show"].str.contains(search, case=False, na=False)
    )
    display_df = display_df[mask]

if lang_filter != "All" and "lang" in display_df.columns:
    display_df = display_df[display_df["lang"] == lang_filter]

if ref_filter == "Has referral":
    display_df = display_df[display_df.get("used_ref", pd.Series(dtype=str)).notna()]
elif ref_filter == "No referral":
    display_df = display_df[display_df.get("used_ref", pd.Series(dtype=str)).isna()]

# Sort newest first
display_df = display_df.sort_values("created_at", ascending=False)

# Build HTML table
rows_html = ""
for _, row in display_df.iterrows():
    ts = row["created_at"].strftime("%Y-%m-%d %H:%M") if pd.notna(row["created_at"]) else "—"
    lang_val = row.get("lang", "—") or "—"
    lang_badge = f'<span class="nx-badge badge-{lang_val.lower()}">{lang_val}</span>'

    used_ref = row.get("used_ref_show", "—")
    ref_badge = (f'<span class="nx-badge badge-ref">{used_ref}</span>'
                 if used_ref not in ["—", None, ""]
                 else '<span class="nx-badge badge-no-ref">Organic</span>')

    rows_html += f"""
    <tr>
        <td>{ts}</td>
        <td style="color:#a2ff00;">{row['email_hash']}</td>
        <td>{row['wallet_short']}</td>
        <td>{row['ref_code_show']}</td>
        <td>{ref_badge}</td>
        <td>{lang_badge}</td>
    </tr>"""

count_shown = len(display_df)
st.markdown(f"""
<div style="font-family:'Space Mono',monospace;font-size:9px;color:#4a6070;
            margin-bottom:10px;">Showing {count_shown} of {count_total} registrants</div>
<div style="max-height:420px;overflow-y:auto;border:1px solid #182230;
            border-radius:10px;background:#040709;">
<table class="nx-table" style="width:100%;">
    <thead><tr>
        <th>Timestamp (UTC)</th>
        <th>Email Hash</th>
        <th>Wallet</th>
        <th>Their Ref Code</th>
        <th>Used Ref</th>
        <th>Lang</th>
    </tr></thead>
    <tbody>{rows_html}</tbody>
</table></div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════
# CSV EXPORT
# ══════════════════════════════════════
st.markdown('<div style="margin-top:16px;"></div>', unsafe_allow_html=True)
exp_left, exp_right = st.columns([2, 5])

with exp_left:
    export_df = display_df[[
        c for c in ["created_at", "email_hash", "wallet_short",
                    "ref_code_show", "used_ref_show", "lang"]
        if c in display_df.columns
    ]].copy()
    export_df.columns = ["Timestamp", "Email Hash", "Wallet", "Ref Code", "Used Ref", "Lang"]

    csv_buf = io.StringIO()
    export_df.to_csv(csv_buf, index=False)
    fname = f"nexaedge_waitlist_{today.strftime('%Y%m%d')}.csv"

    st.download_button(
        label="⬇ Export CSV",
        data=csv_buf.getvalue(),
        file_name=fname,
        mime="text/csv",
    )

with exp_right:
    st.markdown(f"""
    <div style="font-family:'Space Mono',monospace;font-size:9px;color:#2a3a4a;
                line-height:1.8;padding-top:10px;">
        Emails are SHA-256 hashed before export. Raw PII stays in Supabase only.<br>
        Export includes {count_shown} rows · {fname}
    </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════
# HOURLY HEATMAP (signup patterns)
# ══════════════════════════════════════
st.markdown('<hr class="nx-divider">', unsafe_allow_html=True)
st.markdown("""
<div class="nx-card-title">
    <span style="color:#00e5ff;">▸</span> Signup Hour Distribution (UTC)
</div>""", unsafe_allow_html=True)

hourly = df.groupby("hour").size().reset_index(name="signups")
all_hours = pd.DataFrame({"hour": range(24)})
hourly = all_hours.merge(hourly, on="hour", how="left").fillna(0)
hourly["hour_label"] = hourly["hour"].apply(lambda h: f"{h:02d}:00")

st.bar_chart(
    hourly.set_index("hour_label")["signups"],
    color="#00e5ff",
    height=160,
)
st.markdown("""
<div style="font-family:'Space Mono',monospace;font-size:9px;color:#2a3a4a;
            margin-top:4px;line-height:1.7;">
    Peaks indicate your most active user timezones — useful for scheduling announcements.
</div>""", unsafe_allow_html=True)

# ══════════════════════════════════════
# NODE MONITOR
# ══════════════════════════════════════
st.markdown('<hr class="nx-divider">', unsafe_allow_html=True)
st.markdown("""
<div class="nx-card-title">
    <span style="color:#a2ff00;">▸</span> Live Node Monitor
</div>""", unsafe_allow_html=True)

nodes_data = load_nodes()
hb_data    = load_heartbeats(200)

if not nodes_data:
    st.markdown("""
    <div style="font-family:'Space Mono',monospace;font-size:10px;color:#4a6070;
                padding:20px 0;">
        No nodes registered yet. Users register via the Node Portal.
    </div>""", unsafe_allow_html=True)
else:
    # Node KPIs
    total_nodes   = len(nodes_data)
    online_nodes  = sum(1 for n in nodes_data if n.get("status") == "online")
    pending_nodes = sum(1 for n in nodes_data if n.get("status") == "pending")
    offline_nodes = total_nodes - online_nodes - pending_nodes

    n1, n2, n3, n4 = st.columns(4)
    with n1: st.metric("Total Nodes",   total_nodes)
    with n2: st.metric("Online",        online_nodes,  delta="● LIVE" if online_nodes > 0 else None)
    with n3: st.metric("Pending",       pending_nodes)
    with n4: st.metric("Offline",       offline_nodes)

    st.markdown('<div style="margin-top:16px;"></div>', unsafe_allow_html=True)

    # Node table
    node_rows = []
    for n in sorted(nodes_data, key=lambda x: x.get("created_at",""), reverse=True):
        status = n.get("status", "—")
        color  = {"online": "#a2ff00", "pending": "#ffb300", "offline": "#4a6070"}.get(status, "#4a6070")
        last   = n.get("last_seen", "")[:19].replace("T"," ") if n.get("last_seen") else "Never"
        created = n.get("created_at","")[:10] if n.get("created_at") else "—"
        node_rows.append({
            "Registered": created,
            "Token": n.get("node_token","—"),
            "Status": status.upper(),
            "Device": n.get("device_model") or "—",
            "OS": n.get("os_version") or "—",
            "Last Seen": last,
        })

    node_df = pd.DataFrame(node_rows)
    st.dataframe(node_df, use_container_width=True, hide_index=True)

    # Heartbeat chart
    if hb_data:
        st.markdown('<div style="margin-top:20px;"></div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="nx-card-title">
            <span style="color:#00e5ff;">▸</span> Recent Heartbeats — CPU & Temperature
        </div>""", unsafe_allow_html=True)

        hb_df = pd.DataFrame(hb_data)
        hb_df["reported_at"] = pd.to_datetime(hb_df["reported_at"], utc=True)
        hb_df = hb_df.sort_values("reported_at")
        hb_df["time"] = hb_df["reported_at"].dt.strftime("%H:%M:%S")

        hb_chart, hb_info = st.columns([3, 1])
        with hb_chart:
            if "cpu_usage" in hb_df.columns:
                st.markdown('<div style="font-family:monospace;font-size:9px;color:#4a6070;margin-bottom:6px;text-transform:uppercase;">CPU Usage %</div>', unsafe_allow_html=True)
                st.line_chart(
                    hb_df.set_index("time")["cpu_usage"].tail(30),
                    color="#a2ff00", height=140
                )
            if "temperature" in hb_df.columns:
                st.markdown('<div style="font-family:monospace;font-size:9px;color:#4a6070;margin-bottom:6px;text-transform:uppercase;">Temperature °C</div>', unsafe_allow_html=True)
                st.line_chart(
                    hb_df.set_index("time")["temperature"].tail(30),
                    color="#00e5ff", height=140
                )

        with hb_info:
            latest = hb_data[0] if hb_data else {}
            st.markdown(f"""
            <div class="nx-mini-stat" style="margin-bottom:10px;">
                <div class="nx-mini-label">Latest CPU</div>
                <div class="nx-mini-val">{latest.get("cpu_usage", 0):.1f}%</div>
            </div>
            <div class="nx-mini-stat" style="margin-bottom:10px;">
                <div class="nx-mini-label">Latest Temp</div>
                <div class="nx-mini-val cyan">{latest.get("temperature", 0):.1f}°C</div>
            </div>
            <div class="nx-mini-stat" style="margin-bottom:10px;">
                <div class="nx-mini-label">Battery</div>
                <div class="nx-mini-val gold">{latest.get("battery_level", 0)}%</div>
            </div>
            <div class="nx-mini-stat">
                <div class="nx-mini-label">Total HB</div>
                <div class="nx-mini-val">{len(hb_data)}</div>
            </div>
            """, unsafe_allow_html=True)

# ══════════════════════════════════════
# FOOTER
# ══════════════════════════════════════
st.markdown("""
<div style="border-top:1px solid #182230;margin-top:40px;padding-top:16px;
            text-align:center;font-family:'Space Mono',monospace;
            font-size:9px;color:#2a3a4a;line-height:2;">
    NexaEdge Admin · Beta P1+P3 · Waitlist refreshes 60s · Nodes refresh 30s · All emails hashed<br>
    contact@nexaedge.org
</div>""", unsafe_allow_html=True)
