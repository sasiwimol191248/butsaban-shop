import streamlit as st
import datetime
import math
import random

# ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="Butsaban - ร้านดอกไม้ลวดกำมะหยี่", page_icon="🌹", layout="wide")

# ตกแต่ง CSS เพิ่มความสวยงาม
st.markdown("""
    <style>
    @keyframes bannerFadeIn {
        from {
            opacity: 0;
            transform: translateY(-20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    .banner-container {
        animation: bannerFadeIn 1.2s ease-out;
    }
    .product-card {
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #eee;
        background-color: white;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        text-align: center;
        margin-bottom: 20px;
    }
    .product-title {
        font-size: 20px !important;
        font-weight: bold;
        color: #333;
        margin-bottom: 5px;
    }
    .product-desc {
        font-size: 15px !important;
        color: #555;
        min-height: 40px;
    }
    .product-price {
        font-size: 18px !important;
        color: #d9534f;
        font-weight: bold;
        margin: 10px 0;
    }
    .stButton>button {
        width: 100%;
        background-color: #d9534f;
        color: white;
        border-radius: 8px;
        font-weight: bold;
        border: none;
        padding: 0.6rem;
        font-size: 16px;
    }
    .stButton>button:hover {
        background-color: #c9302c;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# 0. ระบบตรวจสอบการเข้าสู่ระบบ (Login System)
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.markdown("<h2 style='text-align: center; color: #d9534f;'>🌹 เข้าสู่ระบบร้าน Butsaban ดอกไม้ลวดกำมะหยี่</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #666;'>กรุณาเข้าสู่ระบบเพื่อเข้าชมสินค้าและสั่งซื้อสินค้า</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.form("login_form"):
            username = st.text_input("ชื่อผู้ใช้งาน (Username)")
            password = st.text_input("รหัสผ่าน (Password)", type="password")
            submit_login = st.form_submit_button("🔑 เข้าสู่ระบบ")
            
            if submit_login:
                # ตั้งค่ารหัสผ่านจำลอง (สามารถใช้อะไรก็ได้ หรือกำหนดตายตัว เช่น user / 1234)
                if username != "" and password != "":
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.success("เข้าสู่ระบบสำเร็จ! กำลังพาท่านเข้าสู่เว็บไซต์...")
                    st.rerun()
                else:
                    st.error("⚠️ กรุณากรอกชื่อผู้ใช้งานและรหัสผ่านให้ครบถ้วน")
        
        st.info("💡 **คำแนะนำเบื้องต้น:** สามารถกรอกชื่ออะไรก็ได้ (เช่น `customer` หรือ `admin`) และใส่รหัสผ่านอะไรก็ได้เพื่อเข้าสู่ระบบทดลองครับ")
    
    # หยุดการทำงานหน้าอื่นไว้ก่อนจนกว่าจะ Login สำเร็จ
    st.stop()

# --- ส่วนของเว็บไซต์หลัก (หลัง Log-in สำเร็จแล้ว) ---
st.sidebar.success(f"👤 เข้าสู่ระบบโดย: **{st.session_state.username}**")
if st.sidebar.button("🚪 ออกจากระบบ (Logout)"):
    st.session_state.logged_in = False
    st.session_state.cart = []
    st.rerun()

# 1. แสดงรูปแบนเนอร์ช่อกุหลาบพร้อมเอฟเฟกต์เด้งขึ้นมาตอนเข้าเว็บ
st.markdown('<div class="banner-container">', unsafe_allow_html=True)
try:
    st.image("Copy.png", use_container_width=True)
except Exception:
    st.error("⚠️ ไม่พบไฟล์รูปภาพ 'Copy.png' บน GitHub กรุณาตรวจสอบการอัปโหลดไฟล์รูปอีกครั้งครับ")
st.markdown('</div>', unsafe_allow_html=True)

st.write("---")

# 2. ข้อมูลรายการสินค้า
products = {
    "1": {"name": "ดอกทานตะวัน", "price": 79, "desc": "สื่อถึงความสดใสและพลังบวก"},
    "2": {"name": "ดอกเดซี่", "price": 79, "desc": "ความรักที่บริสุทธิ์และจริงใจ"},
    "3": {"name": "ดอกทิวลิป", "price": 69, "desc": "ความรักที่สมบูรณ์แบบและความสดใส"},
    "4": {"name": "บอนไซ", "price": 119, "desc": "ความมั่นคงและอายุยืนยาว"},
    "5": {"name": "ดอกบัว", "price": 99, "desc": "ความสงบและสิริมงคล"},
    "6": {"name": "ลาเวนเดอร์", "price": 89, "desc": "ความทรงจำที่งดงามและความผ่อนคลาย"},
}

# 3. แสดงรายการสินค้าแบบการ์ด (Grid View)
st.subheader("📋 เมนูสินค้าแนะนำ")
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
                <p style="font-size: 13px; color: #888; margin: 0;">รหัสสินค้า: #{key}</p>
            </div>
        """, unsafe_allow_html=True)

