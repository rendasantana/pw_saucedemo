import pytest
import logging
from pages.add_remove_cart_page import AddRemoveCartPage


@pytest.mark.parametrize("username,password", [
    ("standard_user", "secret_sauce"),
])
def test_add_products_via_detail_page(page, username, password):
    """🧩 Test Pro: Tambahkan 6 produk melalui halaman detail"""
    logger = logging.getLogger("test_add_products_via_detail_page")
    cart = AddRemoveCartPage(page)

    logger.info("🔹 Buka halaman login SauceDemo")
    cart.navigate()
    cart.login(username, password)

    logger.info("🧭 Tambahkan produk melalui detail page (1 per 1)")
    cart.add_from_detail_pages(6)

    total = cart.get_cart_count()
    logger.info(f"✅ Total produk di cart: {total}")
    assert total == 6, f"❌ Jumlah produk di cart tidak sesuai, seharusnya 6 tapi dapat {total}"
