from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage


class ProductNotFoundPage(BasePage):
    HEADING = (By.CSS_SELECTOR, "#content h1")
    MESSAGE = (By.CSS_SELECTOR, "#content p")
    CONTINUE = (By.CSS_SELECTOR, "#content .buttons a.btn-primary")
    PRODUCT_CONTROLS = (By.CSS_SELECTOR, "#button-cart, ul.thumbnails, .nav-tabs, #input-quantity")

    def open(self, product_id: str) -> "ProductNotFoundPage":
        self.driver.get(self.url_for("product/product", f"product_id={product_id}"))
        self.wait.until(EC.visibility_of_element_located(self.CONTINUE))
        return self

    def message(self) -> str:
        return self.driver.find_element(*self.MESSAGE).text.strip()

    def heading(self) -> str:
        return self.driver.find_element(*self.HEADING).text.strip()

    def shows_product_details(self) -> bool:
        return bool(self.driver.find_elements(*self.PRODUCT_CONTROLS))

    def click_continue(self) -> None:
        self.wait.until(EC.element_to_be_clickable(self.CONTINUE)).click()
        self.wait.until(EC.url_contains("route=common/home"))
