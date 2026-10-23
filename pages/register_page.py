"""Page object for the OpenCart account registration form."""

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

REGISTER_URL = "https://opencart.abstracta.us/index.php?route=account/register"


class RegisterPage:
    FIRST_NAME = (By.ID, "input-firstname")
    LAST_NAME = (By.ID, "input-lastname")
    EMAIL = (By.ID, "input-email")
    TELEPHONE = (By.ID, "input-telephone")
    PASSWORD = (By.ID, "input-password")
    CONFIRM = (By.ID, "input-confirm")
    AGREE = (By.NAME, "agree")
    SUBMIT = (By.CSS_SELECTOR, "input[type='submit'][value='Continue']")
    ERRORS = (By.CSS_SELECTOR, ".text-danger, .alert-danger")
    SUCCESS_HEADING = (By.CSS_SELECTOR, "#content h1")

    def __init__(self, driver: WebDriver, timeout: int = 15, url: str = REGISTER_URL):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)
        self.url = url

    def open(self) -> "RegisterPage":
        self.driver.get(self.url)
        self.wait.until(EC.visibility_of_element_located(self.FIRST_NAME))
        return self

    def _type(self, locator, value: str) -> None:
        field = self.wait.until(EC.visibility_of_element_located(locator))
        field.clear()
        field.send_keys(value)

    def register(self, first_name, last_name, email, telephone, password) -> None:
        self._type(self.FIRST_NAME, first_name)
        self._type(self.LAST_NAME, last_name)
        self._type(self.EMAIL, email)
        self._type(self.TELEPHONE, telephone)
        self._type(self.PASSWORD, password)
        self._type(self.CONFIRM, password)
        agree = self.wait.until(EC.presence_of_element_located(self.AGREE))
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", agree)
        if not agree.is_selected():
            agree.click()
        self.wait.until(EC.element_to_be_clickable(self.SUBMIT)).click()

    def error_messages(self) -> list[str]:
        return [e.text for e in self.driver.find_elements(*self.ERRORS) if e.text.strip()]

    def wait_for_result(self) -> bool:
        """Return True once the success page loads, False if the form shows errors."""
        self.wait.until(
            lambda d: "account/success" in d.current_url or self.error_messages()
        )
        return "account/success" in self.driver.current_url
