import pytest
import logging
from pages.add_remove_cart_page import AddRemoveCartPage

@pytest.mark.parametrize("username,password", [
    ("standard_user", "secret_sauce"),
])
def test_add_products_checkout_flow(page, username, password):
    """🚀 Test Pro Ultra Visual: Tambah produk via detail → ubah qty → checkout"""
    logger = logging.getLogger("test_add_products_checkout_flow")
    cart = AddRemoveCartPage(page)

    logger.info("🔹 Login ke SauceDemo")
    cart.navigate()
    cart.login(username, password)
    page.screenshot(path="reports/screenshots/login_success.png", full_page=True)

    logger.info("🧭 Tambahkan 6 produk lewat halaman detail")
    cart.add_from_detail_pages(6)
    page.screenshot(path="reports/screenshots/add_products_done.png", full_page=True)

    logger.info("🛒 Buka halaman cart dan ubah quantity produk")
    page.locator(".shopping_cart_link").click()
    page.wait_for_selector(".cart_item")
    cart.update_cart_quantities(2)
    page.screenshot(path="reports/screenshots/update_qty_done.png", full_page=True)

    logger.info("💳 Lanjut ke proses checkout")
    cart.proceed_checkout()

    logger.info("✅ Checkout berhasil sampai halaman selesai")
    page.screenshot(path="reports/screenshots/checkout_complete.png", full_page=True)
