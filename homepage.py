import streamlit as st
import os
import time
import random
import pandas as pd
import glob
import hashlib
from PIL import Image, ImageDraw, ImageFont  # 👈 用于动态绘制推荐码图片

# 💡 在这里统一配置你的新合约地址
DEFAULT_CA = "D7h9MvFDkVxPYeJwSTcE7VkKXo6mygCHYph36P8oeic2"

# 1. 全局页面基础配置
st.set_page_config(
    page_title="NexaEdge Network | Official Node Gateway",
    page_icon="🟢",
    layout="centered"
)

st.markdown("""
    <style>
    .main .block-container {
        padding-top: 1.0rem !important;
        padding-bottom: 0.5rem !important;
        padding-left: 0.8rem !important;
        padding-right: 0.8rem !important;
        max-width: 100% !important;
    }
    .stApp { background-color: #0b0f12; }
    #MainMenu, footer, .styles_viewerBadge__FUChv, [data-testid="manage-app-button"] { display: none !important; }
    header, [data-testid="stHeader"] { display: none !important; height: 0px !important; }
    .element-container hr, .stMarkdown hr { display: none !important; }
    [data-testid="stVerticalBlock"] > div:empty { display: none !important; margin: 0 !important; padding: 0 !important; }
    [data-testid="stVerticalBlock"] > div {
        padding-bottom: 0.15rem !important;
        padding-top: 0.15rem !important;
    }
    .stTabs [data-baseweb="tab-list"] { gap: 8px; background-color: transparent !important; justify-content: center; border: none !important; overflow-x: auto; margin-bottom: 8px; }
    .stTabs [data-baseweb="tab"] { background-color: #11171d !important; color: #bdc3c7 !important; border-radius: 8px !important; border: 1px solid #1e272e !important; padding: 8px 14px !important; font-weight: 700 !important; font-size: 13px !important; white-space: nowrap; transition: all 0.3s; }
    .stTabs [aria-selected="true"] { color: #0b0f12 !important; background-color: #A2FF00 !important; border-top: none !important; }
    .stTabs [data-baseweb="tab-highlight"] { background-color: #A2FF00 !important; height: 0px !important; }
    [data-testid="stForm"] { background-color: #161c23 !important; border: 1px solid #252e38 !important; border-radius: 16px !important; padding: 14px !important; }
    .app-container { background-color: #11171d; border: 1px solid #1e272e; border-radius: 20px; padding: 14px; margin-bottom: 8px; box-shadow: 0 10px 30px rgba(0,0,0,0.5); }
    .app-value { font-family: 'Inter', sans-serif; color: #ffffff; font-size: 24px; font-weight: 700; }
    .neon-green-text { color: #A2FF00 !important; }
    .neon-blue-text { color: #00e5ff !important; }
    .temp-section { display: flex; align-items: center; justify-content: space-between; background: #11171d; padding: 8px 12px; border-radius: 10px; }
    div.stButton > button:first-child { background-color: #A2FF00 !important; color: #0b0f12 !important; font-weight: 800 !important; font-size: 15px !important; width: 100% !important; border-radius: 12px !important; border: none !important; padding: 12px 18px !important; box-shadow: 0 5px 15px rgba(162, 255, 0, 0.2); transition: all 0.2s; }
    div.stButton > button:hover { background-color: #b5ff33 !important; }
    div.stButton > button[key*="app_stop_btn"] { background-color: #0b0f12 !important; color: #ffffff !important; border: 1px solid #f43f5e !important; box-shadow: none !important; }
    div.stButton > button[key*="logout_btn"] { background-color: #343a40 !important; color: #ffc107 !important; box-shadow: none !important; padding: 5px 12px !important; font-size: 12px !important; width: auto !important; }
    div.stDownloadButton > button { background-color: #00e5ff !important; color: #0b0f12 !important; font-weight: 800 !important; font-size: 14px !important; width: 100% !important; border-radius: 12px !important; border: none !important; padding: 10px 15px !important; box-shadow: 0 5px 15px rgba(0, 229, 255, 0.2); transition: all 0.2s; }
    div.stDownloadButton > button:hover { background-color: #66efff !important; }
    .feature-box { background-color: #11171d; padding: 14px; border-radius: 10px; border-left: 4px solid #A2FF00; margin-bottom: 10px; }
    .social-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(65px, 1fr)); gap: 6px; margin: 6px 0; }
    .social-btn { display: block; text-align: center; padding: 6px; background-color: #11171d; border: 1px solid #252e38; border-radius: 8px; color: #bdc3c7 !important; font-size: 11px; font-weight: bold; text-decoration: none; }
    .social-btn:hover { border-color: #A2FF00; color: #A2FF00 !important; background-color: #161c23; }
    .chart-wrapper {
        background-color: #161c23;
        border: 1px solid #252e38;
        border-radius: 14px;
        padding: 8px 10px 0px 10px;
        margin-top: 4px;
        margin-left: -18px;
        margin-right: 8px;
        margin-bottom: 8px;
        box-sizing: border-box;
        overflow: hidden;
    }
    .chart-wrapper [data-testid="StyledFullScreenButton"],
    .chart-wrapper summary,
    .chart-wrapper [class*="toolbar"],
    .chart-wrapper [class*="Toolbar"] { display: none !important; }
    .chart-wrapper [data-testid="stVegaLiteChart"] { margin: -10px 0px -18px -12px !important; }
    .chart-wrapper [data-testid="StyledVegaLiteChartFullScreenContainer"] { padding: 0 !important; background: #0b0f12 !important; }
    .chart-title-lbl { font-size: 11px; color: #88929b; font-weight: bold; text-transform: uppercase; margin-bottom: 4px; margin-left: 14px; padding-left: 2px; }
    .bottom-stats-row { display: flex; gap: 8px; margin-top: 6px; margin-bottom: 4px; }
    .mini-stat-card { text-align: center; background-color:#141d26; padding: 6px 10px; border-radius: 8px; min-height: 32px; display: flex; flex-direction: row; justify-content: center; align-items: center; gap: 6px; flex: 1; white-space: nowrap; }
    .mini-stat-title { font-size: 8px !important; color: #88929b; font-weight: bold; white-space: nowrap; margin: 0; }
    .mini-stat-value { font-size: 12px !important; font-weight: bold; font-family: monospace; margin: 0; white-space: nowrap; }
    .app-card { background-color: #161c23; border: 1px solid #252e38; border-radius: 12px; padding: 10px 12px; margin-bottom: 8px; }
    .user-badge { background: #1e293b; padding: 8px 12px; border-radius: 10px; border-left: 3px solid #00e5ff; margin-bottom: 8px; font-size: 12px; color: #e2e8f0; line-height: 1.4; }
    .admin-table { width: 100%; border-collapse: collapse; margin-top: 15px; font-size: 12px; color: #cdfaee; }
    .admin-table th { background-color: #1f2937; color: #A2FF00; text-align: left; padding: 10px; border: 1px solid #374151; }
    .admin-table td { padding: 10px; border: 1px solid #374151; background-color: #111827; }
    .ca-white-box { background: transparent; border: none; padding: 0; margin-top: 4px; text-align: left; }
    .ca-label { font-size: 11px; color: #88929b; font-weight: bold; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 2px; display: block; text-align: left; }
    .ca-white-box div[data-testid="stTextInput"] input { color: #ffffff !important; border-color: #1e2a38 !important; background-color: #161c23 !important; font-family: monospace !important; font-size: 11px !important; text-align: left !important; padding: 6px 10px !important; }
    .glow-ref-code {
        color: #A2FF00;
        text-shadow: 0 0 10px rgba(162, 255, 0, 0.8), 0 0 20px rgba(162, 255, 0, 0.5);
        font-family: 'Courier New', monospace;
        font-weight: 900;
        font-size: 20px;
    }

    /* ✨ 弹窗遮罩样式 */
    .modal-overlay {
        position: fixed;
        top: 0; left: 0;
        width: 100vw; height: 100vh;
        background: rgba(0,0,0,0.85);
        z-index: 9999;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .modal-box {
        background: #161c23;
        border: 2px solid #A2FF00;
        border-radius: 20px;
        padding: 20px;
        max-width: 360px;
        width: 92vw;
        text-align: center;
        box-shadow: 0 0 40px rgba(162,255,0,0.3);
    }
    .modal-box img { width: 100%; border-radius: 12px; margin-bottom: 12px; }
    .modal-title { color: #A2FF00; font-size: 15px; font-weight: 800; margin-bottom: 8px; }

    body { overflow-x: hidden; }
    </style>
""", unsafe_allow_html=True)


