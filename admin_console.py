import streamlit as st
import time
import hashlib
from supabase import create_client, Client

st.set_page_config(
    page_title="NexaEdge Admin Console",
    page_icon="🔐",
    layout="centered"
)

# ══════════════════════════════════════
# 同一个 Supabase 连接 — 读取真实数据
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
        st.error(f"DB Error: {e}")
        return []

def db_count():
    try:
        res = supabase.table("whitelist").select("id", count="exact").execute()
        return res.count or 0
    except:
        return 0

def db_delete(row_id):
    try:
        supabase.table("whitelist").delete().eq("id", row_id).execute()
        return True
    except:
        return False

ADMIN_PASSWORD = "nexaedge2026admin"

# ══════════════════════════════════════
# CSS
# ══════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Syne:wght@400;600;700;800&display=swap');
.main .block-container{padding-top:1.5rem!important;padding-bottom:3rem!important;max-width:1000px!important}
.stApp{background-color:#060b0f}
#MainMenu,footer,header,[data-testid="stHeader"]{display:none!important}
.stApp::before{content:'';position:fixed;inset:0;background-image:linear-gradient(rgba(162,255,0,.015) 1px,transparent 1px),linear-gradient(90deg,rgba(162,255,0,.015) 1px,transparent 1px);background-size:44px 44px;pointer-events:none;z-index:0}
*,h1,h2,h3,h4,p,div,span,label{font-family:'Syne',sans-serif}
[data-testid="stMetric"]{background:linear-gradient(135deg,#0d1720,#0a1118)!important;border:1px solid #182230!important;border-radius:12px!important;padding:18px!important}
[data-testid="stMetricLabel"]{font-family:'Space Mono',monospace!important;font-size:9px!important;color:#4a6070!important;text-transform:uppercase!important;letter-spacing:.1em!important}
[data-testid="stMetricValue"]{font-size:28px!important;font-weight:800!important;color:#e8edf2!important}
div.stButton>button{background:linear-gradient(135deg,#a2ff00,#8de600)!important;color:#060b0f!important;font-family:'Space Mono',monospace!important;font-size:11px!important;font-weight:700!important;text-transform:uppercase!important;letter-spacing:.06em!important;border:none!important;border-radius:8px!important;padding:11px 22px!important;width:100%!important}
div.stButton>button:hover{background:linear-gradient(135deg,#b5ff33,#a2ff00)!important;box-shadow:0 0 20px rgba(162,255,0,.2)!important}
div.stButton>button[kind="secondary"]{background:transparent!important;color:#4a6070!important;border:1px solid #182230!important;box-shadow:none!important}
div.stButton>button[kind="secondary"]:hover{border-color:#f43f5e!important;color:#f43f5e!important}
.stTextInput>div>div>input{background:#060b0f!important;border:1px solid #182230!important;border-radius:8px!important;color:#e8edf2!important;font-family:'Space Mono',monospace!important;font-size:13px!important;padding:12px 14px!important}
.stTextInput>div>div>input:focus{border-color:#a2ff00!important;box-shadow:0 0 0 2px rgba(162,255,0,.1)!important}
.stTextInput label{font-family:'Space Mono',monospace!important;font-size:10px!important;color:#4a6070!important;text-transform:uppercase!important}
.nx-card{background:linear-gradient(160deg,#0d1720,#090e14);border:1px solid #182230;border-radius:14px;padding:22px 24px;margin-bottom:16px}
.nx-card-title{font-family:'Space Mono',monospace;font-size:10px;color:#4a6070;text-transform:uppercase;letter-spacing:.12em;margin-bottom:18px;display:flex;align-items:center;gap:8px}
.nx-card-title .dot{color:#a2ff00}
.nx-divider{border:none;border-top:1px solid #182230;margin:8px 0 16px}
.admin-table{width:100%;border-collapse:collapse;font-size:11px}
.admin-table th{text-align:left;padding:11px 14px;font-family:'Space Mono',monospace;font-size:9px;color:#4a6070;text-transform:uppercase;letter-spacing:.08em;border-bottom:2px solid #182230}
.admin-table td{padding:12px 14px;border-bottom:1px solid rgba(24,34,48,.5);color:#e8edf2;font-family:'Space Mono',monospace;font-size:10px;vertical-align:middle}
.admin-table td.dim{color:#4a6070}
.admin-table td.wallet{max-width:160px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;color:#4a6070}
.admin-table tr:hover td{background:rgba(24,34,48,.4)}
.admin-table tr:last-child td{border-bottom:none}
.admin-badge{display:inline-block;background:rgba(162,255,0,.1);color:#a2ff00;border-radius:4px;padding:3px 9px;font-size:9px;font-weight:700;letter-spacing:.08em;font-family:'Space Mono',monospace}
.badge-en{background:rgba(0,229,255,.1);color:#00e5ff;border-radius:4px;padding:2px 7px;font-size:9px;font-family:'Space Mono',monospace}
.badge-zh{background:rgba(255,179,0,.1);color:#ffb300;border-radius:4px;padding:2px 7px;font-size:9px;font-family:'Space Mono',monospace}
.nx-login-wrap{max-width:420px;margin:60px auto 0}
.nx-footer{border-top:1px solid #182230;margin-top:40px;padding-top:16px;text-align:center;font-family:'Space Mono',monospace;font-size:9px;color:#2a3a4a;line-height:2}
</style>
""", unsafe_allow_html=True)

# Session state
if 'admin_auth' not in st.session_state: st.session_state.admin_auth = False
if 'admin_err' not in st.session_state: st.session_state.admin_err = False

# ══════════════════════════════════════
# HEADER
# ══════════════════════════════════════
st.markdown("""
<div style="display:flex;align-items:center;gap:12px;padding:10px 0 4px;">
    <div style="width:10px;height:10px;background:#a2ff00;border-radius:50%;box-shadow:0 0 12px #a2ff00;flex-shrink:0;"></div>
    <div style="font-family:'Syne',sans-serif;font-size:20px;font-weight:800;color:#e8edf2;">
        Nexa<span style="color:#a2ff00;">Edge</span> · Admin Console
    </div>
    <div style="margin-left:auto;">
        <span style="background:rgba(244,63,94,.1);border:1px solid rgba(244,63,94,.25);color:#f43f5e;font-family:'Space Mono',monospace;font-size:9px;font-weight:700;padding:4px 10px;border-radius:5px;letter-spacing:.08em;">🔐 RESTRICTED</span>
    </div>
</div>
<hr class="nx-divider">
""", unsafe_allow_html=True)

# ══════════════════════════════════════
# LOGIN GATE
# ══════════════════════════════════════
if not st.session_state.admin_auth:
    st.markdown('<div class="nx-login-wrap">', unsafe_allow_html=True)
    st.markdown("""<div class="nx-card" style="text-align:center;padding:36px 28px;">
    <div style="font-size:40px;margin-bottom:14px;">🔐</div>
    <div style="font-family:'Space Mono',monospace;font-size:13px;font-weight:700;color:#e8edf2;margin-bottom:6px;">Admin Authentication</div>
    <div style="font-family:'Space Mono',monospace;font-size:10px;color:#4a6070;margin-bottom:24px;">NexaEdge Whitelist Registry — Restricted Access</div>
    </div>""", unsafe_allow_html=True)
    pw = st.text_input("Password", type="password", placeholder="Enter admin password...", key="admin_pw")
    if st.button("🔓 Unlock Console", key="login_btn"):
        if pw == ADMIN_PASSWORD:
            st.session_state.admin_auth = True
            st.session_state.admin_err = False
            st.rerun()
        else:
            st.session_state.admin_err = True
    if st.session_state.admin_err:
        st.error("❌ Incorrect password.")
    st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# ══════════════════════════════════════
# DASHBOARD（登录后）
# ══════════════════════════════════════
regs = db_get_all()
total = len(regs)
en_count = sum(1 for r in regs if r.get('lang') == 'EN')
zh_count = sum(1 for r in regs if r.get('lang') == 'ZH')
ref_used = sum(1 for r in regs if r.get('used_ref') and r['used_ref'] not in [None, '', '—'])

# Stats
c1,c2,c3,c4 = st.columns(4)
with c1: st.metric("📋 Total Registered", total)
with c2: st.metric("🌐 EN / ZH", f"{en_count} / {zh_count}")
with c3: st.metric("🔗 Used Referral", ref_used)
with c4: st.metric("📅 Latest", regs[0]['created_at'][:10] if regs else "—")

st.markdown('<div style="margin-top:20px;"></div>', unsafe_allow_html=True)

# ── Referral leaderboard
if ref_used > 0:
    from collections import Counter
    top_refs = Counter(r['used_ref'] for r in regs if r.get('used_ref') and r['used_ref'] not in [None,'','—'])
    if top_refs:
        best = top_refs.most_common(3)
        st.markdown("""<div class="nx-card"><div class="nx-card-title"><span class="dot">▸</span> Top Referral Codes</div>""", unsafe_allow_html=True)
        rb = st.columns(len(best))
        for i,(code,count) in enumerate(best):
            with rb[i]:
                st.metric(f"#{i+1}", code, f"{count} referral{'s' if count>1 else ''}")
        st.markdown('</div>', unsafe_allow_html=True)

# ── Main table
st.markdown(f"""<div class="nx-card"><div class="nx-card-title">
<span class="dot">▸</span> Whitelist Registrations
<span style="margin-left:auto;font-size:10px;color:#a2ff00;">{total} total</span>
</div>""", unsafe_allow_html=True)

if regs:
    rows_html = ""
    for i, r in enumerate(regs):
        idx = total - i
        lang_badge = f'<span class="badge-en">EN</span>' if r.get('lang')=='EN' else f'<span class="badge-zh">ZH</span>'
        used = r.get('used_ref') or '—'
        used_html = f'<span style="color:#a2ff00;font-size:9px;">{used}</span>' if used != '—' else '<span style="color:#2a3a4a;">—</span>'
        wallet = r.get('wallet','')
        wallet_short = f"{wallet[:10]}...{wallet[-6:]}" if len(wallet)>20 else wallet
        ts = r.get('created_at','')[:19].replace('T',' ')
        ref_code = r.get('ref_code') or r.get('invitation_code','—')
        rows_html += f"""<tr>
            <td class="dim">{idx}</td>
            <td><strong style="color:#e8edf2;">{r.get('email','')}</strong></td>
            <td class="wallet" title="{wallet}">{wallet_short}</td>
            <td><span class="admin-badge">{ref_code}</span></td>
            <td>{used_html}</td>
            <td>{lang_badge}</td>
            <td class="dim" style="white-space:nowrap;">{ts}</td>
        </tr>"""

    st.markdown(f"""<div style="overflow-x:auto;">
    <table class="admin-table">
        <thead><tr><th>#</th><th>Email</th><th>Solana Wallet</th><th>Ref Code</th><th>Used Ref</th><th>Lang</th><th>Registered At</th></tr></thead>
        <tbody>{rows_html}</tbody>
    </table></div>""", unsafe_allow_html=True)
else:
    st.markdown("""<div style="text-align:center;padding:50px 0;font-family:'Space Mono',monospace;font-size:12px;color:#4a6070;">
    No registrations yet.<br><br>
    <span style="font-size:10px;color:#2a3a4a;">Entries will appear here once users register on the main site.</span>
    </div>""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ── Action buttons
b1,b2,b3 = st.columns([2,1,1])
with b1:
    if regs:
        csv_lines = ["#,Email,Wallet,RefCode,UsedRef,ReferredBy,Lang,RegisteredAt"]
        for i,r in enumerate(reversed(regs)):
            wallet = r.get('wallet','')
            ref_code = r.get('ref_code') or r.get('invitation_code','')
            csv_lines.append(f"{i+1},{r.get('email','')},{wallet},{ref_code},{r.get('used_ref','')},{r.get('referred_by','')},{r.get('lang','')},{r.get('created_at','')[:19]}")
        st.download_button(
            label="⬇ Export Full CSV",
            data="\n".join(csv_lines),
            file_name=f"nexaedge_whitelist_{time.strftime('%Y%m%d_%H%M')}.csv",
            mime="text/csv",
            key="dl_csv"
        )
with b2:
    if st.button("🔄 Refresh", type="secondary", key="refresh"):
        st.rerun()
with b3:
    if st.button("🔒 Logout", type="secondary", key="logout"):
        st.session_state.admin_auth = False
        st.rerun()

st.markdown("""<div class="nx-footer">
NexaEdge Admin Console &nbsp;·&nbsp; Restricted Access &nbsp;·&nbsp; contact@nexaedge.org<br>
© 2026 NexaEdge Network
</div>""", unsafe_allow_html=True)
