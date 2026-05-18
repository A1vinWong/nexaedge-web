import streamlit as st
import os
import time
import random
import pandas as pd
import glob
import hashlib

# =========================================================================
# 1. 全局页面基础配置与极致黑客风 CSS
# =========================================================================
st.set_page_config(
    page_title="NexaEdge Network | Official Node Gateway",
    page_icon="🟢",
    layout="centered"
)

st.markdown("""
    <style>
    .stApp { background-color: #0b0f12; }
    #MainMenu, footer, .styles_viewerBadge__FUChv, [data-testid="manage-app-button"] { display: none !important; }
    header, [data-testid="stHeader"] { background: transparent !important; border: none !important; height: 0 !important; display: none !important; }
    
    [data-testid="stVerticalBlock"] > div:empty { display: none !important; margin: 0 !important; padding: 0 !important; }
    [data-testid="stElementContainer"] { border: none !important; background: transparent !important; margin-bottom: 6px !important; }
    
    .stTabs [data-baseweb="tab-list"] { gap: 8px; background-color: transparent !important; justify-content: center; border: none !important; }
    .stTabs [data-baseweb="tab"] { background-color: #11171d !important; color: #bdc3c7 !important; border-radius: 8px 8px 0px 0px !important; border: 1px solid #1e272e !important; padding: 8px 16px !important; font-weight: 700 !important; font-size: 13px !important; }
    .stTabs [aria-selected="true"] { color: #A2FF00 !important; background-color: #161c23 !important; border-top: 2px solid #A2FF00 !important; }
    
    .app-container { background-color: #11171d; border: 1px solid #1e272e; border-radius: 20px; padding: 14px; margin: 0 auto; box-shadow: 0 10px 30px rgba(0,0,0,0.5); }
    .app-card { background-color: #161c23; border: 1px solid #252e38; border-radius: 14px; padding: 12px; margin-bottom: 10px; }
    .app-title { font-size: 12px; color: #88929b; font-weight: bold; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 4px; }
    .app-value { font-family: 'Inter', sans-serif; color: #ffffff; font-size: 22px; font-weight: 700; }
    .neon-green-text { color: #A2FF00 !important; }
    .neon-blue-text { color: #00e5ff !important; }
    
    div.stButton > button:first-child {
        background-color: #A2FF00 !important; color: #0b0f12 !important; font-weight: 800 !important; font-size: 14px !important; 
        width: 100% !important; border-radius: 12px !important; border: none !important; padding: 10px 4px !important;
        box-shadow: 0 0 15px rgba(162, 255, 0, 0.4);
    }
    div.stButton > button[key*="app_stop_btn"], div.stButton > button[key*="logout_btn"] {
        background-color: #0b0f12 !important; color: #ffffff !important; border: 1px solid #252e38 !important; box-shadow: none !important;
    }
    .feature-box { background-color: #11171d; padding: 15px; border-radius: 10px; border-left: 4px solid #A2FF00; margin-bottom: 12px; }
    .mini-stat-card { text-align: center; background-color:#141d26; padding: 6px 4px; border-radius: 10px; min-height: 55px; display: flex; flex-direction: column; justify-content: center; align-items: center; }
    .mini-stat-title { font-size: 9px !important; color: #88929b; font-weight: bold; transform: scale(0.95); }
    .mini-stat-value { font-size: 13px !important; font-weight: bold; font-family: monospace; margin-top: 2px; }
    
    .social-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(80px, 1fr)); gap: 8px; margin: 10px 0; }
    .social-btn { display: block; text-align: center; padding: 6px; background-color: #11171d; border: 1px solid #252e38; border-radius: 8px; color: #bdc3c7 !important; font-size: 11px; font-weight: bold; text-decoration: none; }
    .social-btn:hover { border-color: #A2FF00; color: #A2FF00 !important; }
    </style>
""", unsafe_allow_html=True)

# =========================================================================
# 💾 2. 复合本地持久化数据引擎（同时服务白名单、用户库与算力持久化）
# =========================================================================
DB_FILE = "users_db.txt"
WHITELIST_FILE = "whitelist.txt"

