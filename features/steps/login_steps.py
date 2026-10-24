from behave import given, then, when

from helpers.session import login, restart_browser
from pages.account_page import AccountPage


@given("I am logged in with the dedicated test account")
def step_logged_in(context):
    settings = context.settings
    if not (settings.test_email and settings.test_password):
        context.scenario.skip("Blocked: TEST_EMAIL / TEST_PASSWORD are not configured.")
        return
    login(context)
    account = AccountPage(context.browser, settings.base_url)
    assert account.is_logged_in(), "My Account did not open with authenticated controls."


@when("I log out")
def step_logout(context):
    AccountPage(context.browser, context.settings.base_url).logout()


@when("I log out, close the browser, and log in again in a fresh session")
def step_fresh_login(context):
    AccountPage(context.browser, context.settings.base_url).logout()
    restart_browser(context)
    login(context)
    account = AccountPage(context.browser, context.settings.base_url)
    assert account.is_logged_in(), "A fresh session did not reach My Account."


@then("I should be logged out")
def step_logged_out(context):
    account = AccountPage(context.browser, context.settings.base_url)
    assert account.is_logged_out(), "Logout controls are still visible."
