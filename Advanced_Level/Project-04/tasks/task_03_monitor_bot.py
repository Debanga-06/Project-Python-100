"""
Task 3: Website Monitor Bot
Monitors websites for changes in content/price/status
and saves timestamped screenshots and diffs.
"""

import json
import logging
import hashlib
import time
from datetime import datetime
from pathlib import Path
from dataclasses import dataclass, field, asdict
from typing import Optional
from selenium.webdriver.common.by import By

from bot.base_bot import TaskBot

logger = logging.getLogger("TaskBot.Monitor")

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

MONITOR_DB = DATA_DIR / "monitor_history.json"


@dataclass
class MonitorTarget:
    """A URL + CSS selector to watch for changes."""
    name: str
    url: str
    selector: str
    check_interval: int = 60        # seconds between checks
    alert_on_change: bool = True


@dataclass
class MonitorResult:
    name: str
    url: str
    selector: str
    content: str
    content_hash: str
    timestamp: str
    changed: bool = False
    previous_content: Optional[str] = None


class WebsiteMonitorBot(TaskBot):
    """Monitors websites and detects content changes."""

    def __init__(self, headless: bool = True, targets: list[MonitorTarget] = None):
        super().__init__(headless=headless)
        self.targets = targets or self._default_targets()
        self.history: dict = self._load_history()
        self.results: list[MonitorResult] = []

    def _default_targets(self) -> list[MonitorTarget]:
        return [
            MonitorTarget(
                name="Hacker News Top Story",
                url="https://news.ycombinator.com",
                selector=".titleline > a",
            ),
            MonitorTarget(
                name="Python.org Latest News",
                url="https://www.python.org",
                selector=".blog-widget li:first-child a",
            ),
            MonitorTarget(
                name="Wikipedia Featured Article",
                url="https://en.wikipedia.org/wiki/Main_Page",
                selector="#mp-tfa b a",
            ),
        ]

    def _load_history(self) -> dict:
        if MONITOR_DB.exists():
            with open(MONITOR_DB, "r") as f:
                return json.load(f)
        return {}

    def _save_history(self):
        with open(MONITOR_DB, "w") as f:
            json.dump(self.history, f, indent=2)

    def _hash_content(self, content: str) -> str:
        return hashlib.md5(content.encode("utf-8")).hexdigest()

    def check_target(self, target: MonitorTarget) -> MonitorResult:
        """Check a single target for changes."""
        logger.info("🔍 Checking: %s", target.name)
        self.go_to(target.url)
        self.sleep(1.5)

        try:
            element = self.find(By.CSS_SELECTOR, target.selector, timeout=10)
            content = element.text.strip()
            content_hash = self._hash_content(content)
        except Exception as e:
            logger.warning("⚠️ Could not read selector '%s' on %s: %s", target.selector, target.url, e)
            content = "[ELEMENT NOT FOUND]"
            content_hash = self._hash_content(content)

        ts = datetime.now().isoformat()
        previous = self.history.get(target.name)
        changed = previous is not None and previous.get("hash") != content_hash

        if changed:
            logger.warning("🔔 CHANGE DETECTED on '%s'!", target.name)
            logger.warning("   Old: %s", previous.get("content", "")[:80])
            logger.warning("   New: %s", content[:80])
            self.screenshot(f"change_{target.name.replace(' ', '_')}")
        else:
            logger.info("✅ No change on '%s'", target.name)
            self.screenshot(f"check_{target.name.replace(' ', '_')}")

        # Update history
        self.history[target.name] = {
            "hash": content_hash,
            "content": content,
            "last_checked": ts,
            "url": target.url,
        }

        result = MonitorResult(
            name=target.name,
            url=target.url,
            selector=target.selector,
            content=content,
            content_hash=content_hash,
            timestamp=ts,
            changed=changed,
            previous_content=previous.get("content") if previous else None,
        )
        self.results.append(result)
        return result

    def run_once(self) -> list[MonitorResult]:
        """Check all targets once."""
        logger.info("🖥️  Running monitor check on %d targets", len(self.targets))
        for target in self.targets:
            try:
                self.check_target(target)
            except Exception as e:
                logger.error("Error checking %s: %s", target.name, e)

        self._save_history()
        logger.info("Monitor run complete. History saved.")
        return self.results

    def run_loop(self, cycles: int = 3, interval: int = 30):
        """Run monitoring in a loop."""
        logger.info("🔄 Starting monitor loop: %d cycles, %ds interval", cycles, interval)
        for i in range(cycles):
            logger.info("── Cycle %d/%d ──", i + 1, cycles)
            self.run_once()
            if i < cycles - 1:
                logger.info("Sleeping %ds before next check...", interval)
                time.sleep(interval)

    def save_report(self) -> Path:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        path = DATA_DIR / f"monitor_report_{ts}.json"
        report = [asdict(r) for r in self.results]
        with open(path, "w") as f:
            json.dump(report, f, indent=2)
        logger.info("📄 Report saved: %s", path)
        return path

    def print_summary(self):
        changes = [r for r in self.results if r.changed]
        print(f"\n{'='*60}")
        print(f"  🖥️  MONITOR SUMMARY")
        print(f"{'='*60}")
        print(f"  Targets checked  : {len(self.results)}")
        print(f"  Changes detected : {len(changes)}")
        print()
        for r in self.results:
            status = "🔔 CHANGED" if r.changed else "✅ No change"
            print(f"  [{status}] {r.name}")
            print(f"    Content: {r.content[:70]}...")
            if r.changed:
                print(f"    Was    : {r.previous_content[:70]}...")
        print(f"{'='*60}\n")


def run_monitor(headless: bool = True, cycles: int = 1):
    """Run the website monitor bot."""
    print("\n🤖 Task Automation Bot — Website Monitor")
    print("   Checking 3 public sites for content changes\n")

    bot = WebsiteMonitorBot(headless=headless)
    bot.start()
    try:
        if cycles == 1:
            bot.run_once()
        else:
            bot.run_loop(cycles=cycles, interval=30)
        bot.save_report()
        bot.print_summary()
    finally:
        bot.stop()


if __name__ == "__main__":
    run_monitor(headless=True, cycles=1)
