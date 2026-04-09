"""
Task 4: Search Automation & Results Extractor
Automates Google/DuckDuckGo searches and extracts result titles, URLs, and snippets.
"""

import json
import csv
import logging
from datetime import datetime
from pathlib import Path
from dataclasses import dataclass, asdict
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

from bot.base_bot import TaskBot

logger = logging.getLogger("TaskBot.Search")

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)


@dataclass
class SearchResult:
    rank: int
    title: str
    url: str
    snippet: str
    query: str
    engine: str
    timestamp: str


class SearchBot(TaskBot):
    """Automates web searches and extracts results."""

    def __init__(self, headless: bool = True, engine: str = "duckduckgo"):
        super().__init__(headless=headless)
        self.engine = engine.lower()
        self.all_results: list[SearchResult] = []

    def search_duckduckgo(self, query: str, max_results: int = 10) -> list[SearchResult]:
        """Search DuckDuckGo and extract results."""
        logger.info("🔍 Searching DuckDuckGo: '%s'", query)
        self.go_to("https://duckduckgo.com")
        self.sleep(1)

        search_box = self.find(By.NAME, "q")
        search_box.clear()
        search_box.send_keys(query)
        search_box.send_keys(Keys.RETURN)
        self.sleep(2)

        self.screenshot(f"search_ddg_{query[:20].replace(' ', '_')}")

        results = []
        result_elements = self.driver.find_elements(By.CSS_SELECTOR, "[data-testid='result']")

        for i, el in enumerate(result_elements[:max_results], 1):
            try:
                title_el = el.find_element(By.CSS_SELECTOR, "h2 a span")
                title = title_el.text.strip()

                url_el = el.find_element(By.CSS_SELECTOR, "h2 a")
                url = url_el.get_attribute("href") or ""

                try:
                    snippet_el = el.find_element(By.CSS_SELECTOR, "[data-result='snippet']")
                    snippet = snippet_el.text.strip()
                except NoSuchElementException:
                    snippet = ""

                result = SearchResult(
                    rank=i,
                    title=title,
                    url=url,
                    snippet=snippet[:200],
                    query=query,
                    engine="DuckDuckGo",
                    timestamp=datetime.now().isoformat(),
                )
                results.append(result)
                logger.debug("  #%d: %s", i, title[:60])

            except NoSuchElementException:
                continue

        logger.info("Found %d results for '%s'", len(results), query)
        self.all_results.extend(results)
        return results

    def search_multiple(self, queries: list[str], max_per_query: int = 5) -> list[SearchResult]:
        """Run multiple searches."""
        logger.info("Running %d searches...", len(queries))
        for query in queries:
            try:
                if self.engine == "duckduckgo":
                    self.search_duckduckgo(query, max_per_query)
                self.sleep(2)
            except Exception as e:
                logger.error("Error searching '%s': %s", query, e)
        return self.all_results

    def save_results(self, fmt: str = "both") -> list[Path]:
        """Save results to JSON and/or CSV."""
        paths = []
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")

        if fmt in ("json", "both"):
            path = DATA_DIR / f"search_results_{ts}.json"
            with open(path, "w", encoding="utf-8") as f:
                json.dump([asdict(r) for r in self.all_results], f, indent=2, ensure_ascii=False)
            logger.info("💾 JSON saved: %s", path)
            paths.append(path)

        if fmt in ("csv", "both"):
            path = DATA_DIR / f"search_results_{ts}.csv"
            with open(path, "w", newline="", encoding="utf-8") as f:
                if self.all_results:
                    writer = csv.DictWriter(f, fieldnames=asdict(self.all_results[0]).keys())
                    writer.writeheader()
                    writer.writerows([asdict(r) for r in self.all_results])
            logger.info("💾 CSV saved: %s", path)
            paths.append(path)

        return paths

    def print_summary(self):
        print(f"\n{'='*65}")
        print(f"  🔍 SEARCH BOT SUMMARY")
        print(f"{'='*65}")
        print(f"  Engine        : {self.engine.title()}")
        print(f"  Total results : {len(self.all_results)}")

        queries = list({r.query for r in self.all_results})
        print(f"  Queries run   : {len(queries)}")
        print()
        for query in queries:
            results = [r for r in self.all_results if r.query == query]
            print(f"  Query: \"{query}\" → {len(results)} results")
            for r in results[:3]:
                print(f"    #{r.rank}. {r.title[:55]}")
                print(f"         {r.url[:65]}")
        print(f"{'='*65}\n")


def run_search_bot(queries: list[str] = None, headless: bool = True):
    """Run the search automation bot."""
    print("\n🤖 Task Automation Bot — Search & Extractor")
    print("   Engine: DuckDuckGo (no tracking)\n")

    if queries is None:
        queries = [
            "Python Flask tutorial 2024",
            "Selenium automation best practices",
            "Python project ideas for beginners",
        ]

    bot = SearchBot(headless=headless, engine="duckduckgo")
    bot.start()
    try:
        bot.search_multiple(queries, max_per_query=5)
        bot.save_results(fmt="both")
        bot.print_summary()
    finally:
        bot.stop()

    return bot.all_results


if __name__ == "__main__":
    run_search_bot(headless=True)