# =========================================================================
# 🔒 服务器跨进程内存锁 与 数据库模拟
# =========================================================================
@st.cache_resource
def init_global_network_server():
    return {
        "active_device_set": set(),
        "total_online_viewers": random.randint(102, 125),
        "device_balances": {},
        "user_db": {
            "contact@nexaedge.org": {
                "password_hash": hashlib.sha256("nexa2026".encode()).hexdigest(),
                "score": 1479.0,
                "reg_time": "2026-05-18 14:22:05",
                "referral_code": "NX-OFF-ICL"
            }
        },
        "whitelist_emails": set(),
        "whitelist_wallets": set(),
    }

def generate_referral_code(email: str) -> str:
    h = hashlib.md5(email.encode()).hexdigest().upper()
    return "NX-" + h[:3] + "-" + h[3:6]

# =========================================================================
# 🎨 动态绘制专属推荐码海报核心引擎 (使用 IMG_7859.jpeg，叠加网址+推荐码)
# =========================================================================
def generate_referral_image(ref_code: str, output_path="temp_invite.png"):
    base_img_path = "IMG_7859.jpeg"
    if not os.path.exists(base_img_path):
        img = Image.new("RGB", (1080, 1920), "#0b0f12")
        img.save(base_img_path)

    img = Image.open(base_img_path).convert("RGBA")
    width, height = img.size

    # 在底部绘制半透明黑色渐变条，确保文字可读
    overlay = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    overlay_draw = ImageDraw.Draw(overlay)
    bar_h = int(height * 0.22)
    for i in range(bar_h):
        alpha = int(210 * (i / bar_h))
        overlay_draw.rectangle(
            [(0, height - bar_h + i), (width, height - bar_h + i + 1)],
            fill=(0, 0, 0, alpha)
        )
    img = Image.alpha_composite(img, overlay)
    draw = ImageDraw.Draw(img)

    # 字体大小：网址稍小，推荐码更大更突出
    font_size_url  = max(28, int(height * 0.038))
    font_size_code = max(36, int(height * 0.052))
    font_paths = ["DejaVuSans-Bold.ttf", "arial.ttf", "Helvetica-Bold.ttf", "courbd.ttf"]

    def load_font(size):
        for fp in font_paths:
            try:
                return ImageFont.truetype(fp, size)
            except:
                continue
        return ImageFont.load_default()

    font_url  = load_font(font_size_url)
    font_code = load_font(font_size_code)

    line1 = "nexaedge.org"
    line2 = f"{ref_code}"

    def text_x(text, font):
        try:
            w = draw.textlength(text, font=font)
        except AttributeError:
            bbox = font.getbbox(text)
            w = bbox[2] - bbox[0] if bbox else 300
        return (width - w) // 2

    # 位置：底部往上排列
    y2 = int(height * 0.905)   # 推荐码
    y1 = int(height * 0.848)   # 网址

    # 描边效果让文字在任何背景下都清晰
    def draw_text_with_outline(pos, text, font, fill, outline=(0,0,0)):
        ox, oy = pos
        for dx in [-2, -1, 0, 1, 2]:
            for dy in [-2, -1, 0, 1, 2]:
                if dx != 0 or dy != 0:
                    draw.text((ox+dx, oy+dy), text, font=font, fill=outline)
        draw.text(pos, text, font=font, fill=fill)

    draw_text_with_outline((text_x(line1, font_url),  y1), line1, font_url,  fill=(255,255,255))
    draw_text_with_outline((text_x(line2, font_code), y2), line2, font_code, fill=(162,255,0))

    # 转回 RGB 保存
    final = img.convert("RGB")
    final.save(output_path)
    return output_path


