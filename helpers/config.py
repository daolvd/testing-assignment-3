"""Load project settings without overwriting exported environment variables."""

import os
from dataclasses import dataclass, field
from pathlib import Path
from urllib.parse import urlsplit

from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_BASE_URL = (
    "https://ecommerce-playground.lambdatest.io/index.php?route=common/home"
)


@dataclass(frozen=True)
class Settings:
    base_url: str
    browser: str
    headless: bool
    test_email: str = field(repr=False)
    test_password: str = field(repr=False)


def load_config() -> Settings:
    load_dotenv(PROJECT_ROOT / ".env", override=False)
    base_url = os.getenv("BASE_URL", DEFAULT_BASE_URL).strip()
    url = urlsplit(base_url)
    if url.scheme not in {"http", "https"} or not url.netloc:
        raise ValueError("BASE_URL must be an absolute HTTP or HTTPS URL.")

    browser = os.getenv("BROWSER", "chrome").strip().lower()
    if browser != "chrome":
        raise ValueError("BROWSER must be chrome; only Chrome is supported.")

    headless = os.getenv("HEADLESS", "false").strip().lower()
    if headless not in {"true", "false"}:
        raise ValueError("HEADLESS must be true or false.")

    return Settings(
        base_url=base_url,
        browser=browser,
        headless=headless == "true",
        test_email=os.getenv("TEST_EMAIL", ""),
        test_password=os.getenv("TEST_PASSWORD", ""),
    )
