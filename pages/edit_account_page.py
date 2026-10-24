import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage


class EditAccountPage(BasePage):
    FIELDS = {
        "First Name": (By.ID, "input-firstname"),
        "Last Name": (By.ID, "input-lastname"),
        "E-Mail": (By.ID, "input-email"),
        "Telephone": (By.ID, "input-telephone"),
    }
    CONTINUE = (By.CSS_SELECTOR, "#content input[type='submit'][value='Continue']")

    def open(self) -> "EditAccountPage":
        self.driver.get(self.url_for("account/edit"))
        return self.wait_until_loaded()

    def wait_until_loaded(self) -> "EditAccountPage":
        self.wait.until(EC.visibility_of_element_located(self.FIELDS["First Name"]))
        return self

    def reload(self) -> "EditAccountPage":
        self.driver.refresh()
        return self.wait_until_loaded()

    def read_profile(self) -> dict:
        return {
            name: self.driver.find_element(*locator).get_attribute("value")
            for name, locator in self.FIELDS.items()
        }

    def fill(self, values: dict) -> None:
        for name, value in values.items():
            self.type_into(self.FIELDS[name], value)

    def submit(self) -> None:
        self.scroll_and_click(self.CONTINUE)

    def is_open(self) -> bool:
        return "route=account/edit" in self.driver.current_url and bool(
            self.driver.find_elements(*self.FIELDS["First Name"])
        )

    def has_validation_errors(self) -> bool:
        return bool(self.driver.find_elements(By.CSS_SELECTOR, ".text-danger"))

    def wait_for_field_error(self, name: str) -> str:
        locator = self.FIELDS[name]
        self.wait.until(lambda d: self.field_error(locator))
        return self.field_error(locator)

    def native_validation_message(self, name: str) -> str:
        field = self.driver.find_element(*self.FIELDS[name])
        return self.driver.execute_script("return arguments[0].validationMessage;", field)

    def show_native_validation(self, name: str) -> None:
        """Scroll to the top and show Chrome's validation bubble again so it is visible in evidence."""
        field = self.driver.find_element(*self.FIELDS[name])
        self.driver.execute_script("window.scrollTo(0, 0); arguments[0].focus(); arguments[0].reportValidity();", field)
        time.sleep(0.7)  # the bubble fades in; there is no DOM signal to wait on

    def is_field_valid(self, name: str) -> bool:
        field = self.driver.find_element(*self.FIELDS[name])
        return self.driver.execute_script("return arguments[0].validity.valid;", field)
