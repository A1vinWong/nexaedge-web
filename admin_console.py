import streamlit as st
import time
import hashlib
from supabase import create_client, Client

st.set_page_config(
    page_title="NexaEdge Admin",
    page_icon="🔐",
    layout="wide"
)

# ══════════════════════════════════════
# Supabase
# ══════════════════════════════════════
@st.cache_resource
def get_supabase() -> Client:
    return create_client(
        st.secrets["supabase"]["url"],
        st.secrets["supabase"]["key"]
    )

supabase = get_supabase()

def db_get_all():
    try:
        res = supabase.table("whitelist").select("*").order("created_at", desc=True).execute()
        return res.data or []
    except Exception as e:
        return []

def db_delete(row_id):
    try:
        supabase.table("whitelist").delete().eq("id", row_id).execute()
        return True
    except:
        return False

ADMIN_PASSWORD = "nexaedge2026admin"

# ══════════════════════════════════════
# CSS — 完全不同于前台，纯管理风格
# ══════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Space+Mono:wght@400;700&display=swap');

.main .block-container {
    padding-top: 0 !important;
    padding-bottom: 2rem !important;
    max-width: 100% !important;
    padding-left: 2rem !important;
    padding-right: 2rem !important;
}
.stApp { background-color: #0f1117; }
#MainMenu, footer, header, [data-testid="stHeader"] { display: none !important; }

/* Override font to Inter for admin */
*, h1, h2, h3, h4, p, div, span, label {
    font-family: 'Inter', sans-serif !important;
}

/* TOP BAR */
.admin-topbar {
    background: #1a1d27;
    border-bottom: 1px solid #2d3142;
    padding: 14px 32px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin: -1rem -2rem 2rem -2rem;
}
.admin-logo {
    display: flex;
    align-items: center;
    gap: 10px;
    font-size: 15px;
    font-weight: 700;
    color: #fff;
}
.admin-logo-dot {
    width: 8px; height: 8px;
    background: #22c55e;
    border-radius: 50%;
    box-shadow: 0 0 8px #22c55e;
}
.admin-badge-restricted {
    background: rgba(239,68,68,0.15);
    border: 1px solid rgba(239,68,68,0.3);
    color: #ef4444;
    font-size: 10px;
    font-weight: 600;
    padding: 4px 10px;
    border-radius: 4px;
    letter-spacing: 0.08em;
}

/* STAT CARDS */
.stat-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 16px;
    margin-bottom: 24px;
}
.stat-card {
    background: #1a1d27;
    border: 1px solid #2d3142;
    border-radius: 10px;
    padding: 20px 24px;
}
.stat-label {
    font-size: 11px;
    font-weight: 600;
    color: #6b7280;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-bottom: 8px;
}
.stat-value {
    font-family: 'Space Mono', monospace !important;
    font-size: 30px;
    font-weight: 700;
    color: #fff;
    line-height: 1;
}
.stat-value.green { color: #22c55e; }
.stat-value.blue { color: #3b82f6; }
.stat-value.yellow { color: #f59e0b; }
.stat-sub {
    font-size: 11px;
    color: #4b5563;
    margin-top: 6px;
}

/* TABLE */
.admin-panel {
    background: #1a1d27;
    border: 1px solid #2d3142;
    border-radius: 12px;
    overflow: hidden;
    margin-bottom: 20px;
}
.admin-panel-header {
    padding: 16px 24px;
    border-bottom: 1px solid #2d3142;
    display: flex;
    align-items: center;
    justify-content: space-between;
    background: #1e2130;
}
.admin-panel-title {
    font-size: 13px;
    font-weight: 600;
    color: #e5e7eb;
}
.admin-panel-count {
    font-family: 'Space Mono', monospace !important;
    font-size: 11px;
    color: #22c55e;
    background: rgba(34,197,94,0.1);
    border: 1px solid rgba(34,197,94,0.2);
    padding: 3px 10px;
    border-radius: 20px;
}

.reg-table {
    width: 100%;
    border-collapse: collapse;
}
.reg-table th {
    text-align: left;
    padding: 12px 20px;
    font-size: 10px;
    font-weight: 600;
    color: #6b7280;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    border-bottom: 1px solid #2d3142;
    background: #1a1d27;
    white-space: nowrap;
}
.reg-table td {
    padding: 13px 20px;
    font-size: 12px;
    color: #d1d5db;
    border-bottom: 1px solid rgba(45,49,66,0.5);
    vertical-align: middle;
}
.reg-table td.email { color: #fff; font-weight: 500; }
.reg-table td.wallet {
    font-family: 'Space Mono', monospace !important;
    font-size: 11px;
    color: #6b7280;
    max-width: 180px;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}
.reg-table td.ts {
    font-family: 'Space Mono', monospace !important;
    font-size: 10px;
    color: #4b5563;
    white-space: nowrap;
}
.reg-table tr:last-child td { border-bottom: none; }
.reg-table tr:hover td { background: rgba(255,255,255,0.02); }

.ref-pill {
    display: inline-block;
    background: rgba(34,197,94,0.1);
    color: #22c55e;
    border: 1px solid rgba(34,197,94,0.2);
    border-radius: 20px;
    padding: 2px 10px;
    font-family: 'Space Mono', monospace !important;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 0.05em;
}
.lang-pill-en {
    display: inline-block;
    background: rgba(59,130,246,0.1);
    color: #3b82f6;
    border-radius: 4px;
    padding: 2px 8px;
    font-size: 10px;
    font-weight: 600;
}
.lang-pill-zh {
    display: inline-block;
    background: rgba(245,158,11,0.1);
    color: #f59e0b;
    border-radius: 4px;
    padding: 2px 8px;
    font-size: 10px;
    font-weight: 600;
}
.used-ref-active {
    color: #22c55e;
    font-family: 'Space Mono', monospace !important;
    font-size: 10px;
}
.used-ref-none { color: #374151; }

/* ROW NUMBER */
.row-num {
    font-family: 'Space Mono', monospace !important;
    font-size: 10px;
    color: #374151;
}

/* REFERRAL BOARD */
.ref-board {
    background: #1a1d27;
    border: 1px solid #2d3142;
    border-radius: 12px;
    padding: 20px 24px;
    margin-bottom: 20px;
}
.ref-board-title {
    font-size: 13px;
    font-weight: 600;
    color: #e5e7eb;
    margin-bottom: 16px;
    padding-bottom: 12px;
    border-bottom: 1px solid #2d3142;
}
.ref-rank-row {
    display: flex;
    align-items: center;
    gap: 16px;
    padding: 10px 0;
    border-bottom: 1px solid rgba(45,49,66,0.4);
}
.ref-rank-row:last-child { border-bottom: none; }
.ref-rank-num {
    font-family: 'Space Mono', monospace !important;
    font-size: 12px;
    color: #4b5563;
    width: 20px;
}
.ref-rank-code {
    font-family: 'Space Mono', monospace !important;
    font-size: 13px;
    font-weight: 700;
    color: #22c55e;
    flex: 1;
}
.ref-rank-bar-wrap {
    flex: 2;
    background: #2d3142;
    border-radius: 3px;
    height: 4px;
    overflow: hidden;
}
.ref-rank-bar { height: 100%; background: #22c55e; border-radius: 3px; }
.ref-rank-count {
    font-family: 'Space Mono', monospace !important;
    font-size: 11px;
    color: #9ca3af;
    width: 50px;
    text-align: right;
}

/* HASH DISPLAY */
.hash-cell {
    font-family: 'Space Mono', monospace !important;
    font-size: 10px;
    color: #4b5563;
}

/* BUTTONS */
div.stButton > button {
    background: #22c55e !important;
    color: #0f1117 !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 12px !important;
    font-weight: 600 !important;
    border: none !important;
    border-radius: 6px !important;
    padding: 9px 18px !important;
    width: 100% !important;
}
div.stButton > button:hover { background: #16a34a !important; }
div.stButton > button[kind="secondary"] {
    background: #1a1d27 !important;
    color: #9ca3af !important;
    border: 1px solid #2d3142 !important;
}
div.stButton > button[kind="secondary"]:hover {
    border-color: #ef4444 !important;
    color: #ef4444 !important;
}

/* LOGIN */
.login-wrap {
    max-width: 380px;
    margin: 80px auto 0;
}
.login-card {
    background: #1a1d27;
    border: 1px solid #2d3142;
    border-radius: 14px;
    padding: 40px 32px;
    text-align: center;
}
.login-icon { font-size: 44px; margin-bottom: 16px; }
.login-title { font-size: 18px; font-weight: 700; color: #fff; margin-bottom: 6px; }
.login-sub { font-size: 12px; color: #4b5563; margin-bottom: 28px; }

.stTextInput > div > div > input {
    background: #0f1117 !important;
    border: 1px solid #2d3142 !important;
    border-radius: 6px !important;
    color: #e5e7eb !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 13px !important;
    padding: 10px 14px !important;
}
.stTextInput > div > div > input:focus {
    border-color: #22c55e !important;
    box-shadow: 0 0 0 2px rgba(34,197,94,0.15) !important;
}
.stTextInput label {
    font-size: 11px !important;
    font-weight: 500 !important;
    color: #6b7280 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.06em !important;
    font-family: 'Inter', sans-serif !important;
}

/* EXPORT BUTTON */
.stDownloadButton > button {
    background: #1e2130 !important;
    color: #22c55e !important;
    border: 1px solid rgba(34,197,94,0.3) !important;
    border-radius: 6px !important;
    font-size: 12px !important;
    font-weight: 600 !important;
    padding: 9px 18px !important;
    width: 100% !important;
}
.stDownloadButton > button:hover {
    background: rgba(34,197,94,0.1) !important;
    border-color: #22c55e !important;
}

.nx-empty {
    text-align: center;
    padding: 60px 0;
    color: #4b5563;
    font-size: 13px;
}
.nx-empty-icon { font-size: 40px; margin-bottom: 12px; }
</style>
""", unsafe_allow_html=True)

# Session state
if 'admin_auth' not in st.session_state:
    st.session_state.admin_auth = False
if 'admin_err' not in st.session_state:
    st.session_state.admin_err = False

# ══════════════════════════════════════
# LOGIN GATE
# ══════════════════════════════════════
if not st.session_state.admin_auth:
    st.markdown('<div class="login-wrap">', unsafe_allow_html=True)
    st.markdown("""
    <div class="login-card">
        <div class="login-icon">🔐</div>
        <div class="login-title">Admin Access</div>
        <div class="login-sub">NexaEdge Whitelist Registry<br>Restricted — Authorised Personnel Only</div>
    </div>
    """, unsafe_allow_html=True)
    pw = st.text_input("Password", type="password", placeholder="Enter admin password")
    if st.button("Unlock Console"):
        if pw == ADMIN_PASSWORD:
            st.session_state.admin_auth = True
            st.session_state.admin_err = False
            st.rerun()
        else:
            st.session_state.admin_err = True
    if st.session_state.admin_err:
        st.error("Incorrect password.")
    st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# ══════════════════════════════════════
# ADMIN DASHBOARD
# ══════════════════════════════════════

# Top bar
st.markdown("""
<div class="admin-topbar">
    <div class="admin-logo">
        <div class="admin-logo-dot"></div>
        NexaEdge &nbsp;<span style="color:#6b7280;font-weight:400;">/ Admin Console</span>
    </div>
    <div style="display:flex;align-items:center;gap:12px;">
        <span style="font-size:11px;color:#4b5563;">Supabase · Live Data</span>
        <span class="admin-badge-restricted">🔐 RESTRICTED</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Load data
regs = db_get_all()
total = len(regs)
en_count = sum(1 for r in regs if r.get('lang') == 'EN')
zh_count = sum(1 for r in regs if r.get('lang') == 'ZH')
ref_used_list = [r for r in regs if r.get('used_ref') and r['used_ref'] not in [None, '', '—']]
ref_used_count = len(ref_used_list)
latest_date = regs[0]['created_at'][:10] if regs else "—"

# ── Stat Cards
st.markdown(f"""
<div class="stat-grid">
    <div class="stat-card">
        <div class="stat-label">Total Registered</div>
        <div class="stat-value green">{total}</div>
        <div class="stat-sub">All whitelist entries</div>
    </div>
    <div class="stat-card">
        <div class="stat-label">Language Split</div>
        <div class="stat-value blue" style="font-size:22px;">{en_count} EN / {zh_count} ZH</div>
        <div class="stat-sub">English vs Chinese users</div>
    </div>
    <div class="stat-card">
        <div class="stat-label">Referrals Used</div>
        <div class="stat-value yellow">{ref_used_count}</div>
        <div class="stat-sub">{round(ref_used_count/total*100) if total else 0}% conversion rate</div>
    </div>
    <div class="stat-card">
        <div class="stat-label">Latest Registration</div>
        <div class="stat-value" style="font-size:20px;color:#9ca3af;">{latest_date}</div>
        <div class="stat-sub">Most recent signup</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Two-column layout
col_main, col_side = st.columns([3, 1])

with col_main:
    # Main registrations table
    st.markdown(f"""
    <div class="admin-panel">
        <div class="admin-panel-header">
            <div class="admin-panel-title">📋 Whitelist Registrations</div>
            <span class="admin-panel-count">{total} entries</span>
        </div>
    """, unsafe_allow_html=True)

    if regs:
        rows_html = ""
        for i, r in enumerate(regs):
            idx = total - i
            lang = r.get('lang', '')
            lang_html = f'<span class="lang-pill-en">EN</span>' if lang == 'EN' else f'<span class="lang-pill-zh">ZH</span>'
            used = r.get('used_ref') or ''
            used_html = f'<span class="used-ref-active">{used}</span>' if used and used != '—' else '<span class="used-ref-none">—</span>'
            wallet = r.get('wallet', '')
            wallet_short = f"{wallet[:12]}...{wallet[-6:]}" if len(wallet) > 20 else wallet
            ts = r.get('created_at', '')[:16].replace('T', ' ')
            ref_code = r.get('ref_code') or r.get('invitation_code', '—')
            email = r.get('email', '')
            email_hash = hashlib.sha256(email.encode()).hexdigest()[:8]
            rows_html += f"""<tr>
                <td class="row-num">{idx}</td>
                <td class="email">{email}</td>
                <td class="wallet" title="{wallet}">{wallet_short}</td>
                <td><span class="ref-pill">{ref_code}</span></td>
                <td>{used_html}</td>
                <td>{lang_html}</td>
                <td class="ts">{ts}</td>
                <td class="hash-cell">{email_hash}...</td>
            </tr>"""

        st.markdown(f"""
        <div style="overflow-x:auto;max-height:520px;overflow-y:auto;">
            <table class="reg-table">
                <thead>
                    <tr>
                        <th>#</th>
                        <th>Email</th>
                        <th>Solana Wallet</th>
                        <th>Ref Code</th>
                        <th>Used Ref</th>
                        <th>Lang</th>
                        <th>Registered</th>
                        <th>Hash</th>
                    </tr>
                </thead>
                <tbody>{rows_html}</tbody>
            </table>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="nx-empty">
            <div class="nx-empty-icon">📭</div>
            No registrations yet.<br>
            <span style="font-size:11px;color:#374151;">Entries appear here once users register on the main site.</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

with col_side:
    # Referral leaderboard
    from collections import Counter
    if ref_used_list:
        top_refs = Counter(r['used_ref'] for r in ref_used_list if r.get('used_ref'))
        top_list = top_refs.most_common(8)
        max_count = top_list[0][1] if top_list else 1

        rows_html = ""
        for i, (code, count) in enumerate(top_list):
            pct = int((count / max_count) * 100)
            rows_html += f"""
            <div class="ref-rank-row">
                <div class="ref-rank-num">#{i+1}</div>
                <div class="ref-rank-code">{code}</div>
                <div class="ref-rank-bar-wrap"><div class="ref-rank-bar" style="width:{pct}%;"></div></div>
                <div class="ref-rank-count">{count}x</div>
            </div>"""

        st.markdown(f"""
        <div class="ref-board">
            <div class="ref-board-title">🏆 Top Referral Codes</div>
            {rows_html}
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="ref-board">
            <div class="ref-board-title">🏆 Referral Leaderboard</div>
            <div style="text-align:center;padding:30px 0;font-size:12px;color:#4b5563;">No referrals used yet.</div>
        </div>
        """, unsafe_allow_html=True)

    # Daily signups mini chart
    if regs:
        from collections import Counter
        days = Counter(r['created_at'][:10] for r in regs)
        day_list = sorted(days.items())[-7:]
        if day_list:
            max_d = max(v for _,v in day_list) or 1
            bars = ""
            for day, count in day_list:
                h = max(6, int((count/max_d)*60))
                short_day = day[5:]
                bars += f'<div style="display:flex;flex-direction:column;align-items:center;gap:4px;flex:1;"><div style="width:100%;background:#22c55e;border-radius:3px 3px 0 0;height:{h}px;"></div><div style="font-size:8px;color:#4b5563;font-family:\'Space Mono\',monospace;">{count}</div><div style="font-size:7px;color:#374151;">{short_day}</div></div>'

            st.markdown(f"""
            <div class="ref-board">
                <div class="ref-board-title">📈 Daily Signups (7d)</div>
                <div style="display:flex;gap:6px;align-items:flex-end;height:80px;padding-top:10px;">
                    {bars}
                </div>
            </div>
            """, unsafe_allow_html=True)

    # Actions
    st.markdown('<div style="margin-top:8px;"></div>', unsafe_allow_html=True)
    if regs:
        csv_lines = ["#,Email,Wallet,RefCode,UsedRef,ReferredBy,Lang,RegisteredAt"]
        for i, r in enumerate(reversed(regs)):
            ref_code = r.get('ref_code') or r.get('invitation_code','')
            csv_lines.append(
                f"{i+1},"
                f"{r.get('email','')},"
                f"{r.get('wallet','')},"
                f"{ref_code},"
                f"{r.get('used_ref','')},"
                f"{r.get('referred_by','')},"
                f"{r.get('lang','')},"
                f"{r.get('created_at','')[:19]}"
            )
        st.download_button(
            label="⬇ Export CSV",
            data="\n".join(csv_lines),
            file_name=f"nexaedge_whitelist_{time.strftime('%Y%m%d_%H%M')}.csv",
            mime="text/csv",
            key="dl_csv"
        )

    st.markdown('<div style="margin-top:8px;"></div>', unsafe_allow_html=True)
    b1, b2 = st.columns(2)
    with b1:
        if st.button("🔄 Refresh", type="secondary"):
            st.rerun()
    with b2:
        if st.button("🔒 Logout", type="secondary"):
            st.session_state.admin_auth = False
            st.rerun()

# Footer
st.markdown("""
<div style="margin-top:40px;padding-top:16px;border-top:1px solid #2d3142;text-align:center;font-size:10px;color:#374151;font-family:'Space Mono',monospace;">
    NexaEdge Admin Console &nbsp;·&nbsp; Live Supabase Connection &nbsp;·&nbsp; contact@nexaedge.org
</div>
""", unsafe_allow_html=True)


