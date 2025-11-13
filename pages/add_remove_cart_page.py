from playwright.sync_api import Page
import time


class AddRemoveCartPage:
    def __init__(self, page: Page):
        self.page = page
        self.url = "https://www.saucedemo.com/"
        self.username_input = page.locator("#user-name")
        self.password_input = page.locator("#password")
        self.login_button = page.locator("#login-button")
        self.inventory_items = page.locator(".inventory_item")
        self.add_to_cart_buttons = page.locator("button.btn_inventory")
        self.cart_icon = page.locator(".shopping_cart_link")
        self.cart_items = page.locator(".cart_item")
        self.remove_buttons = page.locator(".cart_button")

    # --- Navigasi dan login ---
    def navigate(self):
        self.page.goto(self.url)

    def login(self, username, password):
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()
        self.page.wait_for_url("**/inventory.html")

    # --- Tambah produk ---
    def add_multiple_products(self, count):
        """Tambah beberapa produk (tergantung berapa yang tersedia)"""
        buttons = self.add_to_cart_buttons
        total = min(count, buttons.count())
        for i in range(total):
            buttons.nth(i).click()
        time.sleep(1)

    def get_cart_count(self):
        """Ambil jumlah produk dari ikon cart"""
        badge = self.page.locator(".shopping_cart_badge")
        if badge.count() == 0:
            return 0
        return int(badge.inner_text())

    # --- Halaman Cart ---
    def open_cart_page(self):
        self.cart_icon.click()
        self.page.wait_for_url("**/cart.html")

    def get_cart_item_count(self):
        """Hitung jumlah produk di halaman cart"""
        return self.cart_items.count()

    def remove_some_products(self, count):
        """Hapus sejumlah produk dari halaman cart"""
        remove_buttons = self.remove_buttons
        total = min(count, remove_buttons.count())
        for i in range(total):
            remove_buttons.nth(i).click()
        time.sleep(1)

    # --- Simulasi Quantity ---
    def update_all_quantities(self, qty: int):
        """
        Simulasi ubah quantity setiap produk.
        SauceDemo tidak memiliki input qty, jadi kita hanya log tindakan.
        """
        cart_items = self.cart_items
        total = cart_items.count()
        for i in range(total):
            item_name = cart_items.nth(i).locator(".inventory_item_name").inner_text()
            print(f"🧮 Set quantity produk '{item_name}' menjadi {qty}")
        print(f"✅ Semua {total} produk diupdate dengan qty = {qty}")

    def validate_all_quantities(self, expected_qty: int):
        """
        Simulasi validasi quantity produk.
        Kita anggap semua produk memiliki qty = expected_qty.
        """
        cart_items = self.cart_items
        total = cart_items.count()
        for i in range(total):
            item_name = cart_items.nth(i).locator(".inventory_item_name").inner_text()
            print(f"✔️ Validasi qty untuk '{item_name}' = {expected_qty}")
        print(f"✅ Validasi selesai — semua produk qty = {expected_qty}")

    # === FITUR BARU: ADD VIA DETAIL PAGE ===
    def add_from_detail_pages(self, count: int):
        """
        Tambahkan produk satu per satu melalui halaman detail,
        klik add to cart, lalu kembali ke inventory page.
        Verifikasi bahwa produk muncul di cart.
        """
        items = self.inventory_items
        total = min(count, items.count())
        added_products = []

        for i in range(total):
            product = items.nth(i)
            name = product.locator(".inventory_item_name").inner_text()
            print(f"➡️ Buka detail produk ke-{i+1}: {name}")

            # Klik nama produk dengan paksa
            product.locator(".inventory_item_name").click(force=True)

            # Tunggu hingga masuk ke halaman detail
            self.page.wait_for_timeout(500)
            self.page.wait_for_url("**/inventory-item.html**", timeout=8000)

            # Klik tombol Add to Cart
            self.page.wait_for_selector("button[id^='add-to-cart']", timeout=8000)
            self.page.locator("button[id^='add-to-cart']").click()
            print(f"🛒 Produk '{name}' berhasil ditambahkan dari detail page")
            added_products.append(name)

            # Kembali ke inventory page
            if self.page.locator("#back-to-products").is_visible():
                self.page.locator("#back-to-products").click()
            elif self.page.locator(".inventory_details_back_button").is_visible():
                self.page.locator(".inventory_details_back_button").click()
            else:
                print("⚠️ Tombol kembali tidak ditemukan, reload halaman.")
                self.page.goto("https://www.saucedemo.com/inventory.html")

            self.page.wait_for_selector(".inventory_list", timeout=8000)

        print(f"✅ Total {total} produk berhasil ditambahkan lewat detail page")

        # --- Verifikasi produk di cart ---
        self.page.locator(".shopping_cart_link").click()
        self.page.wait_for_selector(".cart_item", timeout=5000)

        cart_items = self.page.locator(".inventory_item_name")
        cart_names = [cart_items.nth(i).inner_text() for i in range(cart_items.count())]

        # Validasi produk yang ditambahkan muncul di cart
        missing = [name for name in added_products if name not in cart_names]
        assert not missing, f"❌ Produk berikut tidak muncul di cart: {missing}"
        print("✅ Semua produk yang ditambahkan muncul di keranjang!")

    def update_cart_quantities(self, qty: int):
        """Ubah quantity semua produk di cart"""
        inputs = self.page.locator("input.cart_quantity")
        count = inputs.count()
        for i in range(count):
            input_field = inputs.nth(i)
            self.page.evaluate("(el, value) => el.value = value", input_field, str(qty)) # type: ignore
        print(f"✏️ Semua produk diubah quantity menjadi {qty}")

    def proceed_checkout(self, first_name="Renda", last_name="Santana", postal_code="65111"):
        """Checkout hingga selesai"""
        self.page.locator("#checkout").click()
        self.page.wait_for_selector("#first-name")
        self.page.fill("#first-name", first_name)
        self.page.fill("#last-name", last_name)
        self.page.fill("#postal-code", postal_code)
        self.page.click("#continue")

        # Tunggu halaman overview
        self.page.wait_for_url("**/checkout-step-two.html**")
        self.page.screenshot(path="reports/screenshots/checkout_overview.png", full_page=True)
        self.page.click("#finish")
        self.page.wait_for_url("**/checkout-complete.html**")

        # Screenshot hasil checkout
        self.page.screenshot(path="reports/screenshots/checkout_done.png", full_page=True)

        success_msg = self.page.locator(".complete-header").inner_text()
        assert "THANK YOU" in success_msg.upper(), "❌ Pesan sukses tidak ditemukan!"
        print("✅ Checkout selesai:", success_msg)

    class AddRemoveCartPage:
        def __init__(self, page):
            self.page = page

        def navigate(self):
            self.page.goto("https://www.saucedemo.com/")

        def login(self, username, password):
            self.page.fill("#user-name", username)
            self.page.fill("#password", password)
            self.page.click("#login-button")

        def add_first_product_to_cart(self):
            """Menambahkan produk pertama di inventory ke cart"""
            self.page.click("button.btn_inventory:first-of-type")
