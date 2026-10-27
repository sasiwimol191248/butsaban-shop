import streamlit as st
import datetime
import math
import random

# ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="Butsaban - ร้านดอกไม้ลวดกำมะหยี่", page_icon="🌹", layout="wide")

# ตกแต่ง CSS
st.markdown("""
    <style>
    .product-card {
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #333;
        background-color: #1e1e1e;
        box-shadow: 0 4px 10px rgba(0,0,0,0.3);
        text-align: center;
        margin-bottom: 20px;
        transition: transform 0.3s ease;
    }
    .product-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 6px 15px rgba(0,0,0,0.5);
    }
    .product-title {
        font-size: 20px !important;
        font-weight: bold;
        color: #ff6b6b;
        margin-bottom: 8px;
    }
    .product-desc {
        font-size: 14px !important;
        color: #ccc;
        min-height: 40px;
    }
    .product-price {
        font-size: 18px !important;
        color: #ff8787;
        font-weight: bold;
        margin: 10px 0;
    }
    .stButton>button {
        width: 100%;
        background-color: #e03131;
        color: white;
        border-radius: 8px;
        font-weight: bold;
        border: none;
        padding: 0.6rem;
        font-size: 16px;
        transition: background-color 0.2s;
    }
    .stButton>button:hover {
        background-color: #c92a2a;
        color: white;
    }
    .big-section-title {
        font-size: 24px !important;
        font-weight: 700 !important;
        color: #ff8787 !important;
        margin-bottom: 15px !important;
        border-bottom: 2px solid #333;
        padding-bottom: 8px;
    }
    </style>
""", unsafe_allow_html=True)

# 0. ระบบตรวจสอบการเข้าสู่ระบบ (Login System)
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        st.markdown("<h2 style='text-align: center; color: #ff6b6b; margin-bottom: 5px; font-size: 32px;'>🌹 ร้าน Butsaban</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #aaa; font-size: 15px; margin-bottom: 25px;'>ระบบสั่งซื้อดอกไม้ลวดกำมะหยี่แฮนด์เมด</p>", unsafe_allow_html=True)
        
        with st.form("login_form"):
            username = st.text_input("ชื่อผู้ใช้งาน (Username)")
            password = st.text_input("รหัสผ่าน (Password)", type="password")
            submit_login = st.form_submit_button("🔑 เข้าสู่ระบบ")
            
            if submit_login:
                if username != "" and password != "":
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.
