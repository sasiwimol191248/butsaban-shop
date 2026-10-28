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
    st.session_state.registered_users = {"admin": "1234", "ใบไผ่": "112233", "customer01": "password"}
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
        st.markdown("<p style='text-align: center; color: #aaa; font-size: 18px; margin-bottom: 20px;'>ระบบสั่งซื้อดอกไม้ลวดกำมะหยี่แฮนด์เมด</p>", unsafe_allow_html=True)
        
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
                        if l_user == "admin":
                            st.session_state.is_admin = True
                        else:
                            st.session_state.is_admin = False
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
                            st.error("⚠️ ชื่อผู้ใช้งานนี้มีคนใช้แล้ว")
                        else:
                            # บันทึกผู้ใช้ใหม่
                            st.session_state.registered_users[r_user] = r_pass
                            # ล็อกอินเข้าสู่ระบบอัตโนมัติทันที
                            st.session_state.logged_in = True
                            st.session_state.username = r_user
                            if r_user == "admin":
                                st.session_state.is_admin = True
                            else:
                                st.session_state.is_admin = False
                            st.success("🎉 สมัครสมาชิกและเข้าสู่ระบบสำเร็จ!")
                            st.rerun()
                    else:
                        st.error("⚠️ กรุณากรอกข้อมูลให้ครบถ้วน")
    
    st.stop()

# ==========================================
# 3. หน้าหลังบ้านเจ้าของร้าน (Admin Dashboard)
# ==========================================
if st.session_state.is_admin:
    st.sidebar.markdown(f"👑 ผู้ดูแลระบบ: **{st.session_state.username}**")
    if st.sidebar.button("🚪 ออกจากระบบ"):
        st.session_state.logged_in = False
        st.session_state.is_admin = False
        st.rerun()

    st.markdown("<h1 style='color: #ff6b6b; text-align: center;'>👑 ระบบหลังบ้านเจ้าของร้าน (Admin Dashboard)</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #aaa;'>จัดการออเดอร์และตรวจสอบหลักฐานการสั่งซื้อของลูกค้า</p>", unsafe_allow_html=True)
    st.write("---")

    if not st.session_state.orders_db:
        st.info("📭 ยังไม่มีออเดอร์สั่งซื้อสินค้าเข้ามาในระบบตอนนี้")
    else:
        st.markdown(f"### 📦 รายการออเดอร์ทั้งหมด ({len(st.session_state.orders_db)} ออเดอร์)")
        
        for i, order in enumerate(reversed(st.session_state.orders_db)):
            real_index = len(st.session_state.orders_db) - 1 - i
            status = order.get("status", "⏳ รอดำเนินการ")
            
            status_badge = f"<span style='color: #ffa94d;'><b>{status}</b></span>" if "รอดำเนินการ" in status else f"<span style='color: #51cf66;'><b>{status}</b></span>"
            
            with st.expander(f"ออเดอร์ที่ #{real_index + 1} | ลูกค้า: {order['customer']} | ยอด: {order['total']:,.2f} บาท ({order['time']}) [{status}]"):
                col_info1, col_info2 = st.columns([2, 1])
                
                with col_info1:
                    st.write(f"⏱️ **เวลาที่สั่งซื้อ (เวลาไทย):** {order['time']}")
                    st.write(f"👤 **ชื่อลูกค้า:** {order['customer']}")
                    st.write(f"💳 **ช่องชำระเงิน:** {order['pay_type']}")
                    st.markdown(f"📌 **สถานะออเดอร์:** {status_badge}", unsafe_allow_html=True)
                    st.write("🛒 **รายการสินค้า:**")
                    for item_name, details in order['items'].items():
                        st.markdown(f"- {item_name} x {details['qty']} กระถาง (ราคา {details['total']:,.2f} บาท)")
                    st.markdown(f"**✨ ยอดสุทธิหลังหักส่วนลด: {order['total']:,.2f} บาท**")
                
                with col_info2:
                    st.markdown("#### ⚙️ จัดการสถานะ")
                    if status == "⏳ รอดำเนินการ":
                        if st.button("✅ ทำเสร็จแล้ว / จัดส่งสำเร็จ", key=f"btn_done_{real_index}"):
                            st.session_state.orders_db[real_index]["status"] = "✅ จัดส่งสำเร็จแล้ว"
                            st.success("อัปเดตสถานะเป็นสำเร็จแล้ว!")
                            st.rerun()
                    else:
                        if st.button("🔄 เปลี่ยนกลับเป็นรอดำเนินการ", key=f"btn_undo_{real_index}"):
                            st.session_state.orders_db[real_index]["status"] = "⏳ รอดำเนินการ"
                            st.success("เปลี่ยนสถานะกลับแล้ว")
                            st.rerun()
                
    st.stop()

