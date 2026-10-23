"""Register a new customer on the OpenCart demo store.

Uses TEST_EMAIL / TEST_PASSWORD when set; otherwise generates a unique email and
random password. With --save-env the credentials are written to the local .env.

Run from the project root:
    .venv/bin/python -m scripts.register_account [--save-env]
"""

import argparse
import re
import secrets
import sys
import time

from helpers.browser_factory import create_browser
from helpers.config import PROJECT_ROOT, load_config
from pages.register_page import RegisterPage

ENV_PATH = PROJECT_ROOT / ".env"


def save_env(email: str, password: str) -> None:
    text = ENV_PATH.read_text() if ENV_PATH.exists() else ""
    for key, value in (("TEST_EMAIL", email), ("TEST_PASSWORD", password)):
        line = f"{key}={value}"
        if re.search(rf"^{key}=.*$", text, flags=re.M):
            text = re.sub(rf"^{key}=.*$", lambda _: line, text, flags=re.M)
        else:
            text += ("" if text.endswith("\n") or not text else "\n") + line + "\n"
    ENV_PATH.write_text(text)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--save-env", action="store_true", help="write credentials to .env")
    parser.add_argument("--first-name", default="Test")
    parser.add_argument("--last-name", default="User")
    parser.add_argument("--telephone", default="0412345678")
    args = parser.parse_args()

    settings = load_config()
    email = settings.test_email or f"qa.{int(time.time())}@example.com"
    password = settings.test_password or secrets.token_urlsafe(12)

    driver = create_browser(settings)
    try:
        page = RegisterPage(driver).open()
        page.register(args.first_name, args.last_name, email, args.telephone, password)
        if not page.wait_for_result():
            print("Registration failed:", *page.error_messages(), sep="\n  ")
            return 1
        print(f"Registered: {email}")
        if args.save_env:
            save_env(email, password)
            print(f"Credentials saved to {ENV_PATH.name}")
        elif not settings.test_password:
            print("Password was generated and not saved; re-run with --save-env.")
        return 0
    finally:
        driver.quit()


if __name__ == "__main__":
    sys.exit(main())
