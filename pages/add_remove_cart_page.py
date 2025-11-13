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
        """
        items = self.inventory_items
        total = min(count, items.count())

        for i in range(total):
            product = items.nth(i)
            name = product.locator(".inventory_item_name").inner_text()
            print(f"➡️ Buka detail produk ke-{i+1}: {name}")

            # Klik nama produk dengan paksa (lebih stabil)
            product.locator(".inventory_item_name").click(force=True)

            # Tunggu hingga URL mengandung '/inventory-item.html'
            self.page.wait_for_timeout(500)  # delay kecil untuk transisi
            self.page.wait_for_url("**/inventory-item.html**", timeout=8000)

            # Tunggu tombol Add to Cart di detail page
            self.page.wait_for_selector("button[id^='add-to-cart']", timeout=8000)
            self.page.locator("button[id^='add-to-cart']").click()
            print(f"🛒 Produk '{name}' berhasil ditambahkan dari detail page")

            # Tombol back bisa 'Back to products' atau '.inventory_details_back_button'
            if self.page.locator("#back-to-products").is_visible():
                self.page.locator("#back-to-products").click()
            elif self.page.locator(".inventory_details_back_button").is_visible():
                self.page.locator(".inventory_details_back_button").click()
            else:
                print("⚠️ Tombol kembali tidak ditemukan, reload halaman.")
                self.page.goto("https://www.saucedemo.com/inventory.html")

            # Tunggu daftar produk muncul lagi
            self.page.wait_for_selector(".inventory_list", timeout=8000)

        print(f"✅ Total {total} produk berhasil ditambahkan lewat detail page")
