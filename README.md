# LambdaTest eCommerce Playground: Selenium + Behave tests

Black-box UI tests for the [LambdaTest eCommerce Playground](https://ecommerce-playground.lambdatest.io/)
(an OpenCart demo store), written in Python with Selenium and Behave (Gherkin).
The suite runs against the live site, so results depend on its current catalogue
and availability.

## Test coverage

| Feature | File | Case | Scenarios |
| --- | --- | --- | --- |
| F3 Address Book | `features/address_book.feature` | T001 | S1 valid address saved; S2 empty First Name rejected; S3 empty City rejected |
| F7 Product Details | `features/product_details.feature` | T002 | S1 search and inspect iPhone; S2 browse Laptops and inspect an out-of-stock product; S3 non-existent product ID |
| F11 User Account (Edit Account) | `features/user_account.feature` | T003 | S1 valid details saved; S2 empty Last Name rejected; S3 malformed email blocked |

Every scenario carries tags for its case ID (`@T001-S1`), its output or input
partition (`@OP-*` / `@IP-*`) and its class (`@valid`, `@invalid`, `@edge`).

Scenarios that change account data record a baseline first and restore it
afterwards, so the test account is left as it was found. Address Book scenarios
mark the records they create with a unique per-run id and delete them during
cleanup.

## Requirements

- Python 3.11 or newer (developed on 3.12)
- Google Chrome. Selenium Manager downloads the matching driver automatically,
  so no manual ChromeDriver install is needed. The first run needs internet access.

## Setup

Run from the project root.

```sh
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

## Configuration

Settings are read from `.env` in the project root. Variables already exported in
the shell take precedence over `.env`. `.env.example` lists every variable.

| Variable | Default | Purpose |
| --- | --- | --- |
| `BASE_URL` | LambdaTest Playground home URL | Site under test (the host is used to build all page URLs) |
| `BROWSER` | `chrome` | Only `chrome` is supported |
| `HEADLESS` | `false` | `true` runs Chrome without a window |
| `TEST_EMAIL` | empty | Email of the dedicated test account |
| `TEST_PASSWORD` | empty | Password of the dedicated test account |

**Before running the tests, fill in `TEST_EMAIL` and `TEST_PASSWORD` in `.env`**
with an existing account on the site. The Address Book and Edit Account
scenarios log in with it. If either value is empty, those scenarios are skipped
(Blocked) instead of run. If you have no account, create one with the command
below.

### Creating a test account

To register a new account on the site and write its credentials to `.env`:

```sh
python -m scripts.register_account --save-env
```

Without `--save-env` the account is created but a generated password is not
kept. Optional arguments: `--first-name`, `--last-name`, `--telephone`. If
`TEST_EMAIL` / `TEST_PASSWORD` are already set, they are used for the new account.

## Running the tests

```sh
python -m behave                                  # all features
HEADLESS=true python -m behave                    # without a browser window
python -m behave features/address_book.feature    # one feature
python -m behave -n "T001-S1"                     # one scenario by name
python -m behave --tags=@T003-S2                  # one scenario by tag
python -m behave --tags=@invalid                  # all scenarios of one class
python -m behave --dry-run --no-snippets          # parse only: lists undefined steps, no browser
```

A dry run does not start Chrome or touch the site, so it only proves that the
feature files and step definitions match, not that the tests pass.

Each scenario starts a fresh Chrome session. After every executed scenario a
screenshot is saved with the scenario name and its result in the file name.
Screenshots can contain account data, so review them before sharing.

## Project structure

```text
.
├── features/
│   ├── address_book.feature       # F3 / T001
│   ├── product_details.feature    # F7 / T002
│   ├── user_account.feature       # F11 / T003
│   ├── environment.py             # Behave hooks: settings, browser, screenshots
│   └── steps/                     # step definitions (thin; delegate to pages)
│       ├── address_book_steps.py
│       ├── product_details_steps.py
│       ├── account_steps.py
│       ├── login_steps.py
│       └── validation_steps.py
├── pages/                         # page objects: locators, interactions, waits
│   ├── base_page.py               # shared driver, wait and form helpers
│   ├── account_page.py
│   ├── address_book_page.py
│   ├── edit_account_page.py
│   ├── home_page.py
│   ├── login_page.py
│   ├── product_details_page.py
│   ├── product_list_page.py
│   ├── product_not_found_page.py
│   └── register_page.py
├── helpers/
│   ├── config.py                  # Settings loaded from the environment and .env
│   ├── browser_factory.py         # Chrome construction
│   └── session.py                 # login, ensure_logged_in, restart_browser
├── scripts/register_account.py    # creates a fresh test account
├── behave.ini
├── requirements.txt
├── .env.example
└── .env
```

## Architecture

The code has three layers:

1. **Feature files** describe behaviour in Gherkin.
2. **Step definitions** (`features/steps/`) stay thin. They share state through
   Behave's `context` and call page objects.
3. **Page objects** (`pages/`) hold all locators, interactions and explicit
   Selenium waits. They all extend `BasePage` and are built from
   `(driver, base_url)`.

`features/environment.py` loads the settings once, opens a new browser before
each scenario and registers its shutdown with `context.add_cleanup`, so the
browser closes even when a hook or step fails. `helpers/session.py` provides the
login and "log out, close the browser, log in again" steps used by the
persistence checks.

## Notes

- The site is a shared public demo. If a prerequisite is missing (for example a
  product was removed from the catalogue), treat the scenario as Blocked rather
  than as an application defect.
- Keep scenarios independent and make sure anything they create is removed in
  cleanup.