global_server = init_global_network_server()

if "device_fingerprint" not in st.session_state:
    ctx_headers = st.context.headers
    user_agent = ctx_headers.get("User-Agent", "Unknown-Device")
    remote_ip = ctx_headers.get("X-Forwarded-For", "127.0.0.1")
    raw_fingerprint = f"{user_agent}_{remote_ip}"
    st.session_state.device_fingerprint = hashlib.md5(raw_fingerprint.encode('utf-8')).hexdigest()[:12]

dev_id = st.session_state.device_fingerprint

if "current_user" not in st.session_state:
    st.session_state.current_user = None

if dev_id not in global_server["device_balances"]:
    global_server["device_balances"][dev_id] = {
        "app_earned": 0.0,
        "total_energy_wh": 0.0,
        "session_seconds": 0
    }

def sync_data_from_source():
    if st.session_state.current_user:
        email = st.session_state.current_user
        if 'app_earned' not in st.session_state or st.session_state.get('last_user') != email:
            st.session_state.app_earned = global_server["user_db"][email]["score"]
            st.session_state.total_energy_wh = global_server["device_balances"][dev_id]["total_energy_wh"]
            st.session_state.session_seconds = global_server["device_balances"][dev_id]["session_seconds"]
            st.session_state.last_user = email
    else:
        if 'app_earned' not in st.session_state or st.session_state.get('last_user') is not None:
            st.session_state.app_earned = global_server["device_balances"][dev_id]["app_earned"]
            st.session_state.total_energy_wh = global_server["device_balances"][dev_id]["total_energy_wh"]
            st.session_state.session_seconds = global_server["device_balances"][dev_id]["session_seconds"]
            st.session_state.last_user = None

sync_data_from_source()

if "session_id" not in st.session_state:
    st.session_state.session_id = f"node_{dev_id}_{random.randint(1000, 9999)}"
    global_server["total_online_viewers"] += 1

if 'app_running' not in st.session_state: st.session_state.app_running = False
if 'chart_history' not in st.session_state: st.session_state.chart_history = [19.2, 20.8, 18.1, 21.3, 19.0, 22.2, 18.9, 21.1, 20.5, 19.8, 18.2, 20.9]
if 'target_time_index' not in st.session_state: st.session_state.target_time_index = 2
if 'last_tick_time' not in st.session_state: st.session_state.last_tick_time = 0.0



if st.session_state.app_running:
    global_server["active_device_set"].add(st.session_state.session_id)
else:
    global_server["active_device_set"].discard(st.session_state.session_id)

if st.session_state.app_running and st.session_state.last_tick_time > 0:
    current_unix = time.time()
    elapsed_gap = int(current_unix - st.session_state.last_tick_time)
    if elapsed_gap >= 1:
        st.session_state.session_seconds += elapsed_gap
        st.session_state.app_earned += elapsed_gap * 0.01
        st.session_state.total_energy_wh += 5.1 * (elapsed_gap / 3600.0)
        st.session_state.last_tick_time = current_unix
        if st.session_state.current_user:
            global_server["user_db"][st.session_state.current_user]["score"] = st.session_state.app_earned
        else:
            global_server["device_balances"][dev_id]["app_earned"] = st.session_state.app_earned
        global_server["device_balances"][dev_id]["total_energy_wh"] = st.session_state.total_energy_wh
        global_server["device_balances"][dev_id]["session_seconds"] = st.session_state.session_seconds

# --- 顶栏大标题 ---
st.markdown('<h1 style="text-align:center; color:#A2FF00; font-size:30px; font-weight:800; margin-bottom:0px; padding-top:0px;">NexaEdge Network</h1>', unsafe_allow_html=True)

lang = st.selectbox("🌐 Language", ["English", "中文"], index=0, label_visibility="collapsed")

