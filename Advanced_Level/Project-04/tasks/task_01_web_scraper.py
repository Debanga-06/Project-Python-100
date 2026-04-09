"""
Task 1: Web Scraper Bot
Scrapes data from public websites (quotes, news headlines, etc.)
and saves results to JSON/CSV.
"""

import json
import csv
import logging
from datetime import datetime
from pathlib import Path
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

from bot.base_bot import TaskBot
from config.settings import BotConfig

logger = logging.getLogger("TaskBot.Scraper")

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)


class WebScraperBot(TaskBot):
    """Scrapes quotes from quotes.toscrape.com — a public scraping sandbox."""

    def __init__(self, headless: bool = True, pages: int = 5):
        super().__init__(headless=headless)
        self.pages = pages
        self.results = []

    def scrape_quotes(self) -> list[dict]:
        """Scrape quotes, authors, and tags from all pages."""
        logger.info("🕷️  Starting quote scraper (pages=%d)", self.pages)
        base_url = "http://quotes.toscrape.com"

        for page_num in range(1, self.pages + 1):
            url = f"{base_url}/page/{page_num}/"
            self.go_to(url)
            logger.info("Scraping page %d...", page_num)

            try:
                quote_elements = self.driver.find_elements(By.CLASS_NAME, "quote")

                if not quote_elements:
                    logger.info("No quotes found on page %d, stopping.", page_num)
                    break

                for el in quote_elements:
                    try:
                        text = el.find_element(By.CLASS_NAME, "text").text.strip('""')
                        author = el.find_element(By.CLASS_NAME, "author").text.strip()
                        tags = [
                            t.text.strip()
                            for t in el.find_elements(By.CLASS_NAME, "tag")
                        ]
                        self.results.append({
                            "quote": text,
                            "author": author,
                            "tags": tags,
                            "page": page_num,
                        })
                    except NoSuchElementException as e:
                        logger.warning("Skipping element: %s", e)

                logger.info("Page %d: collected %d quotes so far", page_num, len(self.results))
                self.screenshot(f"scraper_page_{page_num}")

            except Exception as e:
                logger.error("Error on page %d: %s", page_num, e)
                break

        return self.results

    def save_to_json(self, filename: str = None) -> Path:
        """Save scraped data to JSON."""
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        path = DATA_DIR / (filename or f"quotes_{ts}.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
        logger.info("💾 Saved %d quotes to %s", len(self.results), path)
        return path

    def save_to_csv(self, filename: str = None) -> Path:
        """Save scraped data to CSV."""
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        path = DATA_DIR / (filename or f"quotes_{ts}.csv")
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["quote", "author", "tags", "page"])
            writer.writeheader()
            for row in self.results:
                row_copy = row.copy()
                row_copy["tags"] = ", ".join(row_copy["tags"])
                writer.writerow(row_copy)
        logger.info("💾 Saved %d quotes to %s", len(self.results), path)
        return path

    def print_summary(self):
        """Print a summary of scraped data."""
        print(f"\n{'='*60}")
        print(f"  📊 SCRAPER SUMMARY")
        print(f"{'='*60}")
        print(f"  Total quotes collected : {len(self.results)}")

        authors = {}
        for item in self.results:
            authors[item["author"]] = authors.get(item["author"], 0) + 1

        print(f"  Unique authors         : {len(authors)}")
        print(f"\n  Top Authors:")
        for author, count in sorted(authors.items(), key=lambda x: -x[1])[:5]:
            print(f"    • {author:<30} {count} quotes")

        print(f"\n  Sample Quotes:")
        for item in self.results[:3]:
            print(f"\n    "{item['quote'][:80]}..."")
            print(f"    — {item['author']}")
        print(f"{'='*60}\n")


def run_scraper(headless: bool = True, pages: int = 3):
    """Run the web scraper bot."""
    print("\n🤖 Task Automation Bot — Web Scraper")
    print("   Target: quotes.toscrape.com (public sandbox)\n")

    bot = WebScraperBot(headless=headless, pages=pages)
    bot.start()
    try:
        bot.scrape_quotes()
        bot.save_to_json()
        bot.save_to_csv()
        bot.print_summary()
    finally:
        bot.stop()

    return bot.results


if __name__ == "__main__":
    run_scraper(headless=False, pages=3)
