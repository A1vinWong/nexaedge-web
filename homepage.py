import streamlit as st
import psutil
import time
import hashlib
import pandas as pd

# ── 现代 Streamlit 路由配置 (2026 标准版) ──
st.set_page_config(
    page_title="NexaEdge Engine Console",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── 全局核心内存存储 (本地伪持久化) ──
@st.cache_resource
def get_hardware_runtime_db():
    return {
        "user_registry": {
            "admin@nexaedge.org": hashlib.sha256("nexa2026".encode()).hexdigest()
        },
        "whitelist_ledger": [],
        "telemetry_history": []
    }

runtime_db = get_hardware_runtime_db()

# 初始化节点状态
if "node_active" not in st.session_state:
    st.session_state.node_active = False
if "current_session_user" not in st.session_state:
    st.session_state.current_session_user = None

# ── 瑞士极简重工业风 UI 样式 ──
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Inter:wght@400;600;800&display=swap');

/* 基础架构重置 */
html, body, [data-testid="stAppViewContainer"] {
    background-color: #0d0f12 !important;
    font-family: 'Inter', sans-serif !important;
}
.stMarkdown p, .stMetric label, .stDataFrame, label {
    font-family: 'JetBrains Mono', monospace !important;
}

/* 侧边栏及硬件面板 */
[data-testid="stSidebar"] {
    background-color: #12161a !important;
    border-right: 1px solid #1f262e !important;
}

/* 指标卡片重塑 */
[data-testid="stMetric"] {
    background: #13171c !important;
    border: 1px solid #1f262e !important;
    border-radius: 6px !important;
    padding: 15px !important;
}
[data-testid="stMetricLabel"] {
    color: #64748b !important;
    font-size: 11px !important;
    text-transform: uppercase !important;
    letter-spacing: 0.05em;
}
[data-testid="stMetricValue"] {
    color: #f1f5f9 !important;
    font-size: 24px !important;
    font-weight: 700 !important;
}

/* 按钮规范化 */
div.stButton > button {
    border-radius: 4px !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 12px !important;
    font-weight: 700 !important;
    transition: all 0.2s ease;
}

/* 核心标题 */
.console-header {
    font-size: 22px;
    font-weight: 800;
    color: #f1f5f9;
    letter-spacing: -0.02em;
    margin-bottom: 20px;
    display: flex;
    align-items: center;
    gap: 10px;
}
.console-subtitle {
    font-size: 12px;
    color: #64748b;
    margin-top: -15px;
    margin-bottom: 25px;
}
</style>
""", unsafe_allow_html=True)

# ── 侧边栏：100% 真实的物理设备监控 ──
with st.sidebar:
    st.markdown('<div style="font-size:12px; font-weight:700; color:#94a3b8; letter-spacing:0.1em; margin-bottom:15px;">HOST HARDWARE TELEMETRY</div>', unsafe_allow_html=True)
    
    # 抓取本地真实的系统硬件指标
    real_cpu = psutil.cpu_percent(interval=None)
    real_ram = psutil.virtual_memory().percent
    
    st.metric("Host CPU Load", f"{real_cpu} %")
    st.metric("Host RAM Usage", f"{real_ram} %")
    
    st.markdown("---")
    st.markdown('<div style="font-size:11px; color:#475569;">Console Auth Status:</div>', unsafe_allow_html=True)
    if st.session_state.current_session_user:
        st.markdown(f"🟢 `Authenticated: {st.session_state.current_session_user}`")
        if st.button("Disconnect Session", use_container_width=True):
            st.session_state.current_session_user = None
            st.rerun()
    else:
        st.markdown("⚪ `Guest Mode (Read-Only)`")

# ── 核心多页面结构路由定义 ──
def page_hardware_console():
    st.markdown('<div class="console-header">⚙️ NexaEdge / Compute Core Engine</div>', unsafe_allow_html=True)
    st.markdown('<div class="console-subtitle">Hardware layer optimization & secure localized task routing pipeline.</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("⚡ INITIALIZE ENGINE RUNTIME", type="primary", use_container_width=True, disabled=st.session_state.node_active):
            st.session_state.node_active = True
            st.rerun()
    with col2:
        if st.button("🛑 HALT CORE OPERATION", type="secondary", use_container_width=True, disabled=not st.session_state.node_active):
            st.session_state.node_active = False
            st.rerun()
            
    st.markdown("### System Processing Matrix")
    
    m1, m2, m3 = st.columns(3)
    with m1:
        status_text = "OPERATIONAL ACTIVE" if st.session_state.node_active else "IDLE / STANDBY"
        st.metric("Core Engine State", status_text)
    with m2:
        # 如果激活了，根据真实的处理器分配一个理论的算力值
        hash_rate = (psutil.cpu_count() * 12.4) if st.session_state.node_active else 0.0
        st.metric("Allocated Compute Power", f"{hash_rate:.1f} kH/s")
    with m3:
        # 记录真实的白名单数量
        st.metric("Local Node Registry", f"{len(runtime_db['whitelist_ledger'])} Peers")

    # 真实的日志时间截
    st.markdown("### Cryptographic Verification Pipeline")
    if st.session_state.node_active:
        current_ts = time.strftime("%Y-%m-%d %H:%M:%S")
        log_data = {
            "Timestamp": [current_ts, current_ts, current_ts],
            "Subsystem Thread": ["Thread-0/WASM", "Thread-1/NPU", "Secp256k1/Core"],
            "Operation Event": ["Sandboxed environment loaded successfully.", "Hardware affinity parameters locked.", "Awaiting block instructions from settlement layer."],
            "Status Code": ["OK", "OK", "PENDING"]
        }
        st.dataframe(pd.DataFrame(log_data), use_container_width=True, hide_index=True)
        
        # 挂载低开销物理刷新器，保持系统监控更新
        time.sleep(2.0)
        st.rerun()
    else:
        st.info("Engine is currently dormant. Trigger initialization routine above to feed telemetry pipeline.")

def page_whitelist_ledger():
    st.markdown('<div class="console-header">📋 Genesis Whitelist Database</div>', unsafe_allow_html=True)
    st.markdown('<div class="console-subtitle">Strict cryptographic identity registration for hardware pre-allocations.</div>', unsafe_allow_html=True)
    
    with st.form("real_whitelist_form", clear_on_submit=True):
        st.markdown("**Append New Hardware Node Identity:**")
        operator_email = st.text_input("Operator Contact Email:", placeholder="e.g., engineering@nexaedge.org")
        solana_wallet = st.text_input("Target Solana Public Key Address (SPL):", placeholder="e.g., 7xK...9zP")
        
        submitted = st.form_submit_button("Commit Ledger Record Entry 💾")
        if submitted:
            if operator_email and solana_wallet:
                # 写入真内存数据库
                runtime_db["whitelist_ledger"].append({
                    "Timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                    "Identity Email": operator_email,
                    "Solana Wallet Account": solana_wallet
                })
                st.success("Record committed successfully to local cache runtime memory database.")
            else:
                st.error("Operation Rejected: Input matrices cannot contain null values.")
                
    st.markdown("### Audit Log View (Committed Ledger Records)")
    if runtime_db["whitelist_ledger"]:
        df_ledger = pd.DataFrame(runtime_db["whitelist_ledger"])
        st.dataframe(df_ledger, use_container_width=True, hide_index=True)
    else:
        st.caption("No records present in the local runtime container memory ledger yet.")

def page_account_gateway():
    st.markdown('<div class="console-header">🔑 Identity Encryption Gateway</div>', unsafe_allow_html=True)
    st.markdown('<div class="console-subtitle">Secure SHA-256 cloud-sync profile initialization protocol.</div>', unsafe_allow_html=True)
    
    if st.session_state.current_session_user:
        st.success(f"Session established. Currently authenticated as root operator: {st.session_state.current_session_user}")
    else:
        mode = st.radio("Gateway Mode", ["Operator Authenticate", "Register New Node Profile"], horizontal=True)
        
        with st.form("auth_gateway_form"):
            user_id = st.text_input("Identity Handle (Email):")
            user_secret = st.text_input("Secret Signature Token (Password):", type="password")
            
            action = st.form_submit_button("Execute Protocol Key Exchange")
            if action:
                if user_id and user_secret:
                    hashed_token = hashlib.sha256(user_secret.encode()).hexdigest()
                    
                    if mode == "Register New Node Profile":
                        if user_id in runtime_db["user_registry"]:
                            st.error("Identity handle collision: Record already allocated.")
                        else:
                            runtime_db["user_registry"][user_id] = hashed_token
                            st.session_state.current_session_user = user_id
                            st.success("New node profile cryptographically assigned.")
                            st.rerun()
                    else:
                        if user_id in runtime_db["user_registry"] and runtime_db["user_registry"][user_id] == hashed_token:
                            st.session_state.current_session_user = user_id
                            st.success("Authentication challenge signature accepted.")
                            st.rerun()
                        else:
                            st.error("Access Denied: Signature matrix verification failed.")
                else:
                    st.error("Missing identification strings.")

# ── 纯原生固态状态导航栏（杜绝刷新跳页） ──
pg_console = st.Page(page_hardware_console, title="Engine Control", icon="⚙️")
pg_whitelist = st.Page(page_whitelist_ledger, title="Ledger Registry", icon="📋")
pg_auth = st.Page(page_account_gateway, title="Identity Gateway", icon="🔑")

pg = st.navigation([pg_console, pg_whitelist, pg_auth], position="sidebar")
pg.run()
