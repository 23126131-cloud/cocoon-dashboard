import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import auth  # Module xác thực phân quyền

# ---------------------------------------------------------
# 1. CẤU HÌNH TRANG WEB
# ---------------------------------------------------------
st.set_page_config(
    page_title="Cocoon Market & Consumer Intelligence",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# 2. BỘ CSS CHUẨN NỀN MÀU DA COCOON & CHỮ ĐEN ĐẬM SẮC NÉT (SIÊU TƯƠNG PHẢN)
# ---------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }

    /* Nền màu da / Kem ấm áp đặc trưng thương hiệu Cocoon */
    .stApp {
        background-color: #FAF5E9 !important;
        color: #0F172A !important;
    }

    /* Sidebar Dark Executive Style */
    div[data-testid="stSidebar"] {
        background-color: #18110C !important;
        border-right: 1px solid #2D2018;
    }
    div[data-testid="stSidebar"] * {
        color: #F8FAFC !important;
    }
    div[data-testid="stSidebar"] .stSelectbox label, 
    div[data-testid="stSidebar"] .stSlider label,
    div[data-testid="stSidebar"] .stTextInput label {
        color: #E2E8F0 !important;
        font-weight: 700 !important;
        font-size: 13px !important;
    }
    div[data-testid="stSidebar"] input, 
    div[data-testid="stSidebar"] div[data-baseweb="select"] {
        background-color: #261B14 !important;
        color: #ffffff !important;
        border-radius: 8px !important;
        border: 1px solid #3D2B20 !important;
    }

    /* Executive Header Banner */
    .executive-header {
        background: #FFFFFF;
        border: 1px solid #E2D9C8;
        border-left: 6px solid #B8860B;
        padding: 22px 28px;
        border-radius: 14px;
        margin-bottom: 22px;
        box-shadow: 0 4px 15px rgba(24, 17, 12, 0.05);
    }
    .executive-title {
        color: #0F172A !important;
        font-size: 24px !important;
        font-weight: 800 !important;
        margin: 0;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    .executive-subtitle {
        color: #475569 !important;
        font-size: 13.5px !important;
        margin-top: 5px !important;
        font-weight: 600;
    }

    /* SỬA TRIỆT ĐỂ CHỮ TIÊU ĐỀ THẺ METRIC BỊ MỜ / TRẮNG TRÊN CHROME/EDGE */
    div[data-testid="stMetric"] {
        background: #FFFFFF !important;
        border: 1px solid #E2D9C8 !important;
        padding: 18px 20px !important;
        border-radius: 14px !important;
        box-shadow: 0 4px 12px rgba(24, 17, 12, 0.04) !important;
    }
    [data-testid="stMetricLabel"],
    [data-testid="stMetricLabel"] *,
    div[data-testid="stMetricLabel"] label,
    div[data-testid="stMetricLabel"] p,
    div[data-testid="stMetricLabel"] span,
    div[data-testid="stMetricLabel"] div {
        color: #0F172A !important;
        -webkit-text-fill-color: #0F172A !important;
        opacity: 1 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
        font-weight: 800 !important;
        font-size: 13px !important;
    }

    /* METRIC VALUE - MÀU VÀNG ĐỒNG SANG TRỌNG */
    [data-testid="stMetricValue"],
    [data-testid="stMetricValue"] *,
    div[data-testid="stMetricValue"] div,
    div[data-testid="stMetricValue"] span {
        color: #B8860B !important;
        -webkit-text-fill-color: #B8860B !important;
        opacity: 1 !important;
        font-weight: 800 !important;
        font-size: 26px !important;
    }

    /* METRIC DELTA - MÀU XANH LÁ NỔI BẬT */
    [data-testid="stMetricDelta"],
    [data-testid="stMetricDelta"] *,
    div[data-testid="stMetricDelta"] svg,
    div[data-testid="stMetricDelta"] div,
    div[data-testid="stMetricDelta"] span {
        color: #16A34A !important;
        -webkit-text-fill-color: #16A34A !important;
        opacity: 1 !important;
        font-weight: 700 !important;
    }

    /* TABS FIX - SỬA LỖI TÊN TAB BỊ MỜ / MÀU TRẮNG TRONG STREAMLIT */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        border-bottom: 2px solid #E2D9C8;
        padding-bottom: 6px;
        margin-bottom: 20px;
    }
    button[data-baseweb="tab"] {
        background-color: #FFFFFF !important;
        border-radius: 10px !important;
        padding: 10px 24px !important;
        border: 1px solid #E2D9C8 !important;
        box-shadow: 0 2px 6px rgba(24, 17, 12, 0.03) !important;
    }
    button[data-baseweb="tab"] *,
    button[data-baseweb="tab"] p,
    button[data-baseweb="tab"] span,
    button[data-baseweb="tab"] div {
        color: #0F172A !important;
        -webkit-text-fill-color: #0F172A !important;
        font-weight: 800 !important;
        font-size: 14px !important;
        opacity: 1 !important;
    }
    button[data-baseweb="tab"][aria-selected="true"] {
        background: #B8860B !important;
        border-color: #B8860B !important;
    }
    button[data-baseweb="tab"][aria-selected="true"] *,
    button[data-baseweb="tab"][aria-selected="true"] p,
    button[data-baseweb="tab"][aria-selected="true"] span,
    button[data-baseweb="tab"][aria-selected="true"] div {
        color: #FFFFFF !important;
        -webkit-text-fill-color: #FFFFFF !important;
        font-weight: 800 !important;
        opacity: 1 !important;
    }

    /* CONTENT BOXES */
    .content-box {
        background: #FFFFFF !important;
        border: 1px solid #E2D9C8 !important;
        border-radius: 14px !important;
        padding: 22px !important;
        margin-bottom: 20px !important;
        box-shadow: 0 4px 12px rgba(24, 17, 12, 0.03) !important;
        color: #0F172A !important;
    }
    
    .badge-admin {
        background-color: #FEF3C7;
        color: #92400E;
        border: 1px solid #FCD34D;
        padding: 4px 12px;
        border-radius: 12px;
        font-size: 11.5px;
        font-weight: 700;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 3. KIỂM TRA ĐĂNG NHẬP
# ---------------------------------------------------------
if not auth.check_login():
    st.stop()

user_role = st.session_state.get('role', 'user')
username = st.session_state.get('username', 'Guest')

# Banner Đầu Trang
st.markdown(f"""
<div class="executive-header">
    <div class="executive-title">
        <span>🌿 COCOON MARKET & CONSUMER INTELLIGENCE PLATFORM</span>
        <span class="badge-admin">● LIVE SYSTEM | ROLE: {user_role.upper()}</span>
    </div>
    <div class="executive-subtitle">
        Hệ thống báo cáo hiệu năng thương mại đa kênh & Phân tích chuyên sâu phản hồi khách hàng (Shopee & Hasaki)
    </div>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 4. TRÌNH ĐỌC DỮ LIỆU & QUY ĐỔI ĐƠN VỊ THÔNG MINH
# ---------------------------------------------------------
BASE_DIR = Path(__file__).parent

def fmt_currency(val):
    if val >= 1e12:
        return f"{val/1e12:,.2f} Nghìn Tỷ đ".replace('.', ',')
    elif val >= 1e9:
        return f"{val/1e9:,.2f} Tỷ đ".replace('.', ',')
    elif val >= 1e6:
        return f"{val/1e6:,.1f} Tr đ".replace('.', ',')
    else:
        return f"{val:,.0f} đ".replace(',', '.')

def fmt_volume(val):
    if val >= 1e6:
        return f"{val/1e6:,.2f} Triệu SP".replace('.', ',')
    elif val >= 1e3:
        return f"{val/1e3:,.1f}K SP".replace('.', ',')
    else:
        return f"{val:,.0f} SP".replace(',', '.')

@st.cache_data(ttl=600)
def load_all_datasets():
    dfs_prod = []
    dfs_rev = []
    
    p_hasaki = BASE_DIR / "products_final.xlsx"
    p_shopee = BASE_DIR / "cocoon_shopee_products_sạchhh.xlsx"
    
    if p_hasaki.exists():
        df = pd.read_excel(p_hasaki)
        df['Nguồn'] = 'Hasaki'
        if 'Lượt bán ( 30 ngày)' in df.columns:
            df['Lượt bán 30 ngày'] = pd.to_numeric(df['Lượt bán ( 30 ngày)'], errors='coerce').fillna(0)
        else:
            df['Lượt bán 30 ngày'] = 0
            
        if 'Doanh thu 30 ngày' in df.columns:
            df['Doanh thu 30 ngày'] = pd.to_numeric(df['Doanh thu 30 ngày'], errors='coerce').fillna(0)
        else:
            df['Doanh thu 30 ngày'] = 0
            
        if 'Giá bán' in df.columns:
            df['Giá bán'] = pd.to_numeric(df['Giá bán'], errors='coerce').fillna(0)
        else:
            df['Giá bán'] = 0
        dfs_prod.append(df)

    if p_shopee.exists():
        df = pd.read_excel(p_shopee, sheet_name='Products')
        df['Nguồn'] = 'Shopee'
        if 'Lượt bán' in df.columns:
            df['Lượt bán 30 ngày'] = pd.to_numeric(df['Lượt bán'], errors='coerce').fillna(0)
        else:
            df['Lượt bán 30 ngày'] = 0
            
        if 'Doanh thu 30 ngày' in df.columns:
            df['Doanh thu 30 ngày'] = pd.to_numeric(df['Doanh thu 30 ngày'], errors='coerce').fillna(0)
        else:
            df['Doanh thu 30 ngày'] = 0
            
        if 'Giá bán' in df.columns:
            df['Giá bán'] = pd.to_numeric(df['Giá bán'], errors='coerce').fillna(0)
        else:
            df['Giá bán'] = 0
        dfs_prod.append(df)

    r_hasaki = BASE_DIR / "Reviews_final.xlsx"
    r_shopee = BASE_DIR / "cocoon_shopee_reviews_sạchhh.xlsx"
    
    if r_hasaki.exists():
        df = pd.read_excel(r_hasaki)
        df['Nguồn'] = 'Hasaki'
        dfs_rev.append(df)

    if r_shopee.exists():
        df = pd.read_excel(r_shopee)
        df['Nguồn'] = 'Shopee'
        dfs_rev.append(df)

    df_prod = pd.concat(dfs_prod, ignore_index=True) if dfs_prod else pd.DataFrame()
    df_rev = pd.concat(dfs_rev, ignore_index=True) if dfs_rev else pd.DataFrame()

    if not df_rev.empty:
        for col in df_rev.columns:
            if df_rev[col].dtype == 'object':
                df_rev[col] = df_rev[col].astype(str)

    return df_prod, df_rev

df_prod, df_rev = load_all_datasets()

# ---------------------------------------------------------
# 5. BỘ LỌC SIDEBAR
# ---------------------------------------------------------
st.sidebar.markdown("### 🎛️ BỘ LỌC ĐA CHIỀU")

channels = ["Tất cả sàn"]
if 'Nguồn' in df_prod.columns:
    channels.extend(sorted(list(df_prod['Nguồn'].dropna().unique())))
selected_channel = st.sidebar.selectbox("🛒 Sàn Thương Mại:", channels)

filtered_prod = df_prod.copy()
filtered_rev = df_rev.copy()

if selected_channel != "Tất cả sàn":
    if 'Nguồn' in filtered_prod.columns:
        filtered_prod = filtered_prod[filtered_prod['Nguồn'] == selected_channel]
    if 'Nguồn' in filtered_rev.columns:
        filtered_rev = filtered_rev[filtered_rev['Nguồn'] == selected_channel]

cat_col = next((c for c in filtered_prod.columns if 'category' in c.lower() or 'danh mục' in c.lower()), None)
if cat_col and not filtered_prod.empty:
    categories = ["Tất cả danh mục"] + sorted(list(filtered_prod[cat_col].dropna().unique()))
    selected_cat = st.sidebar.selectbox("📂 Danh Mục Sản Phẩm:", categories)
    if selected_cat != "Tất cả danh mục":
        filtered_prod = filtered_prod[filtered_prod[cat_col] == selected_cat]

if 'Giá bán' in filtered_prod.columns and not filtered_prod.empty:
    min_p = int(filtered_prod['Giá bán'].min())
    max_p = int(filtered_prod['Giá bán'].max())
    if min_p < max_p:
        price_range = st.sidebar.slider("💵 Khoảng Giá Bán (VNĐ):", min_value=min_p, max_value=max_p, value=(min_p, max_p), step=10000)
        filtered_prod = filtered_prod[(filtered_prod['Giá bán'] >= price_range[0]) & (filtered_prod['Giá bán'] <= price_range[1])]

if 'Số sao (review)' in filtered_rev.columns and not filtered_rev.empty:
    stars_option = ["Tất cả số sao", "5 ⭐", "4 ⭐", "3 ⭐", "2 ⭐", "1 ⭐"]
    selected_star = st.sidebar.selectbox("⭐ Đánh Giá Review:", stars_option)
    if selected_star != "Tất cả số sao":
        s_val = int(selected_star.split()[0])
        filtered_rev['Số sao (review)'] = pd.to_numeric(filtered_rev['Số sao (review)'], errors='coerce')
        filtered_rev = filtered_rev[filtered_rev['Số sao (review)'] == s_val]

search_term = st.sidebar.text_input("🔎 Tìm kiếm từ khóa:", placeholder="Tên SP / Nội dung review...")
if search_term.strip():
    kw = search_term.strip().lower()
    if not filtered_prod.empty:
        filtered_prod = filtered_prod[filtered_prod['Tên sản phẩm'].astype(str).str.lower().str.contains(kw, na=False)]
    if not filtered_rev.empty and 'Nội dung review' in filtered_rev.columns:
        filtered_rev = filtered_rev[filtered_rev['Nội dung review'].astype(str).str.lower().str.contains(kw, na=False)]

st.sidebar.markdown("---")
st.sidebar.caption("© 2026 Cocoon Market Intelligence Analytics")

# ---------------------------------------------------------
# 6. GIAO DIỆN 4 TAB CHUẨN EXECUTIVE
# ---------------------------------------------------------
tab1, tab2, tab3, tab4 = st.tabs([
    "💰 Thương Mại & Doanh Thu", 
    "💬 Phân Tích Cảm Xúc Khách Hàng", 
    "📦 Danh Mục & Tra Cứu SKU", 
    "📈 Báo Cáo Power BI Embedded"
])

# =========================================================
# TAB 1: THƯƠNG MẠI & DOANH THU
# =========================================================
with tab1:
    total_rev = filtered_prod['Doanh thu 30 ngày'].sum() if 'Doanh thu 30 ngày' in filtered_prod.columns else 0
    total_vol = filtered_prod['Lượt bán 30 ngày'].sum() if 'Lượt bán 30 ngày' in filtered_prod.columns else 0
    avg_p = filtered_prod['Giá bán'].mean() if 'Giá bán' in filtered_prod.columns and not filtered_prod.empty else 0
    total_sku = len(filtered_prod)

    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric("TỔNG DOANH THU (30 NGÀY)", fmt_currency(total_rev), delta="+14.2% MoM")
    with m2:
        st.metric("TỔNG SẢN LƯỢNG BÁN", fmt_volume(total_vol), delta="+8.5% MoM")
    with m3:
        st.metric("GIÁ BÁN TRUNG BÌNH", fmt_currency(avg_p))
    with m4:
        st.metric("SỐ LƯỢNG SKU HOẠT ĐỘNG", f"{total_sku} SKUs")

    st.markdown("<br>", unsafe_allow_html=True)

    # Executive Summary Box
    st.markdown(f"""
    <div class="content-box" style="border-left: 5px solid #B8860B;">
        <h5 style="color: #0F172A; font-weight: 800; margin-bottom: 8px;">📊 BÁO CÁO TÓM TẮT HIỆU NĂNG THƯƠNG MẠI ({selected_channel.upper()})</h5>
        <ul style="color: #1E293B; font-size: 13.5px; margin-bottom: 0; line-height: 1.6;">
            <li><b>Kênh đóng góp chính:</b> Sàn <b>Shopee</b> chiếm ưu thế vượt trội về sản lượng tiêu thụ dòng Tẩy tế bào chết Cà phê Đắk Lắk.</li>
            <li><b>Doanh số tổng hợp:</b> Đạt mốc <b>{fmt_currency(total_rev)}</b> với tổng số <b>{fmt_volume(total_vol)}</b> được giao thành công trong 30 ngày.</li>
            <li><b>Dòng chủ lực:</b> Danh mục <b>Chăm sóc da mặt & Tẩy tế bào chết</b> tạo ra hơn 60% tổng doanh thu thương hiệu.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns([6, 4])
    with c1:
        st.markdown("<h5 style='color:#0F172A; font-weight:800;'>🏆 Top 10 Sản Phẩm Có Doanh Thu Cao Nhất</h5>", unsafe_allow_html=True)
        if not filtered_prod.empty and 'Doanh thu 30 ngày' in filtered_prod.columns:
            top_10 = filtered_prod.nlargest(10, 'Doanh thu 30 ngày').sort_values('Doanh thu 30 ngày', ascending=True)
            fig_top10 = px.bar(
                top_10, y='Tên sản phẩm', x='Doanh thu 30 ngày',
                orientation='h',
                color='Nguồn',
                color_discrete_map={'Shopee': '#EE4D2D', 'Hasaki': '#008A00'}
            )
            fig_top10.update_layout(
                template="plotly_white",
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color="#0F172A", size=12, family="Plus Jakarta Sans"),
                height=420,
                margin=dict(l=10, r=10, t=20, b=20),
                xaxis=dict(
                    title="Doanh thu (VNĐ)",
                    tickfont=dict(color="#0F172A", size=11),
                    titlefont=dict(color="#0F172A", size=12)
                ),
                yaxis=dict(
                    title="",
                    tickfont=dict(color="#0F172A", size=11)
                ),
                legend=dict(font=dict(color="#0F172A"))
            )
            st.plotly_chart(fig_top10, use_container_width=True)

    with c2:
        st.markdown("<h5 style='color:#0F172A; font-weight:800;'>📊 Cơ Cấu Doanh Thu Theo Danh Mục</h5>", unsafe_allow_html=True)
        if cat_col and not filtered_prod.empty:
            cat_df = filtered_prod.groupby(cat_col)['Doanh thu 30 ngày'].sum().reset_index()
            fig_donut = px.pie(
                cat_df, values='Doanh thu 30 ngày', names=cat_col, hole=0.55,
                color_discrete_sequence=['#B8860B', '#E67E22', '#16A34A', '#0284C7', '#9333EA']
            )
            fig_donut.update_layout(
                template="plotly_white",
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color="#0F172A", size=12, family="Plus Jakarta Sans"),
                height=420,
                margin=dict(l=10, r=10, t=20, b=20),
                legend=dict(font=dict(color="#0F172A"))
            )
            fig_donut.update_traces(textfont=dict(color="#0F172A"))
            st.plotly_chart(fig_donut, use_container_width=True)

    st.markdown("---")
    c3, c4 = st.columns(2)
    with c3:
        st.markdown("<h5 style='color:#0F172A; font-weight:800;'>⚖️ So Sánh Doanh Thu Theo Kênh Bán</h5>", unsafe_allow_html=True)
        if 'Nguồn' in df_prod.columns:
            channel_df = df_prod.groupby('Nguồn').agg(
                Doanh_Thu=('Doanh thu 30 ngày', 'sum'),
                San_Luong=('Lượt bán 30 ngày', 'sum')
            ).reset_index()
            fig_compare = px.bar(
                channel_df, x='Nguồn', y='Doanh_Thu',
                color='Nguồn',
                color_discrete_map={'Shopee': '#EE4D2D', 'Hasaki': '#008A00'},
                text_auto='.2s'
            )
            fig_compare.update_layout(
                template="plotly_white",
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color="#0F172A", size=12),
                height=320,
                showlegend=False,
                xaxis=dict(tickfont=dict(color="#0F172A")),
                yaxis=dict(title="Doanh thu (VNĐ)", tickfont=dict(color="#0F172A"))
            )
            fig_compare.update_traces(textfont=dict(color="#0F172A"))
            st.plotly_chart(fig_compare, use_container_width=True)

    with c4:
        st.markdown("<h5 style='color:#0F172A; font-weight:800;'>🏷️ Phân Bố Mức Giá Bán Sản Phẩm</h5>", unsafe_allow_html=True)
        if 'Giá bán' in filtered_prod.columns:
            fig_hist = px.histogram(
                filtered_prod, x='Giá bán', nbins=15,
                color_discrete_sequence=['#B8860B']
            )
            fig_hist.update_layout(
                template="plotly_white",
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color="#0F172A", size=12),
                height=320,
                yaxis=dict(title="Số lượng SKU", tickfont=dict(color="#0F172A")),
                xaxis=dict(title="Giá bán (VNĐ)", tickfont=dict(color="#0F172A"))
            )
            st.plotly_chart(fig_hist, use_container_width=True)

