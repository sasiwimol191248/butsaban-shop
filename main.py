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
        font-size: 20px !important;
        font-weight: bold !important;
        color: #ffffff !important;
    }
    .stRadio div[role="radiogroup"] label p {
        font-size: 18px !important;
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
                            st.error("⚠️ ชื่อผู้ใช้งานนี้มีคนใช้แล้ว")
                        else:
                            st.session_state.registered_users[r_user] = r_pass
                            st.session_state.logged_in = True
                            st.session_state.username = r_user
                            st.session_state.is_admin = (r_user == "admin")
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
    st.markdown("<p style='text-align: center; color: #aaa;'>จัดการออเดอร์ และตรวจสอบรายการออเดอร์ของลูกค้า</p>", unsafe_allow_html=True)
    st.write("---")

    if not st.session_state.orders_db:
        st.info("📭 ยังไม่มีออเดอร์หรือคำขอจองสินค้าเข้ามาในระบบตอนนี้")
    else:
        st.markdown(f"### 📦 รายการออเดอร์และคิวจองทั้งหมด ({len(st.session_state.orders_db)} รายการ)")
        
        for i, order in enumerate(reversed(st.session_state.orders_db)):
            real_index = len(st.session_state.orders_db) - 1 - i
            status = order.get("status", "⏳ รอดำเนินการ")
            order_type = order.get("type", "🛍️ ซื้อปลีกทั่วไป")
            due_date = order.get("due_date", "-")
            address = order.get("address", "-")
            phone = order.get("phone", "-")
            
            status_badge = f"<span style='color: #ffa94d;'><b>{status}</b></span>" if "รอดำเนินการ" in status else f"<span style='color: #51cf66;'><b>{status}</b></span>"
            due_date_display = f"<span style='color: #ff8787; font-size: 18px;'>📅 <b>กำหนดใช้งาน: {due_date}</b></span>" if due_date != "-" else "-"
            
            with st.expander(f"[{order_type}] ออเดอร์ที่ #{real_index + 1} | ลูกค้า: {order['customer']} | ยอด: {order['total']:,.2f} บาท [{status}]"):
                col_info1, col_info2 = st.columns([2, 1])
                
                with col_info1:
                    st.write(f"🏷️ **ประเภท:** {order_type}")
                    st.write(f"⏱️ **เวลาที่สั่งซื้อ (เวลาไทย):** {order['time']}")
                    if due_date != "-":
                        st.markdown(due_date_display, unsafe_allow_html=True)
                    st.write(f"👤 **ชื่อลูกค้า:** {order['customer']}")
                    st.write(f"📞 **เบอร์โทรศัพท์:** {phone}")
                    st.markdown(f"🏠 **ที่อยู่สำหรับจัดส่ง:** <br><span style='color: #fffa65;'>{address}</span>", unsafe_allow_html=True)
                    st.write(f"💳 **ช่องชำระเงิน:** {order['pay_type']}")
                    st.markdown(f"📌 **สถานะ:** {status_badge}", unsafe_allow_html=True)
                    st.write("🛒 **รายการสินค้า:**")
                    for item_name, details in order['items'].items():
                        st.markdown(f"- {item_name} x {details['qty']} กระถาง (ราคา {details['total']:,.2f} บาท)")
                    st.markdown(f"**✨ ยอดสุทธิ: {order['total']:,.2f} บาท**")
                
                with col_info2:
                    st.markdown("#### ⚙️ จัดการสถานะ")
                    if status == "⏳ รอดำเนินการ":
                        if st.button("✅ อนุมัติ / ทำเสร็จแล้ว", key=f"btn_done_{real_index}"):
                            st.session_state.orders_db[real_index]["status"] = "✅ ดำเนินการสำเร็จแล้ว"
                            st.success("อัปเดตสถานะสำเร็จ!")
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

tab_retail, tab_bulk = st.tabs(["🛍️ สั่งซื้อปลีก (ทั่วไป)", "📦 ระบบจองคิวจำนวนมาก (Pre-order เลือกได้หลายแบบ)"])

with tab_retail:
    st.markdown('<div class="section-header" style="border:none; text-align:center;">📋 รายการสินค้าแนะนำ (สำหรับซื้อจำนวนน้อย)</div>', unsafe_allow_html=True)
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

    # ตะกร้าสินค้าปลีก
    if st.session_state.cart:
        st.markdown('<div class="section-box">', unsafe_allow_html=True)
        
        st.subheader("🛍️ ตะกร้าสินค้าปลีกของคุณ")
        total_price = 0.0
        cart_items_list = list(st.session_state.cart.items())
        
        for idx, (name, info) in enumerate(cart_items_list, 1):
            qty = info["qty"]
            u_price = info["price"]
            item_tot = info["total"]
            
            st.write(f"**{idx}. 🌸 {name}** — จำนวน: {qty} กระถาง | ราคา: {item_tot:,.2f} บาท")
            
            c_item1, c_item2, c_item3 = st.columns([1, 1, 1])
            with c_item1:
                if st.button("➕ เพิ่ม", key=f"cart_plus_{name}"):
                    st.session_state.cart[name]["qty"] += 1
                    st.session_state.cart[name]["total"] = st.session_state.cart[name]["qty"] * u_price
                    st.rerun()
            with c_item2:
                if st.button("➖ ลด", key=f"cart_minus_{name}"):
                    if qty > 1:
                        st.session_state.cart[name]["qty"] -= 1
                        st.session_state.cart[name]["total"] = st.session_state.cart[name]["qty"] * u_price
                    else:
                        del st.session_state.cart[name]
                    st.rerun()
            with c_item3:
                if st.button("❌ ลบ", key=f"cart_del_{name}"):
                    if name in st.session_state.cart:
                        del st.session_state.cart[name]
                    st.rerun()
                    
            st.write("---")
            total_price += item_tot
            
        st.markdown(f"**ราคารวมสินค้าทั้งหมด:** {total_price:,.2f} บาท")
        
        st.write("---")
        st.subheader("💳 สรุปยอด & ชำระเงิน (ซื้อปลีก)")
        
        if "discount_percent" not in st.session_state:
            st.session_state.discount_percent = random.randint(5, 20)
            st.session_state.luck_msg = "ยินดีด้วย! คุณได้รับส่วนลดพิเศษประจำวัน"
            
        disc_pct = st.session_state.discount_percent
        disc_amount = total_price * (disc_pct / 100)
        final_price = total_price - disc_amount
        
        st.success(f"🎁 {st.session_state.luck_msg}")
        st.write(f"🏷️ **ส่วนลด:** {disc_pct}% (ลดไป {disc_amount:,.2f} บาท)")
        st.markdown(f"<h3 style='color: #ff6b6b;'>✨ ยอดสุทธิ: <b>{final_price:,.2f} บาท</b></h3>", unsafe_allow_html=True)
        
        pay_choice = st.radio("เลือกช่องทางการชำระเงิน", ("1. โอนผ่านธนาคาร /พร้อมเพย์", "2. เงินสด"), key="pay_retail")

        st.write("---")
        st.subheader("🚚 ข้อมูลสำหรับจัดส่งสินค้า (ซื้อปลีก)")
        retail_phone = st.text_input("📞 เบอร์โทรศัพท์ติดต่อ", key="r_phone")
        retail_address = st.text_area("🏠 ที่อยู่สำหรับจัดส่งสินค้าอย่างละเอียด", key="r_addr")
        
        btn_col1, btn_col2 = st.columns(2)
        with btn_col1:
            clear_cart = st.button("🗑️ ล้างตะกร้า", type="secondary")
        with btn_col2:
            confirm_order = st.button("✅ ยืนยันการสั่งซื้อปลีก", type="primary")
            
        if clear_cart:
            st.session_state.cart = {}
            st.rerun()

        if confirm_order:
            if retail_phone.strip() == "" or retail_address.strip() == "":
                st.error("⚠️ กรุณากรอกเบอร์โทรศัพท์และที่อยู่จัดส่งให้ครบถ้วนครับ")
            else:
                thai_now = get_thai_time()
                
                new_order = {
                    "type": "🛍️ ซื้อปลีกทั่วไป",
                    "time": thai_now,
                    "phone": retail_phone,
                    "address": retail_address,
                    "customer": st.session_state.username,
                    "items": st.session_state.cart.copy(),
                    "total": final_price,
                    "pay_type": pay_choice,
                    "status": "⏳ รอดำเนินการ"
                }
                st.session_state.orders_db.append(new_order)
                st.session_state.cart = {}
                st.balloons()
                st.success(f"🎉 สั่งซื้อสำเร็จ! จัดส่งไปที่: {retail_address} (เวลาไทย: {thai_now})")

        # แสดง QR Code หรือข้อมูลชำระเงินทันทีหลังยืนยันออเดอร์ปลีก
        if st.session_state.orders_db:
            user_orders = [o for o in st.session_state.orders_db if o["customer"] == st.session_state.username]
            if user_orders:
                latest_order = user_orders[-1]
                if "1." in latest_order["pay_type"]:
                    st.markdown("---")
                    st.warning("📌 **[ ข้อมูลสำหรับโอนเงินชำระค่าสินค้าปลีก ]**")
                    st.write("🔹 ธนาคาร: กรุงไทย (KTB)\n🔹 เลขที่บัญชี: 123-0-56789-0\n🔹 ชื่อบัญชี: ร้าน Butsaban ดอกไม้ลวดกำมะหยี่\n🔹 พร้อมเพย์: 063-472-9594")
                    st.markdown(f"<p style='font-size: 21px; color: #ff8787;'>🔹 <b>ยอดโอนสุทธิ: {latest_order['total']:,.2f} บาท</b></p>", unsafe_allow_html=True)
                    
                    qr_text = f"PromptPay:0634729594:Amount:{latest_order['total']:.2f}"
                    qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=300x300&data={qr_text}"
                    
                    q_col1, q_col2, q_col3 = st.columns([1, 1, 1])
                    with q_col2:
                        st.image(qr_url, caption="พร้อมเพย์ ร้าน Butsaban", width=250)
                else:
                    st.markdown("---")
                    price_floor = math.floor(latest_order['total'])
                    st.info("📌 **[ การชำระด้วยเงินสดหน้าร้าน ]**")
                    st.write(f"🔹 ยอดชำระสุทธิ: {latest_order['total']:,.2f} บาท\n🔹 ยอดปัดเศษสำหรับชำระเงินสดพอดี: **{price_floor} บาท**")

        st.markdown('</div>', unsafe_allow_html=True)

with tab_bulk:
    st.markdown('<div class="section-box">', unsafe_allow_html=True)
    st.subheader("📦 ระบบจองคิวจำนวนมาก (Pre-order เลือกได้หลายแบบพร้อมกัน)")
    st.info("💡 สำหรับงานอีเวนต์หรือของชำร่วย สามารถเลือกติ๊กถูกดอกไม้หลายๆ แบบ และกำหนดจำนวนของแต่ละดอกได้เลยครับ")
    
    with st.form("bulk_multi_order_form"):
        st.markdown("#### 🌸 เลือกรายการดอกไม้และจำนวนที่ต้องการจองพรีออเดอร์")
        
        bulk_selected_items = {}
        for p_id, p_info in products.items():
            col_chk, col_qty = st.columns([2, 1])
            with col_chk:
                is_checked = st.checkbox(f"{p_info['name']} (฿{p_info['price']} / กระถาง)", key=f"bulk_chk_{p_id}")
            with col_qty:
                q_val = st.number_input(f"จำนวน {p_info['name']}", min_value=1, max_value=200, value=10, key=f"bulk_q_{p_id}", label_visibility="collapsed")
            
            if is_checked:
                bulk_selected_items[p_info['name']] = {
                    "qty": q_val,
                    "price": p_info['price'],
                    "total": q_val * p_info['price']
                }
        
        st.write("---")
        b_date = st.date_input("📅 กำหนดวันที่ต้องใช้งานจริง (Pre-order)", value=datetime.date.today() + datetime.timedelta(days=7))
        b_phone = st.text_input("📞 เบอร์โทรศัพท์ติดต่อ (Pre-order)")
        b_address = st.text_area("🏠 ที่อยู่สำหรับจัดส่งงาน Pre-order อย่างละเอียด")
        b_note = st.text_area("รายละเอียดเพิ่มเติม / โทนสีที่ต้องการ")
        b_pay = st.selectbox("ช่องทางชำระเงินมัดจำ", ("โอนมัดจำผ่านพร้อมเพย์", "ชำระเต็มจำนวน"))
        
        submit_bulk_multi = st.form_submit_button("🚀 ส่งคำขอจองคิว Pre-order หลายรายการ")
        
        if submit_bulk_multi:
            if not bulk_selected_items:
                st.error("⚠️ กรุณาเลือกรายการดอกไม้พรีออเดอร์อย่างน้อย 1 ชนิดครับ")
            elif b_phone.strip() == "" or b_address.strip() == "":
                st.error("⚠️ กรุณากรอกเบอร์โทรศัพท์และที่อยู่จัดส่งให้ครบถ้วนครับ")
            else:
                total_bulk_price = sum(item["total"] for item in bulk_selected_items.values())
                thai_now = get_thai_time()
                formatted_b_date = b_date.strftime("%d/%m/%Y")
                
                bulk_order = {
                    "type": "📦 จองคิว Pre-order (หลายแบบ)",
                    "time": thai_now,
                    "due_date": formatted_b_date,
                    "phone": b_phone,
                    "address": b_address,
                    "note": b_note if b_note else "ไม่มีหมายเหตุเพิ่มเติม",
                    "customer": st.session_state.username,
                    "items": bulk_selected_items,
                    "total": total_bulk_price,
                    "pay_type": b_pay,
                    "status": "⏳ รอดำเนินการ (รอคอนเฟิร์มคิว)"
                }
                st.session_state.orders_db.append(bulk_order)
                st.balloons()
                st.success(f"🎉 ส่งคำขอจองคิว Pre-order หลายแบบสำเร็จ! ยอดรวมสุทธิ: {total_bulk_price:,.2f} บาท (เวลาไทย: {thai_now})")

    # แสดง QR Code หรือข้อมูลชำระเงินทันทีหลังกดส่ง Pre-order
    if st.session_state.orders_db:
        user_orders = [o for o in st.session_state.orders_db if o["customer"] == st.session_state.username and "Pre-order" in o["type"]]
        if user_orders:
            latest_bulk = user_orders[-1]
            if "โอนมัดจำ" in latest_bulk["pay_type"]:
                st.markdown("---")
                st.warning("📌 **[ ข้อมูลสำหรับโอนเงินมัดจำ Pre-order ]**")
                st.write("🔹 ธนาคาร: กรุงไทย (KTB)\n🔹 เลขที่บัญชี: 123-0-56789-0\n🔹 ชื่อบัญชี: ร้าน Butsaban ดอกไม้ลวดกำมะหยี่\n🔹 พร้อมเพย์: 063-472-9594")
                st.markdown(f"<p style='font-size: 21px; color: #ff8787;'>🔹 <b>ยอดโอนสุทธิ: {latest_bulk['total']:,.2f} บาท</b></p>", unsafe_allow_html=True)
                
                qr_text = f"PromptPay:0634729594:Amount:{latest_bulk['total']:.2f}"
                qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=300x300&data={qr_text}"
                
                q_col1, q_col2, q_col3 = st.columns([1, 1, 1])
                with q_col2:
                    st.image(qr_url, caption="พร้อมเพย์ มัดจำ Pre-order ร้าน Butsaban", width=250)
            else:
                st.markdown("---")
                st.info("📌 **[ ชำระค่าสินค้า Pre-order เต็มจำนวน ]**")
                st.write(f"🔹 ยอดชำระสุทธิ: **{latest_bulk['total']:,.2f} บาท** (ชำระตามช่องทางที่แอดมินติดต่อกลับ)")

    st.markdown('</div>', unsafe_allow_html=True)
