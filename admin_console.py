import streamlit as st
from supabase import create_client, Client
import pandas as pd
import datetime

# 1. 网页全局基础配置
st.set_page_config(page_title="Nexaedge Admin Console", page_icon="⚡", layout="wide")

# 2. 初始化 Supabase 客户端
@st.cache_resource
def init_supabase() -> Client:
    try:
        url = st.secrets["supabase"]["url"]
        key = st.secrets["supabase"]["key"]
        return create_client(url, key)
    except Exception as e:
        st.error("❌ 无法连接到 Supabase 数据库，请检查 Streamlit 的 Secrets 配置。")
        st.stop()

supabase: Client = init_supabase()

# 3. 🔐 独立安全登录页
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
st.caption("当前时间：2026年 | 实时监控用户注册行为、推荐码裂变效率及白名单资产明细")
st.markdown("---")

# 4. 实时拉取最新完整数据
try:
    response = supabase.table("whitelist").select("*").order("created_at", desc=True).execute()
    raw_data = response.data
except Exception as e:
    st.error(f"❌ 获取数据失败: {str(e)}")
    raw_data = []

# 5. 数据联动渲染逻辑
if not raw_data:
    st.info("💡 数据库目前运行正常，暂时没有新用户提交白名单。")
else:
    df = pd.DataFrame(raw_data)
    
    # 时间转换
    df['created_at_dt'] = pd.to_datetime(df['created_at'])
    df['date'] = df['created_at_dt'].dt.date

    # ==========================================
    # 功能一：📊 注册统计指标
    # ==========================================
    st.markdown("### 📊 实时数据透视")
    
    total_rows = len(df)
    unique_emails = df['email'].nunique() if 'email' in df.columns else 0
    
    # 语种统计
    zh_count = 0
    en_count = 0
    if 'lang' in df.columns:
        lang_counts = df['lang'].value_counts()
        zh_count = int(lang_counts.get('zh-CN', 0)) + int(lang_counts.get('zh', 0))
        en_count = int(lang_counts.get('en', 0))
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(label="📈 总提交次数 (Total)", value=total_rows)
    with col2:
        st.metric(label="👥 唯一独立邮箱 (Unique)", value=unique_emails)
    with col3:
        st.metric(label="🇨🇳 中文用户 (ZH)", value=zh_count)
    with col4:
        st.metric(label="🇺🇸 英文用户 (EN)", value=en_count)

    st.markdown("<br>", unsafe_allow_html=True)
    
    # ==========================================
    # 功能二 & 三：📈 趋势图 + 推荐码排行
    # ==========================================
    chart_col, ref_col = st.columns([2, 1])
    
    with chart_col:
        st.markdown("#### 📅 每日注册趋势")
        trend_df = df.groupby('date').size().reset_index(name='注册数量')
        trend_df = trend_df.set_index('date')
        st.line_chart(trend_df, height=210)

    with ref_col:
        st.markdown("#### 🔥 裂变推荐码活跃度分析")
        # 兼容前台的 referred_by 字段
        ref_field = 'referred_by' if 'referred_by' in df.columns else ('used_ref' if 'used_ref' in df.columns else None)
        if ref_field and ref_field in df.columns:
            ref_ranking = df[ref_field].dropna().value_counts().reset_index()
            ref_ranking.columns = ['邀请码 (Ref Code)', '累计被使用次数']
            ref_ranking = ref_ranking[ref_ranking['邀请码 (Ref Code)'].astype(str).str.strip() != '']
            if not ref_ranking.empty:
                st.dataframe(ref_ranking.head(5), use_container_width=True, hide_index=True)
            else:
                st.caption("⏳ 暂时还没有发生推荐码裂变行为")
        else:
            st.caption("⏳ 暂无裂变分析数据")

    st.markdown("---")

    # ==========================================
    # 功能四：📋 注册明细表 (最新优先 + 钱包截断)
    # ==========================================
    st.markdown("### 📋 白名单全资产明细（默认最新优先）")
    
    df_display = df.copy()
    
    # 钱包截断
    def truncate_wallet_address(address):
        if pd.isna(address) or len(str(address)) <= 12:
            return address
        addr_str = str(address)
        return f"{addr_str[:6]}...{addr_str[-4:]}"

    if 'wallet' in df_display.columns:
        df_display['wallet'] = df_display['wallet'].apply(truncate_wallet_address)
    
    # 动态匹配列名（兼容前后台不同命名）
    all_cols = ["created_at", "email", "wallet", "invitation_code", "ref_code", "referred_by", "used_ref", "lang"]
    display_cols = [col for col in all_cols if col in df_display.columns]
    df_display = df_display[display_cols]

    st.dataframe(df_display, use_container_width=True, hide_index=True)

    # ==========================================
    # 功能五：📥 自动带时间戳的一键导出
    # ==========================================
    st.markdown("<br>", unsafe_allow_html=True)
    current_timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_filename = f"nexaedge_whitelist_{current_timestamp}.csv"
    
    csv_bytes = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 一键导出完整数据明细表 (全量完整钱包地址) 为 CSV 电子表格",
        data=csv_bytes,
        file_name=csv_filename,
        mime="text/csv",
        use_container_width=True
    )
