from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage


class LoginPage(BasePage):
    EMAIL = (By.ID, "input-email")
    PASSWORD = (By.ID, "input-password")
    SUBMIT = (By.CSS_SELECTOR, "input[type='submit'][value='Login']")

    def open(self) -> "LoginPage":
        self.driver.get(self.url_for("account/login"))
        self.wait.until(EC.visibility_of_element_located(self.EMAIL))
        return self

    def login(self, email: str, password: str) -> None:
        self.type_into(self.EMAIL, email)
        self.type_into(self.PASSWORD, password)
        self.wait.until(EC.element_to_be_clickable(self.SUBMIT)).click()

    def error_messages(self) -> list[str]:
        return self.texts(".alert-danger")

    def wait_for_result(self) -> bool:
        self.wait.until(lambda d: "account/login" not in d.current_url or self.error_messages())
        return "account/login" not in self.driver.current_url
