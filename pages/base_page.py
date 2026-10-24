from urllib.parse import urlsplit

from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait


class BasePage:
    """Shared driver, wait and form helpers for the OpenCart page objects."""

    def __init__(self, driver: WebDriver, base_url: str, timeout: int = 15):
        parts = urlsplit(base_url)
        self.driver = driver
        self.root = f"{parts.scheme}://{parts.netloc}"
        self.wait = WebDriverWait(
            driver, timeout, ignored_exceptions=(NoSuchElementException, StaleElementReferenceException)
        )

    def url_for(self, route: str, query: str = "") -> str:
        return f"{self.root}/index.php?route={route}" + (f"&{query}" if query else "")

    def type_into(self, locator, value: str) -> WebElement:
        field = self.wait.until(EC.visibility_of_element_located(locator))
        field.clear()
        field.send_keys(value)
        return field

    def select_option(self, locator, visible_text: str) -> None:
        Select(self.wait.until(EC.element_to_be_clickable(locator))).select_by_visible_text(visible_text)

    def scroll_and_click(self, locator) -> None:
        button = self.wait.until(EC.presence_of_element_located(locator))
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", button)
        self.wait.until(EC.element_to_be_clickable(locator)).click()

    def texts(self, css: str) -> list[str]:
        return [e.text.strip() for e in self.driver.find_elements(By.CSS_SELECTOR, css) if e.text.strip()]

    def field_error(self, locator) -> str:
        """Validation text shown in the same form group as the field."""
        group = self.driver.find_element(*locator).find_element(
            By.XPATH, "./ancestor::div[contains(@class,'form-group')][1]"
        )
        return " ".join(e.text.strip() for e in group.find_elements(By.CSS_SELECTOR, ".text-danger") if e.text.strip())
