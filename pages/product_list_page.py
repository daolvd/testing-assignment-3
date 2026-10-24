from urllib.parse import parse_qs, urlsplit

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage


class ProductListPage(BasePage):
    CARD_LINKS = (By.CSS_SELECTOR, ".product-thumb h4 a")

    def wait_until_loaded(self) -> "ProductListPage":
        self.wait.until(EC.presence_of_element_located(self.CARD_LINKS))
        return self

    def cards(self) -> dict:
        found = {}
        for link in self.driver.find_elements(*self.CARD_LINKS):
            query = parse_qs(urlsplit(link.get_attribute("href")).query)
            found[link.text.strip()] = query.get("product_id", [""])[0]
        return found

    def product_id_of(self, name: str) -> str | None:
        return self.cards().get(name)

    def open_product(self, name: str) -> None:
        for link in self.driver.find_elements(*self.CARD_LINKS):
            if link.text.strip() == name:
                link.click()
                self.wait.until(EC.url_contains("route=product/product"))
                return
        raise AssertionError(f"No product card named {name!r}.")
