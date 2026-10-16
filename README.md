# Member 3 — Selenium + Behave framework

Infrastructure for the LambdaTest eCommerce Playground assignment, using Python
3.11+, Selenium, Behave, and python-dotenv. This workspace was set up with Python
3.12.9. Gherkin feature files are stored under `features/`.
Step definitions and individual page objects have not been implemented.

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

Chrome must be available. `webdriver.Chrome()` uses
[Selenium Manager](https://www.selenium.dev/documentation/selenium_manager/)
to resolve the driver automatically; no manual ChromeDriver installation or
third-party driver manager is needed. Initial driver resolution may require
internet access and a writable Selenium cache.

## Layout and future Page Object Model

```text
features/
├── address_book.feature
├── product_details.feature
├── update_remove_cart.feature
├── environment.py
└── steps/
    └── __init__.py
helpers/
├── __init__.py
├── browser_factory.py
└── config.py
requirements.txt
behave.ini
.env.example
.gitignore
README.md
```

Future step modules will delegate page interactions and locators to a `pages/`
package, created when its first page object is needed. Hooks manage browser
lifecycle; helpers manage configuration and browser construction. Use explicit
Selenium waits in future page objects.

The hooks expose `context.settings` and create a fresh `context.browser` for
each scenario. They do not log in, navigate, or prepare application fixtures.
On failure, a uniquely named PNG is saved under `artifacts/screenshots/` before
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

At this stage, the dry run reports undefined steps and exits nonzero because step definitions are not
implemented. A dry run does not execute hooks, launch Chrome, or exercise the
application. Do not interpret it as a passing test suite. Application scenarios
have not run.
