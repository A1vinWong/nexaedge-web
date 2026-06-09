import streamlit as st
from supabase import create_client, Client
import uuid

# 1. 页面基本配置
st.set_page_config(page_title="Nexaedge Whitelist", page_icon="🚀", layout="centered")

# 2. 初始化 Supabase 客户端
@st.cache_resource
def init_supabase() -> Client:
    try:
        url = st.secrets["supabase"]["url"]
        key = st.secrets["supabase"]["key"]
        return create_client(url, key)
    except Exception as e:
        st.error("无法读取 Streamlit Secrets，请确保已正确配置 [supabase] 的 url 和 key。")
        st.stop()

supabase: Client = init_supabase()

# 3. 辅助函数：生成邀请码
def generate_ref_code():
    return str(uuid.uuid4()).split("-")[0].upper()

# --- 前端界面设计 ---
st.title("🚀 Nexaedge Whitelist Registration")
st.write("欢迎加入 Nexaedge！请填写以下信息以登记您的白名单。")
st.markdown("---")

query_params = st.query_params
url_ref = query_params.get("ref", "")

with st.form("whitelist_form", clear_on_submit=False):
    email = st.text_input("电子邮箱 Email *", placeholder="example@domain.com").strip()
    wallet = st.text_input("钱包地址 Wallet Address *", placeholder="0x...").strip()
    used_ref = st.text_input("邀请码 Referral Code (选填)", value=url_ref, placeholder="如果有邀请码，请在此输入").strip()
    lang = st.selectbox("首选语言 Preferred Language", ["zh-CN", "en", "ja", "ko"])
    
    submit_btn = st.form_submit_button("提交登记 Submit")

# 4. 表单提交后的核心处理逻辑
if submit_btn:
    if not email or not wallet:
        st.error("❌ 邮箱和钱包地址为必填项！")
    elif "@" not in email:
        st.error("❌ 请输入有效的邮箱地址！")
    else:
        with st.spinner("正在提交至 Supabase..."):
            try:
                check_email = supabase.table("whitelist").select("email").eq("email", email).execute()
                
                if check_email.data:
                    st.warning("⚠️ 该邮箱已经注册过白名单，请勿重复提交。")
                else:
                    new_ref_code = generate_ref_code()
                    insert_data = {
                        "email": email,
                        "wallet": wallet,
                        "ref_code": new_ref_code,
                        "used_ref": used_ref if used_ref else None,
                        "lang": lang
                    }
                    supabase.table("whitelist").insert(insert_data).execute()
                    
                    st.success("🎉 恭喜！白名单登记成功！")
                    st.balloons()
                    st.markdown("### 📢 你的专属邀请奖励")
                    st.write("分享你的专属邀请链接，邀请更多好友加入：")
                    
                    # 动态生成当前 App 的邀请链接
                    invite_url = f"https://nexaedge-web.streamlit.app/?ref={new_ref_code}" 
                    st.code(invite_url, language="text")
                    st.info(f"你的独立邀请码为: **{new_ref_code}**")
                    
            except Exception as e:
                st.error(f"提交失败，错误信息: {str(e)}")

