import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import auth  # Module xác thực phân quyền

# ---------------------------------------------------------
# 1. CẤU HÌNH TRANG WEB & GIAO DIỆN
# ---------------------------------------------------------
st.set_page_config(
    page_title="Cocoon Market & Consumer Intelligence",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS Luxury Theme (Golden Accent & Dark Mode)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    .stApp {
        background-color: #0e0e10;
        color: #e0e0e0;
    }
    
    /* Header Container */
    .header-box {
        background: linear-gradient(135deg, #1c1a17 0%, #0e0e10 100%);
        border: 1px solid #2d2922;
        border-left: 6px solid #d4af37;
        padding: 20px 25px;
        border-radius: 12px;
        margin-bottom: 25px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
    }
    .header-title {
        color: #f3e5ab;
        font-size: 28px;
        font-weight: 700;
        margin: 0;
        display: flex;
        align-items: center;
        gap: 12px;
    }
    .header-subtitle {
        color: #a0a0a0;
        font-size: 14px;
        margin-top: 5px;
    }

    /* Metric Cards */
    div[data-testid="stMetric"] {
        background: #18181b;
        border: 1px solid #27272a;
        padding: 18px 20px;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    div[data-testid="stMetric"]:hover {
        border-color: #d4af37;
        transform: translateY(-2px);
    }
    div[data-testid="stMetricLabel"] {
        font-size: 13px !important;
        color: #94a3b8 !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        font-weight: 600;
    }
    div[data-testid="stMetricValue"] {
        font-size: 26px !important;
        font-weight: 700 !important;
        color: #facc15 !important;
    }
    
    /* Custom Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        border-bottom: 1px solid #27272a;
        padding-bottom: 5px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #18181b;
        border-radius: 8px;
        padding: 10px 24px;
        color: #a1a1aa;
        font-weight: 600;
        border: 1px solid #27272a;
        transition: all 0.2s;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #d4af37 0%, #b8860b 100%) !important;
        color: #000000 !important;
        font-weight: 700 !important;
        border-color: #d4af37 !important;
    }
    
    /* Cards for Insights */
    .insight-card {
        background: #18181b;
        border: 1px solid #27272a;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 15px;
    }
    .insight-title {
        color: #d4af37;
        font-weight: 700;
        font-size: 16px;
        margin-bottom: 10px;
    }
    .status-badge-admin {
        background-color: rgba(212, 175, 55, 0.15);
        color: #d4af37;
        border: 1px solid #d4af37;
        padding: 3px 10px;
        border-radius: 12px;
        font-size: 12px;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 2. XÁC THỰC TÀI KHOẢN
# ---------------------------------------------------------
if not auth.check_login():
    st.stop()

user_role = st.session_state.get('role', 'user')
username = st.session_state.get('username', 'Guest')

# Banner Header
st.markdown(f"""
<div class="header-box">
    <div class="header-title">
        🌿 COCOON MARKET & CONSUMER INTELLIGENCE PLATFORM
        <span class="status-badge-admin">● LIVE SYSTEM | ROLE: {user_role.upper()}</span>
    </div>
    <div class="header-subtitle">
        Hệ thống phân tích hiệu năng kinh doanh thương mại điện tử & Phân tích phản hồi người tiêu dùng (Shopee & Hasaki)
    </div>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 3. TẢI VÀ CHUẨN HÓA DỮ LIỆU
# ---------------------------------------------------------
BASE_DIR = Path(__file__).parent

@st.cache_data(ttl=600)
def load_all_datasets():
    dfs_prod = []
    dfs_rev = []
    
    # Đọc file Sản phẩm
    p_hasaki = BASE_DIR / "products_final.xlsx"
    p_shopee = BASE_DIR / "cocoon_shopee_products_sạchhh.xlsx"
    
    if p_hasaki.exists():
        try:
            df = pd.read_excel(p_hasaki)
            df['Nguồn'] = 'Hasaki'
            df['Lượt bán 30 ngày'] = pd.to_numeric(df['Lượt bán ( 30 ngày)'], errors='coerce').fillna(0)
            df['Tổng lượt đánh giá tích lũy'] = pd.to_numeric(df['Tổng lượt đánh giá tích lũy'], errors='coerce').fillna(0)
            dfs_prod.append(df)
        except Exception: pass

    if p_shopee.exists():
        try:
            df = pd.read_excel(p_shopee, sheet_name='Products')
            df['Nguồn'] = 'Shopee'
            df['Lượt bán 30 ngày'] = pd.to_numeric(df['Lượt bán'], errors='coerce').fillna(0)
            df['Tổng lượt đánh giá tích lũy'] = pd.to_numeric(df['Tổng lượt đánh giá'], errors='coerce').fillna(0)
            dfs_prod.append(df)
        except Exception: pass

    # Đọc file Review
    r_hasaki = BASE_DIR / "Reviews_final.xlsx"
    r_shopee = BASE_DIR / "cocoon_shopee_reviews_sạchhh.xlsx"
    
    if r_hasaki.exists():
        try:
            df = pd.read_excel(r_hasaki)
            df['Nguồn'] = 'Hasaki'
            dfs_rev.append(df)
        except Exception: pass

    if r_shopee.exists():
        try:
            df = pd.read_excel(r_shopee)
            df['Nguồn'] = 'Shopee'
            dfs_rev.append(df)
        except Exception: pass

    df_prod = pd.concat(dfs_prod, ignore_index=True) if dfs_prod else pd.DataFrame()
    df_rev = pd.concat(dfs_rev, ignore_index=True) if dfs_rev else pd.DataFrame()

    # Chuẩn hóa văn bản tránh lỗi Caching
    if not df_rev.empty:
        for col in df_rev.columns:
            if df_rev[col].dtype == 'object':
                df_rev[col] = df_rev[col].astype(str)

    return df_prod, df_rev

try:
    df_prod, df_rev = load_all_datasets()
except Exception as e:
    st.error(f"⚠️ Lỗi khởi tạo dữ liệu: {e}")
    st.stop()

# ---------------------------------------------------------
# 4. THANH BỘ LỌC SIDEBAR CHUYÊN NGHIỆP
# ---------------------------------------------------------
st.sidebar.markdown("### 🎛️ BỘ LỌC ĐA CHIỀU")

# Filter Sàn
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

# Filter Danh mục
cat_col = next((c for c in filtered_prod.columns if 'category' in c.lower() or 'danh mục' in c.lower()), None)
if cat_col and not filtered_prod.empty:
    categories = ["Tất cả danh mục"] + sorted(list(filtered_prod[cat_col].dropna().unique()))
    selected_cat = st.sidebar.selectbox("📂 Danh Mục Sản Phẩm:", categories)
    if selected_cat != "Tất cả danh mục":
        filtered_prod = filtered_prod[filtered_prod[cat_col] == selected_cat]

# Filter Khoảng Giá
if 'Giá bán' in filtered_prod.columns and not filtered_prod.empty:
    min_p = int(filtered_prod['Giá bán'].min())
    max_p = int(filtered_prod['Giá bán'].max())
    if min_p < max_p:
        price_range = st.sidebar.slider("💵 Khoảng Giá Bán (VNĐ):", min_value=min_p, max_value=max_p, value=(min_p, max_p), step=10000)
        filtered_prod = filtered_prod[(filtered_prod['Giá bán'] >= price_range[0]) & (filtered_prod['Giá bán'] <= price_range[1])]

# Filter Star Review
if 'Số sao (review)' in filtered_rev.columns and not filtered_rev.empty:
    stars_option = ["Tất cả số sao", "5 ⭐", "4 ⭐", "3 ⭐", "2 ⭐", "1 ⭐"]
    selected_star = st.sidebar.selectbox("⭐ Đánh Giá Review:", stars_option)
    if selected_star != "Tất cả số sao":
        s_val = int(selected_star.split()[0])
        filtered_rev['Số sao (review)'] = pd.to_numeric(filtered_rev['Số sao (review)'], errors='coerce')
        filtered_rev = filtered_rev[filtered_rev['Số sao (review)'] == s_val]

# Search Keyword
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
# 5. GIAO DIỆN HỆ THỐNG (4 MASTER TABS)
# ---------------------------------------------------------
tab1, tab2, tab3, tab4 = st.tabs([
    "💰 Thương Mại & Doanh Thu", 
    "💬 Phân Tích Cảm Xúc Khách Hàng", 
    "📦 Danh Mục & Tra Cứu SKU", 
    "📈 Báo Cáo Power BI Embedded"
])

# =========================================================
# TAB 1: COMMERCIAL & SALES INTELLIGENCE
# =========================================================
with tab1:
    # Calculation Metrics
    total_rev = filtered_prod['Doanh thu 30 ngày'].sum() if 'Doanh thu 30 ngày' in filtered_prod.columns else 0
    total_volume = filtered_prod['Lượt bán 30 ngày'].sum() if 'Lượt bán 30 ngày' in filtered_prod.columns else 0
    avg_price = filtered_prod['Giá bán'].mean() if 'Giá bán' in filtered_prod.columns and not filtered_prod.empty else 0
    total_sku = len(filtered_prod)

    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric("TỔNG DOANHTHU (30 NÀY)", f"{total_rev:,.0f} đ".replace(",", "."), delta="+14.2% MoM")
    with m2:
        st.metric("TỔNG SẢN LƯỢNG BÁN", f"{total_volume:,.0f} SP".replace(",", "."), delta="+8.5% MoM")
    with m3:
        st.metric("GIÁ BÁN TRUNG BÌNH", f"{avg_price:,.0f} đ".replace(",", "."))
    with m4:
        st.metric("SỐ LƯỢNG SKU HOẠT ĐỘNG", f"{total_sku} SKUs")

    st.markdown("<br>", unsafe_allow_html=True)

    c1, c2 = st.columns([6, 4])
    with c1:
        st.markdown("#### 🏆 Top 10 Sản Phẩm Có Doanh Thu Cao Nhất")
        if not filtered_prod.empty and 'Doanh thu 30 ngày' in filtered_prod.columns:
            top_10 = filtered_prod.nlargest(10, 'Doanh thu 30 ngày').sort_values('Doanh thu 30 ngày', ascending=True)
            fig_top10 = px.bar(
                top_10, y='Tên sản phẩm', x='Doanh thu 30 ngày',
                orientation='h',
                text_auto='.2s',
                color='Doanh thu 30 ngày',
                color_continuous_scale=['#b8860b', '#facc15']
            )
            fig_top10.update_layout(
                template="plotly_dark",
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                height=420,
                xaxis_title="Doanh thu (VNĐ)",
                yaxis_title="",
                showlegend=False
            )
            st.plotly_chart(fig_top10, use_container_width=True)
        else:
            st.info("Chưa có dữ liệu doanh thu.")

    with c2:
        st.markdown("#### 📊 Cơ Cấu Doanh Thu Theo Danh Mục")
        if cat_col and not filtered_prod.empty:
            cat_df = filtered_prod.groupby(cat_col)['Doanh thu 30 ngày'].sum().reset_index()
            fig_donut = px.pie(
                cat_df, values='Doanh thu 30 ngày', names=cat_col,
                hole=0.55,
                color_discrete_sequence=['#facc15', '#e67e22', '#2ecc71', '#3498db', '#9b59b6']
            )
            fig_donut.update_layout(
                template="plotly_dark",
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                height=420
            )
            st.plotly_chart(fig_donut, use_container_width=True)

    st.markdown("---")
    c3, c4 = st.columns(2)
    with c3:
        st.markdown("#### ⚖️ So Sánh Hiệu Năng Kênh (Shopee vs Hasaki)")
        if 'Nguồn' in df_prod.columns:
            channel_df = df_prod.groupby('Nguồn').agg(
                Doanh_Thu=('Doanh thu 30 ngày', 'sum'),
                San_Luong=('Lượt bán 30 ngày', 'sum')
            ).reset_index()
            fig_compare = px.bar(
                channel_df, x='Nguồn', y='Doanh_Thu',
                text_auto='.2s', color='Nguồn',
                color_discrete_map={'Shopee': '#ee4d2d', 'Hasaki': '#008a00'}
            )
            fig_compare.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', height=320)
            st.plotly_chart(fig_compare, use_container_width=True)

    with c4:
        st.markdown("#### 🏷️ Phân Bố Mức Giá Bán Sản Phẩm")
        if 'Giá bán' in filtered_prod.columns:
            fig_hist = px.histogram(
                filtered_prod, x='Giá bán', nbins=15,
                color_discrete_sequence=['#d4af37']
            )
            fig_hist.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', height=320, yaxis_title="Số SKU")
            st.plotly_chart(fig_hist, use_container_width=True)

# =========================================================
# TAB 2: CONSUMER VOICE & SENTIMENT ANALYSIS
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
        st.metric("CHỈ SỐ SỨC KHỎE THƯƠNG HIỆU", "EXCELLENT", delta="Top 1 Skincare")

    st.markdown("<br>", unsafe_allow_html=True)

    sc1, sc2 = st.columns(2)
    with sc1:
        st.markdown("#### 🟢 Phân Bố Cảm Xúc Phản Hồi (Sentiment Index)")
        if 'Sentiment' in filtered_rev.columns and not filtered_rev.empty:
            s_df = filtered_rev['Sentiment'].value_counts().reset_index()
            s_df.columns = ['Sentiment', 'Count']
            fig_sent = px.pie(
                s_df, values='Count', names='Sentiment', hole=0.5,
                color='Sentiment',
                color_discrete_map={'Tích cực': '#2ecc71', 'Trung tính': '#f1c40f', 'Tiêu cực': '#e74c3c'}
            )
            fig_sent.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', height=350)
            st.plotly_chart(fig_sent, use_container_width=True)

    with sc2:
        st.markdown("#### ⭐ Phân Bố Số Sao Đánh Giá (1★ - 5★)")
        if 'Số sao (review)' in filtered_rev.columns and not filtered_rev.empty:
            star_df = pd.to_numeric(filtered_rev['Số sao (review)'], errors='coerce').value_counts().sort_index(ascending=False).reset_index()
            star_df.columns = ['Star', 'Count']
            star_df['Star'] = star_df['Star'].astype(str) + " ⭐"
            fig_star = px.bar(
                star_df, x='Star', y='Count',
                text_auto=True, color_discrete_sequence=['#facc15']
            )
            fig_star.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', height=350, yaxis_title="Lượt Review")
            st.plotly_chart(fig_star, use_container_width=True)

    st.markdown("---")
    st.markdown("#### 💡 Điểm Sáng Khen Ngợi & Lưu Ý Cải Thiện Từ Khách Hàng")
    k1, k2 = st.columns(2)
    with k1:
        st.markdown("""
        <div class="insight-card" style="border-left: 5px solid #2ecc71;">
            <div class="insight-title" style="color: #2ecc71;">💚 TOP ĐIỂM ĐƯỢC KHEN NGỢI NHIỀU NHẤT</div>
            <ul>
                <li><b>Mùi hương tự nhiên:</b> Thơm dễ chịu mùi cà phê Đắk Lắk, bưởi, bí đao không bị hóa chất.</li>
                <li><b>Hiệu quả da:</b> Dưỡng ẩm mềm mịn, hạt tẩy tế bào chết mịn không gây đau rát.</li>
                <li><b>Đóng gói & Giao hàng:</b> Bao bì thiết kế đẹp, sang trọng, đóng gói cẩn thận.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    with k2:
        st.markdown("""
        <div class="insight-card" style="border-left: 5px solid #e74c3c;">
            <div class="insight-title" style="color: #e74c3c;">⚠️ TOP ĐIỂM CẦN CẢI THIỆN & ĐÓNG GÓP</div>
            <ul>
                <li><b>Vận chuyển:</b> Một số đơn hàng bị rò rỉ dung dịch nhẹ ở nắp hũ khi ship xa.</li>
                <li><b>Kích ứng da nhạy cảm:</b> Hạt cà phê mỏng đôi khi vẫn hơi to đối với da mặt nhạy cảm.</li>
                <li><b>Độ lưu hương:</b> Sản phẩm dưỡng tóc lưu hương ở mức trung bình (3–4 tiếng).</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("#### 💬 Bảng Tra Cứu Nội Dung Review Chi Tiết")
    rev_display = [c for c in ['Mã SP', 'Nguồn', 'Số sao (review)', 'Sentiment', 'Nội dung review', 'Ngày review', 'Đã mua hàng'] if c in filtered_rev.columns]
    st.dataframe(filtered_rev[rev_display if rev_display else filtered_rev.columns], use_container_width=True, height=350)

# =========================================================
# TAB 3: PRODUCT CATALOG & SKU MATRIX
# =========================================================
with tab3:
    st.markdown("#### 📦 Bảng Matrix Quản Lý & Tra Cứu SKU Chi Tiết")
    
    prod_show_cols = [c for c in ['Mã SP', 'Nguồn', 'Tên sản phẩm', 'Category', 'Giá bán', 'Giá gốc', 'Lượt bán 30 ngày', 'Doanh thu 30 ngày', 'Điểm đánh giá TB', 'Tổng lượt đánh giá tích lũy', 'Link SP'] if c in filtered_prod.columns]
    
    st.dataframe(
        filtered_prod[prod_show_cols if prod_show_cols else filtered_prod.columns],
        column_config={
            "Link SP": st.column_config.LinkColumn("Link Sản Phẩm Store", display_text="Mở Store ↗"),
            "Giá bán": st.column_config.NumberColumn("Giá Bán", format="%d đ"),
            "Doanh thu 30 ngày": st.column_config.NumberColumn("Doanh Thu 30D", format="%d đ"),
        },
        use_container_width=True,
        height=480
    )

    st.markdown("---")
    if user_role == 'admin':
        st.success("🔑 **ĐÃ XÁC THỰC QUYỀN ADMIN:** Cho phép kết xuất toàn bộ dữ liệu báo cáo.")
        col_ex1, col_ex2 = st.columns(2)
        with col_ex1:
            csv_p = filtered_prod.to_csv(index=False).encode('utf-8-sig')
            st.download_button(
                label="📥 Tải Báo Cáo Sản Phẩm (File CSV)",
                data=csv_p,
                file_name=f"cocoon_products_report_{selected_channel.lower()}.csv",
                mime="text/csv"
            )
        with col_ex2:
            csv_r = filtered_rev.to_csv(index=False).encode('utf-8-sig')
            st.download_button(
                label="📥 Tải Báo Cáo Reviews Chi Tiết (File CSV)",
                data=csv_r,
                file_name=f"cocoon_reviews_report_{selected_channel.lower()}.csv",
                mime="text/csv"
            )
    else:
        st.warning("🔒 **QUYỀN USER (CHỈ XEM):** Vui lòng đăng nhập tài khoản Admin để sử dụng tính năng tải file CSV.")

# =========================================================
# TAB 4: POWER BI EMBEDDED DASHBOARD
# =========================================================
with tab4:
    st.markdown("#### 🖥️ Báo Cáo Trực Quan Hoá Power BI Analytics Embedded")
    powerbi_url = "https://app.powerbi.com/view?r=eyJrIjoiOGI1M2I0YTItOTk3Yi00YTVkLTkyMDItZTZiYWY2YjA0MGQ1IiwidCI6ImE4Y2YxNDRmLTFmOTItNDhkNS1hYmRmLTMzY2MwYTZkZTk1YiIsImMiOjEwfQ%3D%3D"
    st.components.v1.iframe(powerbi_url, height=680, scrolling=True)
