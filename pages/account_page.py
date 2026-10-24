from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage


class AccountPage(BasePage):
    ADDRESS_BOOK = (By.CSS_SELECTOR, "#content a[href*='route=account/address']")
    EDIT_ACCOUNT = (By.CSS_SELECTOR, "#content a[href*='route=account/edit']")
    LOGOUT = (By.CSS_SELECTOR, "#column-right a[href*='route=account/logout']")
    HEADING = (By.CSS_SELECTOR, "#content h1, #content h2")

    def open(self) -> "AccountPage":
        self.driver.get(self.url_for("account/account"))
        self.wait.until(EC.visibility_of_element_located(self.HEADING))
        return self

    def is_logged_in(self) -> bool:
        return "route=account/account" in self.driver.current_url and bool(
            self.driver.find_elements(*self.LOGOUT)
        )

    def is_logged_out(self) -> bool:
        return not self.driver.find_elements(*self.LOGOUT)

    def open_address_book(self) -> None:
        self.wait.until(EC.element_to_be_clickable(self.ADDRESS_BOOK)).click()
        self.wait.until(EC.url_contains("route=account/address"))

    def open_edit_account(self) -> None:
        self.wait.until(EC.element_to_be_clickable(self.EDIT_ACCOUNT)).click()
        self.wait.until(EC.url_contains("route=account/edit"))

    def logout(self) -> None:
        self.wait.until(EC.element_to_be_clickable(self.LOGOUT)).click()
        self.wait.until(EC.url_contains("route=account/logout"))
