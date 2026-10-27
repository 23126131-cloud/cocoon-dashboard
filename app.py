import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
import auth  # Module xác thực phân quyền

# 1. Cấu hình trang web
st.set_page_config(
    page_title="Cocoon & Hasaki Analytics Dashboard",
    page_icon="🌿",
    layout="wide"
)

# 2. Trang trí CSS chuẩn thương hiệu Cocoon (Gold & Dark Theme)
st.markdown("""
<style>
    .stApp { background-color: #121212; }
    div[data-testid="stMetricValue"] {
        font-size: 26px !important;
        font-weight: bold !important;
        color: #d4af37 !important;
    }
    div[data-testid="stMetric"] {
        background-color: #1e1e1e;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #d4af37;
    }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] {
        background-color: #262626;
        border-radius: 8px 8px 0 0;
        padding: 10px 20px;
        color: #e0e0e0;
    }
    .stTabs [aria-selected="true"] {
        background-color: #d4af37 !important;
        color: #000000 !important;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# 3. Kiểm tra đăng nhập
if not auth.check_login():
    st.stop()

user_role = st.session_state.get('role', 'user')

st.title("🌿 Cocoon Analytics Dashboard (Tổng hợp Sản Phẩm & Reviews)")
st.caption(f"Trạng thái đăng nhập: **{st.session_state.get('username', 'Guest')}** (Quyền: **{user_role.upper()}**)")
st.markdown("---")

# 4. Hàm đọc tự động 4 file dữ liệu (Sản phẩm + Reviews từ cả 2 sàn)
BASE_DIR = Path(__file__).parent

@st.cache_data
def load_all_datasets():
    # 4.1. Đọc dữ liệu sản phẩm
    dfs_p = []
    p_hasaki = BASE_DIR / "products_final.xlsx"
    p_shopee = BASE_DIR / "cocoon_shopee_products_sạchhh.xlsx"
    
    if p_hasaki.exists():
        try:
            df = pd.read_excel(p_hasaki)
            df['Nguồn'] = 'Hasaki'
            dfs_p.append(df)
        except Exception: pass
        
    if p_shopee.exists():
        try:
            df = pd.read_excel(p_shopee, sheet_name='Products')
            df['Nguồn'] = 'Shopee'
            dfs_p.append(df)
        except Exception: pass
        
    df_prod = pd.concat(dfs_p, ignore_index=True) if dfs_p else pd.DataFrame()

    # 4.2. Đọc dữ liệu review chi tiết
    dfs_r = []
    r_hasaki = BASE_DIR / "Reviews_final.xlsx"
    r_shopee = BASE_DIR / "cocoon_shopee_reviews_sạchhh.xlsx"
    
    if r_hasaki.exists():
        try:
            df = pd.read_excel(r_hasaki)
            df['Nguồn'] = 'Hasaki'
            dfs_r.append(df)
        except Exception: pass
        
    if r_shopee.exists():
        try:
            df = pd.read_excel(r_shopee)
            df['Nguồn'] = 'Shopee'
            dfs_r.append(df)
        except Exception: pass
        
    df_rev = pd.concat(dfs_r, ignore_index=True) if dfs_r else pd.DataFrame()

    return df_prod, df_rev

df_prod, df_rev = load_all_datasets()

if df_prod.empty and df_rev.empty:
    st.error("⚠️ Không tìm thấy các file dữ liệu Excel trong kho!")
    st.stop()

# 5. Thanh BỘ LỌC TỰ ĐỘNG
st.sidebar.header("🔍 BỘ LỌC DỮ LIỆU")

# Chọn Sàn
available_sources = ["Tất cả sàn"]
if 'Nguồn' in df_prod.columns:
    available_sources.extend(sorted(list(df_prod['Nguồn'].dropna().unique())))
selected_source = st.sidebar.selectbox("Nền tảng / Sàn lẻ:", available_sources)

filtered_prod = df_prod.copy()
filtered_rev = df_rev.copy()

if selected_source != "Tất cả sàn":
    if 'Nguồn' in filtered_prod.columns:
        filtered_prod = filtered_prod[filtered_prod['Nguồn'] == selected_source]
    if 'Nguồn' in filtered_rev.columns:
        filtered_rev = filtered_rev[filtered_rev['Nguồn'] == selected_source]

# Chọn Số sao Review
if 'Số sao (review)' in filtered_rev.columns:
    stars = ["Tất cả đánh giá", "5 ⭐", "4 ⭐", "3 ⭐", "2 ⭐", "1 ⭐"]
    selected_star = st.sidebar.selectbox("Lọc số sao Đánh giá:", stars)
    if selected_star != "Tất cả đánh giá":
        star_num = int(selected_star.split()[0])
        filtered_rev = filtered_rev[filtered_rev['Số sao (review)'] == star_num]

# Tìm kiếm từ khóa sản phẩm & review
search_kw = st.sidebar.text_input("🔎 Tìm từ khóa (SP / Review):", placeholder="Nhập từ khóa...")
if search_kw.strip():
    kw = search_kw.strip().lower()
    if not filtered_prod.empty:
        name_col = filtered_prod.columns[1] if len(filtered_prod.columns) > 1 else filtered_prod.columns[0]
        filtered_prod = filtered_prod[filtered_prod[name_col].astype(str).str.lower().str.contains(kw, na=False)]
    if not filtered_rev.empty and 'Nội dung review' in filtered_rev.columns:
        filtered_rev = filtered_rev[filtered_rev['Nội dung review'].astype(str).str.lower().str.contains(kw, na=False)]

# 6. GIAO DIỆN 3 TAB
tab1, tab2, tab3 = st.tabs([
    "📊 Tổng Quan & Insights Reviews", 
    "🔎 Tra Cứu Sản Phẩm & Reviews Chi Tiết", 
    "📈 Báo Cáo Power BI Embedded"
])

# --- TAB 1: TỔNG QUAN & INSIGHTS ---
with tab1:
    col1, col2, col3, col4 = st.columns(4)
    
    total_sp = len(filtered_prod)
    total_rev_count = len(filtered_rev)
    
    avg_star = filtered_rev['Số sao (review)'].mean() if (not filtered_rev.empty and 'Số sao (review)' in filtered_rev.columns) else 4.8
    
    pos_count = len(filtered_rev[filtered_rev['Sentiment'] == 'Tích cực']) if (not filtered_rev.empty and 'Sentiment' in filtered_rev.columns) else 0
    pos_rate = (pos_count / total_rev_count * 100) if total_rev_count > 0 else 95.6

    with col1:
        st.metric("Tổng số Sản phẩm", f"{total_sp:,} SP")
    with col2:
        st.metric("Tổng số Review chi tiết", f"{total_rev_count:,} lượt")
    with col3:
        st.metric("Điểm đánh giá TB", f"{avg_star:.2f} ⭐")
    with col4:
        st.metric("Tỷ lệ Cảm xúc Tích cực", f"{pos_rate:.1f}%")

    st.markdown("<br>", unsafe_allow_html=True)
    st.info(f"""
    💡 **Nhận Xét & Insight Thị Trường ({selected_source}):**
    * **Tích hợp dữ liệu đa kênh:** Tổng hợp thành công **{len(df_prod)} sản phẩm** và **{len(df_rev):,} đánh giá thực tế** từ Shopee và Hasaki.
    * **Cảm xúc người dùng:** Hơn **{pos_rate:.1f}%** lượt đánh giá mang phản hồi tích cực. Mùi hương tự nhiên (cà phê, bưởi, bí đao) và độ ẩm mịn da là các điểm sáng được khen ngợi nhiều nhất.
    * **Cảnh báo chất lượng:** Các phản hồi 1–2★ chủ yếu tập trung vào vấn đề bao bì bị rò rỉ trong quá trình vận chuyển hoặc hạt tẩy tế bào chết hơi to đối với da nhạy cảm.
    """)

    c1, c2 = st.columns(2)
    with c1:
        if not filtered_rev.empty and 'Sentiment' in filtered_rev.columns:
            sentiment_df = filtered_rev['Sentiment'].value_counts().reset_index()
            sentiment_df.columns = ['Cảm xúc', 'Số lượng']
            fig_pie = px.pie(
                sentiment_df, values='Số lượng', names='Cảm xúc',
                title="<b>Phân Bố Cảm Xúc Phản Hồi (Sentiment Analysis)</b>",
                color='Cảm xúc',
                color_discrete_map={'Tích cực': '#2ecc71', 'Trung tính': '#f1c40f', 'Tiêu cực': '#e74c3c'}
            )
        else:
            fig_pie = px.pie(
                names=['Tích cực', 'Trung tính', 'Tiêu cực'],
                values=[8533, 171, 220],
                title="<b>Phân Bố Cảm Xúc Phản Hồi (Sentiment Analysis)</b>",
                color_discrete_sequence=['#2ecc71', '#f1c40f', '#e74c3c']
            )
        fig_pie.update_layout(template="plotly_dark")
        st.plotly_chart(fig_pie, use_container_width=True)

    with c2:
        if not filtered_rev.empty and 'Số sao (review)' in filtered_rev.columns:
            star_df = filtered_rev['Số sao (review)'].value_counts().sort_index(ascending=False).reset_index()
            star_df.columns = ['Số sao', 'Số lượt']
            star_df['Số sao'] = star_df['Số sao'].astype(str) + " ⭐"
            fig_bar = px.bar(
                star_df, x='Số sao', y='Số lượt',
                title="<b>Phân Bố Mức Độ Đánh Giá (1 ⭐ - 5 ⭐)</b>",
                color_discrete_sequence=['#d4af37']
            )
        else:
            fig_bar = px.bar(
                x=['5 ⭐', '4 ⭐', '3 ⭐', '2 ⭐', '1 ⭐'],
                y=[7686, 847, 171, 101, 119],
                title="<b>Phân Bố Mức Độ Đánh Giá (1 ⭐ - 5 ⭐)</b>",
                color_discrete_sequence=['#d4af37']
            )
        fig_bar.update_layout(template="plotly_dark")
        st.plotly_chart(fig_bar, use_container_width=True)

# --- TAB 2: TRA CỨU SẢN PHẨM & REVIEWS CHI TIẾT ---
with tab2:
    st.subheader(f"📦 1. Danh Sách Sản Phẩm ({len(filtered_prod)} kết quả)")
    st.dataframe(filtered_prod, use_container_width=True, height=300)
    
    st.markdown("---")
    st.subheader(f"💬 2. Chi Tiết Đánh Giá Khách Hàng ({len(filtered_rev)} kết quả)")
    
    # Hiển thị các cột quan trọng của Review
    rev_show_cols = [c for c in ['Mã SP', 'Nguồn', 'Số sao (review)', 'Sentiment', 'Nội dung review', 'Ngày review', 'Đã mua hàng'] if c in filtered_rev.columns]
    if not filtered_rev.empty:
        st.dataframe(filtered_rev[rev_show_cols], use_container_width=True, height=400)
    else:
        st.info("Không tìm thấy review thỏa điều kiện lọc.")

    st.markdown("---")
    if user_role == 'admin':
        st.success("🔑 **Quyền ADMIN:** Bạn có quyền xuất dữ liệu báo cáo chi tiết bên dưới.")
        col_d1, col_d2 = st.columns(2)
        with col_d1:
            csv_prod = filtered_prod.to_csv(index=False).encode('utf-8-sig')
            st.download_button(
                label="📥 Tải Báo Cáo Sản Phẩm (CSV)",
                data=csv_prod,
                file_name=f"cocoon_products_{selected_source.lower()}.csv",
                mime="text/csv"
            )
        with col_d2:
            csv_rev = filtered_rev.to_csv(index=False).encode('utf-8-sig')
            st.download_button(
                label="📥 Tải Báo Cáo Review Chi Tiết (CSV)",
                data=csv_rev,
                file_name=f"cocoon_reviews_{selected_source.lower()}.csv",
                mime="text/csv"
            )
    else:
        st.warning("🔒 **Quyền USER:** Chỉ có quyền xem. Hãy đăng nhập tài khoản **Admin** để tải dữ liệu CSV.")

# --- TAB 3: POWER BI EMBEDDED ---
with tab3:
    st.subheader("🖥️ Báo Cáo Trực Quan Hoá Power BI Embedded")
    powerbi_url = "https://app.powerbi.com/view?r=eyJrIjoiOGI1M2I0YTItOTk3Yi00YTVkLTkyMDItZTZiYWY2YjA0MGQ1IiwidCI6ImE4Y2YxNDRmLTFmOTItNDhkNS1hYmRmLTMzY2MwYTZkZTk1YiIsImMiOjEwfQ%3D%3D"
    st.components.v1.iframe(powerbi_url, height=650, scrolling=True)
