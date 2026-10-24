from urllib.parse import parse_qs, urlsplit

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage

IMAGE_LOADED = "return arguments[0].complete && arguments[0].naturalWidth > 0;"


class ProductDetailsPage(BasePage):
    HEADING = (By.CSS_SELECTOR, "#content h1")
    MAIN_IMAGE_LINK = (By.CSS_SELECTOR, "ul.thumbnails a.thumbnail")
    MAIN_IMAGE = (By.CSS_SELECTOR, "ul.thumbnails a.thumbnail img")
    VIEWER_IMAGE = (By.CSS_SELECTOR, ".mfp-img")
    VIEWER_CLOSE = (By.CSS_SELECTOR, ".mfp-close")
    DESCRIPTION = (By.ID, "tab-description")
    CART_BUTTON = (By.ID, "button-cart")
    PRICE = (By.XPATH, "//ul[@class='list-unstyled']//h2")
    DETAIL_ITEM = "//ul[@class='list-unstyled']/li[starts-with(normalize-space(.), '{label}')]"

    def wait_until_loaded(self) -> "ProductDetailsPage":
        self.wait.until(EC.visibility_of_element_located(self.HEADING))
        self.wait.until(EC.presence_of_element_located(self.CART_BUTTON))
        return self

    def reload(self) -> "ProductDetailsPage":
        self.driver.refresh()
        return self.wait_until_loaded()

    def heading(self) -> str:
        return self.driver.find_element(*self.HEADING).text.strip()

    def product_id(self) -> str:
        query = parse_qs(urlsplit(self.driver.current_url).query)
        return query.get("product_id", [""])[0]

    def _detail(self, label: str) -> str:
        return self.driver.find_element(By.XPATH, self.DETAIL_ITEM.format(label=label)).text.strip()

    def brand(self) -> str:
        return self._detail("Brand").replace("Brands", "").replace("Brand", "").strip(" :")

    def availability(self) -> str:
        return self._detail("Availability").split(":", 1)[1].strip()

    def price(self) -> str:
        return self.driver.find_element(*self.PRICE).text.strip()

    def ex_tax(self) -> str:
        return self._detail("Ex Tax").split(":", 1)[1].strip()

    def description(self) -> str:
        return self.driver.find_element(*self.DESCRIPTION).text.strip()

    def main_image_loaded(self) -> bool:
        return self.driver.execute_script(IMAGE_LOADED, self.driver.find_element(*self.MAIN_IMAGE))

    def open_image_viewer(self) -> None:
        self.wait.until(EC.element_to_be_clickable(self.MAIN_IMAGE_LINK)).click()
        self.wait.until(EC.visibility_of_element_located(self.VIEWER_IMAGE))

    def viewer_image_loaded(self) -> bool:
        image = self.driver.find_element(*self.VIEWER_IMAGE)
        try:
            self.wait.until(lambda d: d.execute_script(IMAGE_LOADED, image))
        except TimeoutException:
            return False
        return True

    def close_image_viewer(self) -> None:
        self.wait.until(EC.element_to_be_clickable(self.VIEWER_CLOSE)).click()
        self.wait.until(EC.invisibility_of_element_located(self.VIEWER_IMAGE))
