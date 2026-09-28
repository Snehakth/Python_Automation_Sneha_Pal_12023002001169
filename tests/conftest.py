"""Shared browser, test-data, and screenshot fixtures."""

import os
import re
from pathlib import Path

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from test_data.data_loader import load_purchase_data


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SCREENSHOT_DIR = PROJECT_ROOT / "artifacts" / "screenshots"


@pytest.fixture(scope="session")
def purchase_data():
    return load_purchase_data()


@pytest.fixture
def driver():
    SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)
    options = Options()
    options.add_argument("--window-size=1440,1000")
    options.add_argument("--disable-notifications")
    if os.getenv("HEADLESS", "0").lower() in {"1", "true", "yes"}:
        options.add_argument("--headless=new")

    browser = webdriver.Chrome(options=options)
    browser.set_page_load_timeout(45)
    yield browser
    browser.quit()


@pytest.fixture
def capture_screenshot(driver, request):
    def capture(stage: str) -> Path:
        safe_stage = re.sub(r"[^a-zA-Z0-9_-]", "_", stage)
        image_path = SCREENSHOT_DIR / f"{request.node.name}_{safe_stage}.png"
        driver.save_screenshot(str(image_path))
        return image_path

    return capture


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed:
        browser = item.funcargs.get("driver")
        if browser:
            SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)
            browser.save_screenshot(str(SCREENSHOT_DIR / f"{item.name}_failure.png"))