import pytest
import logging
from pages.add_remove_cart_page import AddRemoveCartPage


@pytest.mark.parametrize("username,password", [
    ("standard_user", "secret_sauce"),
])
def test_add_remove_and_update_qty(page, username, password):
    """🧩 Test Pro Max: Tambah 6 produk, hapus 2, lalu ubah qty jadi 10"""
    logger = logging.getLogger("test_add_remove_and_update_qty")
    cart = AddRemoveCartPage(page)

    logger.info("🔹 Buka halaman login SauceDemo")
    cart.navigate()
    cart.login(username, password)

    logger.info("🛒 Tambahkan 6 produk ke keranjang")
    cart.add_multiple_products(6)
    total_items = cart.get_cart_count()
    assert total_items == 6, f"❌ Jumlah produk tidak sesuai, dapat {total_items}"

    logger.info("🧺 Buka halaman cart dan hapus 2 produk")
    cart.open_cart_page()
    cart.remove_some_products(2)
    remaining = cart.get_cart_item_count()
    assert remaining == 4, f"❌ Setelah hapus 2, seharusnya tersisa 4 tapi {remaining}"

    logger.info("✏️ Ubah quantity setiap produk menjadi 10")
    cart.update_all_quantities(10)
    logger.info("✅ Semua quantity berhasil diubah menjadi 10")

    logger.info("🧾 Validasi bahwa total quantity per produk = 10")
    cart.validate_all_quantities(10)
