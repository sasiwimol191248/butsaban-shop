import streamlit as st
import datetime
import math
import random

# ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="Butsaban - ร้านดอกไม้ลวดกำมะหยี่", page_icon="🌹", layout="wide")

# ตกแต่ง CSS ขยายขนาดฟ้อนท์และปรับแต่งหน้าตาให้ตัวใหญ่ขึ้นชัดเจน
st.markdown("""
    <style>
    /* ขยายฟ้อนท์โดยรวมและหัวข้อต่างๆ */
    html, body, [class*="css"] {
        font-size: 18px !important;
    }
    .product-card {
        padding: 25px;
        border-radius: 15px;
        border: 1px solid #444;
        background-color: #1e1e1e;
        box-shadow: 0 6px 15px rgba(0,0,0,0.4);
        text-align: center;
        margin-bottom: 25px;
        transition: transform 0.3s ease;
    }
    .product-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 20px rgba(0,0,0,0.6);
    }
    .product-title {
        font-size: 26px !important;
        font-weight: bold;
        color: #ff6b6b;
        margin-bottom: 12px;
    }
    .product-desc {
        font-size: 18px !important;
        color: #ddd;
        min-height: 50px;
    }
    .product-price {
        font-size: 24px !important;
        color: #ff8787;
        font-weight: bold;
        margin: 15px 0;
    }
    .stButton>button {
        width: 100%;
        background-color: #e03131;
        color: white;
        border-radius: 10px;
        font-weight: bold;
        border: none;
        padding: 0.8rem;
        font-size: 20px !important;
        transition: background-color 0.2s;
    }
    .stButton>button:hover {
        background-color: #c92a2a;
        color: white;
    }
    .big-section-title {
        font-size: 30px !important;
        font-weight: 700 !important;
        color: #ff8787 !important;
        margin-bottom: 20px !important;
        border-bottom: 3px solid #444;
        padding-bottom: 10px;
    }
    /* ขยายขนาดตัวหนังสือใน input และ selectbox */
    .stTextInput input, .stSelectbox select, .stNumberInput input {
        font-size: 18px !important;
    }
    </style>
""", unsafe_allow_html=True)

# 0. ระบบตรวจสอบการเข้าสู่ระบบ (Login System)
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1.3, 1])
    with col2:
        st.markdown("<h2 style='text-align: center; color: #ff6b6b; margin-bottom: 10px; font-size: 38px;'>🌹 ร้าน Butsaban</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #aaa; font-size: 18px; margin-bottom: 30px;'>ระบบสั่งซื้อดอกไม้ลวดกำมะหยี่แฮนด์เมด</p>", unsafe_allow_html=True)
        
        with st.form("login_form"):
            username = st.text_input("ชื่อผู้ใช้งาน (Username)")
            password = st.text_input("รหัสผ่าน (Password)", type="password")
            submit_login = st.form_submit_button("🔑 เข้าสู่ระบบ")
            
            if submit_login:
                if username != "" and password != "":
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.success("เข้าสู่ระบบสำเร็จ!")
                    st.rerun()
                else:
                    st.error("⚠️ กรุณากรอกข้อมูลให้ครบถ้วน")
        
        st.info("💡 *พิมพ์ชื่ออะไรก็ได้เพื่อเข้าสู่ระบบทดลอง*")
    
    st.stop()

# --- ส่วนของเว็บไซต์หลัก (หลัง Log-in สำเร็จแล้ว) ---
st.sidebar.markdown(f"👤 ผู้ใช้งาน: **{st.session_state.username}**")
if st.sidebar.button("🚪 ออกจากระบบ"):
    st.session_state.logged_in = False
    st.session_state.cart = []
    st.rerun()

# แสดงผลรูปแบนเนอร์เดี่ยวตรงกลางสวยๆ
try:
    col_h1, col_h2, col_h3 = st.columns([1, 2.5, 1])
    with col_h2:
        st.image("header.png", use_container_width=True)
