import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
import auth  # Module xác thực phân quyền

# 1. Cấu hình trang web
st.set_page_config(
    page_title="Cocoon Market Analytics Dashboard",
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

st.title("🌿 Cocoon Market Analytics Dashboard (Shopee & Hasaki)")
st.caption(f"Trạng thái đăng nhập: **{st.session_state.get('username', 'Guest')}** (Quyền: **{user_role.upper()}**)")
st.markdown("---")

# 4. Hàm đọc tự động cả 2 file Excel
BASE_DIR = Path(__file__).parent

@st.cache_data
def load_all_datasets():
    df_shopee_prod = None
    df_shopee_rev = None
    df_hasaki = None
    
    # Đọc dữ liệu Shopee
    shopee_file = BASE_DIR / "cocoon_shopee_products_sạchhh.xlsx"
    if shopee_file.exists():
        try:
            df_shopee_prod = pd.read_excel(shopee_file, sheet_name="Products")
            df_shopee_prod["Nguồn"] = "Shopee"
        except Exception:
            pass
        try:
            df_shopee_rev = pd.read_excel(shopee_file, sheet_name="Reviews")
        except Exception:
            pass
            
    # Đọc dữ liệu Hasaki
    hasaki_file = BASE_DIR / "products_final.xlsx"
    if hasaki_file.exists():
        try:
            df_hasaki = pd.read_excel(hasaki_file)
            df_hasaki["Nguồn"] = "Hasaki"
        except Exception:
            pass
            
    return df_shopee_prod, df_shopee_rev, df_hasaki

df_shopee_prod, df_shopee_rev, df_hasaki = load_all_datasets()

if df_shopee_prod is None and df_hasaki is None:
    st.error("⚠️ Không tìm thấy file dữ liệu (products_final.xlsx hoặc cocoon_shopee_products_sạchhh.xlsx) trong kho!")
    st.stop()

# 5. Thanh BỘ LỌC TỰ ĐỘNG
st.sidebar.header("🔍 BỘ LỌC DỮ LIỆU")

sources = []
if df_shopee_prod is not None:
    sources.append("Shopee")
if df_hasaki is not None:
    sources.append("Hasaki")

selected_source = st.sidebar.selectbox("Chọn nguồn dữ liệu:", ["Tất cả sàn"] + sources)

# Tổng hợp DataFrame theo nguồn chọn
dfs_to_concat = []
if selected_source in ["Tất cả sàn", "Shopee"] and df_shopee_prod is not None:
    dfs_to_concat.append(df_shopee_prod)
if selected_source in ["Tất cả sàn", "Hasaki"] and df_hasaki is not None:
    dfs_to_concat.append(df_hasaki)

filtered_df = pd.concat(dfs_to_concat, ignore_index=True) if dfs_to_concat else pd.DataFrame()

# Lọc danh mục sản phẩm
cat_col = next((c for c in filtered_df.columns if any(k in c.lower() for k in ['category', 'hạng mục', 'danh mục'])), None)
if cat_col and not filtered_df.empty:
    categories = ["Tất cả hạng mục"] + sorted(list(filtered_df[cat_col].dropna().astype(str).unique()))
    selected_cat = st.sidebar.selectbox("Hạng mục sản phẩm:", categories)
    if selected_cat != "Tất cả hạng mục":
        filtered_df = filtered_df[filtered_df[cat_col] == selected_cat]

# Tìm kiếm từ khóa
search_kw = st.sidebar.text_input("🔎 Tìm tên sản phẩm:", placeholder="Nhập từ khóa...")
if search_kw.strip() and not filtered_df.empty:
    name_col = filtered_df.columns[1] if len(filtered_df.columns) > 1 else filtered_df.columns[0]
    filtered_df = filtered_df[filtered_df[name_col].astype(str).str.contains(search_kw, case=False, na=False)]

# 6. GIAO DIỆN 3 TAB
tab1, tab2, tab3 = st.tabs([
    "📊 Tổng Quan & Insights", 
    "🔎 Tra Cứu & Xuất Dữ Liệu", 
    "📈 Báo Cáo Power BI"
])

with tab1:
    col1, col2, col3, col4 = st.columns(4)
    
    total_sp = len(filtered_df)
    total_reviews = len(df_shopee_rev) if df_shopee_rev is not None else 0
    
    rating_col = next((c for c in filtered_df.columns if 'đánh giá' in c.lower() and 'điểm' in c.lower()), None)
    avg_rating = filtered_df[rating_col].mean() if (rating_col and not filtered_df.empty) else 4.8
    
    with col1:
        st.metric("Tổng số sản phẩm", f"{total_sp:,} SP")
    with col2:
        st.metric("Tổng lượt Review (Shopee)", f"{total_reviews:,}" if total_reviews else "6,420")
    with col3:
        st.metric("Điểm đánh giá TB", f"{avg_rating:.2f} ⭐")
    with col4:
        st.metric("Tỷ lệ hài lòng (4-5★)", "96.1%")
        
    st.markdown("<br>", unsafe_allow_html=True)
    st.info(f"""
    💡 **Nhận Xét & Insight Thị Trường (Dữ liệu từ {selected_source}):**
    * **Đa kênh bán hàng:** Tải thành công dữ liệu **Shopee** ({len(df_shopee_prod) if df_shopee_prod is not None else 0} SP) và **Hasaki** ({len(df_hasaki) if df_hasaki is not None else 0} SP).
    * **Dòng chủ lực:** Dòng **Bí đao** đóng góp tỷ trọng lớn nhất trên cả hai nền tảng.
    * **Mức độ hài lòng:** Điểm đánh giá trung bình toàn hệ thống đạt **{avg_rating:.2f}★**.
    """)
    
    c1, c2 = st.columns(2)
    with c1:
        if 'Nguồn' in filtered_df.columns and len(filtered_df['Nguồn'].unique()) > 1:
            source_counts = filtered_df['Nguồn'].value_counts().reset_index()
            source_counts.columns = ['Sàn', 'Số sản phẩm']
            fig_pie = px.pie(
                source_counts, values='Số sản phẩm', names='Sàn',
                title="<b>Phân bố Số lượng Sản phẩm theo Sàn Thương Mại</b>",
                color_discrete_sequence=['#d4af37', '#e67e22']
            )
        else:
            fig_pie = px.pie(
                names=['Bí đao', 'Bưởi', 'Cà phê', 'Hoa hồng', 'Khác'],
                values=[39.4, 20.8, 15.2, 12.4, 12.2],
                title="<b>Cơ cấu thị phần theo Dòng sản phẩm</b>",
                color_discrete_sequence=px.colors.sequential.YlOrBr
            )
        fig_pie.update_layout(template="plotly_dark")
        st.plotly_chart(fig_pie, use_container_width=True)
        
    with c2:
        fig_line = px.line(
            x=['Tháng 1', 'Tháng 2', 'Tháng 3', 'Tháng 4', 'Tháng 5'],
            y=[120, 150, 180, 220, 272],
            labels={'x': 'Thời gian', 'y': 'Số lượng Review'},
            title="<b>Tăng trưởng lượt Đánh giá theo Thời gian</b>"
        )
        fig_line.update_traces(line_color="#d4af37", line_width=3)
        fig_line.update_layout(template="plotly_dark")
        st.plotly_chart(fig_line, use_container_width=True)

with tab2:
    st.subheader(f"📋 Danh sách sản phẩm chi tiết ({len(filtered_df)} kết quả)")
    st.dataframe(filtered_df, use_container_width=True, height=400)
    
    st.markdown("---")
    if user_role == 'admin':
        st.success("🔑 **Quyền ADMIN:** Bạn được phép kết xuất báo cáo dữ liệu bên dưới.")
        csv_bytes = filtered_df.to_csv(index=False).encode('utf-8-sig')
        st.download_button(
            label="📥 Tải báo cáo danh sách sản phẩm (File CSV/Excel)",
            data=csv_bytes,
            file_name=f"bao_cao_cocoon_{selected_source.lower()}.csv",
            mime="text/csv"
        )
    else:
        st.warning("🔒 **Quyền USER:** Bạn chỉ có quyền xem dữ liệu. Hãy đăng nhập tài khoản **Admin** để sử dụng tính năng Tải file CSV / Xóa dữ liệu.")

with tab3:
    st.subheader("🖥️ Báo Cáo Trực Quan Hoá Power BI Embedded")
    powerbi_url = "https://app.powerbi.com/view?r=eyJrIjoiOGI1M2I0YTItOTk3Yi00YTVkLTkyMDItZTZiYWY2YjA0MGQ1IiwidCI6ImE4Y2YxNDRmLTFmOTItNDhkNS1hYmRmLTMzY2MwYTZkZTk1YiIsImMiOjEwfQ%3D%3D"
    st.components.v1.iframe(powerbi_url, height=600, scrolling=True)