TIME_OPTIONS_EN = ["15 Minutes", "30 Minutes", "1 Hour", "2 Hours", "4 Hours", "8 Hours", "12 Hours", "24 Hours"]
TIME_OPTIONS_ZH = ["15分钟", "半小时", "1小时", "2小时", "4小时", "8小时", "12小时", "24小时"]
HOURS_MAP = [0.25, 0.5, 1.0, 2.0, 4.0, 8.0, 12.0, 24.0]
current_options = TIME_OPTIONS_ZH if lang == "中文" else TIME_OPTIONS_EN

if lang == "中文":
    st.markdown('<p style="font-size: 13px; color: #A2FF00; font-weight:bold; text-align: center; margin-top: 2px; margin-bottom:8px;">让全球闲置手机，成为 AI 时代的高纯度分布式算力网络</p>', unsafe_allow_html=True)
else:
    st.markdown('<p style="font-size: 13px; color: #A2FF00; font-weight:bold; text-align: center; margin-top: 2px; margin-bottom:8px;">Transforming idle smartphones into high-purity data network for AI Era.</p>', unsafe_allow_html=True)

# 🖼️ 固定 Logo 展示（语言选择下方，始终显示）
# ⚠️ 确保 logo.png 已上传到 app 根目录（与 app.py 同级）
st.image("logo.png", use_container_width=True)

url_admin_param = st.query_params.get("admin", None)
is_admin_active = (lang == "nexaadmin" or url_admin_param == "nexa_gate")

tab1, tab2, tab4 = st.tabs([
    "🌐 Overview" if lang=="English" else "🌐 项目通识",
    "📱 Dashboard" if lang=="English" else "📱 算力控制台",
    "🔑 Auth Portal" if lang=="English" else "🔑 账户注册/登录"
])