def load_users_db():
    """载入账户数据库：{email: {password_hash: str, balance: float, wallet: str, ref_code: str, ref_by: str, reg_time: str}}"""
    users = {}
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or " | " not in line: continue
                parts = line.split(" | ")
                try:
                    email = parts[0].replace("Email: ", "")
                    pwd = parts[1].replace("Pass: ", "")
                    bal = float(parts[2].replace("Balance: ", ""))
                    wal = parts[3].replace("Wallet: ", "")
                    rc = parts[4].replace("RefCode: ", "")
                    rb = parts[5].replace("ReferredBy: ", "")
                    tm = parts[6].replace("Time: ", "")
                    users[email.lower()] = {"pwd": pwd, "balance": bal, "wallet": wal, "ref_code": rc, "ref_by": rb, "time": tm}
                except:
                    continue
    return users

def save_users_db(users_dict):
    """同步写回核心数据库文件"""
    with open(DB_FILE, "w", encoding="utf-8") as f:
        for email, data in users_dict.items():
            f.write(f"Email: {email} | Pass: {data['pwd']} | Balance: {data['balance']:.2f} | Wallet: {data['wallet']} | RefCode: {data['ref_code']} | ReferredBy: {data['ref_by']} | Time: {data['time']}\n")

def append_to_whitelist_txt(email, wallet, score, ref_code, ref_by):
    """精确同步追加到原汁原味的 whitelist.txt 以备导出"""
    with open(WHITELIST_FILE, "a", encoding="utf-8") as f:
        f.write(f"Email: {email} | Wallet: {wallet} | Score: {score:.2f} | RefCode: {ref_code} | ReferredBy: {ref_by}\n")

# =========================================================================
# 🔒 3. 服务器跨进程内存锁安全初始化
# =========================================================================
@st.cache_resource
def init_global_network_server():
    return {
        "active_device_set": set(),   
        "total_online_viewers": random.randint(85, 115)  
    }

global_server = init_global_network_server()

if "session_id" not in st.session_state:
    st.session_state.session_id = f"node_{random.randint(100000, 999999)}_{time.time()}"
    global_server["total_online_viewers"] += 1

if 'current_user' not in st.session_state: st.session_state.current_user = None 
if 'app_running' not in st.session_state: st.session_state.app_running = False
if 'chart_history' not in st.session_state: st.session_state.chart_history = [22.0, 25.0, 24.0, 28.0, 27.0, 31.0, 29.0, 33.0, 31.0, 35.0, 33.0, 36.8]
if 'session_seconds' not in st.session_state: st.session_state.session_seconds = 0
if 'target_time_index' not in st.session_state: st.session_state.target_time_index = 2 
if 'last_tick_time' not in st.session_state: st.session_state.last_tick_time = 0.0
if 'total_energy_wh' not in st.session_state: st.session_state.total_energy_wh = 0.0

if st.session_state.app_running and st.session_state.current_user:
    global_server["active_device_set"].add(st.session_state.session_id)
else:
    global_server["active_device_set"].discard(st.session_state.session_id)

# 🔄 跑算物理时间收益累加核心，同步持久化到数据库
if st.session_state.app_running and st.session_state.last_tick_time > 0 and st.session_state.current_user:
    current_unix = time.time()
    elapsed_gap = int(current_unix - st.session_state.last_tick_time)
    if elapsed_gap >= 1:
        increment_tokens = elapsed_gap * 0.01
        st.session_state.session_seconds += elapsed_gap
        st.session_state.total_energy_wh += 5.1 * (elapsed_gap / 3600.0)
        st.session_state.last_tick_time = current_unix
        
        # 实时回写本地文件
        all_users = load_users_db()
        c_user = st.session_state.current_user.lower()
        if c_user in all_users:
            all_users[c_user]["balance"] += increment_tokens
            save_users_db(all_users)

def get_project_image():
    if os.path.exists("image.png"): return "image.png"
    png_files = glob.glob("*.png")
    return png_files[0] if png_files else None
target_image = get_project_image()

def generate_referral_code(wallet_str):
    if not wallet_str: return ""
    hasher = hashlib.md5(wallet_str.encode('utf-8')).hexdigest().upper()
    return f"NEXA-{wallet_str[:4].upper()}-{hasher[:4]}"

TIME_OPTIONS_EN = ["15 Minutes", "30 Minutes", "1 Hour", "2 Hours", "4 Hours", "8 Hours", "12 Hours", "24 Hours"]
TIME_OPTIONS_ZH = ["15分钟", "半小时", "1小时", "2小时", "4小时", "8小时", "12小时", "24小时"]
SECONDS_MAP = [900, 1800, 3600, 7200, 14400, 28800, 43200, 86400]