st.markdown("---")

# 4. จัดการตะกร้าสินค้าใน session_state
if "cart" not in st.session_state:
    st.session_state.cart = []

order_col1, order_col2 = st.columns([1, 1])

with order_col1:
    st.subheader("🛒 ฟอร์มสั่งซื้อสินค้า")
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
    st.subheader("🛍️ ตะกร้าสินค้าของคุณ")
    if not st.session_state.cart:
        st.info("ยังไม่มีสินค้าในตะกร้า เลือกสินค้าทางซ้ายมือได้เลยครับ")
    else:
        total_price = 0.0
        for idx, item in enumerate(st.session_state.cart, 1):
            name, qty, u_price, item_tot = item
            st.write(f"**{idx}.** {name} x {qty} = **{item_tot:,.2f} บาท**")
            total_price += item_tot
            
        st.write(f"---")
        st.write(f"**ราคารวมทั้งหมด:** {total_price:,.2f} บาท")
        
        if st.button("🗑️ ล้างตะกร้าสินค้า"):
            st.session_state.cart = []
            st.rerun()

# 5. ส่วนสรุปยอด ชำระเงิน และระบบสุ่มส่วนลด
if st.session_state.cart:
    st.markdown("---")
    st.subheader("💳 สรุปยอดชำระเงิน & ส่วนลดพิเศษ")
    
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
    st.write(f"🏷️ **ส่วนลดที่คุณได้รับ:** {disc_pct}% (ลดไป {disc_amount:,.2f} บาท)")
    st.markdown(f"### ✨ ยอดสุทธิที่ต้องชำระ: **{final_price:,.2f} บาท**")
    
    pay_choice = st.radio("เลือกช่องทางการชำระเงิน", ("1. โอนผ่านธนาคาร / พร้อมเพย์", "2. เงินสด"))
    
    if st.button("✅ ยืนยันการสั่งซื้อสินค้า"):
        now = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        st.balloons()
        st.success(f"🎉 สั่งซื้อสำเร็จ! บันทึกรายการเมื่อ: {now}")
        
        if "1." in pay_choice:
            st.warning("📌 **[ ข้อมูลสำหรับโอนเงินชำระค่าสินค้า ]**")
            st.write("🔹 ธนาคาร: กรุงไทย (KTB)")
            st.write("🔹 เลขที่บัญชี: 123-0-56789-0")
            st.write("🔹 ชื่อบัญชี: ร้าน Butsaban ดอกไม้ลวดกำมะหยี่")
            st.write("🔹 พร้อมเพย์: 063-472-9594")
            st.write(f"🔹 **ยอดโอนสุทธิ: {final_price:,.2f} บาท**")
            st.info("*(รบกวนส่งสลิปหลักฐานการโอนเงินให้ทางร้านด้วยนะคะ)*")
        else:
            price_floor = math.floor(final_price)
            st.info("📌 **[ การชำระด้วยเงินสดหน้าร้าน ]**")
            st.write(f"🔹 ยอดชำระสุทธิ: {final_price:,.2f} บาท")
            st.write(f"🔹 ยอดปัดเศษสำหรับชำระเงินสดพอดี: **{price_floor} บาท**")
