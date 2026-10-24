from behave import then, when
from selenium.common.exceptions import TimeoutException

from helpers.session import ensure_logged_in
from pages.account_page import AccountPage
from pages.edit_account_page import EditAccountPage


def account(context) -> AccountPage:
    return AccountPage(context.browser, context.settings.base_url)


def edit_page(context) -> EditAccountPage:
    return EditAccountPage(context.browser, context.settings.base_url)


def restore_profile(context):
    ensure_logged_in(context)
    page = edit_page(context).open()
    if page.read_profile() != context.profile_baseline:
        page.fill(context.profile_baseline)
        page.submit()
        page.wait.until(lambda d: "route=account/account" in d.current_url)


@when("I click Edit Account and record PROFILE_BASELINE")
def step_record_baseline(context):
    account(context).open_edit_account()
    page = edit_page(context).wait_until_loaded()
    context.profile_baseline = page.read_profile()
    context.add_cleanup(restore_profile, context)
    assert context.profile_baseline["E-Mail"] == context.settings.test_email, (
        "The account email differs from TEST_EMAIL."
    )
    assert all(context.profile_baseline.values()), f"A saved value is empty: {list(context.profile_baseline)}"


@when("I click Edit Account")
def step_click_edit_account(context):
    account(context).open_edit_account()
    edit_page(context).wait_until_loaded()


@when("I enter the following profile values:")
def step_enter_profile(context):
    context.entered = {row["Field"]: row["Value"] for row in context.table}
    edit_page(context).fill(context.entered)


@then("only the entered fields should differ from PROFILE_BASELINE")
def step_only_entered_differ(context):
    current = edit_page(context).read_profile()
    differing = {name for name, value in current.items() if value != context.profile_baseline[name]}
    expected = {name for name, value in context.entered.items() if value != context.profile_baseline[name]}
    assert differing == expected, f"Fields differing from the baseline: {differing}, expected {expected}"


@when("I click Continue on the profile form")
def step_submit_profile(context):
    edit_page(context).submit()


@then("My Account should open after the save")
def step_account_opens(context):
    account(context).wait.until(lambda d: "route=account/account" in d.current_url)


@then("the saved profile should equal PROFILE_BASELINE with the entered values applied")
def step_profile_with_changes(context):
    expected = {**context.profile_baseline, **context.entered}
    actual = edit_page(context).read_profile()
    assert actual == expected, f"Saved profile differs. Expected {expected}, found {actual}."


@then("the saved profile should equal PROFILE_BASELINE")
@then("all PROFILE_BASELINE values should be present")
def step_profile_is_baseline(context):
    actual = edit_page(context).read_profile()
    assert actual == context.profile_baseline, (
        f"Profile differs from PROFILE_BASELINE. Expected {context.profile_baseline}, found {actual}."
    )


@when("I restore all PROFILE_BASELINE values and click Continue")
def step_restore_baseline(context):
    page = edit_page(context)
    page.fill(context.profile_baseline)
    page.submit()
    page.wait.until(lambda d: "route=account/account" in d.current_url)


@when("I reload Edit Account")
def step_reload_edit(context):
    edit_page(context).reload()


@then("the Edit Account form should remain open")
def step_edit_form_open(context):
    page = edit_page(context)
    try:
        page.wait.until(lambda d: page.is_open() and page.has_validation_errors())
    except TimeoutException:
        pass
    assert page.is_open(), "The Edit Account form was left."


@then("Chrome should block submission at the E-Mail field")
def step_native_email_block(context):
    page = edit_page(context)
    assert page.is_open(), "The form was submitted."
    assert not page.is_field_valid("E-Mail"), "The E-Mail control is considered valid."
    context.native_message = page.native_validation_message("E-Mail")
    assert context.native_message, "Chrome showed no native email feedback."
    page.show_native_validation("E-Mail")