# ==========================================
# 4. หน้าเว็บไซต์หลักของลูกค้า (Customer Storefront)
# ==========================================
st.sidebar.markdown(f"👤 ลูกค้า: **{st.session_state.username}**")
if st.sidebar.button("🚪 ออกจากระบบ"):
    st.session_state.logged_in = False
    st.session_state.cart = {}
    st.rerun()

try:
    col_h1, col_h2, col_h3 = st.columns([1, 2.5, 1])
    with col_h2:
        st.image("header.png", use_container_width=True)
except:
    st.markdown("<h1 style='text-align: center; color: #ff6b6b; font-size: 42px;'>🌹 ร้าน Butsaban ดอกไม้ลวดกำมะหยี่</h1>", unsafe_allow_html=True)

st.write("---")

products = {
    "1": {"name": "ดอกทานตะวัน", "price": 79, "desc": "สื่อถึงความสดใสและพลังบวก"},
    "2": {"name": "ดอกเดซี่", "price": 79, "desc": "ความรักที่บริสุทธิ์และจริงใจ"},
    "3": {"name": "ดอกทิวลิป", "price": 69, "desc": "ความรักที่สมบูรณ์แบบและความสดใส"},
    "4": {"name": "บอนไซ", "price": 119, "desc": "ความมั่นคงและอายุยืนยาว"},
    "5": {"name": "ดอกบัว", "price": 99, "desc": "ความสงบและสิริมงคล"},
    "6": {"name": "ลาเวนเดอร์", "price": 89, "desc": "ความทรงจำที่งดงามและความผ่อนคลาย"},
}

