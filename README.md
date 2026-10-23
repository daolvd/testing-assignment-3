# Member 3 — Selenium + Behave framework

Infrastructure for the LambdaTest eCommerce Playground assignment, using Python
3.11+, Selenium, Behave, and python-dotenv. This workspace was set up with Python
3.12.9. Gherkin feature files are stored under `features/`.
Step modules and page objects are scaffolded; scenario behavior and page-specific
locators and interactions have not been implemented.

## Setup

Run from the project root. Select `.venv/bin/python` with VS Code's
**Python: Select Interpreter** command.

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
cp .env.example .env
```

Python 3.11 or newer may be substituted for `python3.12`. The existing `.venv`
is already installed; only recreate it when needed. `requirements.txt` pins the
installed direct and transitive dependencies.

Edit `.env` locally. Exported environment variables take precedence over `.env`.

| Setting | Default | Purpose |
| --- | --- | --- |
| `BASE_URL` | Store home URL in `.env.example` | Future navigation starting point |
| `BROWSER` | `chrome` | Only Chrome is currently supported |
| `HEADLESS` | `false` | Set to `true` to hide the browser window |
| `TEST_EMAIL` | Empty | Authorised test account for future authenticated cases |
| `TEST_PASSWORD` | Empty | Local test account secret |

Credentials are optional for infrastructure checks. Never commit `.env` or
include passwords in evidence. Screenshots can contain account information;
generated artifacts are ignored by Git.

The local `.env` is configured with a dedicated test account. Account creation,
a fresh login after logout and cookie clearing, and authenticated Address Book
access were verified using Selenium on 16 October 2026.

### Test account login

- Login URL: https://ecommerce-playground.lambdatest.io/index.php?route=account/login
- Username / email: `member3.20261016070221.0fc6d9@example.com`
- Password: `M3!muCcbgfgyDSPgkOyovhDX90k`

These credentials are also configured as `TEST_EMAIL` and `TEST_PASSWORD` in
`.env`. Setup evidence is stored under `artifacts/setup/`. This verifies account
setup only; application scenarios have not been executed.

Chrome must be available. `webdriver.Chrome()` uses
[Selenium Manager](https://www.selenium.dev/documentation/selenium_manager/)
to resolve the driver automatically; no manual ChromeDriver installation or
third-party driver manager is needed. Initial driver resolution may require
internet access and a writable Selenium cache.

## Project structure

```text
assignment3-code/
├── features/                      # BDD scenarios
│   ├── address_book.feature
│   ├── product_details.feature
│   ├── update_remove_cart.feature
│   ├── steps/                     # Step definition scaffolds
│   │   ├── __init__.py
│   │   ├── address_book_steps.py
│   │   ├── product_details_steps.py
│   │   └── cart_steps.py
│   └── environment.py             # Behave lifecycle hooks
├── pages/                         # Page Object Model scaffolds
│   ├── __init__.py
│   ├── base_page.py
│   ├── address_book_page.py
│   ├── product_details_page.py
│   └── cart_page.py
├── helpers/                       # Shared infrastructure
│   ├── __init__.py
│   ├── browser_factory.py
│   └── config.py
├── test_data/                     # Optional test fixtures
│   └── products.json
├── reports/                       # Generated test results (ignored by Git)
│   └── screenshots/
├── .env.example
├── .gitignore
├── behave.ini
├── requirements.txt
└── README.md
```

Step modules will delegate page interactions and locators to the corresponding
page objects in `pages/`. `BasePage` provides the scenario browser and an explicit
Selenium wait. Page-specific classes and step modules are placeholders, with no
scenario behavior yet. `test_data/products.json` starts as an empty object; add
fixtures after verifying their prerequisites. Hooks manage browser lifecycle;
helpers manage configuration and browser construction.

The hooks expose `context.settings` and create a fresh `context.browser` for
each scenario. They do not log in, navigate, or prepare application fixtures.
On failure, a uniquely named PNG is saved under `reports/screenshots/` before
Behave's registered scenario cleanup quits the browser. Screenshot errors are
logged without replacing the original failure. Lifecycle follows the
[Behave hook and cleanup API](https://behave.readthedocs.io/en/stable/api/).

## Infrastructure checks

```bash
source .venv/bin/activate
python -m pip check
python -c "import selenium, behave, dotenv; from helpers.config import load_config; from helpers.browser_factory import create_browser; load_config(); print('Imports and config OK')"
```

Optional browser smoke check, using only a blank page:

```bash
HEADLESS=true python - <<'PY'
from helpers.config import load_config
from helpers.browser_factory import create_browser

browser = create_browser(load_config())
try:
    browser.get('about:blank')
    print('Chrome initialised:', browser.capabilities['browserVersion'])
finally:
    browser.quit()
PY
```

## Check features and run Behave when steps are implemented

```bash
source .venv/bin/activate
python -m behave --dry-run --no-snippets
# Once step definitions and page objects are implemented:
python -m behave
# Optional headless run:
HEADLESS=true python -m behave
```

At this stage, the dry run reports undefined steps and exits nonzero because
step definitions are not implemented. A dry run does not execute hooks, launch Chrome, or exercise the
application. Do not interpret it as a passing test suite. Application scenarios
have not run.