except:
    st.markdown("<h1 style='text-align: center; color: #ff6b6b; font-size: 42px;'>🌹 ร้าน Butsaban ดอกไม้ลวดกำมะหยี่</h1>", unsafe_allow_html=True)

st.write("---")

# 1. ข้อมูลรายการสินค้า
products = {
    "1": {"name": "ดอกทานตะวัน", "price": 79, "desc": "สื่อถึงความสดใสและพลังบวก"},
    "2": {"name": "ดอกเดซี่", "price": 79, "desc": "ความรักที่บริสุทธิ์และจริงใจ"},
    "3": {"name": "ดอกทิวลิป", "price": 69, "desc": "ความรักที่สมบูรณ์แบบและความสดใส"},
    "4": {"name": "บอนไซ", "price": 119, "desc": "ความมั่นคงและอายุยืนยาว"},
    "5": {"name": "ดอกบัว", "price": 99, "desc": "ความสงบและสิริมงคล"},
    "6": {"name": "ลาเวนเดอร์", "price": 89, "desc": "ความทรงจำที่งดงามและความผ่อนคลาย"},
}

# 2. แสดงรายการสินค้าแบบการ์ด (Grid View)
st.markdown('<div class="big-section-title">📋 เมนูสินค้าแนะนำ</div>', unsafe_allow_html=True)
cols = st.columns(3)

product_keys = list(products.keys())
for i, key in enumerate(product_keys):
    item = products[key]
    with cols[i % 3]:
        st.markdown(f"""
            <div class="product-card">
                <div class="product-title">{item['name']}</div>
                <div class="product-desc">{item['desc']}</div>
                <div class="product-price">฿{item['price']} / กระถาง</div>
                <p style="font-size: 15px; color: #888; margin: 0;">รหัสสินค้า: #{key}</p>
            </div>
        """, unsafe_allow_html=True)

st.markdown("---")

# 3. จัดการตะกร้าสินค้าใน session_state
if "cart" not in st.session_state:
    st.session_state.cart = []

order_col1, order_col2 = st.columns([1, 1])

with order_col1:
    st.markdown('<div class="big-section-title">🛒 ฟอร์มสั่งซื้อสินค้า</div>', unsafe_allow_html=True)
    product_choice = st.selectbox(
        "เลือกรายการสินค้า",
        options=list(products.keys()),
        format_func=lambda x: f"{x}. {products[x]['name']} ({products[x]['price']} บาท)"
    )

    quantity = st.number_input("จำนวนที่ต้องการ (กระถาง)", min_value=1, value=1, step=1)

    if st.button("➕ เพิ่มสินค้าลงตะกร้า"):
        p_name = products[product_choice]["name"]
        u_price = products[product_choice]["price"]
        item_total = float(u_price * quantity)
        st.session_state.cart.append((p_name, quantity, u_price, item_total))
        st.success(f"เพิ่ม '{p_name}' จำนวน {quantity} กระถาง ลงในตะกร้าแล้ว!")

with order_col2:
    st.markdown('<div class="big-section-title">🛍️ ตะกร้าสินค้าของคุณ</div>', unsafe_allow_html=True)
    if not st.session_state.cart:
        st.info("ยังไม่มีสินค้าในตะกร้า เลือกสินค้าทางซ้ายมือได้เลยครับ")
    else:
        total_price = 0.0
        for idx, item in enumerate(st.session_state.cart, 1):
            name, qty, u_price, item_tot = item
            st.markdown(f"<p style='font-size: 19px;'><b>{idx}.</b> {name} x {qty} = <b>{item_tot:,.2f} บาท</b></p>", unsafe_allow_html=True)
            total_price += item_tot
            
        st.write(f"---")
        st.markdown(f"<p style='font-size: 22px;'><b>ราคารวมทั้งหมด:</b> {total_price:,.2f} บาท</p>", unsafe_allow_html=True)
        
        if st.button("🗑️ ล้างตะกร้าสินค้า"):
            st.session_state.cart = []
            st.rerun()

