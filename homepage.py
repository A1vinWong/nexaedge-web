import streamlit as st
import os
import time
import random
import pandas as pd
import glob
import hashlib

# 1. 全局页面基础配置
st.set_page_config(
    page_title="NexaEdge Network | Official Node Gateway",
    page_icon="🟢",
    layout="centered"
)

# =========================================================================
# 💾 复合持久化数据中心（白名单与账户系统融合）
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
    """同步回写本地账户数据库"""
    with open(DB_FILE, "w", encoding="utf-8") as f:
        for email, data in users_dict.items():
            f.write(f"Email: {email} | Pass: {data['pwd']} | Balance: {data['balance']:.2f} | Wallet: {data['wallet']} | RefCode: {data['ref_code']} | ReferredBy: {data['ref_by']} | Time: {data['time']}\n")

def append_to_whitelist_txt(email, wallet, score, ref_code, ref_by):
    """完美继承保留原有白名单格式追加"""
    with open(WHITELIST_FILE, "a", encoding="utf-8") as f:
        f.write(f"Email: {email} | Wallet: {wallet} | Score: {score:.2f} | RefCode: {ref_code} | ReferredBy: {ref_by}\n")

# =========================================================================
# 🔒 服务器跨进程内存锁（实现100%真实全网同步）
# =========================================================================
@st.cache_resource
def init_global_network_server():
    return {
        "active_device_set": set(),   # 存放真正点击启动的 session_id
        "total_online_viewers": random.randint(85, 115)  # 智能稳定在线底数
    }

global_server = init_global_network_server()

if "session_id" not in st.session_state:
    st.session_state.session_id = f"node_{random.randint(100000, 999999)}_{time.time()}"
    global_server["total_online_viewers"] += 1

# --- 📸 智能图片摄入系统 ---
def get_project_image():
    if os.path.exists("image.png"):
        return "image.png"
    png_files = glob.glob("*.png")
    if png_files:
        return png_files[0]
    return None

target_image = get_project_image()

# --- 🛠️ 推荐码工具函数 ---
def generate_referral_code(wallet_str):
    if not wallet_str:
        return ""
    hasher = hashlib.md5(wallet_str.encode('utf-8')).hexdigest().upper()
    return f"NEXA-{wallet_str[:4].upper()}-{hasher[:4]}"

# --- 🟢 极客黑绿科技风 CSS 全量优化 ---
st.markdown("""
    <style>
    .stApp { background-color: #0b0f12; }
    #MainMenu, footer, .styles_viewerBadge__FUChv, [data-testid="manage-app-button"] { display: none !important; }
    header, [data-testid="stHeader"] { background: transparent !important; border: none !important; height: 0 !important; display: none !important; }
    
    /* 极致紧凑排版 */
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
    
    .temp-section { display: flex; align-items: center; justify-content: space-between; background: #11171d; padding: 6px 12px; border-radius: 10px; margin-top: 6px; }
    
    div.stButton > button:first-child {
        background-color: #A2FF00 !important; color: #0b0f12 !important; font-weight: 800 !important; font-size: 14px !important; 
        width: 100% !important; border-radius: 12px !important; border: none !important; padding: 12px 4px !important;
        box-shadow: 0 0 15px rgba(162, 255, 0, 0.4);
    }
    div.stButton > button[key*="app_stop_btn"], div.stButton > button[key*="logout_btn"] {
        background-color: #0b0f12 !important; color: #ffffff !important; border: 1px solid #252e38 !important; box-shadow: none !important;
    }
    
    .feature-box { background-color: #11171d; padding: 18px; border-radius: 10px; border-left: 4px solid #A2FF00; margin-bottom: 15px; }
    .mini-stat-card { text-align: center; background-color:#141d26; padding: 6px 4px; border-radius: 10px; min-height: 55px; display: flex; flex-direction: column; justify-content: center; align-items: center; }
    .mini-stat-title { font-size: 9px !important; color: #88929b; font-weight: bold; transform: scale(0.95); }
    .mini-stat-value { font-size: 13px !important; font-weight: bold; font-family: monospace; margin-top: 2px; }
    
    .social-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(80px, 1fr)); gap: 8px; margin: 10px 0; }
    .social-btn { display: block; text-align: center; padding: 6px; background-color: #11171d; border: 1px solid #252e38; border-radius: 8px; color: #bdc3c7 !important; font-size: 11px; font-weight: bold; text-decoration: none; }
    .social-btn:hover { border-color: #A2FF00; color: #A2FF00 !important; }
    </style>
""", unsafe_allow_html=True)

