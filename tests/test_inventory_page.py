import pytest
import logging
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage

@pytest.mark.smoke
def test_inventory_page(record_page, per_test_logger):
    """💡 Latihan 2 (Pro+): Verifikasi halaman inventory setelah login"""

    page = record_page
    logger = per_test_logger
    login = LoginPage(page)
    inventory = InventoryPage(page)

    logger.info("🔹 Navigasi ke halaman login")
    login.navigate()
    login.login("standard_user", "secret_sauce")

    logger.info("✅ Login berhasil, memverifikasi halaman inventory")
    assert inventory.is_on_page(), "User seharusnya berada di halaman inventory"

    logger.info("🔹 Memeriksa elemen utama halaman")
    assert inventory.logo.is_visible(), "Logo Swag Labs tidak muncul"
    assert inventory.burger_menu.is_visible(), "Tombol menu tidak muncul"
    assert inventory.cart_icon.is_visible(), "Icon keranjang tidak muncul"

    total_products = inventory.get_total_products()
    logger.info(f"📦 Jumlah produk ditemukan: {total_products}")
    assert total_products == 6, f"Jumlah produk tidak sesuai, seharusnya 6 tapi ditemukan {total_products}"

    logger.info("🔹 Membuka detail produk pertama")
    inventory.open_first_product()
    assert inventory.is_detail_page(), "Detail produk tidak terbuka"

    logger.info("✅ Detail produk berhasil dibuka dan tombol back terlihat")
