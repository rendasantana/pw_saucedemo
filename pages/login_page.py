from playwright.sync_api import Page

class LoginPage:
    def __init__(self, page: Page):
        self.page = page
        self.username_input = page.locator("#user-name")
        self.password_input = page.locator("#password")
        self.login_button = page.locator("#login-button")
        self.error_message = page.locator("[data-test='error']")

    def navigate(self):
        self.page.goto("https://www.saucedemo.com/")

    def login(self, username: str, password: str):
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()

    def is_login_successful(self) -> bool:
        """Cek apakah login sukses dengan melihat URL"""
        try:
            self.page.wait_for_url("**/inventory.html", timeout=5000)
            return True
        except:
            return False

    def get_error_message(self) -> str:
        """Ambil pesan error yang muncul saat login gagal"""
        try:
            self.error_message.wait_for(state="visible", timeout=3000)
            return self.error_message.inner_text()
        except:
            return ""