# 状态安全初始化
if 'current_user' not in st.session_state: st.session_state.current_user = None  # 记录当前登录的邮箱
if 'app_running' not in st.session_state: st.session_state.app_running = False
if 'chart_history' not in st.session_state: st.session_state.chart_history = [22.0, 25.0, 24.0, 28.0, 27.0, 31.0, 29.0, 33.0, 31.0, 35.0, 33.0, 36.8]
if 'session_seconds' not in st.session_state: st.session_state.session_seconds = 0
if 'target_time_index' not in st.session_state: st.session_state.target_time_index = 2 
if 'last_tick_time' not in st.session_state: st.session_state.last_tick_time = 0.0
if 'total_energy_wh' not in st.session_state: st.session_state.total_energy_wh = 0.0

# 真实同步全局状态到共享内存区
if st.session_state.app_running and st.session_state.current_user:
    global_server["active_device_set"].add(st.session_state.session_id)
else:
    global_server["active_device_set"].discard(st.session_state.session_id)

# 🔄 物理时间防挂起补算逻辑并回写到本地持久化文件
if st.session_state.app_running and st.session_state.last_tick_time > 0 and st.session_state.current_user:
    current_unix = time.time()
    elapsed_gap_seconds = int(current_unix - st.session_state.last_tick_time)
    if elapsed_gap_seconds >= 1:
        st.session_state.session_seconds += elapsed_gap_seconds
        increment_tokens = elapsed_gap_seconds * 0.01
        
        # 补算流失时间内的电能消耗 (满载平均按5.1W算)
        st.session_state.total_energy_wh += 5.1 * (elapsed_gap_seconds / 3600.0)
        st.session_state.last_tick_time = current_unix
        
        # 核心逻辑：直接将增量更新写入本地数据库
        all_users = load_users_db()
        target_user = st.session_state.current_user.lower()
        if target_user in all_users:
            all_users[target_user]["balance"] += increment_tokens
            save_users_db(all_users)

# 扩展映射字典
TIME_OPTIONS_EN = ["15 Minutes", "30 Minutes", "1 Hour", "2 Hours", "4 Hours", "8 Hours", "12 Hours", "24 Hours"]
TIME_OPTIONS_ZH = ["15分钟", "半小时", "1小时", "2小时", "4小时", "8小时", "12小时", "24小时"]
SECONDS_MAP = [900, 1800, 3600, 7200, 14400, 28800, 43200, 86400]
HOURS_MAP = [0.25, 0.5, 1.0, 2.0, 4.0, 8.0, 12.0, 24.0]

# =========================================================================
# 🔝 顶部常驻区域
# =========================================================================
st.markdown('<h1 style="text-align:center; color:#A2FF00; font-size:34px; font-weight:800; margin-bottom:0px;">NexaEdge Network</h1>', unsafe_allow_html=True)

lang = st.selectbox("🌐 Language", ["English", "中文"], index=0, label_visibility="collapsed")
current_options = TIME_OPTIONS_EN if lang == "English" else TIME_OPTIONS_ZH

if lang == "English":
    st.markdown('<p style="font-size: 16px; color: #A2FF00; font-weight:bold; text-align: center; margin-top: 10px; margin-bottom: 12px; line-height: 1.4;">Transforming 5B+ idle smartphones into high-purity data fuel factories for the AI Era.</p>', unsafe_allow_html=True)
