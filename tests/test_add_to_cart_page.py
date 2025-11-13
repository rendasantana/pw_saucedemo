import pytest
import logging
from pages.add_to_cart_page import AddToCartPage

@pytest.mark.parametrize("username,password", [
    ("standard_user", "secret_sauce"),
])
def test_add_to_cart(page, username, password):
    """🛒 Test Add to Cart - versi standar"""
    logger = logging.getLogger("test_add_to_cart")
    cart = AddToCartPage(page)
    
    logger.info("🔹 Navigasi ke halaman login")
    cart.navigate()

    logger.info("🔹 Login dengan akun valid")
    cart.login(username, password)

    logger.info("🔹 Tambahkan produk ke keranjang")
    cart.add_first_product_to_cart()

    logger.info("🔹 Validasi jumlah item di cart badge")
    count = cart.get_cart_count()
    assert count == 1, f"❌ Jumlah item di cart salah: {count}"

    logger.info("✅ Produk berhasil ditambahkan ke cart!")
