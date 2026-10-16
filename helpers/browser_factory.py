"""Create Chrome sessions using Selenium Manager for driver management."""

from selenium import webdriver

from helpers.config import Settings


def create_browser(settings: Settings) -> webdriver.Chrome:
    if settings.browser != "chrome":
        raise ValueError("Only Chrome is supported.")

    options = webdriver.ChromeOptions()
    if settings.headless:
        options.add_argument("--headless=new")
    options.add_argument("--window-size=1440,1000")
    return webdriver.Chrome(options=options)
