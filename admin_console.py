import streamlit as st
import pandas as pd
import requests
import datetime

# 1. 网页全局基础配置
st.set_page_config(page_title="Nexaedge Admin Console", page_icon="⚡", layout="wide")

# 2. 🔐 独立安全登录页
ADMIN_PASSWORD = "nexaedge2026admin"

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    _, col_login, _ = st.columns([1, 2, 1])
    with col_login:
        st.markdown("<br><br><br>", unsafe_allow_html=True)
        st.title("🔒 Nexaedge Console")
        st.subheader("核心数据管理后台")
        pwd_input = st.text_input("请输入管理员高级密码", type="password")
        if st.button("解锁控制台", use_container_width=True):
            if pwd_input == ADMIN_PASSWORD:
                st.session_state["authenticated"] = True
                st.rerun()
            else:
                st.error("❌ 密码错误，鉴权失败！")
    st.stop()

# --- 🔓 鉴权通过 ---
st.title("⚡ Nexaedge Whitelist 后端核心控制台")
st.caption("当前时间：2026年 | 实时监控用户注册行为及白名单资产明细")
st.markdown("---")

# 3. 🌐 纯原生网络请求直连 Supabase (免安装任何依赖库)
raw_data = []
try:
    url = st.secrets["supabase"]["url"].strip().rstrip('/')
    key = st.secrets["supabase"]["key"].strip()
    
    # 拼接标准的 Supabase REST API 路径
    endpoint = f"{url}/rest/v1/whitelist?select=*"
    headers = {
        "apikey": key,
        "Authorization": f"Bearer {key}"
    }
    
    response = requests.get(endpoint, headers=headers, timeout=10)
    if response.status_code == 200:
        raw_data = response.json()
    else:
        st.error(f"❌ 数据库接口返回错误码: {response.status_code}")
except Exception as e:
    st.error(f"❌ 建立网络连接连接失败: {str(e)}")

# 4. 数据流动防御渲染
if not raw_data:
    st.info("💡 数据库目前连通正常，正在等待前台用户提交第一条白名单数据。")
else:
    # 转换为 DataFrame 确保安全
    df = pd.DataFrame(raw_data)
    
    # 统一强制补充缺失的核心字段，防止代码崩盘
    required_columns = ["created_at", "email", "wallet", "invitation_code", "ref_code", "referred_by", "lang"]
    for col in required_columns:
        if col not in df.columns:
            df[col] = ""

    # ==========================================
    # 功能一：📊 实时数据简报
    # ==========================================
    total_rows = len(df)
    unique_emails = df['email'].astype(str).str.strip().nunique() if 'email' in df.columns else 0
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="📈 总提交次数 (Total Rows)", value=total_rows)
    with col2:
        st.metric(label="👥 唯一独立邮箱 (Unique Emails)", value=unique_emails)

    st.markdown("<br>", unsafe_allow_html=True)

    # ==========================================
    # 功能二：📋 注册明细表 (带钱包明细)
    # ==========================================
    st.markdown("### 📋 白名单全资产明细")
    
    df_display = df.copy()
    
    # 钱包中间截断函数
    def truncate_wallet_address(address):
        if pd.isna(address) or len(str(address)) <= 12:
            return address
        addr_str = str(address).strip()
        if not addr_str:
            return ""
        return f"{addr_str[:6]}...{addr_str[-4:]}"

    if 'wallet' in df_display.columns:
        df_display['wallet'] = df_display['wallet'].apply(truncate_wallet_address)
    
    clean_cols = [c for c in ["created_at", "email", "wallet", "invitation_code", "lang"] if c in df_display.columns]
    if clean_cols:
        st.dataframe(df_display[clean_cols], use_container_width=True, hide_index=True)
    else:
        st.dataframe(df_display, use_container_width=True, hide_index=True)

    # ==========================================
    # 功能三：📥 一键下载 CSV
    # ==========================================
    st.markdown("<br>", unsafe_allow_html=True)
    try:
        csv_bytes = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 一键导出全量数据明细表为 CSV 电子表格",
            data=csv_bytes,
            file_name="nexaedge_whitelist_export.csv",
            mime="text/csv",
            use_container_width=True
        )
    except Exception:
        pass