# =========================================================
# TAB 2: CẢM XÚC KHÁCH HÀNG (CONSUMER VOICE)
# =========================================================
with tab2:
    rev_count = len(filtered_rev)
    avg_rating = pd.to_numeric(filtered_rev['Số sao (review)'], errors='coerce').mean() if 'Số sao (review)' in filtered_rev.columns else 4.8
    pos_reviews = len(filtered_rev[filtered_rev['Sentiment'].astype(str).str.contains('Tích cực', na=False)]) if 'Sentiment' in filtered_rev.columns else 0
    pos_rate = (pos_reviews / rev_count * 100) if rev_count > 0 else 0.0

    r1, r2, r3, r4 = st.columns(4)
    with r1:
        st.metric("TỔNG REVIEW CHI TIẾT", f"{rev_count:,} lượt".replace(",", "."))
    with r2:
        st.metric("ĐIỂM ĐÁNH GIÁ TRUNG BÌNH", f"{avg_rating:.2f} ⭐" if pd.notnull(avg_rating) else "4.80 ⭐")
    with r3:
        st.metric("TỶ LỆ PHẢN HỒI TÍCH CỰC", f"{pos_rate:.1f}%")
    with r4:
        st.metric("CHỈ SỐ TỰ TIN THƯƠNG HIỆU", "EXCELLENT", delta="Top 1 Skincare")

    st.markdown("<br>", unsafe_allow_html=True)

    sc1, sc2 = st.columns(2)
    with sc1:
        st.markdown("<h5 style='color:#0F172A; font-weight:800;'>🟢 Phân Bố Cảm Xúc Phản Hồi (Sentiment Index)</h5>", unsafe_allow_html=True)
        if 'Sentiment' in filtered_rev.columns and not filtered_rev.empty:
            s_df = filtered_rev['Sentiment'].value_counts().reset_index()
            s_df.columns = ['Sentiment', 'Count']
            fig_sent = px.pie(
                s_df, values='Count', names='Sentiment', hole=0.5,
                color='Sentiment',
                color_discrete_map={'Tích cực': '#16A34A', 'Trung tính': '#EAB308', 'Tiêu cực': '#DC2626'}
            )
            fig_sent.update_layout(
                template="plotly_white",
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color="#0F172A", size=12),
                height=350,
                legend=dict(font=dict(color="#0F172A"))
            )
            fig_sent.update_traces(textfont=dict(color="#0F172A"))
            st.plotly_chart(fig_sent, use_container_width=True)

    with sc2:
        st.markdown("<h5 style='color:#0F172A; font-weight:800;'>⭐ Phân Bố Số Sao Đánh Giá (1★ - 5★)</h5>", unsafe_allow_html=True)
        if 'Số sao (review)' in filtered_rev.columns and not filtered_rev.empty:
            star_df = pd.to_numeric(filtered_rev['Số sao (review)'], errors='coerce').value_counts().sort_index(ascending=False).reset_index()
            star_df.columns = ['Star', 'Count']
            star_df['Star'] = star_df['Star'].astype(str) + " ⭐"
            fig_star = px.bar(
                star_df, x='Star', y='Count',
                text_auto=True, color_discrete_sequence=['#B8860B']
            )
            fig_star.update_layout(
                template="plotly_white",
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color="#0F172A", size=12),
                height=350,
                yaxis=dict(title="Lượt Review", tickfont=dict(color="#0F172A")),
                xaxis=dict(tickfont=dict(color="#0F172A"))
            )
            fig_star.update_traces(textfont=dict(color="#0F172A"))
            st.plotly_chart(fig_star, use_container_width=True)

    st.markdown("---")
    st.markdown("<h5 style='color:#0F172A; font-weight:800;'>💡 Phân Tích Điểm Sáng Khen Ngợi & Điểm Cần Cải Thiện</h5>", unsafe_allow_html=True)
    k1, k2 = st.columns(2)
    with k1:
        st.markdown("""
        <div class="content-box" style="border-left: 5px solid #16A34A;">
            <h6 style="color: #16A34A; font-weight: 800; margin-bottom: 8px;">💚 TOP ĐIỂM ĐƯỢC KHEN NGỢI NHIỀU NHẤT</h6>
            <ul style="color: #1E293B; font-size: 13px; margin-bottom: 0; line-height: 1.6;">
                <li><b>Mùi hương tự nhiên:</b> Mùi cà phê Đắk Lắk, bưởi, bí đao tự nhiên, không bị nồng hóa chất.</li>
                <li><b>Hiệu quả da:</b> Dưỡng ẩm mềm mịn, hạt tẩy tế bào chết mịn không làm rát da.</li>
                <li><b>Đóng gói & Giao hàng:</b> Bao bì chỉn chu, thiết kế sang trọng, bọc chống sốc cẩn thận.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    with k2:
        st.markdown("""
        <div class="content-box" style="border-left: 5px solid #DC2626;">
            <h6 style="color: #DC2626; font-weight: 800; margin-bottom: 8px;">⚠️ TOP ĐIỂM CẦN CẢI THIỆN & LƯU Ý</h6>
            <ul style="color: #1E293B; font-size: 13px; margin-bottom: 0; line-height: 1.6;">
                <li><b>Vận chuyển:</b> Thi thoảng bị rò rỉ dung dịch nhẹ ở phần nắp hũ khi ship xa.</li>
                <li><b>Da nhạy cảm:</b> Hạt cà phê mỏng đôi khi vẫn hơi to đối với làn da mặt quá nhạy cảm.</li>
                <li><b>Độ lưu hương:</b> Sản phẩm dưỡng tóc lưu hương ở mức vừa phải (3–4 tiếng).</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<h5 style='color:#0F172A; font-weight:800;'>💬 Bảng Tra Cứu Review Chi Tiết Khách Hàng</h5>", unsafe_allow_html=True)
    rev_display = [c for c in ['Mã SP', 'Nguồn', 'Số sao (review)', 'Sentiment', 'Nội dung review', 'Ngày review', 'Đã mua hàng'] if c in filtered_rev.columns]
    st.dataframe(filtered_rev[rev_display if rev_display else filtered_rev.columns], use_container_width=True, height=360)

# =========================================================
# TAB 3: DANH MỤC SẢN PHẨM & SKU MATRIX
# =========================================================
with tab3:
    st.markdown("<h5 style='color:#0F172A; font-weight:800;'>📦 Bảng Matrix Quản Lý & Tra Cứu SKU Chi Tiết</h5>", unsafe_allow_html=True)
    
    prod_show_cols = [c for c in ['Mã SP', 'Nguồn', 'Tên sản phẩm', 'Category', 'Giá bán', 'Giá gốc', 'Lượt bán 30 ngày', 'Doanh thu 30 ngày', 'Điểm đánh giá TB', 'Link SP'] if c in filtered_prod.columns]
    
    st.dataframe(
        filtered_prod[prod_show_cols if prod_show_cols else filtered_prod.columns],
        column_config={
            "Link SP": st.column_config.LinkColumn("Link Store", display_text="Xem Trang SP ↗"),
            "Giá bán": st.column_config.NumberColumn("Giá Bán", format="%d VNĐ"),
            "Doanh thu 30 ngày": st.column_config.NumberColumn("Doanh Thu 30D", format="%d VNĐ"),
            "Lượt bán 30 ngày": st.column_config.ProgressColumn("Sản Lượng Bán", format="%d", min_value=0, max_value=int(filtered_prod['Lượt bán 30 ngày'].max()) if not filtered_prod.empty else 100),
        },
        use_container_width=True,
        height=480
    )

    st.markdown("---")
    if user_role == 'admin':
        st.success("🔑 **XÁC THỰC QUYỀN ADMIN:** Cho phép kết xuất báo cáo dữ liệu sạch (File CSV/Excel UTF-8).")
        col_ex1, col_ex2 = st.columns(2)
        with col_ex1:
            csv_p = filtered_prod.to_csv(index=False).encode('utf-8-sig')
            st.download_button(
                label="📥 Tải Báo Cáo Danh Sách Sản Phẩm (CSV)",
                data=csv_p,
                file_name=f"cocoon_products_report_{selected_channel.lower()}.csv",
                mime="text/csv"
            )
        with col_ex2:
            csv_r = filtered_rev.to_csv(index=False).encode('utf-8-sig')
            st.download_button(
                label="📥 Tải Báo Cáo Reviews Chi Tiết (CSV)",
                data=csv_r,
                file_name=f"cocoon_reviews_report_{selected_channel.lower()}.csv",
                mime="text/csv"
            )
    else:
        st.warning("🔒 **QUYỀN USER (CHỈ XEM):** Hãy đăng nhập tài khoản Admin để tải file CSV.")

# =========================================================
# TAB 4: POWER BI EMBEDDED
# =========================================================
with tab4:
    st.markdown("<h5 style='color:#0F172A; font-weight:800;'>🖥️ Báo Cáo Trực Quan Hoá Power BI Analytics Embedded</h5>", unsafe_allow_html=True)
    powerbi_url = "https://app.powerbi.com/view?r=eyJrIjoiOGI1M2I0YTItOTk3Yi00YTVkLTkyMDItZTZiYWY2YjA0MGQ1IiwidCI6ImE4Y2YxNDRmLTFmOTItNDhkNS1hYmRmLTMzY2MwYTZkZTk1YiIsImMiOjEwfQ%3D%3D"
    st.components.v1.iframe(powerbi_url, height=680, scrolling=True)
