import pytest
import logging
from pages.add_remove_cart_page import AddRemoveCartPage

@pytest.mark.parametrize("username,password", [
    ("standard_user", "secret_sauce"),
])
def test_add_multiple_and_remove_some(page, username, password):
    """🧩 Test Pro Plus: Tambah beberapa produk & hapus sebagian"""
    logger = logging.getLogger("test_add_multiple_and_remove_some")
    cart = AddRemoveCartPage(page)

    logger.info("🔹 Buka halaman login SauceDemo")
    cart.navigate()

    logger.info("🔹 Login dengan akun valid")
    cart.login(username, password)

    logger.info("🔹 Tambahkan beberapa produk ke keranjang")
    cart.add_multiple_products(4)
    total_items = cart.get_cart_count()
    assert total_items == 4, f"❌ Jumlah produk di cart tidak sesuai, seharusnya 4 tapi dapat {total_items}"
    logger.info(f"✅ {total_items} produk berhasil ditambahkan ke cart")

    logger.info("🔹 Buka halaman cart")
    cart.open_cart_page()

    logger.info("🔹 Hapus 2 produk dari cart")
    cart.remove_some_products(2)

    logger.info("🔹 Validasi jumlah produk setelah penghapusan")
    remaining = cart.get_cart_count()
    assert remaining == 2, f"❌ Setelah hapus 2 produk, seharusnya tersisa 2 tapi ada {remaining}"
    logger.info("✅ Penghapusan sebagian produk berhasil, jumlah akhir sesuai!")
