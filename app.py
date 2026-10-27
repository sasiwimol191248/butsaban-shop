<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Butsaban - ร้านดอกไม้ลวดกำมะหยี่</title>
    <!-- นำเข้า Google Fonts และ Tailwind CSS เพื่อความสวยงามพรีเมียม -->
    <link href="https://fonts.googleapis.com/css2?family=Prompt:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        body { font-family: 'Prompt', sans-serif; }
        .fade-in { animation: fadeIn 0.4s ease-out forwards; }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
    </style>
</head>
<body class="bg-stone-50 text-stone-800 min-h-screen flex flex-col justify-between">

    <!-- 0. หน้าเข้าสู่ระบบ (Login Section) -->
    <div id="login-section" class="fixed inset-0 bg-stone-900/60 backdrop-blur-sm flex items-center justify-center z-50 p-4">
        <div class="bg-white w-full max-w-md p-8 rounded-2xl shadow-2xl border border-stone-100 fade-in">
            <div class="text-center mb-6">
                <span class="text-4xl">🌹</span>
                <h2 class="text-2xl font-bold text-rose-600 mt-2">ร้าน Butsaban</h2>
                <p class="text-stone-500 text-sm">ระบบสั่งซื้อดอกไม้ลวดกำมะหยี่แฮนด์เมด</p>
            </div>
            <form id="login-form" onsubmit="handleLogin(event)" class="space-y-4">
                <div>
                    <label class="block text-sm font-medium text-stone-700 mb-1">ชื่อผู้ใช้งาน (Username)</label>
                    <input type="text" id="username-input" required class="w-full px-4 py-2.5 rounded-lg border border-stone-300 focus:ring-2 focus:ring-rose-500 focus:outline-none" placeholder="กรอกชื่อผู้ใช้...">
                </div>
                <div>
                    <label class="block text-sm font-medium text-stone-700 mb-1">รหัสผ่าน (Password)</label>
                    <input type="password" id="password-input" required class="w-full px-4 py-2.5 rounded-lg border border-stone-300 focus:ring-2 focus:ring-rose-500 focus:outline-none" placeholder="กรอกรหัสผ่าน...">
                </div>
                <button type="submit" class="w-full bg-rose-600 hover:bg-rose-700 text-white font-semibold py-3 rounded-lg shadow-md transition-all duration-200">
                    🔑 เข้าสู่ระบบ
                </button>
            </form>
            <div class="mt-4 p-3 bg-rose-50 rounded-lg text-center text-xs text-rose-600 font-medium">
                💡 พิมพ์ชื่อและรหัสผ่านอะไรก็ได้เพื่อเข้าสู่ระบบทดลอง
            </div>
        </div>
    </div>

    <!-- ส่วนเนื้อหาหลักของเว็บไซต์ (แสดงหลังเข้าสู่ระบบ) -->
    <div id="app-section" class="hidden flex-grow">
        <!-- แถบบน (Header) -->
        <header class="bg-white shadow-sm border-b border-stone-200 sticky top-0 z-30">
            <div class="max-w-6xl mx-auto px-4 py-4 flex justify-between items-center">
                <div class="flex items-center space-x-2">
                    <span class="text-2xl">🌹</span>
                    <span class="text-xl font-bold text-rose-600">Butsaban Shop</span>
                </div>
                <div class="flex items-center space-x-4">
                    <span id="user-display" class="text-sm font-medium text-stone-600 bg-stone-100 px-3 py-1.5 rounded-full"></span>
                    <button onclick="handleLogout()" class="text-sm bg-stone-200 hover:bg-stone-300 text-stone-700 px-3 py-1.5 rounded-lg transition">🚪 ออกจากระบบ</button>
                </div>
            </div>
        </header>

        <!-- เนื้อหาหลัก (Main Content) -->
        <main class="max-w-6xl mx-auto px-4 py-8 space-y-10">
            <!-- แบนเนอร์หัวข้อร้าน -->
            <div class="text-center space-y-2 fade-in">
                <h1 class="text-3xl md:text-4xl font-bold text-rose-600">🌹 ร้าน Butsaban ดอกไม้ลวดกำมะหยี่</h1>
                <p class="text-stone-500">ยินดีต้อนรับสู่ร้านดอกไม้แฮนด์เมดเพื่อคนพิเศษของคุณ</p>
            </div>

            <hr class="border-stone-200">

            <!-- 1. เมนูสินค้าแนะนำ (Grid View) -->
            <section class="space-y-4">
                <h2 class="text-xl font-bold text-stone-700">📋 เมนูสินค้าแนะนำ</h2>
                <div id="product-grid" class="grid grid-cols-1 md:grid-cols-3 gap-6">
                    <!-- สินค้าจะถูกเรนเดอร์ด้วย JavaScript ด้านล่าง -->
                </div>
            </section>

            <hr class="border-stone-200">

            <!-- 2. ฟอร์มสั่งซื้อสินค้า & ตะกร้าสินค้า -->
            <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
                <!-- ฟอร์มเลือกสินค้า -->
                <div class="bg-white p-6 rounded-2xl shadow-sm border border-stone-200 space-y-4">
                    <h2 class="text-xl font-bold text-stone-700">🛒 ฟอร์มสั่งซื้อสินค้า</h2>
                    <div>
                        <label class="block text-sm font-medium text-stone-700 mb-1">เลือกรายการสินค้า</label>
                        <select id="product-select" class="w-full px-4 py-2.5 rounded-lg border border-stone-300 focus:ring-2 focus:ring-rose-500 focus:outline-none">
                            <!-- ตัวเลือกสินค้า -->
                        </select>
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-stone-700 mb-1">จำนวนที่ต้องการ (กระถาง)</label>
                        <input type="number" id="quantity-input" min="1" value="1" class="w-full px-4 py-2.5 rounded-lg border border-stone-300 focus:ring-2 focus:ring-rose-500 focus:outline-none">
                    </div>
                    <button onclick="addToCart()" class="w-full bg-rose-600 hover:bg-rose-700 text-white font-semibold py-3 rounded-lg shadow transition">
                        ➕ เพิ่มสินค้าลงตะกร้า
                    </button>
                </div>

                <!-- ตะกร้าสินค้า -->
                <div class="bg-white p-6 rounded-2xl shadow-sm border border-stone-200 flex flex-col justify-between">
                    <div>
                        <h2 class="text-xl font-bold text-stone-700 mb-4">🛍️ ตะกร้าสินค้าของคุณ</h2>
                        <div id="cart-items" class="space-y-3 max-h-60 overflow-y-auto pr-2">
                            <p class="text-stone-400 text-sm">ยังไม่มีสินค้าในตะกร้า เลือกสินค้าทางซ้ายมือได้เลยครับ</p>
                        </div>
                    </div>
                    <div id="cart-summary" class="mt-6 pt-4 border-t border-stone-200 hidden">
                        <div class="flex justify-between text-lg font-bold text-stone-800 mb-4">
                            <span>ราคารวมทั้งหมด:</span>
                            <span id="total-price-text" class="text-rose-600">0.00 บาท</span>
                        </div>
                        <button onclick="clearCart()" class="w-full bg-stone-200 hover:bg-stone-300 text-stone-700 font-medium py-2 rounded-lg transition text-sm">
                            🗑️ ล้างตะกร้าสินค้า
                        </button>
                    </div>
                </div>
            </div>

            <!-- 3. ส่วนสรุปยอด ชำระเงิน และระบบสุ่มส่วนลด -->
            <section id="checkout-section" class="bg-white p-8 rounded-2xl shadow-sm border border-stone-200 space-y-6 hidden fade-in">
                <h2 class="text-xl font-bold text-stone-700">💳 สรุปยอดชำระเงิน & ส่วนลดพิเศษ</h2>
                <div id="discount-banner" class="p-4 bg-emerald-50 border border-emerald-200 rounded-xl text-emerald-800 font-medium"></div>
                
                <div class="space-y-2 text-stone-600">
                    <div class="flex justify-between">
                        <span>ส่วนลดที่คุณได้รับ:</span>
                        <span id="discount-detail" class="font-bold text-emerald-600"></span>
                    </div>
                    <div class="flex justify-between text-xl font-bold text-stone-900 pt-2 border-t border-stone-100">
                        <span>ยอดสุทธิที่ต้องชำระ:</span>
                        <span id="final-price-text" class="text-rose-600"></span>
                    </div>
                </div>

                <div class="space-y-2">
                    <label class="block text-sm font-medium text-stone-700">เลือกช่องทางการชำระเงิน</label>
                    <div class="flex space-x-6">
                        <label class="flex items-center space-x-2 cursor-pointer">
                            <input type="radio" name="payment" value="bank" checked onchange="togglePaymentMethod()" class="text-rose-600 focus:ring-rose-500">
                            <span>โอนผ่านธนาคาร / พร้อมเพย์</span>
                        </label>
                        <label class="flex items-center space-x-2 cursor-pointer">
                            <input type="radio" name="payment" value="cash" onchange="togglePaymentMethod()" class="text-rose-600 focus:ring-rose-500">
                            <span>เงินสดหน้าร้าน</span>
                        </label>
                    </div>
                </div>

                <div id="bank-info" class="p-4 bg-stone-50 rounded-xl border border-stone-200 text-sm space-y-1">
                    <p class="font-bold text-stone-800 mb-2">📌 [ ข้อมูลสำหรับโอนเงินชำระค่าสินค้า ]</p>
                    <p>🔹 ธนาคาร: กรุงไทย (KTB)</p>
                    <p>🔹 เลขที่บัญชี: 123-0-56789-0</p>
                    <p>🔹 ชื่อบัญชี: ร้าน Butsaban ดอกไม้ลวดกำมะหยี่</p>
                    <p>🔹 พร้อมเพย์: 063-472-9594</p>
                </div>

                <div id="cash-info" class="p-4 bg-stone-50 rounded-xl border border-stone-200 text-sm space-y-1 hidden">
                    <p class="font-bold text-stone-800 mb-2">📌 [ การชำระด้วยเงินสดหน้าร้าน ]</p>
                    <p id="cash-floor-text" class="font-medium text-rose-600"></p>
                </div>

                <button onclick="confirmCheckout()" class="w-full bg-emerald-600 hover:bg-emerald-700 text-white font-semibold py-3.5 rounded-xl shadow-md transition">
                    ✅ ยืนยันการสั่งซื้อสินค้า
                </button>
            </section>
        </main>

        <!-- Footer -->
        <footer class="bg-white border-t border-stone-200 py-6 mt-12 text-center text-stone-400 text-sm">
            © 2026 Butsaban Shop. Handmade Velvet Wire Flowers.
        </footer>
    </div>

    <!-- JavaScript ควบคุมการทำงานทั้งหมด -->
    <script>
        const products = {
            "1": { name: "ดอกทานตะวัน", price: 79, desc: "สื่อถึงความสดใสและพลังบวก" },
            "2": { name: "ดอกเดซี่", price: 79, desc: "ความรักที่บริสุทธิ์และจริงใจ" },
            "3": { name: "ดอกทิวลิป", price: 69, desc: "ความรักที่สมบูรณ์แบบและความสดใส" },
            "4": { name: "บอนไซ", price: 119, desc: "ความมั่นคงและอายุยืนยาว" },
            "5": { name: "ดอกบัว", price: 99, desc: "ความสงบและสิริมงคล" },
            "6": { name: "ลาเวนเดอร์", price: 89, desc: "ความทรงจำที่งดงามและความผ่อนคลาย" }
        };

        let cart = [];
        let discountPercent = 0;
        let luckMsg = "";

        // เริ่มต้นเรนเดอร์สินค้าใส่หน้าเว็บและ Dropdown
        window.onload = function() {
            const grid = document.getElementById('product-grid');
            const select = document.getElementById('product-select');

            for (let key in products) {
                let p = products[key];
                // สร้าง Card แสดงสินค้า
                grid.innerHTML += `
                    <div class="bg-white p-6 rounded-2xl shadow-sm border border-stone-200 hover:shadow-md transition text-center space-y-2">
                        <h3 class="text-lg font-bold text-stone-800">${p.name}</h3>
                        <p class="text-stone-500 text-sm min-h-[40px]">${p.desc}</p>
                        <div class="text-rose-600 font-bold text-lg">฿${p.price} / กระถาง</div>
                        <span class="text-xs text-stone-400">รหัสสินค้า: #${key}</span>
                    </div>
                `;
                // เพิ่มตัวเลือกใน Dropdown
                select.innerHTML += `<option value="${key}">${key}. ${p.name} (${p.price} บาท)</option>`;
            }
        };

        // ระบบ Login
        function handleLogin(event) {
            event.preventDefault();
            const username = document.getElementById('username-input').value.trim();
            if (username) {
                document.getElementById('user-display').innerText = `👤 ผู้ใช้งาน: ${username}`;
                document.getElementById('login-section').classList.add('hidden');
                document.getElementById('app-section').classList.remove('hidden');
                
                // สุ่มส่วนลดประจำตัวผู้ใช้
                discountPercent = Math.floor(Math.random() * 16) + 5; // 5% - 20%
                const messages = [
                    "ยินดีด้วย! คุณได้รับส่วนลดพิเศษประจำวัน",
                    "ขอบคุณที่สนับสนุนร้าน Butsaban ขอให้มีความสุขมากๆ นะคะ",
                    "ดอกไม้น่ารักๆ เหมาะกับวันพิเศษของคุณ!"
                ];
                luckMsg = messages[Math.floor(Math.random() * messages.length)];
            }
        }

        function handleLogout() {
            cart = [];
            document.getElementById('username-input').value = '';
            document.getElementById('password-input').value = '';
            document.getElementById('app-section').classList.add('hidden');
            document.getElementById('login-section').classList.remove('hidden');
            updateCartUI();
        }

        // เพิ่มสินค้าลงตะกร้า
        function addToCart() {
            const selectKey = document.getElementById('product-select').value;
            const qty = parseInt(document.getElementById('quantity-input').value);
            const prod = products[selectKey];
            const itemTotal = prod.price * qty;

            cart.push({ name: prod.name, qty: qty, price: prod.price, total: itemTotal });
            updateCartUI();
        }

        function clearCart() {
            cart = [];
            updateCartUI();
        }

        // อัปเดตหน้าจอตะกร้าสินค้า
        function updateCartUI() {
            const container = document.getElementById('cart-items');
            const summary = document.getElementById('cart-summary');
            const checkoutSection = document.getElementById('checkout-section');
            
            container.innerHTML = '';

            if (cart.length === 0) {
                container.innerHTML = `<p class="text-stone-400 text-sm">ยังไม่มีสินค้าในตะกร้า เลือกสินค้าทางซ้ายมือได้เลยครับ</p>`;
                summary.classList.add('hidden');
                checkoutSection.classList.add('hidden');
                return;
            }

            let totalPrice = 0;
            cart.forEach((item, index) => {
                totalPrice += item.total;
                container.innerHTML += `
                    <div class="flex justify-between items-center text-sm bg-stone-50 p-2.5 rounded-lg border border-stone-100">
                        <span><b>${index + 1}.</b> ${item.name} x ${item.qty}</span>
                        <span class="font-semibold text-stone-700">${item.total.toLocaleString('th-TH', {minimumFractionDigits: 2})} บาท</span>
                    </div>
                `;
            });

            document.getElementById('total-price-text').innerText = `${totalPrice.toLocaleString('th-TH', {minimumFractionDigits: 2})} บาท`;
            summary.classList.remove('hidden');
            checkoutSection.classList.remove('hidden');

            // คำนวณส่วนลด & ยอดสุทธิ
            const discAmount = totalPrice * (discountPercent / 100);
            const finalPrice = totalPrice - discAmount;

            document.getElementById('discount-banner').innerText = `🎁 ข้อความจากร้าน: ${luckMsg}`;
            document.getElementById('discount-detail').innerText = `${discountPercent}% (ลดไป ${discAmount.toLocaleString('th-TH', {minimumFractionDigits: 2})} บาท)`;
            document.getElementById('final-price-text').innerText = `${finalPrice.toLocaleString('th-TH', {minimumFractionDigits: 2})} บาท`;
            document.getElementById('cash-floor-text').innerText = `🔹 ยอดปัดเศษสำหรับชำระเงินสดพอดี: ${Math.floor(finalPrice).toLocaleString('th-TH')} บาท`;
        }

        function togglePaymentMethod() {
            const method = document.querySelector('input[name="payment"]:checked').value;
            if (method === 'bank') {
                document.getElementById('bank-info').classList.remove('hidden');
                document.getElementById('cash-info').classList.add('hidden');
            } else {
                document.getElementById('bank-info').classList.add('hidden');
                document.getElementById('cash-info').classList.remove('hidden');
            }
        }

        function confirmCheckout() {
            const now = new Date().toLocaleString('th-TH');
            alert(`🎉 สั่งซื้อสินค้าสำเร็จ!\nบันทึกรายการเมื่อ: ${now}`);
            cart = [];
            updateCartUI();
        }
    </script>
</body>
</html>
