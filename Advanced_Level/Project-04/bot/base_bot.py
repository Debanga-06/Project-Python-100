"""
Task Automation Bot — Core Engine
Python Project #100 | Project #05
"""

import time
import logging
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    WebDriverException,
)
from webdriver_manager.chrome import ChromeDriverManager

from config.settings import BotConfig

# ── Logging Setup ──────────────────────────────────────────────────────────────
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s — %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(LOG_DIR / "bot.log", encoding="utf-8"),
    ],
)
logger = logging.getLogger("TaskBot")


# ── Base Bot ───────────────────────────────────────────────────────────────────
class TaskBot:
    """Base Selenium automation bot with reusable helper methods."""

    def __init__(self, headless: bool = False, config: BotConfig = None):
        self.config = config or BotConfig()
        self.headless = headless
        self.driver: webdriver.Chrome | None = None
        self.wait: WebDriverWait | None = None
        self.screenshots_dir = Path("screenshots")
        self.screenshots_dir.mkdir(exist_ok=True)
        logger.info("TaskBot initialized (headless=%s)", headless)

    # ── Driver Lifecycle ────────────────────────────────────────────────────────
    def start(self):
        """Launch Chrome WebDriver."""
        options = Options()
        if self.headless:
            options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1440,900")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)
        options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        )

        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=options)
        self.driver.execute_script(
            "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
        )
        self.wait = WebDriverWait(self.driver, self.config.WAIT_TIMEOUT)
        logger.info("Chrome WebDriver started")
        return self

    def stop(self):
        """Quit the browser."""
        if self.driver:
            self.driver.quit()
            self.driver = None
            logger.info("WebDriver stopped")

    def __enter__(self):
        return self.start()

    def __exit__(self, *args):
        self.stop()

    # ── Navigation ──────────────────────────────────────────────────────────────
    def go_to(self, url: str):
        """Navigate to URL."""
        logger.info("→ Navigating to: %s", url)
        self.driver.get(url)
        time.sleep(self.config.PAGE_LOAD_DELAY)

    def get_current_url(self) -> str:
        return self.driver.current_url

    def get_title(self) -> str:
        return self.driver.title

    # ── Element Interactions ────────────────────────────────────────────────────
    def find(self, by: By, value: str, timeout: int = None):
        """Wait for and return an element."""
        t = timeout or self.config.WAIT_TIMEOUT
        try:
            return WebDriverWait(self.driver, t).until(
                EC.presence_of_element_located((by, value))
            )
        except TimeoutException:
            logger.error("Element not found: %s = %s", by, value)
            raise

    def find_clickable(self, by: By, value: str, timeout: int = None):
        """Wait for element to be clickable."""
        t = timeout or self.config.WAIT_TIMEOUT
        return WebDriverWait(self.driver, t).until(
            EC.element_to_be_clickable((by, value))
        )

    def click(self, by: By, value: str):
        """Click an element."""
        el = self.find_clickable(by, value)
        el.click()
        logger.debug("Clicked: %s = %s", by, value)
        return el

    def type_text(self, by: By, value: str, text: str, clear: bool = True):
        """Type text into an input field."""
        el = self.find(by, value)
        if clear:
            el.clear()
        for char in text:
            el.send_keys(char)
            time.sleep(0.03)
        logger.debug("Typed into %s: %s = [%s chars]", by, value, len(text))
        return el

    def get_text(self, by: By, value: str) -> str:
        """Get text content of an element."""
        return self.find(by, value).text.strip()

    def get_attribute(self, by: By, value: str, attr: str) -> str:
        """Get an attribute from an element."""
        return self.find(by, value).get_attribute(attr)

    def element_exists(self, by: By, value: str, timeout: int = 3) -> bool:
        """Check if element exists (non-throwing)."""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )
            return True
        except TimeoutException:
            return False

    def scroll_to_bottom(self):
        """Scroll page to bottom."""
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(0.5)

    def scroll_to_element(self, element):
        """Scroll element into view."""
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        time.sleep(0.3)

    # ── Screenshots ─────────────────────────────────────────────────────────────
    def screenshot(self, name: str = "screenshot") -> Path:
        """Take a screenshot and save it."""
        ts = time.strftime("%Y%m%d_%H%M%S")
        path = self.screenshots_dir / f"{name}_{ts}.png"
        self.driver.save_screenshot(str(path))
        logger.info("📸 Screenshot saved: %s", path)
        return path

    # ── Utilities ───────────────────────────────────────────────────────────────
    def sleep(self, seconds: float):
        """Human-like delay."""
        time.sleep(seconds)

    def wait_for_url_change(self, original_url: str, timeout: int = 10):
        """Wait until URL changes from original."""
        WebDriverWait(self.driver, timeout).until(
            EC.url_changes(original_url)
        )

    def switch_to_new_tab(self):
        """Switch to the most recently opened tab."""
        self.driver.switch_to.window(self.driver.window_handles[-1])

    def close_current_tab(self):
        """Close current tab and switch back to first."""
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])

    def execute_js(self, script: str, *args):
        """Run arbitrary JavaScript."""
        return self.driver.execute_script(script, *args)
