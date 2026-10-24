from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage


class HomePage(BasePage):
    CURRENCY_TOGGLE = (By.CSS_SELECTOR, "#form-currency .dropdown-toggle")
    CURRENCY_SYMBOL = (By.CSS_SELECTOR, "#form-currency .dropdown-toggle strong")
    US_DOLLAR = (By.CSS_SELECTOR, "#form-currency button[name='USD']")
    SEARCH_BOX = (By.CSS_SELECTOR, "#search input[name='search']")
    SEARCH_BUTTON = (By.CSS_SELECTOR, "#search button")
    MENU = (By.CSS_SELECTOR, "#menu .nav > li > a.dropdown-toggle")

    def open(self) -> "HomePage":
        self.driver.get(self.url_for("common/home"))
        self.wait.until(EC.visibility_of_element_located(self.SEARCH_BOX))
        return self

    def select_us_dollar(self) -> None:
        if self.currency_symbol() == "$":
            return
        page = self.driver.find_element(By.TAG_NAME, "html")
        self.wait.until(EC.element_to_be_clickable(self.CURRENCY_TOGGLE)).click()
        self.wait.until(EC.element_to_be_clickable(self.US_DOLLAR)).click()
        self.wait.until(EC.staleness_of(page))
        self.wait.until(EC.visibility_of_element_located(self.SEARCH_BOX))

    def currency_symbol(self) -> str:
        return self.driver.find_element(*self.CURRENCY_SYMBOL).text.strip()

    def search(self, term: str) -> None:
        self.type_into(self.SEARCH_BOX, term)
        self.driver.find_element(*self.SEARCH_BUTTON).click()
        self.wait.until(EC.url_contains("route=product/search"))

    def open_menu(self, menu_name: str) -> None:
        for link in self.driver.find_elements(*self.MENU):
            if link.text.strip() == menu_name:
                link.click()
                return
        raise AssertionError(f"Menu {menu_name!r} not found.")

    def click_menu_link(self, text: str) -> None:
        link = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, f"//*[@id='menu']//*[contains(@class,'dropdown-menu')]//a[starts-with(normalize-space(.), {text!r})]")
            )
        )
        link.click()
        self.wait.until(EC.url_contains("route=product/category"))
