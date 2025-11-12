import pytest
import logging
from pages.login_page import LoginPage

# Logger global fallback
logger = logging.getLogger(__name__)

@pytest.mark.parametrize("data", [
    {"username": "standard_user", "password": "secret_sauce", "expected_result": "success"},
    {"username": "invalid_user", "password": "secret_sauce", "expected_result": "fail"},
    {"username": "standard_user", "password": "wrong_pass", "expected_result": "fail"}
])
def test_login_saucedemo(record_page, per_test_logger, data):
    """
    💡 Login test (Data Driven) - hasil lengkap akan masuk HTML report
    """
    log = per_test_logger  # gunakan logger per test
    login = LoginPage(record_page)

    log.info(f"🔹 Testing login dengan: {data}")

    # 1️⃣ Navigate ke halaman login
    login.navigate()

    # 2️⃣ Input username & password
    login.login(data["username"], data["password"])

    # 3️⃣ Validasi hasil
    if data["expected_result"] == "success":
        assert login.is_login_successful(), "Login seharusnya berhasil!"
        log.info(f"✅ Login sukses untuk user: {data['username']}")
    else:
        error_text = login.get_error_message()
        assert "Epic sadface" in error_text, "Pesan error tidak sesuai!"
        log.warning(f"⚠️ Login gagal sesuai ekspektasi: {error_text}")

    # 4️⃣ Tambahkan catatan penutup
    log.info("📋 Test selesai untuk satu kombinasi data.")



def test_dummy_video_check(record_page, per_test_logger, browser_name):
    """
    🎥 Tes dummy hanya untuk memverifikasi perekaman video berjalan.
    """
    log = per_test_logger
    log.info(f"Memulai dummy test untuk {browser_name}")

    record_page.goto("https://www.saucedemo.com/")
    record_page.wait_for_timeout(2000)
    log.info("Menunggu sebentar agar video tidak kosong...")

    assert record_page.title() == "Swag Labs"
    log.info("✅ Dummy video test sukses!")
