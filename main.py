import streamlit as st
import datetime
import math
import random

# ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="Butsaban - ร้านดอกไม้ลวดกำมะหยี่", page_icon="🌹", layout="wide")

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
        transition: transform 0.3s ease;
    }
    .product-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 25px rgba(0,0,0,0.6);
        border-color: #ff6b6b;
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
if "registered_users" not in st.session_state:
    st.session_state.registered_users = {"admin": "1234", "ใบไผ่": "112233", "customer01": "password
