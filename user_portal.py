"""
NexaEdge User Portal — Beta P2
Supabase Magic Link Auth + Personal Dashboard
Run: streamlit run user_portal.py
"""

import streamlit as st
import hashlib
import time
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

/* Inputs */
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

/* Buttons */
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

/* Alert overrides */
.stAlert { border-radius: 8px !important; }

/* Custom components */
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

/* Rank badge — the signature element */
.nx-rank-wrap {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 32px 0 24px;
}
.nx-rank-ring {
    position: relative;
    width: 120px;
    height: 120px;
    margin-bottom: 16px;
}
.nx-rank-ring svg {
    position: absolute;
    inset: 0;
    transform: rotate(-90deg);
}
.nx-rank-number {
    position: absolute;
    inset: 0;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
}
.nx-rank-num {
    font-family: 'Space Mono', monospace;
    font-size: 28px;
    font-weight: 700;
    color: #a2ff00;
    line-height: 1;
}
.nx-rank-label {
    font-family: 'Space Mono', monospace;
    font-size: 8px;
    color: #4a6070;
    text-transform: uppercase;
    letter-spacing: .1em;
    margin-top: 4px;
}
.nx-rank-title {
    font-size: 18px;
    font-weight: 800;
    color: #e8edf2;
    margin-bottom: 4px;
}
.nx-rank-sub {
    font-family: 'Space Mono', monospace;
    font-size: 10px;
    color: #4a6070;
    text-align: center;
    line-height: 1.6;
}

/* Ref code */
.nx-ref-box {
    background: #060b0f;
    border: 1px solid rgba(162,255,0,.25);
    border-radius: 12px;
    padding: 20px;
    text-align: center;
    margin-bottom: 14px;
}
.nx-ref-code {
    font-family: 'Space Mono', monospace;
    font-size: 28px;
    font-weight: 700;
    color: #a2ff00;
    letter-spacing: .25em;
    margin: 8px 0 4px;
}
.nx-ref-label {
    font-family: 'Space Mono', monospace;
    font-size: 8px;
    color: #4a6070;
    text-transform: uppercase;
    letter-spacing: .1em;
}
.nx-ref-count {
    font-family: 'Space Mono', monospace;
    font-size: 12px;
    color: #00e5ff;
    margin-top: 10px;
}

