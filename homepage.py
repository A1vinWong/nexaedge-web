import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import os
import hashlib
# ... 其他引入 ...

# ...

# --- 🛠️ 核心修改：强制 TrueType 字体加载与坐标调整 ---
def generate_referral_image(ref_code: str, output_path: str):
    """
    读取背景图 image.png，在底部动态绘制:
    WebApp : nexaedge.org
    REFERRAL CODE: NX-XXX-XXX
    """
    base_img_path = "image.png"
    if not os.path.exists(base_img_path):
        # ... 备用图代码 ...
        pass
        
    img = Image.open(base_img_path).convert("RGBA")
    draw = ImageDraw.Draw(img)
    width, height = img.size

    # 使用项目根目录下的 project_font.ttf 强制 TrueType 字体加载
    font_path = "project_font.ttf"
    try:
        font_main = ImageFont.truetype(font_path, int(height * 0.05)) # 字体大小自适应
    except IOError:
        # 如果字体文件丢失，报错并在表单外显示错误
        font_main = ImageFont.load_default()

    # 要写入的两行文本
    line1 = "WebApp : nexaedge.org"
    line2 = f"REFERRAL CODE: {ref_code}"

    # 核心修改：新的文本纵坐标坐标，将文本向上调整，避开海报下边缘
    y1 = int(height * 0.81) 
    y2 = int(height * 0.88)

    # ... 文本居中计算和绘制代码 ...

    # 保存文件
    img.save(output_path)
    return output_path

# ...

# ==========================================
# TAB 1: 修复后的布局与状态管理 ( session_state)
# ==========================================
with tab1:
    # ... 其他 metric ...

    # 定义 session_state 用于在表单外部存储结果
    if 'assignment_ref_image_path' not in st.session_state:
        st.session_state.assignment_ref_image_path = None
        st.session_state.assignment_ref_code = None

    st.markdown("<br>", unsafe_allow_html=True)
    with st.form("unified_whitelist_form"):
        # ... 白名单表单输入块 ...

        if st.form_submit_button(btn_wl_txt):
            if not u_email or not u_wallet:
                st.error(msg_empty)
            # ... 其他表单逻辑 ...
            else:
                # 表单条件块内：执行数据处理和图片烘焙
                wl_ref_code = generate_referral_code(u_email)
                wl_img_path = f"user_invite_{wl_ref_code}.png" # 统一文件名

                # 条件块内核心逻辑：烘焙图片并保存路径到 session_state
                generate_referral_image(wl_ref_code, wl_img_path) 
                
                with open("whitelist.txt", "a", encoding="utf-8") as f:
                    f.write(f"Email: {u_email} | Wallet: {u_wallet} | RefCode: {u_ref if u_ref else 'None'} | AssignedRef: {wl_ref_code} | Time: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                
                # 更新 session_state，不在这里直接显示布局
                st.session_state.assignment_ref_image_path = wl_img_path
                st.session_state.assignment_ref_code = wl_ref_code
                st.success(msg_success)

    # 核心修改：在表单外部检查状态，并显示布局元素
    if st.session_state.assignment_ref_image_path:
        st.markdown("---")
        st.markdown("### 🎁 Your Genesis Invitation Poster / 您的专属创世邀请海报")
        st.image(st.session_state.assignment_ref_image_path, caption=f"Personal Node Card: {st.session_state.assignment_ref_code}", use_container_width=True)
        
        dl_btn_label = "📥 Download Invitation Poster / 下载专属分享海报" if lang == "中文" else "📥 Download Invitation Poster"
        with open(st.session_state.assignment_ref_image_path, "rb") as file:
            st.download_button(
                label=dl_btn_label,
                data=file,
                file_name=f"NexaEdge_Invite_{st.session_state.assignment_ref_code}.png",
                mime="image/png",
                key="tab1_download_btn" # 确保 key 唯一
            )
        # 可选：显示结果后清除 session_state
        # st.session_state.assignment_ref_image_path = None

# ...其他选项卡代码...