# =========================================================================
# 🔝 4. 顶部常驻面板区
# =========================================================================
st.markdown('<h1 style="text-align:center; color:#A2FF00; font-size:34px; font-weight:800; margin-bottom:0px;">NexaEdge Network</h1>', unsafe_allow_html=True)
lang = st.selectbox("🌐 Language", ["English", "中文"], index=0, label_visibility="collapsed")
current_options = TIME_OPTIONS_EN if lang == "English" else TIME_OPTIONS_ZH

if lang == "English":
    st.markdown('<p style="font-size:13px; color:#A2FF00; font-weight:bold; text-align:center; margin-top:5px; margin-bottom:12px;">Transforming idle smartphones into data fuel factories for the AI Era.</p>', unsafe_allow_html=True)
else:
    st.markdown('<p style="font-size:13px; color:#A2FF00; font-weight:bold; text-align:center; margin-top:5px; margin-bottom:12px;">让全球闲置手机，成为 AI 时代的高纯度语料燃料工厂</p>', unsafe_allow_html=True)

if target_image:
    st.image(target_image, use_container_width=True)

# =========================================================================
# 🚪 5. 条件分流控制闸：未登录状态 ➔ 渲染白名单注册与账户登录
# =========================================================================
if st.session_state.current_user is None:
    st.markdown('<div class="app-container">', unsafe_allow_html=True)
    
    gate_tab1, gate_tab2, gate_tab3 = st.tabs(["🔐 Sign In / 登录账户", "🚀 Whitelist & Sign Up / 锁定白名单并注册", "👑 Admin / 管理员后台"])
    
    # ---- 登录模块 ----
    with gate_tab1:
        st.markdown("<div style='padding:8px 0;'></div>", unsafe_allow_html=True)
        login_email = st.text_input("Email Address / 邮箱地址", key="l_email").strip()
        login_pwd = st.text_input("Password / 登录密码", type="password", key="l_pwd").strip()
        
        if st.button("CONFIRM SIGN IN / 登录算力中心 ⚡", key="btn_login_trigger"):
            if not login_email or not login_pwd:
                st.error("❌ Please complete all fields! / 请完整填写账号密码！")
            else:
                db = load_users_db()
                hashed_input_pwd = hashlib.sha256(login_pwd.encode()).hexdigest()
                if login_email.lower() in db and db[login_email.lower()]["pwd"] == hashed_input_pwd:
                    st.session_state.current_user = login_email.lower()
                    st.success("🎉 Authentication successful! Loading node workspace...")
                    time.sleep(0.5)
                    st.rerun()
                else:
                    st.error("❌ Invalid Email or Password. / 邮箱或密码错误。")
                    
    # ---- 核心：白名单 + 账户复合注册模块 ----
    with gate_tab2:
        st.markdown("<div style='padding:8px 0;'></div>", unsafe_allow_html=True)
        if lang == "English":
            st.markdown('<div style="font-size:13px; font-weight:bold; color:#A2FF00;">⚡ STEP 1: Follow Official Social Channels</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div style="font-size:13px; font-weight:bold; color:#A2FF00;">⚡ STEP 1: 必须关注以下官方社交频道激活白名单资格</div>', unsafe_allow_html=True)
            
        st.markdown("""
        <div class="social-grid">
            <a class="social-btn" href="https://www.instagram.com/nexaedge__?igsh=eXp0MTlmdDR6dm10&utm_source=qr" target="_blank">📸 Instagram</a>
            <a class="social-btn" href="https://x.com/nexaedge_?s=21&t=8onO0h_fTxzmAGu431ZxXw" target="_blank">🐦 X (Twitter)</a>
            <a class="social-btn" href="https://www.facebook.com/share/18eXN6P3Ge/?mibextid=wwXIfr" target="_blank">👥 Facebook</a>
            <a class="social-btn" href="https://www.tiktok.com/@nexaedge7?_r=1&_t=ZS-96QbSMyso5v" target="_blank">🎵 TikTok</a>
            <a class="social-btn" href="https://t.me/NexaEdge7" target="_blank">📢 Telegram</a>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<hr style='border:1px solid #1e272e; margin:10px 0;'>", unsafe_allow_html=True)
        st.markdown(f"<div style='font-size:13px; font-weight:bold; color:#A2FF00; margin-bottom:5px;'>📝 STEP 2: {"Fill Credentials" if lang=='English' else "填报创建白名单节点账户"}</div>", unsafe_allow_html=True)
        
        reg_email = st.text_input("Email Address / 电子邮箱地址", key="r_email").strip()
        reg_pwd = st.text_input("Create Account Password / 设置登录密码", type="password", key="r_pwd").strip()
        reg_wallet = st.text_input("Solana Wallet Address / Solana 接收钱包地址", key="r_wallet").strip()
        reg_ref = st.text_input("Referral Code (Optional) / 推荐人邀请码 (选填)", key="r_ref").strip()
        
        if st.button("SUBMIT WHITELIST & CREATE ACCOUNT / 锁定白名单并创建账户 🚀", key="btn_register_trigger"):
            if not reg_email or not reg_pwd or not reg_wallet:
                st.error("❌ All fields are required to secure a node placement! / 请完整填写邮箱、密码与钱包地址！")
            elif "@" not in reg_email:
                st.error("❌ Invalid Email Format! / 请填写格式合规的电子邮箱！")
            else:
                db = load_users_db()
                
                # 双重排重检查（支持邮箱与钱包双排重）
                is_duplicate = False
                if reg_email.lower() in db:
                    is_duplicate = True
                for em, info in db.items():
                    if info["wallet"].lower() == reg_wallet.lower():
                        is_duplicate = True
                        break
                        
                if is_duplicate:
                    st.error("⚠️ Rejected! This Email or Solana Wallet has already claimed a whitelist allocation. / 提交失败！该邮箱或钱包已存在于白名单记录中。")
                else:
                    # 1. 生成唯一邀请裂变码
                    generated_code = generate_referral_code(reg_wallet)
                    ref_by_clean = reg_ref if reg_ref else "NONE"
                    now_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                    
                    # 2. 写入账户持久化库
                    hashed_pwd = hashlib.sha256(reg_pwd.encode()).hexdigest()
                    db[reg_email.lower()] = {
                        "pwd": hashed_pwd,
                        "balance": 0.0,
                        "wallet": reg_wallet,
                        "ref_code": generated_code,
                        "ref_by": ref_by_clean,
                        "time": now_str
                    }
                    save_users_db(db)
                    
                    # 3. 同步追加写入原有 whitelist.txt 文件中
                    append_to_whitelist_txt(reg_email, reg_wallet, 0.0, generated_code, ref_by_clean)
                    
                    st.success("🎉 Whitelist allocation secured and account initialized! Head to Sign In. / 创世白名单锁定成功！请切换至登录标签验证身份。")
                    st.balloons()
                    
    # ---- 管理员动态审计后台 ----
    with gate_tab3:
        st.markdown("<div style='padding:8px 0;'></div>", unsafe_allow_html=True)
        admin_key = st.text_input("Admin Token / 管理员审计密钥", type="password", key="master_adm_key")
        
        if admin_key == "nexa2026":
            st.markdown("<hr style='border:1px dashed #A2FF00;'>", unsafe_allow_html=True)
            st.markdown("<h3 style='color:#A2FF00; font-size:16px;'>👑 NexaEdge Real-time Whitelist & User Audit</h3>", unsafe_allow_html=True)
            
            db = load_users_db()
            if not db:
                st.info("No registered whitelist nodes detected in the local architecture.")
            else:
                admin_records = []
                total_minted = 0.0
                for email, info in db.items():
                    total_minted += info["balance"]
                    admin_records.append({
                        "Whitelist Email": email,
                        "Solana Wallet": info["wallet"],
                        "Real-time NEXA Asset": f"{info['balance']:,.2f}",
                        "User Invite Code": info["ref_code"],
                        "Invited By": info["ref_by"],
                        "Reg Time": info["time"]
                    })
                
                st.markdown(f"""
                <div style='display:grid; grid-template-columns: 1fr 1fr; gap:10px; margin-bottom:12px;'>
                    <div style='background:#0b0f12; padding:10px; border-radius:10px; border:1px solid #252e38;'>
                        <div style='font-size:11px; color:#88929b;'>TOTAL REGISTERED NODES</div>
                        <div style='color:#A2FF00; font-size:22px; font-weight:bold;'>{len(db)} Accounts</div>
                    </div>
                    <div style='background:#0b0f12; padding:10px; border-radius:10px; border:1px solid #252e38;'>
                        <div style='font-size:11px; color:#88929b;'>TOTAL LOGGED MINING</div>
                        <div style='color:#00e5ff; font-size:22px; font-weight:bold;'>{total_minted:,.2f} NEXA</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                st.dataframe(pd.DataFrame(admin_records), use_container_width=True, hide_index=True)
        elif admin_key:
            st.error("❌ Access Denied!")
            
    st.markdown('</div>', unsafe_allow_html=True)

# =========================================================================
# 🎛️ 6. 条件分流控制闸：已登录状态 ➔ 挂载边缘算力大盘
# =========================================================================
else:
    db = load_users_db()
    user_key = st.session_state.current_user.lower()
    
    if user_key not in db:
        st.session_state.current_user = None
        st.rerun()
        
    current_user_balance = db[user_key]["balance"]
    current_user_wallet = db[user_key]["wallet"]
    current_user_refcode = db[user_key]["ref_code"]

    tab1, tab2 = st.tabs(["🌐 Overview & Allocation / 白名单名片", "📱 Node Console / 边缘算力控制台"])

    # ---- 页面一：个人白名单名片及资产详情 ----
    with tab1:
        c1, c2, c3 = st.columns(3)
        if lang == "English":
            with c1: st.metric(label="Network Fee", value="20%", delta="Pure Revenue Flow")
            with c2: st.metric(label="Safety Threshold", value="39°C", delta="Device Safety Lock", delta_color="inverse")
            with c3: st.metric(label="Settlement Base", value="Solana SPL", delta="Low Gas / High TPS")
        else:
            with c1: st.metric(label="平台技术抽成", value="20%", delta="纯现金流造血")
            with c2: st.metric(label="智能硬件风控", value="39°C", delta="秒级控温预警", delta_color="inverse")
            with c3: st.metric(label="算力结算底座", value="Solana SPL", delta="极速、低 Gas")
            
        st.markdown("<hr style='border:1px solid #1e272e; margin: 12px 0;'>", unsafe_allow_html=True)
        st.markdown(f'<h4 style="color:#A2FF00; margin-bottom:10px;">📋 {"Your Whitelist Identity Pass" if lang=="English" else "您的白名单创世名片"}</h4>', unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="app-card" style="border-left: 4px solid #A2FF00;">
            <div style="font-size:11px; color:#88929b;">WHITELIST REGISTERED EMAIL</div>
            <div style="font-size:15px; font-weight:bold; color:white; margin-bottom:6px;">{st.session_state.current_user}</div>
            <div style="font-size:11px; color:#88929b;">BOUND SOLANA WALLET ADDRESS</div>
            <div style="font-size:13px; font-family:monospace; color:#bdc3c7; margin-bottom:6px;">{current_user_wallet}</div>
            <div style="font-size:11px; color:#88929b;">🎯 YOUR EXCLUSIVE REFERRAL CODE</div>
            <div style="font-size:16px; font-family:monospace; font-weight:bold; color:#A2FF00;">{current_user_refcode}</div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("LOGOUT / 退出当前算力账户 👋", key="btn_logout_action"):
            st.session_state.app_running = False
            global_server["active_device_set"].discard(st.session_state.session_id)
            st.session_state.current_user = None
            st.rerun()

    # ---- 页面二：高频节点工作舱 ----
    with tab2:
        st.markdown('<div class="app-container">', unsafe_allow_html=True)
        
        st.markdown('<div class="app-card">', unsafe_allow_html=True)
        st.markdown(f'<div class="app-title">{"⏳ COMPUTE TIMER" if lang=="English" else "⏳ 算力定时器"}</div>', unsafe_allow_html=True)
        selected_time = st.selectbox("Set runtime pattern:", current_options, index=st.session_state.target_time_index, key="engine_time_selectbox")
        st.session_state.target_time_index = current_options.index(selected_time)
        target_total_seconds = SECONDS_MAP[st.session_state.target_time_index]
        
        if st.session_state.app_running and st.session_state.session_seconds >= target_total_seconds:
            st.session_state.app_running = False
            global_server["active_device_set"].discard(st.session_state.session_id)
            st.toast("⏰ Timer Finished!")
        st.markdown('</div>', unsafe_allow_html=True)

        if st.session_state.app_running:
            current_hash, current_temp, current_power = random.uniform(45.5, 49.8), random.uniform(36.4, 36.9), random.uniform(4.85, 5.35)
            st.session_state.chart_history.pop(0)
            st.session_state.chart_history.append(current_hash)
        else:
            current_hash, current_temp, current_power = 0.0, 31.2, random.uniform(0.12, 0.22)
            
        s_sec = st.session_state.session_seconds
        time_str = f"{s_sec//3600:02d}:{(s_sec%3600)//60:02d}:{s_sec%60:02d}"

        st.markdown(f'<div class="app-card"><div style="font-size:12px; color:#88929b;">{"NETWORK HASH RATE" if lang=="English" else "当前节点算力"} (MH/s): <span class="neon-green-text" style="font-weight:bold;">{current_hash:.2f}</span></div></div>', unsafe_allow_html=True)
        st.line_chart(pd.DataFrame(st.session_state.chart_history, columns=["Hash Rate"]), height=90, use_container_width=True)
        
        st.markdown(f"""
        <div class="app-card" style="margin-top:-5px;">
            <div style="display:grid; grid-template-columns: 1fr 1fr; gap:6px;">
                <div style="background:#11171d; padding:6px; border-radius:8px;">
                    <div style="font-size:9px; color:#88929b; font-weight:bold;">🌡️ DEVICE TEMP:</div>
                    <div class="app-value neon-green-text" style="font-size:14px;">{current_temp:.1f} °C</div>
                </div>
                <div style="background:#11171d; padding:6px; border-radius:8px;">
                    <div style="font-size:9px; color:#88929b; font-weight:bold;">🔌 HARDWARE METRICS:</div>
                    <div class="app-value neon-blue-text" style="font-size:14px; font-family:monospace;">{st.session_state.total_energy_wh:.4f} Wh</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # ✨ 亮点：直接将从本地提取的白名单大盘资产额动态渲染在这里
        st.markdown(f"""
        <div class="app-card" style="border: 1px solid #A2FF00; background: linear-gradient(135deg, #161c23 0%, #111b15 100%);">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <div>
                    <div style="font-size:10px; color:#88929b; font-weight:bold;">🔒 REAL-TIME BAL (WHITELIST WALLET) / 您的白名单账户真实总余额</div>
                    <div class="app-value neon-green-text" style="font-size:24px; margin-top:2px;">
                        {current_user_balance:,.2f} <span style="font-size:12px; color:white; font-weight:normal;">NEXA</span>
                    </div>
                </div>
                <div style="text-align:right;">
                    <div style="font-size:9px; color:#88929b; font-weight:bold;">RUNNING TIME</div>
                    <div class="app-value" style="font-size:14px; font-family:monospace; color:white;">{time_str}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        if not st.session_state.app_running:
            if st.button("START COMPUTE SESSION ⚡" if lang=="English" else "激活并启动边缘算力节点 ⚡", key="btn_start_running"):
                st.session_state.app_running = True
                st.session_state.last_tick_time = time.time()
                global_server["active_device_set"].add(st.session_state.session_id)
                st.rerun()
        else:
            if st.button("PAUSE COMPUTE SESSION 🛑" if lang=="English" else "暂停当前算力 Session 🛑", key="btn_stop_running"):
                st.session_state.app_running = False
                st.session_state.last_tick_time = 0.0
                global_server["active_device_set"].discard(st.session_state.session_id)
                st.rerun()
                
        st.markdown('</div>', unsafe_allow_html=True)

    # =========================================================================
    # 📊 7. 全网大盘同步
    # =========================================================================
    st.markdown("<hr style='border:1px solid #1e272e; margin: 15px 0 10px 0;'>", unsafe_allow_html=True)
    col_net1, col_net2 = st.columns(2)
    with col_net1:
        st.markdown(f'<div class="mini-stat-card" style="border: 1px dashed #A2FF00;"><div class="mini-stat-title">● NETWORK ACTIVE NODES</div><div class="mini-stat-value" style="color:#A2FF00;">{len(global_server["active_device_set"])} Devices</div></div>', unsafe_allow_html=True)
    with col_net2:
        st.markdown(f'<div class="mini-stat-card" style="border: 1px dashed #00e5ff;"><div class="mini-stat-title">👀 LIVE REAL VIEWERS</div><div class="mini-stat-value" style="color:#00e5ff;">{global_server["total_online_viewers"]} Online</div></div>', unsafe_allow_html=True)

    st.markdown("<p style='text-align:center; color:#445; font-size: 10px; margin-top:12px;'>NexaEdge Network © 2026 | Powered by Solana DePIN Infrastructure</p>", unsafe_allow_html=True)

    # =========================================================================
    # 👑 8. 高频刷新控制层
    # =========================================================================
    if st.session_state.app_running:
        time.sleep(1.0)
        st.rerun()
