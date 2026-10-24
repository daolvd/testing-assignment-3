from behave import then

from pages.address_book_page import AddressBookPage
from pages.edit_account_page import EditAccountPage


@then("the validation beside {field} should identify it as invalid")
def step_field_invalid(context, field):
    if "route=account/edit" in context.browser.current_url:
        message = EditAccountPage(context.browser, context.settings.base_url).wait_for_field_error(field)
    else:
        message = AddressBookPage(context.browser, context.settings.base_url).address_field_error(field)
    assert message, f"No validation text beside {field}."