st.markdown('<div class="section-header" style="border:none; text-align:center;">📋 รายการสินค้าแนะนำ (เลือกสินค้าที่ชื่นชอบ)</div>', unsafe_allow_html=True)
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
                <p style="font-size: 14px; color: #888; margin: 0 0 10px 0;">รหัสสินค้า: #{key}</p>
            </div>
        """, unsafe_allow_html=True)
        
        if st.button(f"➕ สั่งซื้อ {item['name']}", key=f"shop_btn_{key}"):
            p_name = item["name"]
            u_price = item["price"]
            
            if p_name in st.session_state.cart:
                st.session_state.cart[p_name]["qty"] += 1
                st.session_state.cart[p_name]["total"] = st.session_state.cart[p_name]["qty"] * u_price
            else:
                st.session_state.cart[p_name] = {"qty": 1, "price": u_price, "total": u_price}
                
            st.success(f"เพิ่ม '{p_name}' ลงในตะกร้าแล้ว!")

# ==========================================
# ตะกร้าสินค้าและระบบชำระเงิน
# ==========================================
if st.session_state.cart:
    st.markdown('<div class="section-box">', unsafe_allow_html=True)
    
    cart_col1, cart_col2 = st.columns([1, 1])
    
    with cart_col1:
        st.markdown('<div class="section-header">🛍️ ตะกร้าสินค้าของคุณ</div>', unsafe_allow_html=True)
        total_price = 0.0
        
        cart_items_list = list(st.session_state.cart.items())
        
        for idx, (name, info) in enumerate(cart_items_list, 1):
            qty = info["qty"]
            u_price = info["price"]
            item_tot = info["total"]
            
            c_item1, c_item2, c_item3, c_item4 = st.columns([1.8, 1, 1, 1])
            with c_item1:
                st.markdown(f"<p style='font-size: 18px; color: #ffffff; padding-top: 5px;'><b>{idx}.</b> {name} x {qty}<br><span style='color: #ff8787; font-size: 15px;'>({item_tot:,.2f} บาท)</span></p>", unsafe_allow_html=True)
            with c_item2:
                if st.button("➕ เพิ่ม", key=f"cart_plus_{name}"):
                    st.session_state.cart[name]["qty"] += 1
                    st.session_state.cart[name]["total"] = st.session_state.cart[name]["qty"] * u_price
                    st.rerun()
            with c_item3:
                if st.button("➖ ลด", key=f"cart_minus_{name}"):
                    if qty > 1:
                        st.session_state.cart[name]["qty"] -= 1
                        st.session_state.cart[name]["total"] = st.session_state.cart[name]["qty"] * u_price
                    else:
                        del st.session_state.cart[name]
                    st.rerun()
            with c_item4:
                if st.button("❌ ลบ", key=f"cart_del_{name}"):
                    if name in st.session_state.cart:
                        del st.session_state.cart[name]
                    st.rerun()
                    
            total_price += item_tot
            
        st.write(f"---")
        st.markdown(f"<p style='font-size: 22px; color: #ffffff;'><b>ราคารวมทั้งหมด:</b> {total_price:,.2f} บาท</p>", unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        btn_col1, btn_col2 = st.columns(2)
        with btn_col1:
            clear_cart = st.button("🗑️ ล้างตะกร้าทั้งหมด", type="secondary")
        with btn_col2:
            confirm_order = st.button("✅ ยืนยันการสั่งซื้อสินค้า", type="primary")
            
        if clear_cart:
            st.session_state.cart = {}
            st.rerun()

    with cart_col2:
        st.markdown('<div class="section-header">💳 สรุปยอด & ส่วนลดพิเศษ</div>', unsafe_allow_html=True)
        
        total_price = sum(info["total"] for info in st.session_state.cart.values())
        
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
        st.markdown(f"<p style='font-size: 18px; color: #ffffff;'>🏷️ <b>ส่วนลด:</b> {disc_pct}% (ลดไป {disc_amount:,.2f} บาท)</p>", unsafe_allow_html=True)
        st.markdown(f"<h3 style='color: #ff6b6b;'>✨ ยอดสุทธิที่ต้องชำระ: <b>{final_price:,.2f} บาท</b></h3>", unsafe_allow_html=True)
        
        pay_choice = st.radio("เลือกช่องทางการชำระเงิน", ("1. โอนผ่านธนาคาร /พร้อมเพย์", "2. เงินสด"))

    if confirm_order:
        thai_now = get_thai_time()
        
        new_order = {
            "time": thai_now,
            "customer": st.session_state.username,
            "items": st.session_state.cart.copy(),
            "total": final_price,
            "pay_type": pay_choice,
            "status": "⏳ รอดำเนินการ"
        }
        
        st.session_state.orders_db.append(new_order)
        st.session_state.cart = {}
        
        st.markdown("---")
        st.balloons()
        st.success(f"🎉 สั่งซื้อสำเร็จ! บันทึกออเดอร์เมื่อเวลาไทย: {thai_now}")
        
        if "1." in pay_choice:
            st.warning("📌 **[ ข้อมูลสำหรับโอนเงินชำระค่าสินค้า ]**")
            st.markdown("<p style='font-size: 18px; color: #ffffff;'>🔹 ธนาคาร: กรุงไทย (KTB)<br>🔹 เลขที่บัญชี: 123-0-56789-0<br>🔹 ชื่อบัญชี: ร้าน Butsaban ดอกไม้ลวดกำมะหยี่<br>🔹 พร้อมเพย์: 063-472-9594</p>", unsafe_allow_html=True)
            st.markdown(f"<p style='font-size: 21px; color: #ff8787;'>🔹 <b>ยอดโอนสุทธิ: {final_price:,.2f} บาท</b></p>", unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("#### 📱 สแกน QR Code เพื่อชำระเงิน (พร้อมเพย์)")
            qr_text = f"PromptPay:0634729594:Amount:{final_price:.2f}"
            qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=300x300&data={qr_text}"
            
            q_col1, q_col2, q_col3 = st.columns([1, 1, 1])
            with q_col2:
                st.image(qr_url, caption="พร้อมเพย์ ร้าน Butsaban", width=300)
        else:
            price_floor = math.floor(final_price)
            st.info("📌 **[ การชำระด้วยเงินสดหน้าร้าน ]**")
            st.markdown(f"<p style='font-size: 18px; color: #ffffff;'>🔹 ยอดชำระสุทธิ: {final_price:,.2f} บาท<br>🔹 ยอดปัดเศษสำหรับชำระเงินสดพอดี: <b>{price_floor} บาท</b></p>", unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
