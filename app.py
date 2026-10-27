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
# 2. BỘ CSS BẢN SÁNG ĐỘ TƯƠNG PHẢN CAO (EXECUTIVE LIGHT MODE)
# ---------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }

    /* Force Light Background */
    .stApp {
        background-color: #f8fafc !important;
        color: #0f172a !important;
    }

    /* Sidebar - Dark Navy Style */
    div[data-testid="stSidebar"] {
        background-color: #0f172a !important;
        border-right: 1px solid #1e293b;
    }
    div[data-testid="stSidebar"] * {
        color: #f8fafc !important;
    }
    div[data-testid="stSidebar"] .stSelectbox label, 
    div[data-testid="stSidebar"] .stSlider label,
    div[data-testid="stSidebar"] .stTextInput label {
        color: #cbd5e1 !important;
        font-weight: 700 !important;
        font-size: 13px !important;
    }
    div[data-testid="stSidebar"] input, 
    div[data-testid="stSidebar"] div[data-baseweb="select"] {
        background-color: #1e293b !important;
        color: #ffffff !important;
        border-radius: 8px !important;
        border: 1px solid #334155 !important;
    }

    /* Executive Header Banner */
    .executive-header {
        background: #ffffff;
        border: 1px solid #cbd5e1;
        border-left: 6px solid #d4af37;
        padding: 22px 28px;
        border-radius: 14px;
        margin-bottom: 22px;
        box-shadow: 0 4px 15px rgba(15, 23, 42, 0.04);
    }
    .executive-title {
        color: #0f172a !important;
        font-size: 24px !important;
        font-weight: 800 !important;
        letter-spacing: -0.5px;
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

    /* METRIC CARDS - TỐI ƯU HIỂN THỊ CHỮ TÊN CHỈ SỐ ĐEN ĐẬM 100% */
    div[data-testid="stMetric"] {
        background: #ffffff !important;
        border: 1px solid #cbd5e1 !important;
        padding: 18px 20px !important;
        border-radius: 14px !important;
        box-shadow: 0 4px 12px rgba(15, 23, 42, 0.04) !important;
    }
    div[data-testid="stMetricLabel"],
    div[data-testid="stMetricLabel"] *,
    div[data-testid="stMetricLabel"] p {
        font-size: 13px !important;
        color: #0f172a !important; /* ĐEN ĐẬM SẮC NẾT HOÀN TOÀN */
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
        font-weight: 800 !important;
    }
    div[data-testid="stMetricValue"],
    div[data-testid="stMetricValue"] * {
        font-size: 26px !important;
        font-weight: 800 !important;
        color: #b8860b !important;
    }

    /* TABS - MÀU CHỮ RÕ NÉT CẢ TAB ĐANG CHỌN & CHƯA CHỌN */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        border-bottom: 2px solid #cbd5e1;
        padding-bottom: 6px;
        margin-bottom: 20px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #ffffff !important;
        border-radius: 10px !important;
        padding: 10px 24px !important;
        border: 1px solid #cbd5e1 !important;
        box-shadow: 0 2px 6px rgba(15, 23, 42, 0.03) !important;
    }
    .stTabs [data-baseweb="tab"] *,
    .stTabs [data-baseweb="tab"] p {
        color: #1e293b !important; /* MÀU CHỮ TAB CHƯA CHỌN: ĐEN XÁM ĐẬM RÕ NÉT */
        font-weight: 700 !important;
        font-size: 14px !important;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #d4af37 0%, #b8860b 100%) !important;
        border-color: #d4af37 !important;
    }
    .stTabs [aria-selected="true"] *,
    .stTabs [aria-selected="true"] p {
        color: #ffffff !important; /* MÀU CHỮ TAB ĐANG CHỌN: TRẮNG TINH */
        font-weight: 800 !important;
    }

    /* CONTENT BOXES */
    .content-box {
        background: #ffffff !important;
        border: 1px solid #cbd5e1 !important;
        border-radius: 14px !important;
        padding: 22px !important;
        margin-bottom: 20px !important;
        box-shadow: 0 4px 12px rgba(15, 23, 42, 0.03) !important;
        color: #0f172a !important;
    }
    
    .badge-admin {
        background-color: #fef3c7;
        color: #92400e;
        border: 1px solid #fcd34d;
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
        try:
            df = pd.read_excel(p_hasaki)
            df['Nguồn'] = 'Hasaki'
            df['Lượt bán 30 ngày'] = pd.to_numeric
