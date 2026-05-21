import hashlib
import os
import random
import time
from PIL import Image, ImageDraw, ImageFont
import glob
import pandas as pd
import streamlit as st

# 💡 在这里统一配置你的新合约地址
DEFAULT_CA = "D7h9MvFDkVxPYeJWSTcE7VKkXo6myg..."

# 1. 全局页面基础配置
st.set_page_config(
    page_title="NexaEdge Network | Official",
    page_icon="🟢",
    layout="centered"
)

# ==============================================================================
# 🔒 服务器跨进程内存锁 与 数据库模拟（持久化防清零账本）
# ==============================================================================
@st.cache_resource
def init_global_network_server():
    return {
        "active_device_set": set(),
    }

# --- 页面头部标题与介绍 ---
st.title("NexaEdge Network")

# 语言选择器
st.selectbox("", ["English"], label_visibility="collapsed")

st.markdown(
    "<p style='color:#8efc33; text-align:center; font-weight:bold;'>"
    "Transforming idle smartphones into high-purity data network for AI Era."
    "</p>", 
    unsafe_allow_html=True
)

# --- 渲染图片 (Logo / Phone Mockup) ---
logo_path = "logo.png"
if os.path.exists(logo_path):
    st.image(logo_path, use_column_width=True)

# ==============================================================================
# 📱 核心特性介绍区块 (Overview 页面核心)
# ==============================================================================

# 1. 第一个介绍：被动收入
st.markdown("""
<div style="padding:15px; border-radius:10px; border-left: 5px solid #8efc33; background-color:#14171f; margin-bottom:15px;">
    <h4 style="margin:0 0 8px 0; color:#ffffff;">📱 Passive Income via Charging</h4>
    <p style="color:#a3a8b4; font-size:14px; margin:0;">Just plug in and connect Wi-Fi at night, NexaEdge's lightweight WASM Sandbox cleans AI datasets silently.</p>
</div>
""", unsafe_allow_html=True)

# 2. 第二个介绍：控温保护
st.markdown("""
<div style="padding:15px; border-radius:10px; border-left: 5px solid #8efc33; background-color:#14171f; margin-bottom:15px;">
    <h4 style="margin:0 0 8px 0; color:#ffffff;">🔥 39°C Thermal Guard Barrier</h4>
    <p style="color:#a3a8b4; font-size:14px; margin:0;">Total hardware protection. System auto-throttles load instantly if battery hits 39°C.</p>
</div>
""", unsafe_allow_html=True)

# 🟢 3. 帮你加回来的——第三个介绍：去中心化共识/数据安全
st.markdown("""
<div style="padding:15px; border-radius:10px; border-left: 5px solid #8efc33; background-color:#14171f; margin-bottom:15px;">
    <h4 style="margin:0 0 8px 0; color:#ffffff;">🔒 Decentralized Consensus Network</h4>
    <p style="color:#a3a8b4; font-size:14px; margin:0;">Proprietary BFT protocols with 2:1 Redundant Voting guarantee absolute data shards integrity and user privacy.</p>
</div>
""", unsafe_allow_html=True)


# --- 底部项目简介区块 ---
st.markdown("""
<div style="padding:15px; border-radius:10px; background-color:#14171f; margin-top:20px;">
    <h4 style="color:#8efc33; margin:0 0 10px 0;">⚡ PROJECT BRIEFING</h4>
    <p style="color:#ffffff; font-size:13px; line-height:1.6; margin:0;">
    NexaEdge empowers users to monetize unutilized smartphone capabilities via encrypted decentralized sandbox networks easily.
    </p>
</div>
""", unsafe_allow_html=True)
