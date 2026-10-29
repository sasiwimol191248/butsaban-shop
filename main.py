import streamlit as st
import datetime
import math
import random

# ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="Butsaban - ร้านดอกไม้ลวดกำมะหยี่", page_icon="🌹", layout="wide")

# ฟังก์ชันดึงเวลาปัจจุบันของประเทศไทย (UTC+7) และแปลงปีเป็น พ.ศ.
def get_thai_time():
    thai_time = datetime.datetime.utcnow() + datetime.timedelta(hours=7)
    day = thai_time.strftime("%d/%m")
    year_be = thai_time.year + 543
    time_str = thai_time.strftime("%H:%M:%S")
    return f"{day}/{year_be} {time_str}"

# ตกแต่ง CSS
st.markdown("""
    <style>
    html, body, [class*="css"] {
        font-size: 18px !important;
    }
    .product-card {
        padding: 25px;
        border-radius: 16px;
        border: 1px solid #333;
        background-color: #161616;
        box-shadow: 0 6px 15px rgba(0,0,0,0.4);
        text-align: center;
        margin-bottom: 20px;
    }
    .product-title {
        font-size: 26px !important;
        font-weight: bold;
        color: #ff6b6b;
        margin-bottom: 10px;
    }
    .product-desc {
        font-size: 16px !important;
        color: #ccc;
        min-height: 45px;
    }
    .product-price {
        font-size: 24px !important;
        color: #ff8787;
        font-weight: bold;
        margin: 15px 0;
    }

    div.stButton > button[kind="secondary"] {
        width: 100% !important;
        background-color: #e03131 !important;
        color: white !important;
        border-radius: 10px !important;
        font-weight: bold !important;
        border: none !important;
        padding: 0.7rem !important;
        font-size: 18px !important;
    }
    div.stButton > button[kind="secondary"] p {
        color: white !important;
        font-size: 18px !important;
    }
    div.stButton > button[kind="secondary"]:hover {
        background-color: #c92a2a !important;
    }

    div.stButton > button[kind="primary"] {
        width: 100% !important;
        background-color: #2b8a3e !important;
        color: white !important;
        border-radius: 10px !important;
        font-weight: bold !important;
        border: none !important;
        padding: 0.7rem !important;
        font-size: 18px !important;
    }
    div.stButton > button[kind="primary"] p {
        color: white !important;
        font-size: 18px !important;
    }
    div.stButton > button[kind="primary"]:hover {
        background-color: #237032 !important;
    }

    .section-box {
        background-color: #181818;
        padding: 30px;
        border-radius: 16px;
        border: 1px solid #2c2c2c;
        box-shadow: 0 8px 30px rgba(0,0,0,0.5);
        margin-top: 30px;
        margin-bottom: 30px;
    }
    .section-header {
        font-size: 26px !important;
        font-weight: 700 !important;
        color: #ff8787 !important;
        margin-bottom: 20px !important;
        border-bottom: 2px solid #333;
        padding-bottom: 10px;
    }
    
    .stRadio label {
        font-size: 22px !important;
        font-weight: bold !important;
        color: #ffffff !important;
    }
    .stRadio div[role="radiogroup"] label p {
        font-size: 20px !important;
        color: #ffffff !important;
    }
    </style>
""", unsafe_allow_html=True)

# 1. กำหนดค่าเริ่มต้นระบบ (Session State)
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "is_admin" not in st.session_state:
    st.session_state.is_admin = False
if "cart" not in st.session_state:
    st.session_state.cart = {}
# อัปเดตรหัสผ่านแอดมินเป็น 12345600
if "registered_users" not in st.session_state:
    st.session_state.registered_users = {"admin": "12345600", "ใบไผ่": "112233", "customer01": "password"}
if "orders_db" not in st.session_state:
    st.session_state.orders_db = []

# ==========================================
# 2. หน้าล็อกอิน และ สมัครสมาชิก
# ==========================================
if not st.session_state.logged_in:
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1.4, 1])
    with col2:
        st.markdown("<h2 style='text-align: center; color: #ff6b6b; margin-bottom: 10px; font-size: 38px;'>🌹 ร้าน Butsaban</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #aaa; font-size: 18px; margin-bottom: 20px;'>ระบบสั่งซื้อและจองดอกไม้ลวดกำมะหยี่แฮนด์เมด</p>", unsafe_allow_html=True)
        
        tab_login, tab_reg = st.tabs(["🔑 เข้าสู่ระบบ", "📝 สมัครสมาชิกใหม่"])
        
        with tab_login:
            with st.form("login_form"):
                l_user = st.text_input("ชื่อผู้ใช้งาน (Username)")
                l_pass = st.text_input("รหัสผ่าน (Password)", type="password")
                submit_login = st.form_submit_button("🚀 เข้าสู่ระบบ")
                
                if submit_login:
                    if l_user in st.session_state.registered_users and st.session_state.registered_users[l_user] == l_pass:
                        st.session_state.logged_in = True
                        st.session_state.username = l_user
                        st.session_state.is_admin = (l_user == "admin")
                        st.success("เข้าสู่ระบบสำเร็จ!")
                        st.rerun()
                    else:
                        st.error("⚠️ ชื่อผู้ใช้งานหรือรหัสผ่านไม่ถูกต้อง")

        with tab_reg:
            with st.form("reg_form"):
                r_user = st.text_input("กำหนดชื่อผู้ใช้งาน (Username)")
                r_pass = st.text_input("กำหนดรหัสผ่าน (Password)", type="password")
                submit_reg = st.form_submit_button("✨ สมัครสมาชิก")
                
                if submit_reg:
                    if r_user != "" and r_pass != "":
                        if r_user in st.session_state.registered_users:
                            st.error("⚠️ ชื่อผู้ใช้งานนี้มีคนใช้
