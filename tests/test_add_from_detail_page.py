import pytest
import logging
from pages.add_remove_cart_page import AddRemoveCartPage

@pytest.mark.parametrize("username,password", [
    ("standard_user", "secret_sauce"),
])
def test_add_products_via_detail_page(page, username, password):
    """🧩 Test Pro+: Tambahkan produk lewat halaman detail & verifikasi muncul di cart"""
    logger = logging.getLogger("test_add_products_via_detail_page")
    cart = AddRemoveCartPage(page)

    logger.info("🔹 Buka halaman login SauceDemo")
    cart.navigate()
    cart.login(username, password)

    logger.info("🧭 Tambahkan produk lewat detail page")
    cart.add_from_detail_pages(6)
    logger.info("✅ Semua produk dari detail page diverifikasi di cart")
