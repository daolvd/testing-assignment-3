from urllib.parse import parse_qs, urlsplit

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

from pages.base_page import BasePage


class AddressBookPage(BasePage):
    FIRST_NAME = (By.ID, "input-firstname")
    LAST_NAME = (By.ID, "input-lastname")
    COMPANY = (By.ID, "input-company")
    ADDRESS_1 = (By.ID, "input-address-1")
    ADDRESS_2 = (By.ID, "input-address-2")
    CITY = (By.ID, "input-city")
    POSTCODE = (By.ID, "input-postcode")
    COUNTRY = (By.ID, "input-country")
    REGION = (By.ID, "input-zone")
    NEW_ADDRESS = (By.CSS_SELECTOR, "#content a[href*='account/address/add']")
    DEFAULT_YES = (By.CSS_SELECTOR, "input[name='default'][value='1']")
    DEFAULT_NO = (By.CSS_SELECTOR, "input[name='default'][value='0']")
    SUBMIT = (By.CSS_SELECTOR, "#content input[type='submit'][value='Continue']")
    HEADING = (By.CSS_SELECTOR, "#content h2")

    TEXT_FIELDS = {
        "First Name": FIRST_NAME,
        "Last Name": LAST_NAME,
        "Company": COMPANY,
        "Address 1": ADDRESS_1,
        "Address 2": ADDRESS_2,
        "City": CITY,
        "Postcode": POSTCODE,
    }

    def open_page(self) -> "AddressBookPage":
        self.driver.get(self.url_for("account/address"))
        return self

    def entries(self) -> list[dict]:
        result = []
        for row in self.driver.find_elements(By.CSS_SELECTOR, "#content table tbody tr"):
            href = row.find_element(By.CSS_SELECTOR, "a[href*='address/edit']").get_attribute("href")
            address_id = parse_qs(urlsplit(href).query)["address_id"][0]
            text = " ".join(row.find_element(By.CSS_SELECTOR, "td").text.split())
            result.append({"id": address_id, "text": text})
        return result

    def default_address_id(self) -> str | None:
        default_id = None
        for entry in self.entries():
            self.open_edit(entry["id"])
            if self.driver.find_element(*self.DEFAULT_YES).is_selected():
                default_id = entry["id"]
                break
        self.open_page()
        return default_id

    def click_new_address(self) -> None:
        self.wait.until(EC.element_to_be_clickable(self.NEW_ADDRESS)).click()
        self.wait.until(EC.visibility_of_element_located(self.FIRST_NAME))

    def open_edit(self, address_id: str) -> None:
        self.driver.get(self.url_for("account/address/edit", f"address_id={address_id}"))
        self.wait.until(EC.visibility_of_element_located(self.FIRST_NAME))

    def delete(self, address_id: str) -> None:
        self.driver.get(self.url_for("account/address/delete", f"address_id={address_id}"))
        self.wait.until(EC.visibility_of_element_located(self.HEADING))

    def fill_form(self, data: dict) -> None:
        for name, locator in self.TEXT_FIELDS.items():
            if name in data:
                self.type_into(locator, data[name])
        if "Country" in data:
            self.select_option(self.COUNTRY, data["Country"])
        if "Region / State" in data:
            region = data["Region / State"]
            self.wait.until(lambda d: region in [o.text for o in Select(d.find_element(*self.REGION)).options])
            self.select_option(self.REGION, region)
        if "Default" in data:
            yes = data["Default"].strip().lower() == "yes"
            self.driver.find_element(*(self.DEFAULT_YES if yes else self.DEFAULT_NO)).click()

    def submit(self) -> None:
        self.scroll_and_click(self.SUBMIT)

    def success_message(self) -> str:
        return self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".alert-success"))).text.strip()

    def error_messages(self) -> list[str]:
        return self.texts(".text-danger, .alert-danger")

    def has_success_alert(self) -> bool:
        return bool(self.driver.find_elements(By.CSS_SELECTOR, ".alert-success"))

    def address_field_error(self, field_name: str) -> str:
        return self.field_error(self.TEXT_FIELDS[field_name])