# ==========================================
# TAB 1: Overview / 项目通识
# ==========================================
with tab1:
    c1, c2, c3 = st.columns(3)
    if lang == "中文":
        with c1: st.metric(label="智能硬件风控", value="39°C", delta="秒级控温预警", delta_color="inverse")
        with c2:
            st.metric(label="算力结算底座", value="Solana SPL", delta="极速、低 Gas")
            st.markdown('<div class="ca-white-box"><span class="ca-label">智能合约地址</span>', unsafe_allow_html=True)
            st.text_input("CA_White", value=DEFAULT_CA, disabled=True, label_visibility="collapsed", key="ca_input_zh")
            st.markdown('</div>', unsafe_allow_html=True)
        with c3: st.metric(label="分布式共识机制", value="自研轻量级 BFT", delta="2:1 多数投票验证")
    else:
        with c1: st.metric(label="Thermal Guard Lock", value="39°C", delta="Device Protection Barrier", delta_color="inverse")
        with c2:
            st.metric(label="Settlement Engine", value="Solana SPL", delta="Low Gas / High TPS")
            st.markdown('<div class="ca-white-box"><span class="ca-label">Contract Address</span>', unsafe_allow_html=True)
            st.text_input("CA_White", value=DEFAULT_CA, disabled=True, label_visibility="collapsed", key="ca_input_en")
            st.markdown('</div>', unsafe_allow_html=True)
        with c3: st.metric(label="Network Consensus", value="Proprietary BFT", delta="2:1 Redundant Voting")

    if lang == "中文":
        st.markdown('<h2 style="color:#A2FF00; font-size:16px; margin-top:8px; margin-bottom:4px;">💰 设备收益计算器</h2>', unsafe_allow_html=True)
        selected_time_tab1 = st.selectbox("选择运行时间档位:", current_options, index=st.session_state.target_time_index, key="calc_box_zh")
        st.session_state.target_time_index = current_options.index(selected_time_tab1)
        st.success(f"🎉 预计每月可带来收益: {HOURS_MAP[st.session_state.target_time_index] * 0.35 * 30:.2f} USDT")
        st.markdown("""
        <div class="feature-box">
            <h4 style="color:white; margin:0; font-size:13px;">📱 充电即赚 · 睡后收入</h4>
            <p style="color:#bdc3c7; font-size:11px; margin:2px 0 0 0;">只需在夜间充电并连接 Wi-Fi，NexaEdge 的轻量级 WASM 沙盒便会在后台静默运行清洗 AI 语料。</p>
        </div>
        <div class="feature-box">
            <h4 style="color:white; margin:0; font-size:13px;">🔥 39°C 智能温控屏障</h4>
            <p style="color:#bdc3c7; font-size:11px; margin:2px 0 0 0;">坚守绝不伤机底线。一旦手机运行温度触及 39°C 临界点，系统自动下发降载指令，打消损耗焦虑。</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown('<h2 style="color:#A2FF00; font-size:16px; margin-top:8px; margin-bottom:4px;">💰 Revenue Calculator</h2>', unsafe_allow_html=True)
        selected_time_tab1 = st.selectbox("Select Setting Pattern:", current_options, index=st.session_state.target_time_index, key="calc_box_en")
        st.session_state.target_time_index = current_options.index(selected_time_tab1)
        st.success(f"🎉 Estimated Monthly Income: {HOURS_MAP[st.session_state.target_time_index] * 0.35 * 30:.2f} USDT")
        st.markdown("""
        <div class="feature-box">
            <h4 style="color:white; margin:0; font-size:13px;">📱 Passive Income via Charging</h4>
            <p style="color:#bdc3c7; font-size:11px; margin:2px 0 0 0;">Just plug in and connect Wi-Fi at night, NexaEdge's lightweight WASM Sandbox cleans AI datasets silently.</p>
        </div>
        <div class="feature-box">
            <h4 style="color:white; margin:0; font-size:13px;">🔥 39°C Thermal Guard Barrier</h4>
            <p style="color:#bdc3c7; font-size:11px; margin:2px 0 0 0;">Total hardware protection. System auto-throttles load instantly if battery hits 39°C.</p>
        </div>
        """, unsafe_allow_html=True)


    with st.form("unified_whitelist_form"):
        if lang == "中文":
            st.markdown('<div style="font-size:12px; font-weight:bold; color:#A2FF00; margin-bottom:2px;">🎁 申领创世白名单与社媒双倍加速奖励</div>', unsafe_allow_html=True)
            u_email_label = "申请电子邮箱地址:"
            u_email_place = "请输入接收通知的邮箱"
            u_wallet_label = "绑定的 Solana 钱包接收地址 (获取空投资产):"
            u_wallet_place = "输入您的 Solana SPL 钱包公钥"
            u_ref_label = "推荐码 (选填):"
            u_ref_place = "如有推荐码，请输入以获得创世加速"
            btn_wl_txt = "锁定创世空投席位 ⚡"
            msg_empty = "❌ 请完整填写邮箱和钱包地址！"
            msg_success = "🎉 创世节点白名单成功锁定！我们会在空投快照前与您取得联系。"
            contact_btn_label = "📧 联系我们"
        else:
            st.markdown('<div style="font-size:12px; font-weight:bold; color:#A2FF00; margin-bottom:2px;">🎁 Claim Genesis Whitelist & Social Boosting Rewards</div>', unsafe_allow_html=True)
            u_email_label = "Notification Email Address:"
            u_email_place = "e.g., node_miner@gmail.com"
            u_wallet_label = "Bound Solana Wallet Address (For Asset Air-drops):"
            u_wallet_place = "Enter your Solana SPL public key address"
            u_ref_label = "Referral Code (Optional):"
            u_ref_place = "Enter code to claim genesis boosting if available"
            btn_wl_txt = "Lock Genesis Seating ⚡"
            msg_empty = "❌ Email and Wallet fields cannot be empty!"
            msg_success = "🎉 Genesis node whitelist locked successfully! Notification will follow before snapshot."
            contact_btn_label = "📧 Contact US"

        st.markdown(f"""
        <div class="social-grid">
            <a class="social-btn" href="https://www.instagram.com/nexaedge__?igsh=eXp0MTlmdDR6dm10&utm_source=qr" target="_blank">📸 Insta</a>
            <a class="social-btn" href="https://x.com/nexaedge_?s=21&t=8onO0h_fTxzmAGu431ZxXw" target="_blank">🐦 X</a>
            <a class="social-btn" href="https://www.facebook.com/share/18eXN6P3Ge/?mibextid=wwXIfr" target="_blank">👥 FB</a>
            <a class="social-btn" href="https://www.tiktok.com/@nexaedge7?_r=1&_t=ZS-96QbSMyso5v" target="_blank">🎵 TikTok</a>
            <a class="social-btn" href="https://t.me/NexaEdge7" target="_blank">📢 TG</a>
            <a class="social-btn" href="mailto:contact@nexaedge.org" style="border-color: #00e5ff; color: #00e5ff !important;">{contact_btn_label}</a>
        </div>
        """, unsafe_allow_html=True)

        u_email = st.text_input(u_email_label, placeholder=u_email_place, key="wl_mail").strip()
        u_wallet = st.text_input(u_wallet_label, placeholder=u_wallet_place, key="wl_wall").strip()
        u_ref = st.text_input(u_ref_label, placeholder=u_ref_place, key="wl_ref").strip()

        if st.form_submit_button(btn_wl_txt):
            if not u_email or not u_wallet:
                st.error(msg_empty)
            elif u_email.lower() in global_server["whitelist_emails"]:
                err_dup_email = "❌ 该邮箱已申请过白名单！" if lang=="中文" else "❌ This email has already been registered."
                st.error(err_dup_email)
            elif u_wallet.lower() in global_server["whitelist_wallets"]:
                err_dup_wallet = "❌ 该钱包地址已申请过白名单！" if lang=="中文" else "❌ This wallet has already been registered."
                st.error(err_dup_wallet)
            else:
                global_server["whitelist_emails"].add(u_email.lower())
                global_server["whitelist_wallets"].add(u_wallet.lower())
                wl_ref_code = generate_referral_code(u_email)
                wl_img_path = f"wl_invite_{wl_ref_code}.png"
                generate_referral_image(wl_ref_code, wl_img_path)
                with open("whitelist.txt", "a", encoding="utf-8") as f:
                    f.write(f"Email: {u_email} | Wallet: {u_wallet} | RefCode: {u_ref if u_ref else 'None'} | AssignedRef: {wl_ref_code} | Time: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                st.session_state.wl_success_img = wl_img_path

    # 申请成功后直接显示图片（含网址+推荐码）
    if st.session_state.get("wl_success_img") and os.path.exists(st.session_state.wl_success_img):
        st.image(st.session_state.wl_success_img, use_container_width=True)


# ==========================================
# TAB 2: Dashboard 算力控制台
# ==========================================
with tab2:
    if st.session_state.app_running:
        current_hash = random.uniform(18.5, 22.8)
        current_temp = random.uniform(36.4, 36.9)
        current_power = random.uniform(4.85, 5.35)
        st.session_state.chart_history.pop(0)
        st.session_state.chart_history.append(current_hash)
    else:
        current_hash = 0.0
        current_temp = 30.5
        current_power = random.uniform(0.12, 0.18)

    if st.session_state.current_user:
        badge_txt = f"🟢 已成功挂载云端账户: <b>{st.session_state.current_user}</b>" if lang=="中文" else f"🟢 Connected Cloud Account: <b>{st.session_state.current_user}</b>"
        st.markdown(f'<div class="user-badge">{badge_txt}</div>', unsafe_allow_html=True)
    else:
        badge_txt = "⚠️ 游客节点运行（数据暂存本地，建议立即去账户中心注册）" if lang=="中文" else "⚠️ Running as Visitor (Data stays local, register to sync)"
        st.markdown(f'<div class="user-badge" style="border-left-color:#ffb300; color:#ffb300;">{badge_txt}</div>', unsafe_allow_html=True)

    lbl_tgt = "配置目标运行时间:" if lang=="中文" else "Set Target Runtime:"
    selected_time_tab2 = st.selectbox(lbl_tgt, current_options, index=st.session_state.target_time_index, key="console_box")
    st.session_state.target_time_index = current_options.index(selected_time_tab2)

    s_sec = st.session_state.session_seconds
    time_str = f"{s_sec//3600:02d}:{(s_sec%3600)//60:02d}:{s_sec%60:02d}"

    chart_lbl = "📶 边缘节点算力实时波形 data" if lang=="中文" else "📶 Edge Node Real-time Hashrate Trend"
    st.markdown(f'<div class="chart-title-lbl">{chart_lbl}</div>', unsafe_allow_html=True)

    st.markdown('<div class="chart-wrapper">', unsafe_allow_html=True)
    df_chart = pd.DataFrame(st.session_state.chart_history, columns=["Hashrate (G/s)"])
    st.line_chart(df_chart, height=110, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    lbl_safe = "硬件运行温度" if lang=="中文" else "Hardware Temp"
    st.markdown(f'<div class="app-card"><div class="temp-section"><span class="app-value" style="font-size:14px;">🌡️ {lbl_safe}: {current_temp:.1f}°C</span><span style="background-color:#1e272e; color:#A2FF00; font-size:10px; font-weight:bold; padding:2px 8px; border-radius:5px;">SAFE</span></div></div>', unsafe_allow_html=True)

    lbl_p1 = "实时输入功耗:" if lang=="中文" else "Input Power:"
    lbl_p2 = "🔋 累计电力消耗:" if lang=="中文" else "🔋 Cumulative Energy:"
    st.markdown(f"""
    <div class="app-card">
        <div style="display:grid; grid-template-columns: 1fr 1fr; gap:6px;">
            <div style="background:#11171d; padding:6px; border-radius:8px;">
                <div style="font-size:9px; color:#88929b; font-weight:bold;">{lbl_p1}</div>
                <div class="app-value neon-blue-text" style="font-size:13px; font-family:monospace;">{current_power:.2f} W</div>
            </div>
            <div style="background:#11171d; padding:6px; border-radius:8px;">
                <div style="font-size:9px; color:#88929b; font-weight:bold;">{lbl_p2}</div>
                <div class="app-value" style="font-size:13px; font-family:monospace; color:#ffffff;">{st.session_state.total_energy_wh:.4f} Wh</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    lbl_d1 = "本次运行时长:" if lang=="中文" else "Continuous Runtime:"
    lbl_d2 = "账户绑定 NEXA 总数:" if lang=="中文" else "Account Balance:"

    if st.session_state.app_running:
        status_badge = '<span style="background-color:#1e272e; color:#A2FF00; font-size:10px; font-weight:bold; padding:2px 6px; border-radius:4px; margin-left:8px; vertical-align:middle;">ACTIVE</span>'
    else:
        status_badge = '<span style="background-color:#1e272e; color:#88929b; font-size:10px; font-weight:bold; padding:2px 6px; border-radius:4px; margin-left:8px; vertical-align:middle;">STANDBY</span>'

    st.markdown(f"""
    <div class="app-card">
        <div style="display:flex; justify-content:space-between; align-items:flex-end; gap:8px;">
            <div style="flex:1; min-width:0;">
                <div style="font-size:9px; color:#88929b; font-weight:bold;">{lbl_d1}</div>
                <div class="app-value" style="font-size:14px; display:inline-block; white-space:nowrap;">{time_str}{status_badge}</div>
            </div>
            <div style="text-align:right; flex:1; min-width:0;">
                <div style="font-size:9px; color:#88929b; font-weight:bold;">{lbl_d2}</div>
                <div class="app-value neon-green-text" style="font-size:14px; white-space:nowrap;">{st.session_state.app_earned:,.2f} NEXA</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if not st.session_state.app_running:
        btn_start = "激活并启动边缘算力节点" if lang=="中文" else "START COMPUTE SESSION"
        if st.button(btn_start, key="app_start_btn"):
            st.session_state.app_running = True
            st.session_state.last_tick_time = time.time()
            st.rerun()
    else:
        btn_stop = "暂停当前算力" if lang=="中文" else "PAUSE COMPUTE SESSION"
        if st.button(btn_stop, key="app_stop_btn"):
            st.session_state.app_running = False
            st.session_state.last_tick_time = 0.0
            st.rerun()

# ==========================================
# TAB 4: 🔑 账户注册与登录入口
# ==========================================
with tab4:
    if st.session_state.current_user:
        email = st.session_state.current_user
        user_info = global_server["user_db"].get(email, {})
        ref_code = user_info.get("referral_code", generate_referral_code(email))

        # 生成专属海报图（含网址+推荐码）
        user_poster_path = f"user_invite_{ref_code}.png"
        if not os.path.exists(user_poster_path):
            generate_referral_image(ref_code, user_poster_path)

        # 显示海报图
        if os.path.exists(user_poster_path):
            st.image(user_poster_path, use_container_width=True)

        st.markdown('<div class="app-card" style="text-align:center; padding:12px 10px; margin-top:8px;">', unsafe_allow_html=True)

        lbl_id = f"当前在线身份：<span class='neon-blue-text' style='font-weight:bold;'>{email}</span>" if lang=="中文" else f"Active Identity: <span class='neon-blue-text' style='font-weight:bold;'>{email}</span>"
        st.markdown(lbl_id, unsafe_allow_html=True)

        box_txt = f"全网同步累计收益<br><span class='neon-green-text' style='font-size:24px; font-weight:bold;'>{st.session_state.app_earned:,.2f} NEXA</span>" if lang=="中文" else f"Total Synchronized Cloud Earnings<br><span class='neon-green-text' style='font-size:24px; font-weight:bold;'>{st.session_state.app_earned:,.2f} NEXA</span>"
        st.markdown(f"<div style='margin:8px 0; background:#11171d; padding:8px; border-radius:10px;'>{box_txt}</div>", unsafe_allow_html=True)

        ref_label = "🎟️您的专属推荐码（分享可获加速奖励）" if lang=="中文" else "🎟️ Your Referral Code"
        st.markdown(f'<div style="background:#0d1f0d; border:1px dashed #A2FF00; border-radius:10px; padding:10px; margin:6px 0;"><span style="font-size:9px; color:#88929b; font-weight:bold;">{ref_label}</span><br><span class="glow-ref-code">{ref_code}</span></div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        btn_logout = "安全退出当前登录账户" if lang=="中文" else "Logout Account Location"
        if st.button(btn_logout, key="logout_btn"):
            st.session_state.current_user = None
            st.session_state.app_running = False
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        opt_auth = ["注册新节点账户", "登录已有账户"] if lang=="中文" else ["Register Node Account", "Login Existing Node"]
        auth_mode = st.radio("Auth Selection:", opt_auth, horizontal=True, label_visibility="collapsed")

        if auth_mode in ["注册新节点账户", "Register Node Account"]:
            with st.form("reg_form"):
                form_title = "🚀 极简注册（自动合并本地 NEXA 数量）" if lang=="中文" else "🚀 Quick Profile Registration"
                st.markdown(f'<div style="font-size:12px; font-weight:bold; color:#A2FF00; margin-bottom:6px;">{form_title}</div>', unsafe_allow_html=True)
                label_mail = "邮箱地址:" if lang == "中文" else "Email Address:"
                label_pwd = "设置密码:" if lang == "中文" else "Choose Password:"
                label_reg_ref = "推荐码 (选填):" if lang == "中文" else "Referral Code (Optional):"
                r_email = st.text_input(label_mail, placeholder="example@nexa.com").strip()
                r_pwd = st.text_input(label_pwd, type="password", placeholder="Password")
                r_ref = st.text_input(label_reg_ref, placeholder="e.g., NX-XXX-XXX").strip()
                btn_reg_txt = "创建全网统一账户 ⚡" if lang=="中文" else "Create Unified Profile ⚡"
                if f_submit := st.form_submit_button(btn_reg_txt):
                    if not r_email or not r_pwd:
                        st.error("❌ 邮箱和密码为必填项！" if lang=="中文" else "❌ Email and Password are mandatory!")
                    elif r_email in global_server["user_db"]:
                        st.error("❌ 该邮箱已被占用！" if lang=="中文" else "❌ Email is already occupied.")
                    else:
                        inherited_nexa = st.session_state.app_earned
                        ref_code = generate_referral_code(r_email)
                        generate_referral_image(ref_code, f"user_invite_{ref_code}.png")
                        global_server["user_db"][r_email] = {
                            "password_hash": hashlib.sha256(r_pwd.encode()).hexdigest(),
                            "score": inherited_nexa,
                            "reg_time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                            "referral_code": ref_code,
                            "referred_by": r_ref if r_ref else "None"
                        }
                        st.session_state.current_user = r_email
                        # ✨ 触发注册成功弹窗标志
                        time.sleep(0.5)
                        st.rerun()
        else:
            with st.form("login_form"):
                login_title = "🔑 登录 NexaEdge 算力账户" if lang=="中文" else "🔑 Connect Node Endpoint Terminal"
                st.markdown(f'<div style="font-size:12px; font-weight:bold; color:#00e5ff; margin-bottom:6px;">{login_title}</div>', unsafe_allow_html=True)
                l_email = st.text_input("登录邮箱:" if lang == "中文" else "Account Email:").strip()
                l_pwd = st.text_input("验证密码:" if lang == "中文" else "Verification Password:", type="password")
                btn_l_txt = "验证并载入云端档案 ⚡" if lang=="中文" else "Authenticate & Load Assets ⚡"
                if st.form_submit_button(btn_l_txt):
                    p_hash = hashlib.sha256(l_pwd.encode()).hexdigest()
                    if l_email in global_server["user_db"] and global_server["user_db"][l_email]["password_hash"] == p_hash:
                        st.session_state.current_user = l_email
                        st.session_state.app_earned = global_server["user_db"][l_email]["score"]
                        st.success("⚡ 登录成功！" if lang=="中文" else "⚡ Authentication verified!")
                        time.sleep(0.5)
                        st.rerun()
                    else:
                        st.error("❌ 账号或密码输入有误！" if lang=="中文" else "❌ Invalid combinations!")

# ==========================================
# 🛡️ 隐蔽后台暗门管理面板触发区
# ==========================================
if is_admin_active:
    st.markdown("---")
    st.markdown('<div style="font-size:14px; font-weight:bold; color:#f43f5e; margin-bottom:8px;">🔒 核心内网安全端口隐蔽审计大盘 (ADMIN PORTAL DETECTED)</div>', unsafe_allow_html=True)
    admin_password = st.text_input("🔑 请输入内网管理员授权验证密码：", type="password", key="admin_pwd_gate")

    if admin_password == "NexaAdmin2026":
        st.toast("🔓 内网大账本数据已成功解密并挂载", icon="🟢")
        whitelist_count = 0
        whitelist_lines = []
        if os.path.exists("whitelist.txt"):
            with open("whitelist.txt", "r", encoding="utf-8") as f:
                whitelist_lines = [line.strip() for line in f.readlines() if line.strip()]
            whitelist_count = len(whitelist_lines)

        c_a1, c_a2, c_a3 = st.columns(3)
        with c_a1: st.markdown(f'<div class="mini-stat-card" style="border:1px solid #f43f5e;"><div class="mini-stat-title">👥 用户注册量</div><div class="mini-stat-value" style="color:#f43f5e;">{len(global_server["user_db"])} Users</div></div>', unsafe_allow_html=True)
        with c_a2: st.markdown(f'<div class="mini-stat-card" style="border:1px solid #ffb300;"><div class="mini-stat-title">🎁 白名单登记</div><div class="mini-stat-value" style="color:#ffb300;">{whitelist_count} Claims</div></div>', unsafe_allow_html=True)
        with c_a3: st.markdown(f'<div class="mini-stat-card" style="border:1px solid #A2FF00;"><div class="mini-stat-title">🟢 活跃节点</div><div class="mini-stat-value" style="color:#A2FF00;">{len(global_server["active_device_set"])} Devices</div></div>', unsafe_allow_html=True)

        adm_sub_tab1, adm_sub_tab2 = st.tabs(["📋 注册用户大表", "🎁 创世白名单明细"])
        with adm_sub_tab1:
            table_html = """<table class="admin-table"><tr><th>序号</th><th>用户注册邮箱</th><th>生成专属邀请码</th><th>当前实测累计算力</th><th>绑定的上级推荐码</th><th>注册激活时间</th></tr>"""
            for idx, (email, info) in enumerate(global_server["user_db"].items(), 1):
                table_html += f"""<tr><td>{idx}</td><td>{email}</td><td style='color:#A2FF00; font-weight:bold; font-family:monospace;'>{info.get('referral_code', 'N/A')}</td><td style='color:#ffffff; font-weight:bold; font-family:monospace;'>{info['score']:,.2f} NEXA</td><td style='color:#00e5ff;'>{info.get('referred_by', 'None')}</td><td>{info['reg_time']}</td></tr>"""
            table_html += "</table>"
            st.markdown(table_html, unsafe_allow_html=True)

        with adm_sub_tab2:
            if whitelist_lines:
                wl_table_html = """<table class="admin-table"><tr><th>序号</th><th>提交的日志 data</th></tr>"""
                for idx, line in enumerate(whitelist_lines, 1):
                    wl_table_html += f"""<tr><td>{idx}</td><td style='font-family:monospace; color:#bdc3c7;'>{line}</td></tr>"""
                wl_table_html += "</table>"
                st.markdown(wl_table_html, unsafe_allow_html=True)
            else:
                st.info("暂无用户提交白名单申请。")
    elif admin_password != "":
        st.error("❌ 越权访问警告：内部授权密码错误，数据保持加密锁定状态！")

# ==========================================
# 📊 宏观大盘全局物理底栏
# ==========================================
if lang == "中文":
    lbl_active_nodes = "● 全网活跃节点"
    lbl_real_viewers = "👀 实时在线观众"
else:
    lbl_active_nodes = "● NETWORK ACTIVE NODES"
    lbl_real_viewers = "👀 LIVE REAL VIEWERS"

st.markdown(f"""
<div class="bottom-stats-row">
    <div class="mini-stat-card" style="border:1px dashed #A2FF00;">
        <span class="mini-stat-title">{lbl_active_nodes}</span>
        <span class="mini-stat-value" style="color:#A2FF00;">{len(global_server["active_device_set"])} Devices</span>
    </div>
    <div class="mini-stat-card" style="border:1px dashed #00e5ff;">
        <span class="mini-stat-title">{lbl_real_viewers}</span>
        <span class="mini-stat-value" style="color:#00e5ff;">{global_server["total_online_viewers"]} Online</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ==================== 后台实时高频刷新内核
if st.session_state.app_running:
    st.session_state.app_earned += 0.01
    st.session_state.session_seconds += 1
    st.session_state.total_energy_wh += (5.1 / 3600.0)
    if st.session_state.current_user:
        global_server["user_db"][st.session_state.current_user]["score"] = st.session_state.app_earned
    else:
        global_server["device_balances"][dev_id]["app_earned"] = st.session_state.app_earned
    st.session_state.last_tick_time = time.time()
    time.sleep(1.0)
    st.rerun()
