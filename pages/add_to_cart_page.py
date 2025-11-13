from playwright.sync_api import Page

class AddToCartPage:
    def __init__(self, page: Page):
        self.page = page
        self.base_url = "https://www.saucedemo.com/"
        self.username_input = "#user-name"
        self.password_input = "#password"
        self.login_button = "#login-button"
        self.inventory_item = ".inventory_item"
        self.add_to_cart_button = ".btn_inventory"
        self.cart_badge = ".shopping_cart_badge"

    def navigate(self):
        self.page.goto(self.base_url)

    def login(self, username, password):
        self.page.fill(self.username_input, username)
        self.page.fill(self.password_input, password)
        self.page.click(self.login_button)
        self.page.wait_for_url("**/inventory.html")

    def add_first_product_to_cart(self):
        self.page.locator(self.add_to_cart_button).first.click()

    def get_cart_count(self):
        badge = self.page.locator(self.cart_badge)
        return int(badge.inner_text()) if badge.count() > 0 else 0
