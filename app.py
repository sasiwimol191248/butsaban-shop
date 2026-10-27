import streamlit as st
import datetime
import math
import random

# ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="Butsaban - ร้านดอกไม้ลวดกำมะหยี่", page_icon="🌹")

# แสดงรูปแบนเนอร์ด้านบนสุด (หากอัปโหลดไฟล์ Copy.png ไว้แล้ว)
try:
    st.image("Copy.png", use_container_width=True)
except:
    st.title("🌹 Butsaban. ร้านดอกไม้ลวดกำมะหยี่")

st.write("ยินดีต้อนรับสู่ระบบสั่งซื้อสินค้าออนไลน์ (Python Creative Challenge)")

# 1. ข้อมูลรายการสินค้า
products = {
    "1": ("ดอกทานตะวัน", 79),
    "2": ("ดอกเดซี่", 79),
    "3": ("บอนไซ", 119),
    "4": ("ดอกบัว", 99),
    "5": ("ลาเวนเดอร์", 89),
}

# 2. แสดงเมนูสินค้า
st.subheader("📋 รายการสินค้า")
for key, (name, price) in products.items():
    st.write(f"**{key}.** {name} — **{price}** บาท/กระถาง")

st.markdown("---")

# 3. จัดการตะกร้าสินค้าใน session_state
if "cart" not in st.session_state:
    st.session_state.cart = []

st.subheader("🛒 สั่งซื้อสินค้า")
product_choice = st.selectbox(
    "เลือกหมายเลขสินค้า",
    options=list(products.keys()),
    format_func=lambda x: f"{x}. {products[x][0]} ({products[x][1]} บาท)"
)

quantity = st.number_input("จำนวน (กระถาง)", min_value=1, value=1, step=1)

if st.button("➕ เพิ่มลงตะกร้า"):
    p_name, u_price = products[product_choice]
    item_total = float(u_price * quantity)
    st.session_state.cart.append((p_name, quantity, u_price, item_total))
    st.success(f"เพิ่ม '{p_name}' จำนวน {quantity} กระถาง เรียบร้อย!")

# 4. แสดงสรุปรายการและคำนวณเงิน
if st.session_state.cart:
    st.markdown("---")
    st.subheader("🛍️ สรุปรายการสินค้าในตะกร้า")
    
    total_price = 0.0
    for idx, item in enumerate(st.session_state.cart, 1):
        name, qty, u_price, item_tot = item
        st.write(f"{idx}. {name} x {qty} กระถาง ({u_price} บาท/กระถาง) = **{item_tot:,.2f} บาท**")
        total_price += item_tot
        
    st.write(f"**ราคารวมทั้งหมดก่อนลด:** {total_price:,.2f} บาท")
    
    # สุ่มส่วนลดและข้อความ
    if "discount_percent" not in st.session_state:
        st.session_state.discount_percent = random.randint(5, 20)
        st.session_state.luck_msg = random.choice([
            "ขอให้เป็นวันที่สดใส!",
            "ขอบคุณที่อุดหนุนค่ะ",
            "ดอกไม้น่ารักเหมาะกับคุณมาก!"
        ])
        
    disc_pct = st.session_state.discount_percent
    luck_msg = st.session_state.luck_msg
    disc_amount = total_price * (disc_pct / 100)
    final_price = total_price - disc_amount
    
    st.info(f"🎁 ข้อความจากร้าน: {luck_msg}")
    st.write(f"**คูปองส่วนลดสุ่มได้:** {disc_pct}% (ประหยัดไป {disc_amount:,.2f} บาท)")
    st.markdown(f"### 💳 ยอดสุทธิที่ต้องชำระ: {final_price:,.2f} บาท")
    
    # 5. ช่องทางการชำระเงิน
    pay_choice = st.radio("เลือกช่องทางการชำระเงิน", ("1. เงินสด", "2. โอนผ่านธนาคาร / พร้อมเพย์"))
    
    if st.button("✅ ยืนยันการสั่งซื้อ"):
        now = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        st.success(f"ทำรายการสำเร็จเมื่อเวลา: {now}")
        
        if "2." in pay_choice:
            st.warning("📌 [ ข้อมูลสำหรับโอนเงิน ]")
            st.write("-> ธนาคาร: กรุงไทย (KTB)")
            st.write("-> เลขที่บัญชี: 123-0-56789-0")
            st.write("-> ชื่อบัญชี: ร้าน Butsaban ดอกไม้ลวดกำมะหยี่")
            st.write("-> พร้อมเพย์: 063-472-9594")
            st.write(f"-> ยอดที่ต้องโอนสุทธิ: **{final_price:,.2f} บาท**")
            st.info("*(เมื่อโอนแล้ว กรุณาแนบสลิปเพื่อยืนยันการชำระเงิน)*")
        else:
            price_floor = math.floor(final_price)
            st.info("📌 [ การชำระด้วยเงินสด ]")
            st.write(f"-> ยอดชำระสุทธิ: {final_price:,.2f} บาท")
            st.write(f"-> ยอดปัดเศษลง (สำหรับจ่ายเงินสดพอดี): **{price_floor} บาท**")
            
        st.balloons()