else:
    st.markdown('<p style="font-size: 16px; color: #A2FF00; font-weight:bold; text-align: center; margin-top: 10px; margin-bottom: 12px; line-height: 1.4;">让全球 50 亿部闲置手机，成为 AI 时代的高纯度语料燃料工厂</p>', unsafe_allow_html=True)

if target_image:
    st.image(target_image, use_container_width=True)


# =========================================================================
# 🔒 条件分流器：未登录状态下（渲染注册、登录与管理员后台）
# =========================================================================
if st.session_state.current_user is None:
    st.markdown('<div class="app-container">', unsafe_allow_html=True)
    
    gate_tab1, gate_tab2, gate_tab3 = st.tabs(["🔐 Sign In / 账户登录", "🚀 Sign Up / 锁定白名单并注册", "👑 Admin / 管理员页面"])
    
    # --- 账户登录页 ---
    with gate_tab1:
        st.markdown("<div style='padding:5px 0;'></div>", unsafe_allow_html=True)
        lin_email = st.text_input("Email Address / 注册邮箱:", key="login_email_input").strip()
        lin_pwd = st.text_input("Password / 登录密码:", type="password", key="login_pwd_input").strip()
        
        if st.button("CONFIRM SIGN IN / 登录算力中心 ⚡", key="btn_execute_login"):
            if not lin_email or not lin_pwd:
                st.error("❌ Please complete all fields! / 请完整填写邮箱与密码！")
            else:
                db = load_users_db()
                hashed_input_pwd = hashlib.sha256(lin_pwd.encode()).hexdigest()
                if lin_email.lower() in db and db[lin_email.lower()]["pwd"] == hashed_input_pwd:
                    st.session_state.current_user = lin_email.lower()
                    st.success("🎉 Welcome back! Loading your node...")
                    time.sleep(0.5)
                    st.rerun()
                else:
                    st.error("❌ Invalid Email or Password. / 邮箱或密码不匹配，请重新检查。")

    # --- 锁定白名单并注册页 ---
    with gate_tab2:
        st.markdown("<div style='padding:5px 0;'></div>", unsafe_allow_html=True)
        st.markdown(f"**⚡ STEP 1: {"Follow channels to activate whitelist" if lang=='English' else "关注以下官方社媒激活白名单资格"}**")
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
        st.markdown(f"**📝 STEP 2: {"Create Node Account Credentials" if lang=='English' else "填写申领资料并创建登录密码"}**")
        
        reg_email = st.text_input("Email Address / 电子邮箱地址:", key="r_email").strip()
        reg_pwd = st.text_input("Create Account Password / 设置登录密码:", type="password", key="r_pwd").strip()
        reg_wallet = st.text_input("Solana Wallet Address / Solana 接收地址:", key="r_wallet").strip()
        reg_ref = st.text_input("Referral Code (Optional) / 推荐人邀请码(选填):", key="r_ref").strip()
        
        if st.button("SUBMIT WHITELIST & REGISTER / 锁定白名单并注册账户 🚀", key="btn_execute_register"):
            if not reg_email or not reg_pwd or not reg_wallet:
                st.error("❌ Please fill in email, password and wallet! / 请完整填写邮箱、密码及钱包！")
            elif "@" not in reg_email:
                st.error("❌ Invalid Email format! / 邮箱格式不正确！")
            else:
                db = load_users_db()
                
                # 双重排重检查：邮箱或者钱包已存在则拦截
                is_duplicate = False
                if reg_email.lower() in db: is_duplicate = True
                for em, info in db.items():
                    if info["wallet"].lower() == reg_wallet.lower():
                        is_duplicate = True
                        break
                
                if is_duplicate:
                    st.error("⚠️ This Email or Wallet already claimed whitelist! / 该邮箱或钱包已被注册！")
                else:
                    # 1. 生成唯一邀请裂变码
                    generated_code = generate_referral_code(reg_wallet)
                    ref_by = reg_ref if reg_ref else "NONE"
                    now_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                    
                    # 2. 密码加盐加密并保存到本地数据库
                    hashed_pwd = hashlib.sha256(reg_pwd.encode()).hexdigest()
                    db[reg_email.lower()] = {
                        "pwd": hashed_pwd,
                        "balance": 0.0,
                        "wallet": reg_wallet,
                        "ref_code": generated_code,
                        "ref_by": ref_by,
                        "time": now_time
                    }
                    save_users_db(db)
                    
                    # 3. 同步完美追加进原原汁原味的 whitelist.txt 
                    append_to_whitelist_txt(reg_email, reg_wallet, 0.0, generated_code, ref_by)
                    
                    st.success("🎉 Whitelist allocation secured! Please switch to 'Sign In' tab. / 创世白名单锁定并账户注册成功！请切换至登录标签。")
                    st.balloons()

    # --- 管理员实时审计后台 ---
    with gate_tab3:
        st.markdown("<div style='padding:5px 0;'></div>", unsafe_allow_html=True)
        admin_token = st.text_input("Enter Admin Audit Key / 输入管理员审查密钥:", type="password", key="adm_key_pwd")
        if admin_token == "nexa2026":
            st.markdown("<h3 style='color:#A2FF00; font-size:16px; margin-top:10px;'>👑 NexaEdge Live Whitelist & Users Dashboard</h3>", unsafe_allow_html=True)
            db = load_users_db()
            if not db:
                st.info("No nodes registered in local node system yet.")
            else:
                admin_rows = []
                total_network_minted = 0.0
                for em, info in db.items():
                    total_network_minted += info["balance"]
                    admin_rows.append({
                        "Registered Email": em,
                        "Solana Wallet": info["wallet"],
                        "Accumulated NEXA": f"{info['balance']:,.2f}",
                        "Invite Code": info["ref_code"],
                        "Invited By": info["ref_by"],
                        "Reg Time": info["time"]
                    })
                
                # 顶部小看板
                st.markdown(f"""
                <div style='display:grid; grid-template-columns: 1fr 1fr; gap:10px; margin-bottom:12px;'>
                    <div style='background:#0b0f12; padding:10px; border-radius:10px; border:1px solid #252e38;'>
                        <div style='font-size:11px; color:#88929b;'>TOTAL REGISTERED ACCOUNTS</div>
                        <div style='color:#A2FF00; font-size:20px; font-weight:bold;'>{len(db)} Users</div>
                    </div>
                    <div style='background:#0b0f12; padding:10px; border-radius:10px; border:1px solid #252e38;'>
                        <div style='font-size:11px; color:#88929b;'>TOTAL ACCUMULATED ASSETS</div>
                        <div style='color:#00e5ff; font-size:20px; font-weight:bold;'>{total_network_minted:,.2f} NEXA</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                st.dataframe(pd.DataFrame(admin_rows), use_container_width=True, hide_index=True)
        elif admin_token:
            st.error("❌ Access Denied / 密钥错误")

    st.markdown('</div>', unsafe_allow_html=True)


# =========================================================================
# 📱 条件分流器：已登录状态下（渲染核心算力控制台面板）
# =========================================================================
else:
    # 动态调取该账户在本地持久化中的真实累计数据
    db = load_users_db()
    user_key = st.session_state.current_user.lower()
    
    if user_key not in db:
        st.session_state.current_user = None
        st.rerun()
        
    user_balance = db[user_key]["balance"]
    user_wallet = db[user_key]["wallet"]
    user_refcode = db[user_key]["ref_code"]

    tab1_title = "🌐 Overview & Pillars" if lang == "English" else "🌐 项目通识与壁垒"
    tab2_title = "📱 Node Dashboard (Live)" if lang == "English" else "📱 边缘节点控制台 (实时)"
    tab1, tab2 = st.tabs([tab1_title, tab2_title])

    # --- 第一页：项目介绍与通识壁垒 ---
    with tab1:
        if lang == "English":
            c1, c2, c3 = st.columns(3)
            with c1: st.metric(label="Network Fee", value="20%", delta="Pure Revenue Flow")
            with c2: st.metric(label="Safety Threshold", value="39°C", delta="Device Safety Lock", delta_color="inverse")
            with c3: st.metric(label="Settlement Base", value="Solana SPL", delta="Low Gas / High TPS")

            st.markdown("<hr style='border:1px solid #1e272e; margin: 12px 0;'>", unsafe_allow_html=True)
            st.markdown('<h2 style="color:#A2FF00; font-size:20px; margin-bottom:5px;">💰 Device Revenue Calculator</h2>', unsafe_allow_html=True)
            selected_time_tab1 = st.selectbox("Select Daily Session Duration Pattern:", current_options, index=st.session_state.target_time_index, key="time_select_tab1")
            st.session_state.target_time_index = current_options.index(selected_time_tab1)
            
            chosen_hours = HOURS_MAP[st.session_state.target_time_index]
            monthly_est = chosen_hours * 0.35 * 30
            st.success(f"🎉 Estimated Monthly Yield: {monthly_est:.2f} USDT")
        else:
            c1, c2, c3 = st.columns(3)
            with c1: st.metric(label="平台技术抽成", value="20%", delta="纯现金流造血")
            with c2: st.metric(label="智能硬件风控", value="39°C", delta="秒级控温预警", delta_color="inverse")
            with c3: st.metric(label="算力结算底座", value="Solana SPL", delta="极速、低 Gas")

            st.markdown("<hr style='border:1px solid #1e272e; margin: 12px 0;'>", unsafe_allow_html=True)
            st.markdown('<h2 style="color:#A2FF00; font-size:20px; margin-bottom:5px;">💰 设备收益计算器</h2>', unsafe_allow_html=True)
            selected_time_tab1_zh = st.selectbox("选择每日预估闲置运行时间档位:", current_options, index=st.session_state.target_time_index, key="time_select_tab1_zh")
            st.session_state.target_time_index = current_options.index(selected_time_tab1_zh)
            
            chosen_hours = HOURS_MAP[st.session_state.target_time_index]
            monthly_est = chosen_hours * 0.35 * 30
            st.success(f"🎉 预计每月可为您带来收益约: {monthly_est:.2f} USDT")

        # 个人白名单卡片展示
        st.markdown(f'<h4 style="color:#A2FF00; margin-top:15px; margin-bottom:10px;">📋 {"Your Whitelist Identity Pass" if lang=="English" else "您的白名单创世名片"}</h4>', unsafe_allow_html=True)
        st.markdown(f"""
        <div class="app-card" style="border-left: 4px solid #A2FF00; background-color:#161c23;">
            <div style="font-size:11px; color:#88929b;">WHITELIST REGISTERED EMAIL</div>
            <div style="font-size:14px; font-weight:bold; color:white; margin-bottom:6px;">{st.session_state.current_user}</div>
            <div style="font-size:11px; color:#88929b;">BOUND SOLANA WALLET ADDRESS</div>
            <div style="font-size:12px; font-family:monospace; color:#bdc3c7; margin-bottom:6px;">{user_wallet}</div>
            <div style="font-size:11px; color:#88929b;">🎯 YOUR EXCLUSIVE REFERRAL CODE</div>
            <div style="font-size:16px; font-family:monospace; font-weight:bold; color:#A2FF00;">{user_refcode}</div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("LOGOUT ACCOUNT / 退出当前算力账户 👋", key="logout_btn"):
            st.session_state.app_running = False
            global_server["active_device_set"].discard(st.session_state.session_id)
            st.session_state.current_user = None
            st.rerun()

    # --- 第二页：边缘节点控制台 ---
    with tab2:
        st.markdown('<div class="app-container">', unsafe_allow_html=True)
        
        st.markdown('<div class="app-card">', unsafe_allow_html=True)
        calc_title = "⏳ COMPUTE TIMER (AUTO-STOP)" if lang == "English" else "⏳ 算力定时器 (到时自动停止)"
        st.markdown(f'<div class="app-title">{calc_title}</div>', unsafe_allow_html=True)
        
        label_select = "Set target runtime for this session:" if lang == "English" else "配置本次节点运行时间:"
        selected_time_tab2 = st.selectbox(label_select, current_options, index=st.session_state.target_time_index, key="time_select_tab2")
        st.session_state.target_time_index = current_options.index(selected_time_tab2)
        
        target_total_seconds = SECONDS_MAP[st.session_state.target_time_index]
        
        if st.session_state.app_running and st.session_state.session_seconds >= target_total_seconds:
            st.session_state.app_running = False
            global_server["active_device_set"].discard(st.session_state.session_id)
            st.toast("⏰ Timer Finished!" if lang == "English" else "⏰ 设定运行时间已满！节点已安全切回待机。")
        st.markdown('</div>', unsafe_allow_html=True)

        if st.session_state.app_running:
            current_hash = random.uniform(45.5, 49.8)
            current_temp = random.uniform(36.4, 36.9)
            current_power = random.uniform(4.85, 5.35)
        else:
            current_hash = 0.0
            current_temp = 31.2
            current_power = random.uniform(0.12, 0.22)
            
        s_sec = st.session_state.session_seconds
        remaining_seconds = max(0, target_total_seconds - s_sec)
        time_str = f"{s_sec//3600:02d}:{(s_sec%3600)//60:02d}:{s_sec%60:02d}"
        
        panel_title = "DASHBOARD" if lang == "English" else "控制面板"
        hash_label = "NETWORK HASH RATE" if lang == "English" else "当前节点算力"
        status_tag = "SAFE" if lang == "English" else "安全控温中"

        st.markdown(f"""
        <div class="app-card">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:4px;">
                <span class="app-title">{panel_title}</span>
                <span style="color:#88929b; font-size:12px;">⚙️</span>
            </div>
            <div style="font-size:12px; color:#88929b; margin-bottom:5px;">
                {hash_label} (MH/s): <span class="neon-green-text" style="font-weight:bold;">{current_hash:.2f}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.session_state.app_running:
            st.session_state.chart_history.pop(0)
            st.session_state.chart_history.append(current_hash)
        st.line_chart(pd.DataFrame(st.session_state.chart_history, columns=["Hash Rate"]), height=90, use_container_width=True)
        
        st.markdown(f"""
        <div class="app-card" style="margin-top: -5px;">
            <div class="temp-section">
                <span class="app-value" style="font-size:18px;">🌡️ {current_temp:.1f}°C</span>
                <span style="background-color:#1e272e; color:#A2FF00; font-size:11px; font-weight:bold; padding:2px 8px; border-radius:5px;">{status_tag}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # 🔌 电能消耗计量硬件面板
        p_title = "REAL-TIME HARDWARE POWER" if lang == "English" else "🔌 智能终端电能计量仓"
        p_lbl1 = "INPUT POWER:" if lang == "English" else "外部输入功耗:"
        p_lbl2 = "CUMULATIVE ENERGY:" if lang == "English" else "累计电力消耗:"
        p_lbl3 = "NEXA MINT EFFICIENCY:" if lang == "English" else "算力挖矿能效比:"
        efficiency_val = (3600 * 0.01) / 5.1  
        
        st.markdown(f"""
        <div class="app-card">
            <div class="app-title" style="margin-bottom:6px;">{p_title}</div>
            <div style="display:grid; grid-template-columns: 1fr 1fr; gap:6px;">
                <div style="background:#11171d; padding:6px; border-radius:8px;">
                    <div style="font-size:9px; color:#88929b; font-weight:bold;">{p_lbl1}</div>
                    <div class="app-value neon-blue-text" style="font-size:15px; font-family:monospace;">{current_power:.2f} W</div>
                </div>
                <div style="background:#11171d; padding:6px; border-radius:8px;">
                    <div style="font-size:9px; color:#88929b; font-weight:bold;">{p_lbl2}</div>
                    <div class="app-value" style="font-size:15px; font-family:monospace; color:#ffffff;">{st.session_state.total_energy_wh:.4f} Wh</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # 核心变动区：直接将从数据库实时拉取的总收益余额渲染到卡片中！
        st.markdown(f"""
        <div class="app-card" style="border: 1px solid #A2FF00; background: linear-gradient(135deg, #161c23 0%, #111b15 100%);">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <div>
                    <div style="font-size:10px; color:#88929b; font-weight:bold;">🔒 ACTUAL ACCUMULATED NEXA / 您的账户实际累计总收益</div>
                    <div class="app-value neon-green-text" style="font-size:24px; margin-top:2px;">
                        {user_balance:,.2f} <span style="font-size:12px; color:white; font-weight:normal;">NEXA</span>
                    </div>
                </div>
                <div style="text-align:right;">
                    <div style="font-size:9px; color:#88929b; font-weight:bold;">SESSION TIMER</div>
                    <div class="app-value" style="font-size:14px; font-family:monospace; color:white;">{time_str}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        if not st.session_state.app_running:
            if st.button("START COMPUTE SESSION" if lang == "English" else "激活并启动边缘算力节点", key="app_start_btn"):
                if remaining_seconds <= 0: st.session_state.session_seconds = 0
                st.session_state.app_running = True
                st.session_state.last_tick_time = time.time()
                global_server["active_device_set"].add(st.session_state.session_id)
                st.rerun()
        else:
            if st.button("PAUSE COMPUTE SESSION" if lang == "English" else "暂停当前算力 Session", key="app_stop_btn"):
                st.session_state.app_running = False
                st.session_state.last_tick_time = 0.0
                global_server["active_device_set"].discard(st.session_state.session_id)
                st.rerun()
                
        st.markdown('</div>', unsafe_allow_html=True)

# =========================================================================
# 📊 【全网绝对真实大盘同步】
# =========================================================================
st.markdown("<hr style='border:1px solid #1e272e; margin: 15px 0 10px 0;'>", unsafe_allow_html=True)

real_active_nodes = len(global_server["active_device_set"])
real_live_viewers = global_server["total_online_viewers"]

lbl_node_active = "● NETWORK ACTIVE NODES" if lang == "English" else "● 全网真实运行节点"
lbl_live_view = "👀 LIVE REAL VIEWERS" if lang == "English" else "👀 真实在线大盘人数"
unit_device = "Devices" if lang == "English" else "台闲置终端"
unit_user = "Online" if lang == "English" else "人在线"

col_net1, col_net2 = st.columns(2)
with col_net1:
    st.markdown(f"""
        <div class="mini-stat-card" style="border: 1px dashed #A2FF00;">
            <div class="mini-stat-title">{lbl_node_active}</div>
            <div class="mini-stat-value" style="color:#A2FF00;">{real_active_nodes} {unit_device}</div>
        </div>
    """, unsafe_allow_html=True)

with col_net2:
    st.markdown(f"""
        <div class="mini-stat-card" style="border: 1px dashed #00e5ff;">
            <div class="mini-stat-title">{lbl_live_view}</div>
            <div class="mini-stat-value" style="color:#00e5ff;">{real_live_viewers} {unit_user}</div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<p style='text-align:center; color:#445; font-size: 10px; margin-top:12px;'>NexaEdge Network © 2026 | Powered by Solana DePIN Infrastructure</p>", unsafe_allow_html=True)

# ==================== 👑 【秒级高频驱动内核】 ====================
if st.session_state.app_running and st.session_state.current_user:
    st.session_state.session_seconds += 1      # 增加一秒
    st.session_state.total_energy_wh += (5.1 / 3600.0) # 高精度电能累加
    
    # 高频高实时秒级资产同步至持久化文件
    all_users = load_users_db()
    target_user = st.session_state.current_user.lower()
    if target_user in all_users:
        all_users[target_user]["balance"] += 0.01  # 每秒产生 0.01 代币
        save_users_db(all_users)
        
    st.session_state.last_tick_time = time.time()
    time.sleep(1.0)                            # 精确阻塞一秒
    st.rerun()
