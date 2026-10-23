"""Behave lifecycle hooks; application navigation belongs in future steps."""

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
    # Behave runs this even if a later step or hook fails.
    context.add_cleanup(context.browser.quit)


def after_scenario(context, scenario):
    if scenario.status != Status.failed:
        return
    browser = getattr(context, "browser", None)
    if browser is None:
        return

    try:
        directory = PROJECT_ROOT / "reports" / "screenshots"
        directory.mkdir(parents=True, exist_ok=True)
        name = re.sub(r"[^A-Za-z0-9_-]+", "_", scenario.name).strip("_")[:80]
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
        path = directory / f"{name or 'scenario'}_{timestamp}_{uuid4().hex[:8]}.png"
        if not browser.save_screenshot(str(path)):
            LOGGER.warning("Browser could not save failure screenshot: %s", path)
            return
        LOGGER.warning("Failure screenshot saved: %s", path)
    except Exception:
        # Screenshot errors must not replace the original scenario failure.
        LOGGER.exception("Could not capture failure screenshot")
