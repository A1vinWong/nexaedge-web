import streamlit as st
import os
import time
import random
import pandas as pd
import glob
import hashlib
from PIL import Image, ImageDraw, ImageFont

# ==========================================
# # 💡 在这里统一配置你的新合约地址
# ==========================================
DEFAULT_CA = "D7h9MvFDkVxPYeJwSTcE7VKkXo6myg"

# ==========================================
# # 1. 全局页面基础配置
# ==========================================
st.set_page_config(
    page_title="NexaEdge Network | Official",
    page_icon="🟢",
    layout="centered"
)

# ==========================================
# # 📱 注入自定义 CSS：强行消除移动端多余空白，实现完美贴合布局
# ==========================================
st.markdown("""
    <style>
    /* 1. 核心：大幅缩减主容器的上下左右留白，把下方内容硬拉上来 */
    .main .block-container {
        padding-top: 1.2rem !important;
        padding-bottom: 0.5rem !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
        max-width: 100% !important;
    }
    
    /* 2. 彻底隐藏 Streamlit 自带的底部页脚与无用标签留白 */
    footer {
        display: none !important;
    }
    [data-testid="stBorderProcessor"] {
        display: none !important;
    }
    
    /* 3. 修正大图弹性膨胀 Bug：强制图片容器高度跟着物理图片走，绝不多占一像素 */
    [data-testid="stImage"] {
        margin-bottom: -5px !important;
        text-align: center;
    }
    [data-testid="stImage"] img {
        height: auto !important;
        max-height: 65vh !important; /* 限制图片在手机屏幕中的最大高度比例 */
        object-fit: contain !important;
        margin: 0 auto;
    }
    
    /* 4. 压缩组件之间的上下行间距（Gap），让文字、下拉框和图片贴合更紧凑 */
    [data-testid="stVerticalBlock"] > div {
        padding-bottom: 0.15rem !important;
        padding-top: 0.15rem !important;
    }
    
    /* 5. 针对移动端隐藏不必要的滚动条，保持界面干净 */
    body {
        overflow-x: hidden;
    }
    </style>
""", unsafe_allow_html=True)


# ==========================================
# # 🔒 服务器跨进程内存锁 与 数据库模拟（持久化防清零账号）
# ==========================================
@st.cache_resource
def init_global_network_server():
    return {
        "active_device_set": set(),
        # 如果你后续有其他需要常驻内存的全局变量，可以在这里继续添加
    }

# 初始化全局网络数据
global_server_data = init_global_network_server()


# ==========================================
# # 渲染前端主体内容（示例占位，会完美应用上面的紧凑样式）
# ==========================================

# 标题
st.markdown("<h1 style='text-align: center; color: #99ff33; margin-bottom: 0;'>NexaEdge Network</h1>", unsafe_allow_html=True)

# 语言选择器
language = st.selectbox("", ["English", "简体中文"], label_visibility="collapsed")

# 副标题
st.markdown("<p style='text-align: center; color: #99ff33; font-size: 0.95rem;'>Transforming idle smartphones into high-purity data network for AI Era.</p>", unsafe_allow_html=True)

# 渲染手机模拟器大图（核心优化点：现在它不会在下方撑开黑块了）
# 这里的 "logo.png" 对应你仓库里的 1.08 MB 的大图
try:
    st.image("logo.png", use_container_width=True)
except Exception:
    # 防止本地调试找不到图片报错
    st.info("⚡ [Image Placeholder] 手机模拟器图片正在加载或路径不正确")

# 项目简报模块
st.markdown("""
<div style='background-color: #111; padding: 15px; border-radius: 10px; border: 1px solid #222;'>
    <b style='color: #99ff33;'>⚡ PROJECT BRIEFING</b><br><br>
    <p style='color: #ccc; font-size: 0.85rem; margin: 0; line-height: 1.4;'>
    NexaEdge empowers users to monetize unutilized smartphone capabilities. By creating an encrypted decentralized sandbox network, your device seamlessly routes localized data verification processes to unlock institutional level rewards while you sleep.
    </p>
</div>
""", unsafe_allow_html=True)