/* Stats row */
.nx-stat-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 10px;
    margin-bottom: 14px;
}
.nx-stat-item {
    background: #060b0f;
    border: 1px solid #182230;
    border-radius: 10px;
    padding: 16px;
    text-align: center;
}
.nx-stat-val {
    font-family: 'Space Mono', monospace;
    font-size: 20px;
    font-weight: 700;
    color: #e8edf2;
    line-height: 1.1;
}
.nx-stat-val.green { color: #a2ff00; }
.nx-stat-val.cyan  { color: #00e5ff; }
.nx-stat-val.gold  { color: #ffb300; }
.nx-stat-label {
    font-family: 'Space Mono', monospace;
    font-size: 8px;
    color: #4a6070;
    text-transform: uppercase;
    letter-spacing: .08em;
    margin-top: 5px;
}

/* Timeline */
.nx-timeline { padding: 4px 0; }
.nx-tl-item {
    display: flex;
    gap: 14px;
    padding-bottom: 20px;
    position: relative;
}
.nx-tl-item::before {
    content: '';
    position: absolute;
    left: 9px;
    top: 22px;
    bottom: 0;
    width: 1px;
    background: #182230;
}
.nx-tl-item:last-child::before { display: none; }
.nx-tl-dot {
    width: 20px;
    height: 20px;
    border-radius: 50%;
    background: #182230;
    border: 2px solid #182230;
    flex-shrink: 0;
    margin-top: 2px;
}
.nx-tl-dot.done  { background: #a2ff00; border-color: #a2ff00; }
.nx-tl-dot.now   { background: #00e5ff; border-color: #00e5ff;
                   box-shadow: 0 0 10px rgba(0,229,255,.5); }
.nx-tl-title {
    font-size: 13px;
    font-weight: 700;
    color: #e8edf2;
    line-height: 1.3;
}
.nx-tl-title.muted { color: #2a3a4a; }
.nx-tl-sub {
    font-family: 'Space Mono', monospace;
    font-size: 9px;
    color: #4a6070;
    margin-top: 3px;
    line-height: 1.6;
}

/* Share buttons */
.nx-share-row {
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
    gap: 8px;
    margin-top: 12px;
}
.nx-share-btn {
    display: block;
    text-align: center;
    padding: 10px 8px;
    background: #0d1720;
    border: 1px solid #182230;
    border-radius: 10px;
    color: #4a6070 !important;
    font-size: 11px;
    font-weight: 700;
    text-decoration: none;
    transition: all .2s;
}
.nx-share-btn:hover {
    border-color: #a2ff00;
    color: #a2ff00 !important;
}

/* Login page */
.nx-login-hero {
    text-align: center;
    padding: 40px 0 32px;
}
.nx-login-dot {
    width: 14px;
    height: 14px;
    background: #a2ff00;
    border-radius: 50%;
    box-shadow: 0 0 18px #a2ff00;
    margin: 0 auto 20px;
}
.nx-login-title {
    font-size: 28px;
    font-weight: 800;
    color: #e8edf2;
    letter-spacing: -.02em;
    margin-bottom: 6px;
}
.nx-login-sub {
    font-family: 'Space Mono', monospace;
    font-size: 10px;
    color: #4a6070;
    line-height: 1.7;
    max-width: 340px;
    margin: 0 auto 32px;
}

/* Stage badge */
.nx-stage {
    display: inline-block;
    background: rgba(0,229,255,.07);
    border: 1px solid rgba(0,229,255,.2);
    color: #00e5ff;
    font-family: 'Space Mono', monospace;
    font-size: 9px;
    font-weight: 700;
    padding: 4px 10px;
    border-radius: 6px;
    letter-spacing: .1em;
    margin-bottom: 20px;
}

.nx-footer {
    border-top: 1px solid #182230;
    margin-top: 40px;
    padding-top: 16px;
    text-align: center;
    font-family: 'Space Mono', monospace;
    font-size: 9px;
    color: #2a3a4a;
    line-height: 2;
}
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════
# SUPABASE CLIENT
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
    "login_tab": "login",  # login | verify
}.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ══════════════════════════════════════
# HELPERS
# ══════════════════════════════════════
def lookup_waitlist(email: str):
    """Find user in whitelist table by email."""
    try:
        res = (supabase.table("whitelist")
               .select("*")
               .eq("email", email.lower())
               .execute())
        return res.data[0] if res.data else None
    except:
        return None

def get_queue_rank(email: str) -> int:
    """Return 1-based position of email in waitlist ordered by created_at."""
    try:
        res = (supabase.table("whitelist")
               .select("email")
               .order("created_at", desc=False)
               .execute())
        emails = [r["email"] for r in res.data]
        idx = emails.index(email.lower())
        return idx + 1
    except:
        return 0

def get_total_signups() -> int:
    try:
        res = supabase.table("whitelist").select("id", count="exact").execute()
        return res.count or 0
    except:
        return 0

def count_referrals(ref_code: str) -> int:
    """How many people used this ref code."""
    try:
        res = (supabase.table("whitelist")
               .select("id", count="exact")
               .eq("used_ref", ref_code)
               .execute())
        return res.count or 0
    except:
        return 0

def send_otp(email: str) -> bool:
    """Send Supabase email OTP (6-digit code, no magic link)."""
    try:
        supabase.auth.sign_in_with_otp({
            "email": email,
            "options": {
                "should_create_user": True,
                "data": {}
            }
        })
        return True
    except Exception as e:
        st.error(f"Failed to send code: {e}")
        return False

def verify_otp(email: str, token: str):
    """Verify the 6-digit OTP code."""
    try:
        res = supabase.auth.verify_otp({
            "email": email,
            "token": token.strip(),
            "type": "email"
        })
        return res.user
    except Exception as e:
        return None

# ══════════════════════════════════════
# HEADER (always visible)
# ══════════════════════════════════════
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
        # Email exists in auth but not in waitlist
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

    rank        = get_queue_rank(email)
    total       = get_total_signups()
    referrals   = count_referrals(ref_code)
    pct_rank    = round((1 - (rank - 1) / max(total, 1)) * 100) if total > 0 else 0

    # ── Rank ring (signature element)
    # SVG ring: circumference = 2π×52 ≈ 326.7
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

    # ── Stats
    wallet_short = wallet[:6] + "…" + wallet[-4:] if wallet != "—" and len(wallet) > 10 else wallet
    used_ref = data.get("used_ref") or "—"

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

    # ── Referral code box
    share_text = f"Join the NexaEdge waitlist — distributed edge AI on smartphones. Use my code {ref_code}"
    tg_url  = f"https://t.me/share/url?url=https://nexaedge.streamlit.app&text={share_text}"
    x_url   = f"https://twitter.com/intent/tweet?text={share_text}"
    wa_url  = f"https://wa.me/?text={share_text}"

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

    # Copy button
    if st.button("📋 Copy Referral Code"):
        st.components.v1.html(
            f'<script>navigator.clipboard.writeText("{ref_code}").catch(()=>{{}});</script>',
            height=0, width=0
        )
        st.toast("✅ Code copied!")

    # ── Node Roadmap
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
                <div class="nx-tl-dot now"></div>
                <div>
                    <div class="nx-tl-title">Community Building</div>
                    <div class="nx-tl-sub">Refer friends to move up the queue · Q2 2026</div>
                </div>
            </div>
            <div class="nx-tl-item">
                <div class="nx-tl-dot"></div>
                <div>
                    <div class="nx-tl-title muted">Alpha Invite</div>
                    <div class="nx-tl-sub">50-device internal test · Q3 2026</div>
                </div>
            </div>
            <div class="nx-tl-item">
                <div class="nx-tl-dot"></div>
                <div>
                    <div class="nx-tl-title muted">Beta Node Client</div>
                    <div class="nx-tl-sub">Install app · start earning sim NEXA · Q4 2026</div>
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

    # ── NEXA disclaimer
    st.markdown("""
    <div class="nx-notice">
        ⚠ NEXA tokens are minted on Solana but not yet in public circulation.
        Your wallet address is saved for future airdrop eligibility.
        No tokens have been distributed. This is not a financial instrument.
    </div>
    """, unsafe_allow_html=True)

    # ── Sign out
    if st.button("Sign Out", type="secondary"):
        st.session_state.user_email = None
        st.session_state.user_data  = None
        st.session_state.magic_sent = False
        st.rerun()

# ══════════════════════════════════════
# NOT LOGGED IN — LOGIN FLOW
# ══════════════════════════════════════
else:
    total = get_total_signups()

    st.markdown(f"""
    <div class="nx-login-hero">
        <div class="nx-login-dot"></div>
        <div style="margin-bottom:10px;">
            <span class="nx-stage">⚠ CONCEPT DEMO · PRE-SEED</span>
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

    # ── Step 1: enter email
    if not st.session_state.magic_sent:
        email_input = st.text_input(
            "Email Address",
            placeholder="you@example.com",
            key="login_email_input"
        )

        if st.button("Send Login Code"):
            if not email_input or "@" not in email_input:
                st.error("Please enter a valid email address.")
            else:
                # Check if email is on waitlist first
                record = lookup_waitlist(email_input)
                if not record:
                    st.error("This email is not on the waitlist. Please register at the main site first.")
                else:
                    ok = send_otp(email_input)
                    if ok:
                        st.session_state.magic_sent  = True
                        st.session_state.magic_email = email_input
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

    # ── Step 2: enter OTP code
    else:
        st.markdown(f"""
        <div style="background:rgba(162,255,0,.04);border:1px solid rgba(162,255,0,.15);
                    border-radius:12px;padding:20px;text-align:center;margin-bottom:20px;">
            <div style="font-size:24px;margin-bottom:8px;">📬</div>
            <div style="font-size:14px;font-weight:700;color:#e8edf2;margin-bottom:6px;">
                Check your inbox
            </div>
            <div style="font-family:'Space Mono',monospace;font-size:10px;color:#4a6070;
                        line-height:1.7;">
                We sent a 6-digit code to<br>
                <strong style="color:#a2ff00;">{st.session_state.magic_email}</strong>
            </div>
        </div>
        """, unsafe_allow_html=True)

        otp_input = st.text_input(
            "6-Digit Code",
            placeholder="e.g. 123456",
            max_chars=6,
            key="otp_input"
        )

        if st.button("Verify & Sign In"):
            if not otp_input or len(otp_input) < 6:
                st.error("Please enter the 6-digit code from your email.")
            else:
                with st.spinner("Verifying…"):
                    user = verify_otp(st.session_state.magic_email, otp_input.strip())
                if user:
                    record = lookup_waitlist(st.session_state.magic_email)
                    st.session_state.user_email = st.session_state.magic_email
                    st.session_state.user_data  = record
                    st.session_state.magic_sent = False
                    st.rerun()
                else:
                    st.error("Invalid or expired code. Please try again.")

        st.markdown('<div style="margin-top:10px;"></div>', unsafe_allow_html=True)
        if st.button("← Use a different email", type="secondary"):
            st.session_state.magic_sent  = False
            st.session_state.magic_email = ""
            st.rerun()

# ══════════════════════════════════════
# FOOTER
# ══════════════════════════════════════
st.markdown("""
<div class="nx-footer">
    NexaEdge Node Portal · Beta P2 · Magic link auth via Supabase<br>
    NEXA minted on Solana · Not yet in public circulation · contact@nexaedge.org
</div>
""", unsafe_allow_html=True)
