import pytest
import logging
from pages.add_remove_cart_page import AddRemoveCartPage

@pytest.mark.parametrize("username,password", [
    ("standard_user", "secret_sauce"),
])
def test_add_and_remove_cart(page, username, password):
    """🛒 Test Pro: Tambah & Hapus produk dari Cart"""
    logger = logging.getLogger("test_add_and_remove_cart")
    cart = AddRemoveCartPage(page)

    logger.info("🔹 Navigasi ke halaman login")
    cart.navigate()

    logger.info("🔹 Login dengan akun valid")
    cart.login(username, password)

    logger.info("🔹 Tambahkan produk pertama ke keranjang")
    cart.add_first_product_to_cart()
    count = cart.get_cart_count()
    assert count == 1, f"❌ Gagal menambah produk, cart count: {count}"

    logger.info("✅ Produk berhasil ditambahkan ke keranjang")

    logger.info("🔹 Buka halaman cart")
    cart.open_cart_page()

    logger.info("🔹 Hapus produk dari cart")
    cart.remove_product_from_cart()

    logger.info("🔹 Validasi cart kembali kosong")
    count_after = cart.get_cart_count()
    assert count_after == 0, f"❌ Produk belum terhapus, cart count: {count_after}"

    logger.info("✅ Produk berhasil dihapus dari cart!")
