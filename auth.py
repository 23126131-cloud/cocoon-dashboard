import streamlit as st

def check_login():
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False

    if not st.session_state["logged_in"]:
        st.sidebar.title("🔐 Đăng nhập hệ thống")
        username = st.sidebar.text_input("Tên đăng nhập")
        password = st.sidebar.text_input("Mật khẩu", type="password")
        login_btn = st.sidebar.button("Đăng nhập")

        if login_btn:
            if username == "admin" and password == "admin123":
                st.session_state["logged_in"] = True
                st.session_state["username"] = "admin"
                st.session_state["role"] = "admin"
                st.rerun()
            elif username == "user" and password == "user123":
                st.session_state["logged_in"] = True
                st.session_state["username"] = "user"
                st.session_state["role"] = "user"
                st.rerun()
            else:
                st.sidebar.error("Sai tài khoản hoặc mật khẩu!")
        return False
    
    if st.sidebar.button("Đăng xuất"):
        st.session_state.clear()
        st.rerun()
    return True
