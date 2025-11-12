from playwright.sync_api import Page

class InventoryPage:
    def __init__(self, page: Page):
        self.page = page
        self.logo = self.page.locator(".app_logo")
        self.burger_menu = self.page.locator("#react-burger-menu-btn")
        self.cart_icon = self.page.locator(".shopping_cart_link")
        self.inventory_items = self.page.locator(".inventory_item")
        self.first_item = self.page.locator(".inventory_item_name").first
        self.back_button = self.page.locator("#back-to-products")

    def is_on_page(self):
        return "inventory.html" in self.page.url and self.logo.is_visible()

    def get_total_products(self):
        return self.inventory_items.count()

    def open_first_product(self):
        self.first_item.click()

    def is_detail_page(self):
        return self.back_button.is_visible()
