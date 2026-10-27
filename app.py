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

# 5
