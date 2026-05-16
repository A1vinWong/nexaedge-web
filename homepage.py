import streamlit as st
import os

# 1. Page Configuration
st.set_page_config(
    page_title="NexaEdge Network | Dual-Language DePIN Gateway",
    page_icon="🟢",
    layout="centered"
)

# --- 🟢 DYNAMIC LANGUAGE SELECTION ---
# 在手机侧边栏增加语言切换器
with st.sidebar:
    st.title("🌐 Language / 语言")
    lang = st.radio("Select Language / 选择语言", ["English", "中文"], index=0)
    st.markdown("---")
    st.caption("NexaEdge Protocol v1.0.2-Stable")

# --- 🟢 CYBER-TECH CSS STYLING ---
st.markdown("""
    <style>
    .stApp { background-color: #0b0f12; }
    .feature-box {
        background-color: #11171d; 
        padding: 20px; 
        border-radius: 10px; 
        border-left: 5px solid #A2FF00; 
        margin-bottom: 20px;
    }
    div.stButton > button:first-child {
        background-color: #A2FF00 !important;
        color: #0b0f12 !important;
        font-weight: 800 !important;
        width: 100%;
        border-radius: 8px !important;
    }
    </style>
""", unsafe_allow_html=True)

# ==================== 🪐 HEADER SECTION ====================
if os.path.exists("logo.png"):
    st.image("logo.png", use_container_width=True)
else:
    st.markdown(f'<h1 style="text-align:center; color:#A2FF00;">{"NexaEdge Network" if lang == "English" else "NexaEdge 算力网络"}</h1>', unsafe_allow_html=True)

if lang == "English":
    st.markdown('<p style="font-size: 18px; color: #bdc3c7; text-align: center; margin-bottom: 35px;">Transforming 5B+ idle smartphones into high-purity data fuel factories for the AI Era.</p>', unsafe_allow_html=True)
else:
    st.markdown('<p style="font-size: 18px; color: #bdc3c7; text-align: center; margin-bottom: 35px;">让全球 50 亿部闲置手机，成为 AI 时代的高纯度语料燃料工厂</p>', unsafe_allow_html=True)

# Metric Row
c1, c2, c3 = st.columns(3)
with c1:
    st.metric(label="Fee / 抽成" if lang == "English" else "平台抽成", value="20%")
with c2:
    st.metric(label="Safety / 安全" if lang == "English" else "安全阈值", value="39°C")
with c3:
    st.metric(label="Base / 底层" if lang == "English" else "结算底座", value="Solana")

st.markdown("<hr style='border:1px solid #1e272e;'>", unsafe_allow_html=True)

# ==================== 🛠️ CORE FEATURES ====================
header_text = "⚡ Key Pillars" if lang == "English" else "⚡ 核心壁垒"
st.markdown(f'<h2 style="color:#A2FF00;">{header_text}</h2>', unsafe_allow_html=True)

if lang == "English":
    st.markdown("""
    <div class="feature-box">
        <h4 style="color:white; margin-top:0;">📱 Passive Income via Charging</h4>
        <p style="color:#bdc3c7; font-size:14px;">Earn ~0.35 USDT/hr. Just plug in, connect Wi-Fi, and lock your screen. Our WASM Sandbox cleans AI data silently.</p>
    </div>
    <div class="feature-box">
        <h4 style="color:white; margin-top:0;">🔥 39°C Thermal Guard</h4>
        <p style="color:#bdc3c7; font-size:14px;">Total device protection. System auto-throttles if the battery reaches 39°C. Zero hardware anxiety.</p>
    </div>
    <div class="feature-box">
        <h4 style="color:white; margin-top:0;">🤝 2:1 Anti-Cheat Verification</h4>
        <p style="color:#bdc3c7; font-size:14px;">Decentralized majority-voting consensus. We deliver 100% verified datasets to AI clients.</p>
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <div class="feature-box">
        <h4 style="color:white; margin-top:0;">📱 锁屏充电·睡后收入</h4>
        <p style="color:#bdc3c7; font-size:14px;">每小时赚约 0.35 USDT。只需夜间充电、连 Wi-Fi 并锁屏，WASM 沙盒即可在后台静默清洗 AI 语料。</p>
    </div>
    <div class="feature-box">
        <h4 style="color:white; margin-top:0;">🔥 39°C 智能温控屏障</h4>
        <p style="color:#bdc3c7; font-size:14px;">绝不伤机。一旦手机温度触及 39°C 临界点，系统自动降载报警，彻底打消硬件焦虑。</p>
    </div>
    <div class="feature-box">
        <h4 style="color:white; margin-top:0;">🤝 2:1 多数表决防作弊</h4>
        <p style="color:#bdc3c7; font-size:14px;">原始语料切块多点分发，通过 3 节点冗余计算与多数表决，向 AI 厂商交付 100% 验证后的数据集。</p>
    </div>
    """, unsafe_allow_html=True)

# ==================== 📊 CALCULATOR ====================
calc_header = "🧮 Yield Calculator" if lang == "English" else "🧮 收益计算器"
st.markdown(f'<h2 style="color:#A2FF00;">{calc_header}</h2>', unsafe_allow_html=True)

roles = ["Node Operator (Retail)", "AI Client (Enterprise)"] if lang == "English" else ["手机持有者 (C端)", "AI 厂商 (B端)"]
role = st.selectbox("Identity / 身份:" if lang == "English" else "选择您的身份:", roles)

if "Retail" in role or "C端" in role:
    h = st.slider("Hours/Day" if lang == "English" else "每天挂机小时数:", 1, 12, 6)
    daily = h * 0.35
    monthly = daily * 30
    if lang == "English":
        st.success(f"🎉 Est. Monthly Yield: **{monthly:.2f} USDT**")
    else:
        st.success(f"🎉 预计每月躺赚: **{monthly:.2f} USDT**")
else:
    gb = st.number_input("Dataset Size (GB):" if lang == "English" else "需要清洗的语料 (GB):", min_value=1, value=100)
    cost = gb * 6.0
    if lang == "English":
        st.warning(f"💼 Total Procurement Cost: **{cost:.2f} USD**")
    else:
        st.warning(f"💼 算力采购总预算: **{cost:.2f} USD**")

st.markdown("<hr style='border:1px solid #1e272e;'>", unsafe_allow_html=True)

# ==================== 📧 WHITELIST FORM ====================
join_header = "🚀 Genesis Whitelist" if lang == "English" else "🚀 早期白名单预约"
st.markdown(f'<h2 style="color:#A2FF00;">{join_header}</h2>', unsafe_allow_html=True)

with st.form("whitelist_form"):
    email_label = "Email Address" if lang == "English" else "电子邮箱"
    wallet_label = "Solana Wallet (Optional)" if lang == "English" else "Solana 钱包地址 (选填)"
    btn_label = "SECURE MY SEAT ⚡" if lang == "English" else "立即锁定席位 ⚡"
    
    user_email = st.text_input(email_label)
    wallet_addr = st.text_input(wallet_label)
    submitted = st.form_submit_button(btn_label)
    
    if submitted:
        if user_email:
            st.balloons()
            msg = "Whitelisted!" if lang == "English" else "已加入白名单！"
            st.success(f"🎯 {msg}")
            with open("whitelist.txt", "a") as f:
                f.write(f"{user_email},{wallet_addr}\n")
        else:
            err = "Enter a valid email." if lang == "English" else "请输入有效的邮箱。"
            st.error(err)
