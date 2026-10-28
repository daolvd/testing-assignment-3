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

## Quick start (Automated execution)

The repository provides automated runner scripts that handle everything from zero to test execution on first run (virtual environment, dependencies, `.env`, test account creation, and test execution).

### macOS / Linux / Git Bash

```sh
./run.sh
```

### Windows (Command Prompt / Double-click)

```cmd
run.bat
```

> [!NOTE]
> On the first execution, `run.sh` and `run.bat` automatically:
> 1. Detect Python 3.11+.
> 2. Create and activate `.venv`.
> 3. Install required packages from `requirements.txt`.
> 4. Create `.env` from `.env.example` if it does not exist.
> 5. Automatically provision and save a test account to `.env` if credentials are not configured.
> 6. Launch the Behave test suite.
>
> If you only want to set up the environment without running tests, run `./setup.sh` (macOS/Linux) or `setup.bat` (Windows).

## Manual setup (Alternative)

If you prefer to configure the environment manually:

```sh
python3.12 -m venv .venv
source .venv/bin/activate        # On Windows: .venv\Scripts\activate
python -m pip install -r requirements.txt
cp .env.example .env             # On Windows: copy .env.example .env
python -m scripts.register_account --save-env
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

### Creating a test account manually

To register a new account on the site and write its credentials to `.env`:

```sh
python -m scripts.register_account --save-env
```

Without `--save-env` the account is created but a generated password is not
kept. Optional arguments: `--first-name`, `--last-name`, `--telephone`. If
`TEST_EMAIL` / `TEST_PASSWORD` are already set, they are used for the new account.

## Running tests

You can pass any arguments to `run.sh` / `run.bat` (or `python -m behave`).

### Running independent test cases

| Filter target | macOS / Linux / Git Bash | Windows (CMD) |
| --- | --- | --- |
| **All features** | `./run.sh` | `run.bat` |
| **By scenario tag** | `./run.sh --tags=@T001-S1` | `run.bat --tags=@T001-S1` |
| **By scenario name** | `./run.sh -n "T002-S1"` | `run.bat -n "T002-S1"` |
| **By feature file** | `./run.sh features/product_details.feature` | `run.bat features\product_details.feature` |
| **By exact line** | `./run.sh features/address_book.feature:8` | `run.bat features\address_book.feature:8` |
| **By class tag** | `./run.sh --tags=@valid` | `run.bat --tags=@valid` |
| **Dry run (syntax only)** | `./run.sh --dry-run --no-snippets` | `run.bat --dry-run --no-snippets` |
| **Headless mode** | `HEADLESS=true ./run.sh` | Set `HEADLESS=true` in `.env`, run `run.bat` |

### Available test case IDs

* **F3 Address Book**:
  * `@T001-S1`: Valid address saved and verified after new login.
  * `@T001-S2`: Reject address with empty First Name.
  * `@T001-S3`: Reject address with empty City.
* **F7 Product Details**:
  * `@T002-S1`: Search and inspect iPhone product details.
  * `@T002-S2`: Browse out-of-stock product details.
  * `@T002-S3`: Handle non-existent product ID.
* **F11 User Account (Edit Profile)**:
  * `@T003-S1`: Save valid profile update and verify persistence.
  * `@T003-S2`: Reject update with empty Last Name.
  * `@T003-S3`: Browser HTML5 validation blocks malformed email.

### Manual Behave commands

If your virtual environment is already activated (`source .venv/bin/activate`):

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
screenshot is saved with the scenario name and its result in the file name under
`reports/screenshots/`. Screenshots can contain account data, so review them before sharing.

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
├── run.sh                         # All-in-one runner for macOS / Linux / Git Bash
├── run.bat                        # All-in-one runner for Windows (CMD / double-click)
├── setup.sh                       # Dedicated setup script for macOS / Linux
├── setup.bat                      # Dedicated setup script for Windows
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