# 4. ส่วนสรุปยอด ชำระเงิน และระบบสุ่มส่วนลด
if st.session_state.cart:
    st.markdown("---")
    st.markdown('<div class="big-section-title">💳 สรุปยอดชำระเงิน & ส่วนลดพิเศษ</div>', unsafe_allow_html=True)
    
    total_price = sum(item[3] for item in st.session_state.cart)
    
    if "discount_percent" not in st.session_state:
        st.session_state.discount_percent = random.randint(5, 20)
        st.session_state.luck_msg = random.choice([
            "ยินดีด้วย! คุณได้รับส่วนลดพิเศษประจำวัน",
            "ขอบคุณที่สนับสนุนร้าน Butsaban ขอให้มีความสุขมากๆ นะคะ",
            "ดอกไม้น่ารักๆ เหมาะกับวันพิเศษของคุณ!"
        ])
        
    disc_pct = st.session_state.discount_percent
    luck_msg = st.session_state.luck_msg
    disc_amount = total_price * (disc_pct / 100)
    final_price = total_price - disc_amount
    
    st.success(f"🎁 **ข้อความจากร้าน:** {luck_msg}")
    st.markdown(f"<p style='font-size: 20px;'>🏷️ <b>ส่วนลดที่คุณได้รับ:</b> {disc_pct}% (ลดไป {disc_amount:,.2f} บาท)</p>", unsafe_allow_html=True)
    st.markdown(f"<h2 style='color: #ff6b6b;'>✨ ยอดสุทธิที่ต้องชำระ: <b>{final_price:,.2f} บาท</b></h2>", unsafe_allow_html=True)
    
    pay_choice = st.radio("เลือกช่องทางการชำระเงิน", ("1. โอนผ่านธนาคาร /พร้อมเพย์", "2. เงินสด"))
    
    if st.button("✅ ยืนยันการสั่งซื้อสินค้า"):
        now = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        st.balloons()
        st.success(f"สั่งซื้อสำเร็จ! บันทึกรายการเมื่อ: {now}")
        
        if "1." in pay_choice:
            st.warning("📌 **[ ข้อมูลสำหรับโอนเงินชำระค่าสินค้า ]**")
            st.markdown("<p style='font-size: 19px;'>🔹 ธนาคาร: กรุงไทย (KTB)<br>🔹 เลขที่บัญชี: 123-0-56789-0<br>🔹 ชื่อบัญชี: ร้าน Butsaban ดอกไม้ลวดกำมะหยี่<br>🔹 พร้อมเพย์: 063-472-9594</p>", unsafe_allow_html=True)
            st.markdown(f"<p style='font-size: 22px; color: #ff8787;'>🔹 <b>ยอดโอนสุทธิ: {final_price:,.2f} บาท</b></p>", unsafe_allow_html=True)
            
            # --- สร้าง QR Code พร้อมเพย์ขนาดใหญ่พิเศษ ---
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("### 📱 สแกน QR Code เพื่อชำระเงิน (พร้อมเพย์)")
            qr_text = f"PromptPay:0634729594:Amount:{final_price:.2f}"
            # ปรับขนาด QR Code ให้ใหญ่ขึ้นเป็น 320x320 พิกเซล
            qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=320x320&data={qr_text}"
            
            col_q1, col_q2, col_q3 = st.columns([1, 1.2, 1])
            with col_q2:
                st.image(qr_url, caption="พร้อมเพย์ ร้าน Butsaban", width=320)
        else:
            price_floor = math.floor(final_price)
            st.info("📌 **[ การชำระด้วยเงินสดหน้าร้าน ]**")
            st.markdown(f"<p style='font-size: 19px;'>🔹 ยอดชำระสุทธิ: {final_price:,.2f} บาท<br>🔹 ยอดปัดเศษสำหรับชำระเงินสดพอดี: <b>{price_floor} บาท</b></p>", unsafe_allow_html=True)
