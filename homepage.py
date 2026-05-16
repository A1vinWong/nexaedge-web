import streamlit as st
import os

# 1. Global Page Configuration (Responsive for Mobile & Desktop)
st.set_page_config(
    page_title="NexaEdge Network | Tier-3 Mobile DePIN Network",
    page_icon="🟢",
    layout="centered"
)

# Custom Cyberpunk Cyber-Green CSS (Perfect match for your high-tech Logo)
st.markdown("""
    <style>
    .stApp {
        background-color: #0b0f12;
    }
    h1, h2, h3, h4 {
        font-family: 'Inter', sans-serif;
    }
    .metric-card {
        background-color: #11171d;
        padding: 15px;
        border-radius: 8px;
        border: 1px solid #1e272e;
        text-align: center;
    }
    /* Streamlit widget styling override for dark mode consistency */
    div.stButton > button:first-child {
        background-color: #A2FF00 !important;
        color: #0b0f12 !important;
        font-weight: 700 !important;
        border: none !important;
        width: 100%;
    }
    </style>
""", unsafe_allow_html=True)

# ==================== 🪐 HEADER: LOGO & HERO SECTION ====================

# Render the high-end NexaEdge Logo from your repository
if os.path.exists("logo.png"):
    st.image("logo.png", use_container_width=True)
else:
    st.markdown('<h1 style="text-align:center; color:#A2FF00; font-size:42px; font-weight:800; margin-bottom:0;">NexaEdge Network</h1>', unsafe_allow_html=True)
    st.caption("⚠️ Founder Note: Please ensure 'logo.png' is in the root directory to activate brand visuals.")

st.markdown('<p style="font-size: 18px; color: #bdc3c7; text-align: center; margin-top:10px; margin-bottom: 35px;">Transforming 5B+ idle smartphones into high-purity data fuel factories for the AI Era.</p>', unsafe_allow_html=True)

# Real-time Ecosystem Metrics Group
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="💰 Network Protocol Fee", value="20%", delta="Pure Revenue Generation")
with col2:
    st.metric(label="🌡️ Fail-Safe Threshold", value="39°C", delta="Device Safety Lock", delta_color="inverse")
with col3:
    st.metric(label="🌐 Settlement Base Layer", value="Solana SPL", delta="Ultra-Low Gas / High TPS")

st.markdown("<hr style='border:1px solid #1e272e;'>", unsafe_allow_html=True)

# ==================== 🛠️ CORE VALUE PROPOSITIONS ====================
st.markdown('<h2 style="color:#A2FF00; font-size:26px;">⚡ Why NexaEdge?</h2>', unsafe_allow_html=True)

st.markdown("""
<div style="background-color: #11171d; padding: 20px; border-radius: 10px; border-left: 5px solid #A2FF00; margin-bottom: 15px;">
    <h4 style="color:#ffffff; margin-top:0; font-size:18px;">📱 For Users: Screen-Locked Charging = Passive Income</h4>
    <p style="color:#bdc3c7; margin-bottom:0; font-size:14px;">No expensive proprietary hardware required. Simply plug in your phone at night, connect to Wi-Fi, and lock your screen. NexaEdge’s lightweight WASM Sandbox runs seamlessly in the background, earning you approximately <b>0.30 to 0.35 USDT per hour</b> by processing micro-tasks for AI training models.</p>
</div>
<div style="background-color: #11171d; padding: 20px; border-radius: 10px; border-left: 5px solid #A2FF00; margin-bottom: 15px;">
    <h4 style="color:#ffffff; margin-top:0; font-size:18px;">🔥 Hardware Guard: The 39°C Smart Thermal Barrier</h4>
    <p style="color:#bdc3c7; margin-bottom:0; font-size:14px;">Device longevity is our absolute bottom line. If battery temperature touches the 39°C threshold, a multi-end synchronized protocol triggers instantly, flashing real-time dashboards and automatically throttling computational loads. Zero hardware degradation anxiety.</p>
</div>
<div style="background-color: #11171d; padding: 20px; border-radius: 10px; border-left: 5px solid #A2FF00; margin-bottom: 15px;">
    <h4 style="color:#ffffff; margin-top:0; font-size:18px;">🤝 For AI Clients: 2:1 Redundant Anti-Cheat Verification</h4>
    <p style="color:#bdc3c7; margin-bottom:0; font-size:14px;">Raw datasets are sharded and distributed across 3 independent nodes. Employing a decentralized majority-voting consensus mechanism, the network completely eliminates simulator exploits and corrupted inputs, guaranteeing 100% verified, golden-grade datasets for LLM refinement.</p>
</div>
""", unsafe_allow_html=True)

st.markdown("<hr style='border:1px solid #1e272e;'>", unsafe_allow_html=True)

# ==================== 📊 INTERACTIVE ECOSYSTEM CALCULATOR ====================
st.markdown('<h2 style="color:#A2FF00; font-size:26px;">🧮 Interactive Tokenomic Calculator</h2>', unsafe_allow_html=True)
role = st.selectbox("Select Your Role in the Ecosystem:", ["Node Operator (Supply-Side / Retail User)", "AI Enterprise Client (Demand-Side / Model Buyer)"])

if role == "Node Operator (Supply-Side / Retail User)":
    hours = st.slider("Estimated overnight session duration (Hours/Day):", 1, 12, 6)
    device = st.radio("Your Mobile Operating System:", ["iOS (iPhone)", "Android Device"])
    
    # Premium rate for iOS sandboxing due to security primitives
    rate = 0.35 if "iOS" in device else 0.30
    daily_earn = hours * rate
    monthly_earn = daily_earn * 30
    
    st.success(f"🎉 Estimated Daily Earnings: **{daily_earn:.2f} USDT**")
    st.info(f"📈 Estimated Monthly Cumulative Yield: **{monthly_earn:.2f} USDT** (Easily offsets your mobile carrier bill!)")

else:
    data_need = st.number_input("Compute / Data Dataset Size Required (GB):", min_value=1, value=100)
    # Enterprise standard B2B pricing setup at $6.00 / GB of ultra-purified data
    total_cost = data_need * 6.0
    platform_cut = total_cost * 0.20
    
    st.warning(f"💼 Total Computing Procurement Budget: **{total_cost:.2f} USD**")
    st.success(f"🪙 NexaEdge Protocol Service Fee Capture (20% Pure Cashflow Margin): **{platform_cut:.2f} USD**")

st.markdown("<hr style='border:1px solid #1e272e;'>", unsafe_allow_html=True)

# ==================== 📧 LEAD GENERATION: WHITELIST & AIRDROP ====================
st.markdown('<h2 style="color:#A2FF00; font-size:26px;">🚀 Join the Alpha Testnet Whitelist (Airdrop Reservation)</h2>', unsafe_allow_html=True)
st.write("Submit your credentials below to lock in Genesis Node status and receive priority `$NEXA` airdrop distribution when we go live on Solana.")

with st.form("whitelist_form"):
    user_email = st.text_input("Enter your institutional or personal Email Address:")
    wallet_addr = st.text_input("Your Solana Wallet Address (Phantom / Solflare - Optional):")
    submitted = st.form_submit_button("SECURE MY GENESIS NODE SEAT NOW ⚡")
    
    if submitted:
        if user_email:
            st.balloons()
            st.success(f"🎯 Verified! {user_email} has been successfully whitelisted for the NexaEdge Tier-3 Genesis Launch.")
            with open("whitelist.txt", "a") as f:
                f.write(f"{user_email},{wallet_addr}\n")
        else:
            st.error("Please enter a valid email address to complete registration.")
