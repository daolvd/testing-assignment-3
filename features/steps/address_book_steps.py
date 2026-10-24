import re
from uuid import uuid4

from behave import given, then, when
from selenium.common.exceptions import TimeoutException

from helpers.session import ensure_logged_in
from pages.account_page import AccountPage
from pages.address_book_page import AddressBookPage

RUN_ID = uuid4().hex[:6]
MARKER = re.compile(r"M3-[A-Za-z0-9]+-T001S\d")

BASELINE = {
    "First Name": "Alex", "Last Name": "Nguyen", "Company": "",
    "Address 1": "1 Baseline Street", "Address 2": "", "City": "Sydney",
    "Postcode": "2000", "Country": "Australia", "Region / State": "New South Wales",
    "Default": "Yes",
}


def address_book(context) -> AddressBookPage:
    return AddressBookPage(context.browser, context.settings.base_url)


def entered_address(context) -> dict:
    for step in context.scenario.steps:
        if step.table is not None and "enter the following address" in step.name:
            return {row["Field"]: row["Value"].replace("-RUN-", f"-{RUN_ID}-") for row in step.table}
    raise AssertionError("This scenario has no address table.")


def remove_marked_addresses(context):
    ensure_logged_in(context)
    page = address_book(context).open_page()
    for entry in page.entries():
        if context.marker in entry["text"]:
            page.delete(entry["id"])


@given("the default baseline address exists")
def step_baseline(context):
    page = address_book(context).open_page()
    if not page.entries():
        page.click_new_address()
        page.fill_form(BASELINE)
        page.submit()
        page.success_message()
        page.open_page()
    default_id = page.default_address_id()
    if default_id is None:
        context.scenario.skip("Blocked: Address Book has no default baseline address.")
        return
    context.baseline_id = default_id


@when("I click Address Book on My Account and record the existing addresses")
def step_open_and_record(context):
    AccountPage(context.browser, context.settings.base_url).open().open_address_book()
    context.before_entries = address_book(context).entries()


@then("the baseline should be present and no address should contain the scenario marker")
def step_baseline_present(context):
    context.address = entered_address(context)
    context.marker = MARKER.search(context.address["Address 1"]).group(0)
    context.add_cleanup(remove_marked_addresses, context)
    ids = [e["id"] for e in context.before_entries]
    assert context.baseline_id in ids, "The baseline address is missing."
    assert not [e for e in context.before_entries if context.marker in e["text"]], (
        f"Marker {context.marker} is already in Address Book."
    )


@when("I click New Address")
def step_new_address(context):
    address_book(context).click_new_address()


@when("I enter the following address:")
def step_enter_address(context):
    address_book(context).fill_form(context.address)


@when("I click Continue on the address form")
def step_continue(context):
    address_book(context).submit()


@then("the address list should open without validation errors")
def step_list_opens(context):
    page = address_book(context)
    page.wait.until(lambda d: "address/add" not in d.current_url or page.error_messages())
    assert not page.error_messages(), f"Validation errors: {page.error_messages()}"


@then("the Add Address form should remain open")
def step_form_remains(context):
    page = address_book(context)
    try:
        page.wait.until(lambda d: page.error_messages())
    except TimeoutException:
        pass
    assert "address/add" in context.browser.current_url, "The form was left."
    assert page.error_messages(), "No validation is displayed."
    assert not page.has_success_alert(), "A success message appeared."
