import streamlit as st
import time
import hashlib

st.set_page_config(
    page_title="NexaEdge Admin Console",
    page_icon="🔐",
    layout="centered"
)

# ══════════════════════════════════════
# 共享同一个全局数据库
# ══════════════════════════════════════
@st.cache_resource
def get_global_db():
    return {
        "registrations": [],
        "whitelisted_emails": set(),
        "base_sessions": 142,
    }

global_db = get_global_db()

ADMIN_PASSWORD = "nexaedge2026admin"

# ══════════════════════════════════════
# CSS
# ══════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Syne:wght@400;600;700;800&display=swap');

.main .block-container { padding-top: 1.5rem !important; padding-bottom: 3rem !important; max-width: 960px !important; }
.stApp { background-color: #060b0f; }
#MainMenu, footer, header, [data-testid="stHeader"] { display: none !important; }

.stApp::before {
    content: ''; position: fixed; inset: 0;
    background-image: linear-gradient(rgba(162,255,0,0.015) 1px, transparent 1px), linear-gradient(90deg, rgba(162,255,0,0.015) 1px, transparent 1px);
    background-size: 44px 44px; pointer-events: none; z-index: 0;
}

*, h1, h2, h3, h4, p, div, span, label { font-family: 'Syne', sans-serif; }

[data-testid="stMetric"] { background: linear-gradient(135deg, #0d1720 0%, #0a1118 100%) !important; border: 1px solid #182230 !important; border-radius: 12px !important; padding: 18px !important; }
[data-testid="stMetricLabel"] { font-family: 'Space Mono', monospace !important; font-size: 9px !important; color: #4a6070 !important; text-transform: uppercase !important; letter-spacing: 0.1em !important; }
[data-testid="stMetricValue"] { font-size: 28px !important; font-weight: 800 !important; color: #e8edf2 !important; }

div.stButton > button {
    background: linear-gradient(135deg, #a2ff00 0%, #8de600 100%) !important;
    color: #060b0f !important; font-family: 'Space Mono', monospace !important;
    font-size: 11px !important; font-weight: 700 !important; text-transform: uppercase !important;
    letter-spacing: 0.06em !important; border: none !important; border-radius: 8px !important;
    padding: 11px 22px !important; width: 100% !important;
}
div.stButton > button:hover { background: linear-gradient(135deg, #b5ff33 0%, #a2ff00 100%) !important; box-shadow: 0 0 20px rgba(162,255,0,0.2) !important; }
div.stButton > button[kind="secondary"] { background: transparent !important; color: #4a6070 !important; border: 1px solid #182230 !important; box-shadow: none !important; }
div.stButton > button[kind="secondary"]:hover { border-color: #f43f5e !important; color: #f43f5e !important; box-shadow: none !important; }

.stTextInput > div > div > input {
    background: #060b0f !important; border: 1px solid #182230 !important;
    border-radius: 8px !important; color: #e8edf2 !important;
    font-family: 'Space Mono', monospace !important; font-size: 13px !important; padding: 12px 14px !important;
}
.stTextInput > div > div > input:focus { border-color: #a2ff00 !important; box-shadow: 0 0 0 2px rgba(162,255,0,0.1) !important; }
.stTextInput label { font-family: 'Space Mono', monospace !important; font-size: 10px !important; color: #4a6070 !important; text-transform: uppercase !important; }

.nx-card { background: linear-gradient(160deg, #0d1720 0%, #090e14 100%); border: 1px solid #182230; border-radius: 14px; padding: 22px 24px; margin-bottom: 16px; }
.nx-card-title { font-family: 'Space Mono', monospace; font-size: 10px; color: #4a6070; text-transform: uppercase; letter-spacing: 0.12em; margin-bottom: 18px; display: flex; align-items: center; gap: 8px; }
.nx-card-title .dot { color: #a2ff00; }

.admin-table { width: 100%; border-collapse: collapse; font-size: 11px; }
.admin-table th { text-align: left; padding: 11px 14px; font-family: 'Space Mono', monospace; font-size: 9px; color: #4a6070; text-transform: uppercase; letter-spacing: 0.08em; border-bottom: 2px solid #182230; }
.admin-table td { padding: 12px 14px; border-bottom: 1px solid rgba(24,34,48,0.5); color: #e8edf2; font-family: 'Space Mono', monospace; font-size: 10px; vertical-align: middle; }
.admin-table td.dim { color: #4a6070; }
.admin-table td.wallet { max-width: 160px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; color: #4a6070; }
.admin-table tr:hover td { background: rgba(24,34,48,0.4); }
.admin-table tr:last-child td { border-bottom: none; }

.admin-badge { display: inline-block; background: rgba(162,255,0,0.1); color: #a2ff00; border-radius: 4px; padding: 3px 9px; font-size: 9px; font-weight: 700; letter-spacing: 0.08em; font-family: 'Space Mono', monospace; }
.badge-en { background: rgba(0,229,255,0.1); color: #00e5ff; border-radius: 4px; padding: 2px 7px; font-size: 9px; font-family: 'Space Mono', monospace; }
.badge-zh { background: rgba(255,179,0,0.1); color: #ffb300; border-radius: 4px; padding: 2px 7px; font-size: 9px; font-family: 'Space Mono', monospace; }

.nx-login-wrap { max-width: 400px; margin: 60px auto 0; }
.nx-divider { border: none; border-top: 1px solid #182230; margin: 8px 0 16px 0; }

.stat-highlight { font-family: 'Space Mono', monospace; font-size: 10px; color: #4a6070; margin-top: 4px; }
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════
# Session state
# ══════════════════════════════════════
if 'admin_auth' not in st.session_state:
    st.session_state.admin_auth = False
if 'admin_pw_err' not in st.session_state:
    st.session_state.admin_pw_err = False

# ══════════════════════════════════════
# Header
# ══════════════════════════════════════
st.markdown("""
<div style="display:flex;align-items:center;gap:12px;padding:10px 0 4px 0;">
    <div style="width:10px;height:10px;background:#a2ff00;border-radius:50%;box-shadow:0 0 12px #a2ff00;flex-shrink:0;"></div>
    <div style="font-family:'Syne',sans-serif;font-size:20px;font-weight:800;color:#e8edf2;letter-spacing:-0.02em;">
        Nexa<span style="color:#a2ff00;">Edge</span> · Admin Console
    </div>
    <div style="margin-left:auto;">
        <span style="background:rgba(244,63,94,0.1);border:1px solid rgba(244,63,94,0.25);color:#f43f5e;font-family:'Space Mono',monospace;font-size:9px;font-weight:700;padding:4px 10px;border-radius:5px;letter-spacing:0.08em;">🔐 RESTRICTED</span>
    </div>
</div>
<hr class="nx-divider">
""", unsafe_allow_html=True)

# ══════════════════════════════════════
# LOGIN GATE
# ══════════════════════════════════════
if not st.session_state.admin_auth:
    st.markdown('<div class="nx-login-wrap">', unsafe_allow_html=True)
    st.markdown("""
    <div class="nx-card" style="text-align:center;padding:36px 28px;">
        <div style="font-size:40px;margin-bottom:14px;">🔐</div>
        <div style="font-family:'Space Mono',monospace;font-size:13px;font-weight:700;color:#e8edf2;margin-bottom:6px;">Admin Authentication</div>
        <div style="font-family:'Space Mono',monospace;font-size:10px;color:#4a6070;margin-bottom:24px;">Enter your admin password to continue</div>
    </div>
    """, unsafe_allow_html=True)

    pw = st.text_input("Admin Password", type="password",
                       placeholder="Enter password...", key="admin_pw_field")

    if st.button("🔓 Unlock Console", key="admin_login_btn"):
        if pw == ADMIN_PASSWORD:
            st.session_state.admin_auth = True
            st.session_state.admin_pw_err = False
            st.rerun()
        else:
            st.session_state.admin_pw_err = True

    if st.session_state.admin_pw_err:
        st.error("❌ Incorrect password. Access denied.")

    st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# ══════════════════════════════════════
# ADMIN DASHBOARD（登录后）
# ══════════════════════════════════════
regs = global_db["registrations"]
total_sessions = global_db['base_sessions'] + len(regs)

# Top stats
c1, c2, c3, c4 = st.columns(4)
with c1: st.metric("📋 Registrations", len(regs))
with c2: st.metric("✅ Unique Emails", len(global_db["whitelisted_emails"]))
with c3: st.metric("🌐 Total Sessions", total_sessions)
with c4:
    en_count = sum(1 for r in regs if r.get('lang') == 'EN')
    zh_count = sum(1 for r in regs if r.get('lang') == 'ZH')
    st.metric("🌍 EN / ZH", f"{en_count} / {zh_count}")

st.markdown('<div style="margin-top:20px;"></div>', unsafe_allow_html=True)

# ── Referral network stats
if regs:
    ref_used = [r for r in regs if r.get('used_ref') and r['used_ref'] != '—']
    top_refs = {}
    for r in ref_used:
        code = r['used_ref']
        top_refs[code] = top_refs.get(code, 0) + 1

    if top_refs:
        best_ref = max(top_refs, key=top_refs.get)
        r1, r2 = st.columns(2)
        with r1:
            st.markdown(f"""
            <div class="nx-card" style="padding:16px 20px;">
                <div class="nx-card-title"><span class="dot">▸</span> Referral Activity</div>
                <div style="display:flex;gap:24px;">
                    <div><div style="font-family:'Space Mono',monospace;font-size:22px;font-weight:700;color:#a2ff00;">{len(ref_used)}</div><div class="stat-highlight">used a ref code</div></div>
                    <div><div style="font-family:'Space Mono',monospace;font-size:22px;font-weight:700;color:#00e5ff;">{len(top_refs)}</div><div class="stat-highlight">unique codes used</div></div>
                    <div><div style="font-family:'Space Mono',monospace;font-size:14px;font-weight:700;color:#ffb300;">{best_ref}</div><div class="stat-highlight">top referrer ({top_refs[best_ref]}x)</div></div>
                </div>
            </div>""", unsafe_allow_html=True)
        with r2:
            # Timeline - registrations per day
            from collections import Counter
            days = Counter(r['timestamp'][:10] for r in regs)
            day_list = sorted(days.items())
            timeline_html = '<div class="nx-card" style="padding:16px 20px;"><div class="nx-card-title"><span class="dot">▸</span> Daily Registrations</div><div style="display:flex;gap:6px;align-items:flex-end;height:50px;">'
            if day_list:
                max_count = max(v for _, v in day_list)
                for day, count in day_list[-7:]:
                    h = max(4, int((count / max_count) * 46))
                    timeline_html += f'<div style="display:flex;flex-direction:column;align-items:center;gap:3px;flex:1;"><div style="width:100%;background:#a2ff00;border-radius:3px 3px 0 0;height:{h}px;"></div><div style="font-family:\'Space Mono\',monospace;font-size:7px;color:#4a6070;">{count}</div></div>'
            timeline_html += '</div></div>'
            st.markdown(timeline_html, unsafe_allow_html=True)

# ── Main registrations table
st.markdown(f"""
<div class="nx-card">
    <div class="nx-card-title">
        <span class="dot">▸</span> Whitelist Registrations
        <span style="margin-left:auto;font-size:10px;color:#a2ff00;">{len(regs)} total</span>
    </div>
""", unsafe_allow_html=True)

if regs:
    rows_html = ""
    for i, r in enumerate(reversed(regs)):  # newest first
        idx = len(regs) - i
        lang_badge = f'<span class="badge-en">EN</span>' if r.get('lang') == 'EN' else f'<span class="badge-zh">ZH</span>'
        used_ref = r.get('used_ref', '—')
        used_ref_html = f'<span style="color:#a2ff00;font-size:9px;">{used_ref}</span>' if used_ref != '—' else '<span style="color:#2a3a4a;">—</span>'
        rows_html += f"""<tr>
            <td class="dim">{idx}</td>
            <td><strong style="color:#e8edf2;">{r['email']}</strong></td>
            <td class="wallet" title="{r['wallet']}">{r['wallet'][:16]}...{r['wallet'][-6:]}</td>
            <td><span class="admin-badge">{r['ref_code']}</span></td>
            <td>{used_ref_html}</td>
            <td>{lang_badge}</td>
            <td class="dim" style="white-space:nowrap;">{r['timestamp']}</td>
        </tr>"""

    st.markdown(f"""
    <div style="overflow-x:auto;">
        <table class="admin-table">
            <thead><tr>
                <th>#</th>
                <th>Email</th>
                <th>Solana Wallet</th>
                <th>Ref Code</th>
                <th>Used Ref</th>
                <th>Lang</th>
                <th>Timestamp</th>
            </tr></thead>
            <tbody>{rows_html}</tbody>
        </table>
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <div style="text-align:center;padding:40px 0;font-family:'Space Mono',monospace;font-size:12px;color:#4a6070;">
        No registrations yet.<br><br>
        <span style="font-size:10px;color:#2a3a4a;">Whitelist entries will appear here once users register.</span>
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ── Action buttons
b1, b2, b3 = st.columns([2, 1, 1])
with b1:
    if regs:
        csv_lines = ["#,Email,Wallet,RefCode,UsedRef,Lang,Timestamp"]
        for i, r in enumerate(regs):
            csv_lines.append(f"{i+1},{r['email']},{r['wallet']},{r['ref_code']},{r.get('used_ref','')},{r.get('lang','')},{r['timestamp']}")
        st.download_button(
            label="⬇ Export Full CSV",
            data="\n".join(csv_lines),
            file_name=f"nexaedge_whitelist_{time.strftime('%Y%m%d_%H%M')}.csv",
            mime="text/csv",
            key="dl_csv_admin"
        )
with b2:
    if st.button("🔄 Refresh Data", type="secondary", key="refresh_btn"):
        st.rerun()
with b3:
    if st.button("🔒 Logout", type="secondary", key="logout_btn"):
        st.session_state.admin_auth = False
        st.session_state.admin_pw_err = False
        st.rerun()

# Footer
st.markdown("""
<div style="border-top:1px solid #182230;margin-top:40px;padding-top:16px;text-align:center;font-family:'Space Mono',monospace;font-size:9px;color:#2a3a4a;line-height:2;">
    NexaEdge Admin Console · Restricted Access · contact@nexaedge.org<br>
    © 2026 NexaEdge Network
</div>
""", unsafe_allow_html=True)

