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

# 5. 数据流动防御渲染
if not raw_data:
    st.info("💡 数据库目前运行正常，暂时没有新用户提交白名单。")
else:
    # 转换为 DataFrame 确保安全
    df = pd.DataFrame(raw_data)
    
    # 统一强制补充缺失的核心字段，防止代码因列不存在而崩盘
    required_columns = ["created_at", "email", "wallet", "invitation_code", "ref_code", "referred_by", "used_ref", "lang"]
    for col in required_columns:
        if col not in df.columns:
            df[col] = ""

    # 安全地将创建时间转化为日期类型
    try:
        df['created_at_dt'] = pd.to_datetime(df['created_at'], errors='coerce')
        df['date'] = df['created_at_dt'].dt.date
    except Exception:
        df['date'] = datetime.date.today()

    # ==========================================
    # 功能一：📊 实时数据透视卡片 (安全统计)
    # ==========================================
    st.markdown("### 📊 实时数据透视")
    
    total_rows = len(df)
    unique_emails = df['email'].astype(str).str.strip().nunique() if 'email' in df.columns else 0
    
    # 极其宽容的中英文语种模糊匹配计数
    zh_count = 0
    en_count = 0
    if 'lang' in df.columns:
        lang_series = df['lang'].astype(str).str.lower()
        zh_count = lang_series.str.contains('zh').sum()
        en_count = lang_series.str.contains('en').sum()
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(label="📈 总提交次数 (Total)", value=total_rows)
    with col2:
        st.metric(label="👥 唯一独立邮箱 (Unique)", value=unique_emails)
    with col3:
        st.metric(label="🇨🇳 中文用户 (ZH)", value=int(zh_count))
    with col4:
        st.metric(label="🇺🇸 英文用户 (EN)", value=int(en_count))

    st.markdown("<br>", unsafe_allow_html=True)
    
    # ==========================================
    # 功能二 & 三：📈 趋势图 + 推荐码排行 (防御式渲染)
    # ==========================================
    chart_col, ref_col = st.columns([2, 1])
    
    with chart_col:
        st.markdown("#### 📅 每日注册趋势")
        try:
            trend_df = df.groupby('date').size().reset_index(name='注册数量')
            trend_df = trend_df.set_index('date')
            st.line_chart(trend_df, height=210)
        except Exception:
            st.caption("⏳ 正在等待更多日期的注册数据以生成趋势图...")

    with ref_col:
        st.markdown("#### 🔥 裂变推荐码活跃度分析")
        try:
            # 聚合所有的可能推荐码字段，防止漏算
            df['final_ref'] = df['referred_by'].fillna(df['used_ref']).astype(str).str.strip()
            # 过滤掉空字符串
            ref_filtered = df[df['final_ref'] != '']
            
            if not ref_filtered.empty:
                ref_ranking = ref_filtered['final_ref'].value_counts().reset_index()
                ref_ranking.columns = ['邀请码 (Ref Code)', '累计被使用次数']
                st.dataframe(ref_ranking.head(5), use_container_width=True, hide_index=True)
            else:
                st.caption("⏳ 暂时还没有发生推荐码裂变行为")
        except Exception:
            st.caption("⏳ 暂无裂变分析数据")

    st.markdown("---")

    # ==========================================
    # 功能四：📋 注册明细表 (带钱包强制安全截断)
    # ==========================================
    st.markdown("### 📋 白名单全资产明细（默认最新优先）")
    
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
    
    # 精简展示的字段，不要让表格太乱
    clean_cols = [c for c in ["created_at", "email", "wallet", "invitation_code", "referred_by", "lang"] if c in df_display.columns]
    if clean_cols:
        st.dataframe(df_display[clean_cols], use_container_width=True, hide_index=True)
    else:
        st.dataframe(df_display, use_container_width=True, hide_index=True)

    # ==========================================
    # 功能五：📥 自动带时间戳的一键导出
    # ==========================================
    st.markdown("<br>", unsafe_allow_html=True)
    try:
        current_timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        csv_filename = f"nexaedge_whitelist_{current_timestamp}.csv"
        
        # 导出最原始完整的全量数据（包含完整钱包地址）
        csv_bytes = df[required_columns].to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 一键导出完整数据明细表 (全量完整钱包地址) 为 CSV 电子表格",
            data=csv_bytes,
            file_name=csv_filename,
            mime="text/csv",
            use_container_width=True
        )
    except Exception as e:
        st.caption("无法生成导出按钮，等待数据格式化...")
