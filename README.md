# Member 3 — Selenium + Behave framework

Infrastructure for the LambdaTest eCommerce Playground assignment, using Python
3.11+, Selenium, Behave, and python-dotenv. This workspace was set up with Python
3.12.9. Gherkin feature files are stored under `features/`.

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

## Project structure

```text
assignment3-code/
├── features/
│   ├── address_book.feature       # F3 / T001
│   ├── product_details.feature    # F7 / T002
│   ├── user_account.feature       # F11 / T003 (Edit Account)
│   ├── environment.py             # Behave hooks
│   └── steps/                     # thin step definitions
├── pages/                         # page objects (locators, interactions, waits)
│   └── base_page.py               # shared driver, wait and form helpers
├── helpers/                       # config, browser factory, login/session helpers
├── scripts/register_account.py    # create a fresh test account
├── reports/                       # generated screenshots (ignored by Git)
├── .env.example
├── behave.ini
└── requirements.txt
```

Steps delegate locators and interactions to the page objects in `pages/`, which
all extend `BasePage`. Hooks expose `context.settings`, create a fresh
`context.browser` per scenario and save a PNG under `reports/screenshots/`
after each executed scenario before the registered cleanup quits the browser.

Create a test account with `python -m scripts.register_account --save-env`.

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

## Run

```bash
source .venv/bin/activate
python -m behave --dry-run --no-snippets   # parse only; no browser
HEADLESS=true python -m behave             # live run against the shared demo site
```

A dry run does not execute hooks, launch Chrome, or exercise the application.
