import streamlit as st
from supabase import create_client, Client
import pandas as pd
import datetime

# 1. 网页全局基础配置 (支持宽屏，UI 更像专业 SaaS 看板)
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
    # 手机端/电脑端均能完美居中的紧凑登录框
    _, col_login, _ = st.columns([1, 2, 1])
    with col_login:
        st.markdown("<br><br><br>", unsafe_allow_html=True)
        st.title("🔒 Nexaedge Console")
        st.subheader("核心数据管理后台")
        pwd_input = st.text_input("请输入管理员高级密码", type="password", help="请输入官方发放的管理员凭证")
        if st.button("解锁控制台", use_container_width=True):
            if pwd_input == ADMIN_PASSWORD:
                st.session_state["authenticated"] = True
                st.rerun()
            else:
                st.error("❌ 密码错误，鉴权失败！")
    st.stop()

# --- 🔓 鉴权通过：正式进入核心控制台 ---
st.title("⚡ Nexaedge Whitelist 后端核心控制台")
st.caption("当前时间：2026年 | 实时监控用户注册行为、推荐码裂变效率及白名单资产明细")
st.markdown("---")

# 4. 🔄 实时拉取最新完整数据 (对齐新版 SDK 语法规范)
with st.spinner("正在从区块链底座调取实时数据..."):
    try:
        # 按最新优先排序 (created_at desc)
        response = supabase.table("whitelist").select("*").order("created_at", desc=True).execute()
        raw_data = response.data
    except Exception as e:
        st.error(f"❌ 获取数据失败，请检查数据库连接或表结构: {str(e)}")
        raw_data = []

# 5. 数据联动渲染逻辑
if not raw_data:
    st.info("💡 数据库目前运行正常，暂时没有新用户提交白名单。")
else:
    # 转化为 Pandas DataFrame 进行高性能前端数据切片
    df = pd.DataFrame(raw_data)
    
    # 统一转换并清洗时间戳数据
    df['created_at_dt'] = pd.to_datetime(df['created_at'])
    df['date'] = df['created_at_dt'].dt.date

    # ==========================================
    # 功能一：📊 注册统计指标核心看板
    # ==========================================
    st.markdown("### 📊 实时数据透视")
    
    total_rows = len(df)
    unique_emails = df['email'].nunique() if 'email' in df.columns else 0
    
    # 精准捕获 EN/ZH 语种分布数
    zh_count = 0
    en_count = 0
    if 'lang' in df.columns:
        lang_counts = df['lang'].value_counts()
        zh_count = int(lang_counts.get('zh-CN', 0)) + int(lang_counts.get('zh', 0))
        en_count = int(lang_counts.get('en', 0))
    other_lang_count = total_rows - (zh_count + en_count)
    
    # 前端分设四个精美卡片指标
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(label="📈 总提交次数 (Total)", value=total_rows)
    with col2:
        st.metric(label="👥 唯一独立邮箱 (Unique)", value=unique_emails, help="自动进行去重后的真实有效总量")
    with col3:
        st.metric(label="🇨🇳 中文用户 (ZH)", value=zh_count)
    with col4:
        st.metric(label="🇺🇸 英文用户 (EN)", value=en_count)

    st.markdown("<br>", unsafe_allow_html=True)
    
    # ==========================================
    # 功能二 & 三：📈 趋势图 + 推荐码活跃度排行
    # ==========================================
    chart_col, ref_col = st.columns([2, 1])
    
    with chart_col:
        st.markdown("#### 📅 每日注册趋势（近 30 天趋势迷你图）")
        # 按天聚合每日新注册量
        trend_df = df.groupby('date').size().reset_index(name='注册数量')
        trend_df = trend_df.set_index('date')
        # 官方原生流线型折线迷你图
        st.line_chart(trend_df, height=210)

    with ref_col:
        st.markdown("#### 🔥 裂变推荐码活跃度分析")
        if 'used_ref' in df.columns:
            # 统计谁的码被填写的频次最高
            ref_ranking = df['used_ref'].dropna().value_counts().reset_index()
            ref_ranking.columns = ['邀请码 (Ref Code)', '累计被使用次数']
            
            # 清理无效的空值或空白字符
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
    st.markdown("### 📋 白名单全资产明细明细（默认最新优先）")
    
    df_display = df.copy()
    
    # 钱包地址安全脱敏/截断处理逻辑 (例如: 0x5a31...2b8c)
    def truncate_wallet_address(address):
        if pd.isna(address) or len(str(address)) <= 12:
            return address
        addr_str = str(address)
        return f"{addr_str[:6]}...{addr_str[-4:]}"

    if 'wallet' in df_display.columns:
        df_display['wallet'] = df_display['wallet'].apply(truncate_wallet_address)
    
    # 清晰映射标准出表字段
    all_possible_cols = ["created_at", "email", "wallet", "ref_code", "used_ref", "lang"]
    display_cols = [col for col in all_possible_cols if col in df_display.columns]
    df_display = df_display[display_cols]
    
    # 高级全局即时模糊搜索框
    search_query = st.text_input("🔍 模糊检索邮箱或完整原始钱包地址...", placeholder="输入任意关键词回车即可筛选...")
    if search_query:
        email_mask = df['email'].str.contains(search_query, case=False, na=False) if 'email' in df.columns else False
        wallet_mask = df['wallet'].str.contains(search_query, case=False, na=False) if 'wallet' in df.columns else False
        df_filtered = df_display[email_mask | wallet_mask]
    else:
        df_filtered = df_display

    # 前端交互式表格渲染
    st.dataframe(df_filtered, use_container_width=True, hide_index=True)

    # ==========================================
    # 功能五：📥 自动带时间戳的一键导出
    # ==========================================
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 自动生成当前动态时间戳后缀 (格式例如: nexaedge_whitelist_20260609_162315.csv)
    current_timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_filename = f"nexaedge_whitelist_{current_timestamp}.csv"
    
    # 核心安全机制：导出时务必抽取 `df`（原全量未截断数据），确保管理员拿到的钱包完整无损！
    export_cols = [col for col in ["id", "email", "wallet", "ref_code", "used_ref", "lang", "created_at"] if col in df.columns]
    export_df = df[export_cols]
    csv_bytes = export_df.to_csv(index=False).encode('utf-8')
    
    st.download_button(
        label="📥 一键导出完整数据明细表 (全量完整钱包地址) 为 CSV 电子表格",
        data=csv_bytes,
        file_name=csv_filename,
        mime="text/csv",
        use_container_width=True
    )
