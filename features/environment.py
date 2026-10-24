import logging
import re
from datetime import datetime, timezone
from uuid import uuid4

from behave.model_core import Status

from helpers.browser_factory import create_browser
from helpers.config import PROJECT_ROOT, load_config

LOGGER = logging.getLogger(__name__)


def before_all(context):
    context.settings = load_config()


def before_scenario(context, scenario):
    context.browser = create_browser(context.settings)
    context.add_cleanup(lambda: context.browser.quit())


def after_scenario(context, scenario):
    if scenario.status in (Status.skipped, Status.untested):
        return
    browser = getattr(context, "browser", None)
    if browser is None:
        return
    capture_screenshot(browser, scenario)


def capture_screenshot(browser, scenario):
    try:
        directory = PROJECT_ROOT / "reports" / "screenshots"
        directory.mkdir(parents=True, exist_ok=True)
        name = re.sub(r"[^A-Za-z0-9_-]+", "_", scenario.name).strip("_")[:80]
        result = scenario.status.name
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
        path = directory / f"{name or 'scenario'}_{result}_{timestamp}_{uuid4().hex[:8]}.png"
        if not browser.save_screenshot(str(path)):
            LOGGER.warning("Browser could not save %s screenshot: %s", result, path)
            return
        LOGGER.info("Screenshot (%s) saved: %s", result, path)
    except Exception:
        LOGGER.exception("Could not capture screenshot")
