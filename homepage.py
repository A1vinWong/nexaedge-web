import streamlit as st
import os

# 1. 网页全局基础配置 (支持手机自适应)
st.set_page_config(
    page_title="NexaEdge Network | The Tier 3 DePIN Giant",
    page_icon="🟢",
    layout="centered"
)

# 自定义超酷暗黑科技风 CSS 样式（全面适配你的荧光绿 Logo 配色）
st.markdown("""
    <style>
    /* 整体背景微调 */
    .stApp {
        background-color: #0b0f12;
    </style>
""", unsafe_allow_html=True)

# ==================== 🪐 头部：Logo 与项目门面介入 ====================

# 检查当前目录下是否存在 logo.png
if os.path.exists("logo.png"):
    # 在页面正中央渲染你的高颜值 Logo，大小适配手机与电脑屏幕
    st.image("logo.png", use_container_width=True)
else:
    # 如果图片还没放进去，显示炫酷的备用文字文字
    st.markdown('<h1 style="text-align:center; color:#A2FF00; font-size:42px; font-weight:800;">NexaEdge</h1>', unsafe_allow_html=True)
    st.caption("⚠️ 创始人提醒：请将 Logo 图片命名为 'logo.png' 并放在当前代码同目录下以完美激活视觉。")

st.markdown('<p style="font-size: 18px; color: #bdc3c7; text-align: center; margin-top:10px; margin-bottom: 30px;">让全球 50 亿部闲置手机，成为 AI 时代的高纯度语料燃料工厂</p>', unsafe_allow_html=True)

# 震撼的 Banner 数据大牌（数字颜色与 Logo 同步）
col1, col2, col3 = st.columns(3)
with col1:
    st.image("https://img.icons8.com/nolan/64/coins.png", width=40)
    st.metric(label="💰 平台技术抽成", value="20%", delta="纯现金流造血")
with col2:
    st.image("https://img.icons8.com/nolan/64/temperature.png", width=40)
    st.metric(label="🌡️ 智能硬件风控", value="39°C", delta="多端联动秒级预警", delta_color="inverse")
with col3:
    st.image("https://img.icons8.com/nolan/64/blockchain.png", width=40)
    st.metric(label="🌐 算力结算底座", value="Solana SPL", delta="极速、低Gas")

st.markdown("<hr style='border:1px solid #1e272e;'>", unsafe_allow_html=True)

# ==================== 🛠️ 核心三大技术壁垒展示 ====================
st.markdown('<h2 style="color:#A2FF00;">⚡ 为什么选择 NexaEdge？</h2>', unsafe_allow_html=True)

st.markdown("""
<div style="background-color: #11171d; padding: 20px; border-radius: 10px; border-left: 5px solid #A2FF00; margin-bottom: 15px;">
    <h4 style="color:#ffffff; margin-top:0;">📱 C端：锁屏充电·睡后收入 (零门槛)</h4>
    <p style="color:#bdc3c7; margin-bottom:0;">无需购买昂贵的专用硬件。用户只需在夜间充电、连接 Wi-Fi 并锁屏，NexaEdge 的轻量级 WASM 沙盒便会在后台静默运行，利用闲置 CPU/NPU 算力清洗 AI 语料，单机每小时可赚取约 <b>RM 1.33 ~ RM 1.53</b>。</p>
</div>
<div style="background-color: #11171d; padding: 20px; border-radius: 10px; border-left: 5px solid #A2FF00; margin-bottom: 15px;">
    <h4 style="color:#ffffff; margin-top:0;">🔥 独创：39°C 智能温控风控屏障</h4>
    <p style="color:#bdc3c7; margin-bottom:0;">我们坚守绝不伤机的底线。一旦手机运行温度触及 39°C 临界点，系统触发多端联动机制，立即向手机端和电脑大屏发送警报，并自动下发降载指令。彻底打消 C 端用户的硬件焦虑。</p>
</div>
<div style="background-color: #11171d; padding: 20px; border-radius: 10px; border-left: 5px solid #A2FF00; margin-bottom: 15px;">
    <h4 style="color:#ffffff; margin-top:0;">🤝 B端：2:1 多数表决防作弊机制</h4>
    <p style="color:#bdc3c7; margin-bottom:0;">原始语料切块多点分发，通过 3 节点冗余计算。平台采用去中心化的多数表决机制，彻底过滤和封杀模拟器等恶意篡改行为，向 AI 大模型购买方交付 100% 验证过的高纯度干净数据集。</p>
</div>
""", unsafe_allow_html=True)

st.markdown("<hr style='border:1px solid #1e272e;'>", unsafe_allow_html=True)

# ==================== 📊 算力价格双向实时计算器 ====================
st.markdown('<h2 style="color:#A2FF00;">🧮 生态双向收益计算器</h2>', unsafe_allow_html=True)
role = st.selectbox("请选择您的身份：", ["我是手机持有者 (C端算力提供方)", "我是 AI 大模型厂商 (B端算力购买方)"])

if role == "我是手机持有者 (C端算力提供方)":
    hours = st.slider("预估您每天夜间挂机打工的小时数：", 1, 12, 6)
    device = st.radio("您的设备系统：", ["iOS 苹果手机", "Android 安卓手机"])
    
    rate = 1.53 if "iOS" in device else 1.33
    daily_earn = hours * rate
    monthly_earn = daily_earn * 30
    
    st.success(f"🎉 预计您的手机每晚可为您赚取 **RM {daily_earn:.2f}**")
    st.info(f"📈 一个月（30天）累计可躺赚 **RM {monthly_earn:.2f}**（轻松解决您的家庭宽带和手机网费！）")

else:
    data_need = st.number_input("您需要平台全球手机节点为您清洗/采集的语料大小 (GB):", min_value=1, value=100)
    total_cost = data_need * 25.0
    platform_cut = total_cost * 0.20
    
    st.warning(f"💼 您的算力采购预算总计：**RM {total_cost:.2f}**")
    st.success(f"🪙 包含 NexaEdge 平台截留的 20% 技术服务费（纯利润）：**RM {platform_cut:.2f}**")

st.markdown("<hr style='border:1px solid #1e272e;'>", unsafe_allow_html=True)

# ==================== 📧 早期用户白名单预约 ====================
st.markdown('<h2 style="color:#A2FF00;">🚀 抢先加入早期白名单 (Airdrop 预约)</h2>', unsafe_allow_html=True)
st.write("提交您的邮箱，在 `$NEXA` 代币正式在 Solana 首发（TGE）时，优先获得测试网上线空投奖励资格！")

with st.form("whitelist_form"):
    user_email = st.text_input("输入您的 Email 地址:")
    wallet_addr = st.text_input("您的 Solana 钱包接收地址 (选填):")
    submitted = st.form_submit_with_button("立刻锁定白名单席位 ⚡")
    
    if submitted:
        if user_email:
            st.balloons()
            st.success(f"🎯 恭喜！{user_email} 已成功列入 NexaEdge 早期白名单。")
            with open("whitelist.txt", "a") as f:
                f.write(f"{user_email},{wallet_addr}\n")
        else:
            st.error("请输入有效的邮箱地址。")
