from behave import given, then, when

from pages.home_page import HomePage
from pages.product_details_page import ProductDetailsPage
from pages.product_not_found_page import ProductNotFoundPage
from pages.product_list_page import ProductListPage


def home(context) -> HomePage:
    return HomePage(context.browser, context.settings.base_url)


def product(context) -> ProductDetailsPage:
    return ProductDetailsPage(context.browser, context.settings.base_url)


def product_list(context) -> ProductListPage:
    return ProductListPage(context.browser, context.settings.base_url)


def snapshot(context) -> dict:
    page = product(context)
    return {
        "heading": page.heading(),
        "product_id": page.product_id(),
        "brand": page.brand(),
        "availability": page.availability(),
        "price": page.price(),
        "image_loaded": page.main_image_loaded(),
        "description": page.description(),
    }


@given("I am a guest on the Home page with US Dollar selected")
def step_guest_home(context):
    page = home(context).open()
    page.select_us_dollar()
    assert page.currency_symbol() == "$", f"US Dollar is not selected: {page.currency_symbol()!r}"


@when("I search for {term}")
def step_search(context, term):
    home(context).search(term)
    product_list(context).wait_until_loaded()


@when("I open the {menu} menu and click Show All {menu_again}")
def step_show_all(context, menu, menu_again):
    page = home(context)
    page.open_menu(menu)
    page.click_menu_link(f"Show All {menu_again}")
    product_list(context).wait_until_loaded()


@then("the search results should contain an {name} card for product ID {product_id}")
@then("the category listing should contain a {name} card for product ID {product_id}")
@then("the category listing should contain an {name} card for product ID {product_id}")
def step_card_present(context, name, product_id):
    actual = product_list(context).product_id_of(name)
    assert actual == product_id, f"Card {name!r} has product ID {actual!r}, expected {product_id}."


@when("I open the product card named {name}")
def step_open_card(context, name):
    product_list(context).open_product(name)
    product(context).wait_until_loaded()


@then("the details page should show the heading {name} for product ID {product_id}")
def step_details_heading(context, name, product_id):
    page = product(context)
    assert page.heading() == name, f"Heading is {page.heading()!r}, expected {name!r}."
    assert page.product_id() == product_id, f"Product ID is {page.product_id()!r}, expected {product_id}."


@then("the product details should show:")
def step_details_table(context):
    page = product(context)
    readers = {
        "Brand": page.brand,
        "Availability": page.availability,
        "Price": page.price,
        "Ex Tax": page.ex_tax,
    }
    for row in context.table:
        actual = readers[row["Detail"]]()
        assert actual == row["Value"], f"{row['Detail']} is {actual!r}, expected {row['Value']!r}."
    context.snapshot_before = snapshot(context)


@when("I open the main product image and close the image viewer")
def step_image_viewer(context):
    page = product(context)
    page.open_image_viewer()
    context.viewer_loaded = page.viewer_image_loaded()
    page.close_image_viewer()


@then("the enlarged image should load and the viewer should close on the same product")
def step_viewer_result(context):
    assert context.viewer_loaded, "The enlarged image did not load."
    assert product(context).heading() == context.snapshot_before["heading"], "The product changed."


@then("the Description tab should show a non-empty description")
def step_description_present(context):
    assert product(context).description(), "The description is empty."


@then("the main image should be loaded and the Description tab should be readable")
def step_image_and_description(context):
    page = product(context)
    assert page.main_image_loaded(), "The main image did not load."
    assert len(page.description()) > 20, "The description is not readable."


@when("I reload the product page")
def step_reload_product(context):
    product(context).reload()


@then("the product information and image should be unchanged after the reload")
def step_unchanged_after_reload(context):
    after = snapshot(context)
    assert after == context.snapshot_before, f"Product changed after reload: {context.snapshot_before} -> {after}"


def not_found(context) -> ProductNotFoundPage:
    return ProductNotFoundPage(context.browser, context.settings.base_url)


@when("I open the product page for product ID {product_id}")
def step_open_missing_product(context, product_id):
    not_found(context).open(product_id)


@then("the page should state {message}")
def step_not_found_message(context, message):
    page = not_found(context)
    assert page.message() == message, f"The page states {page.message()!r}, expected {message!r}."


@then("no product details should be shown")
def step_no_product_details(context):
    page = not_found(context)
    assert not page.heading(), f"A product heading is shown: {page.heading()!r}."
    assert not page.shows_product_details(), "Product controls are displayed on the not-found page."


@when("I click Continue on the not-found page")
def step_continue_not_found(context):
    not_found(context).click_continue()


@then("the Home page should open")
def step_home_opens(context):
    assert "route=common/home" in context.browser.current_url, f"Opened {context.browser.current_url}."
