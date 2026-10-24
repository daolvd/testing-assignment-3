from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage


class RegisterPage(BasePage):
    FIRST_NAME = (By.ID, "input-firstname")
    LAST_NAME = (By.ID, "input-lastname")
    EMAIL = (By.ID, "input-email")
    TELEPHONE = (By.ID, "input-telephone")
    PASSWORD = (By.ID, "input-password")
    CONFIRM = (By.ID, "input-confirm")
    AGREE = (By.NAME, "agree")
    SUBMIT = (By.CSS_SELECTOR, "input[type='submit'][value='Continue']")

    def open(self) -> "RegisterPage":
        self.driver.get(self.url_for("account/register"))
        self.wait.until(EC.visibility_of_element_located(self.FIRST_NAME))
        return self

    def register(self, first_name, last_name, email, telephone, password) -> None:
        self.type_into(self.FIRST_NAME, first_name)
        self.type_into(self.LAST_NAME, last_name)
        self.type_into(self.EMAIL, email)
        self.type_into(self.TELEPHONE, telephone)
        self.type_into(self.PASSWORD, password)
        self.type_into(self.CONFIRM, password)
        agree = self.wait.until(EC.presence_of_element_located(self.AGREE))
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", agree)
        if not agree.is_selected():
            agree.click()
        self.wait.until(EC.element_to_be_clickable(self.SUBMIT)).click()

    def error_messages(self) -> list[str]:
        return self.texts(".text-danger, .alert-danger")

    def wait_for_result(self) -> bool:
        """Return True once the success page loads, False if the form shows errors."""
        self.wait.until(lambda d: "account/success" in d.current_url or self.error_messages())
        return "account/success" in self.driver.current_url
