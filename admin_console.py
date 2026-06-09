import streamlit as st
from supabase import create_client, Client
import pandas as pd
import datetime
import os

# 1. 页面基础配置 (宽屏模式更适合看报表)
st.set_page_config(page_title="Nexaedge Admin Console", page_icon="⚡", layout="wide")

# 2. 初始化 Supabase 客户端
@st.cache_resource
def init_supabase() -> Client:
    try:
        url = st.secrets["supabase"]["url"]
        key = st.secrets["supabase"]["key"]
        return create_client(url, key)
    except Exception as e:
        st.error("无法读取 Streamlit Secrets，请确保已正确配置 [supabase]。")
        st.stop()

supabase: Client = init_supabase()

# 3. 独立安全登录页
ADMIN_PASSWORD = "nexaedge2026admin"

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    # 居中紧凑的登录框设计
    _, col_login, _ = st.columns([1, 2, 1])
    with col_login:
        st.markdown("<br><br><br>", unsafe_allow_html=True)
        st.title("🔒 Nexaedge Console")
        st.subheader("核心数据管理后台")
        pwd_input = st.text_input("请输入管理员高级密码", type="password", help="请向技术负责人获取")
        if st.button("解锁控制台", use_container_width=True):
            if pwd_input == ADMIN_PASSWORD:
                st.session_state["authenticated"] = True
                st.rerun()
            else:
                st.error("❌ 密码错误，鉴权失败！")
    st.stop()

# --- 验证通过：进入正式控制台 ---
st.title("⚡ Nexaedge Whitelist 后端核心控制台")
st.caption("实时监控用户注册行为、推荐码裂变效率及白名单资产明细")
st.markdown("---")

# 4. 从 Supabase 拉取最新完整数据 (修复在新版 SDK 下的排序报错问题)
with st.spinner("正在从区块链底座调取实时数据..."):
    try:
        # 【核心修正】：新版 Supabase Python SDK 移除了 descending 参数，改用 desc=True
        response = supabase.table("whitelist").select("*").order("created_at", desc=True).execute()
        raw_data = response.data
    except Exception as e:
        st.error(f"获取数据失败，请检查数据库连接: {str(e)}")
        raw_data = []

if not raw_data:
    st.info("💡 数据库目前处于真空状态，暂时没有用户提交白名单。")
else:
    # 转换为 Pandas DataFrame 方便深度处理
    df = pd.DataFrame(raw_data)
    
    # 统一处理时间格式（处理时区，保留到天用于统计趋势）
    df['created_at_dt'] = pd.to_datetime(df['created_at'])
    df['date'] = df['created_at_dt'].dt.date

    # ==========================================
    # 📊 第一部分：注册统计核心指标看板
    # ==========================================
    st.markdown("### 📊 实时数据透视")
    
    total_rows = len(df)
    unique_emails = df['email'].nunique() if 'email' in df.columns else 0  # 唯一邮箱总数
    
    # 统计语言分布（防止没有值的异常情况）
    zh_count = 0
    en_count = 0
    if 'lang' in df.columns:
        lang_counts = df['lang'].value_counts()
        zh_count = int(lang_counts.get('zh-CN', 0))
        en_count = int(lang_counts.get('en', 0))
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(label="📈 总提交次数", value=total_rows)
    with col2:
        st.metric(label="👥 唯一独立邮箱", value=unique_emails, help="去重后的真实邮箱总量")
    with col3:
        st.metric(label="🇨🇳 中文用户 (ZH)", value=zh_count)
    with col4:
        st.metric(label="🇺🇸 英文用户 (EN)", value=en_count)

    st.markdown("<br>", unsafe_allow_html=True)
    
    # ==========================================
    # 📈 第二部分：每日注册趋势迷你图 + 推荐码分析
    # ==========================================
    chart_col, ref_col = st.columns([2, 1])
    
    with chart_col:
        st.markdown("#### 📅 每日注册趋势（近30天）")
        # 按日期分组统计每日数量
        trend_df = df.groupby('date').size().reset_index(name='注册数量')
        trend_df = trend_df.set_index('date')
        # Streamlit 官方原生迷你折线图
        st.line_chart(trend_df, height=200)

    with ref_col:
        st.markdown("#### 🔥 裂变推荐码 Top 5")
        if 'used_ref' in df.columns:
            # 统计 used_ref 哪个被填写的次数最多 (即谁的码最活跃)
            ref_ranking = df['used_ref'].dropna().value_counts().reset_index()
            ref_ranking.columns = ['邀请码 (Ref)', '被使用次数']
            
            # 过滤掉可能存在的空字符串邀请码
            ref_ranking = ref_ranking[ref_ranking['邀请码 (Ref)'].str.strip() != '']
            
            if not ref_ranking.empty:
                st.dataframe(ref_ranking.head(5), use_container_width=True, hide_index=True)
            else:
                st.caption("暂无邀请裂变数据")
        else:
            st.caption("暂无邀请裂变数据")

    st.markdown("---")

    # ==========================================
    # 📋 第三部分：白名单数据明细表（截断钱包显示）
    # ==========================================
    st.markdown("### 📋 白名单资产明细（最新优先）")
    
    # 克隆一个用于前端脱敏展示的 DataFrame
    df_display = df.copy()
    
    # 实现钱包地址截断显示 (例如: 0x1234...abcd)
    def truncate_wallet(address):
        if pd.isna(address) or len(str(address)) <= 10:
            return address
        addr_str = str(address)
        return f"{addr_str[:6]}...{addr_str[-4:]}"

    if 'wallet' in df_display.columns:
        df_display['wallet'] = df_display['wallet'].apply(truncate_wallet)
    
    # 检查并整理表格展示列（确保即使有缺失列程序也不会崩溃）
    all_possible_cols = ["created_at", "email", "wallet", "ref_code", "used_ref", "lang"]
    display_cols = [col for col in all_possible_cols if col in df_display.columns]
    df_display = df_display[display_cols]
    
    # 搜索和筛选框
    search_query = st.text_input("🔍 搜索邮箱或原始钱包地址...", placeholder="输入任意关键字后回车...")
    if search_query:
        # 搜索时支持使用原始完整地址/邮箱进行过滤
        email_mask = df['email'].str.contains(search_query, case=False, na=False) if 'email' in df.columns else False
        wallet_mask = df['wallet'].str.contains(search_query, case=False, na=False) if 'wallet' in df.columns else False
        df_filtered = df_display[email_mask | wallet_mask]
    else:
        df_filtered = df_display

    # 渲染明细表格
    st.dataframe(df_filtered, use_container_width=True, hide_index=True)

    # ==========================================
    # 📥 第四部分：自动带时间戳的一键导出
    # ==========================================
    st.markdown("<br>", unsafe_allow_html=True)
    # 获取当前时间并格式化为安全的文件名字符串 (例如: 20260609_1530)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_filename = f"nexaedge_whitelist_{timestamp}.csv"
    
    # 导出完整的、未截断的数据（确保导出的钱包地址是完整的！）
    export_cols = [col for col in ["id", "email", "wallet", "ref_code", "used_ref", "lang", "created_at"] if col in df.columns]
    export_df = df[export_cols]
    csv_bytes = export_df.to_csv(index=False).encode('utf-8')
    
    st.download_button(
        label="📥 一键导出完整数据 (带全量钱包地址) 为 CSV 电子表格",
        data=csv_bytes,
        file_name=csv_filename,
        mime="text/csv",
        use_container_width=True
    )
