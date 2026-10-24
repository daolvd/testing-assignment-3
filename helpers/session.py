from helpers.browser_factory import create_browser
from pages.account_page import AccountPage
from pages.login_page import LoginPage


def login(context):
    settings = context.settings
    page = LoginPage(context.browser, settings.base_url).open()
    page.login(settings.test_email, settings.test_password)
    assert page.wait_for_result(), f"Login failed: {page.error_messages()}"


def restart_browser(context):
    context.browser.quit()
    context.browser = create_browser(context.settings)


def ensure_logged_in(context):
    account = AccountPage(context.browser, context.settings.base_url).open()
    if not account.is_logged_in():
        login(context)
