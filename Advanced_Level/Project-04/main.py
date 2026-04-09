#!/usr/bin/env python3
"""
Task Automation Bot — Main Entry Point
Python Project #100 | Project #05

Usage:
    python main.py                   # Interactive menu
    python main.py --task scraper    # Run web scraper
    python main.py --task form       # Run form filler
    python main.py --task monitor    # Run website monitor
    python main.py --task search     # Run search bot
    python main.py --task all        # Run all tasks
    python main.py --headless        # Run in headless mode
"""

import argparse
import sys
import logging

logger = logging.getLogger("TaskBot.Main")


BANNER = """
╔══════════════════════════════════════════════════════════╗
║         🤖  TASK AUTOMATION BOT                          ║
║         Python Project #100  |  Project #05             ║
║         Selenium · Web Automation · Data Extraction      ║
╚══════════════════════════════════════════════════════════╝
"""

MENU = """
  Select a task to run:

  [1] 🕷️  Web Scraper      — Scrape quotes from toscrape.com
  [2] 📝  Form Filler      — Auto-fill DemoQA practice form
  [3] 🖥️  Website Monitor  — Track content changes on 3 sites
  [4] 🔍  Search Bot       — DuckDuckGo search + result extractor
  [5] 🚀  Run All Tasks    — Execute all tasks sequentially
  [0] ❌  Exit

"""


def run_task(task: str, headless: bool = False):
    """Run a specific task by name."""
    task = task.lower().strip()

    if task in ("1", "scraper", "scrape"):
        from tasks.task_01_web_scraper import run_scraper
        run_scraper(headless=headless, pages=3)

    elif task in ("2", "form", "filler"):
        from tasks.task_02_form_filler import run_form_filler
        run_form_filler(headless=headless)

    elif task in ("3", "monitor"):
        from tasks.task_03_monitor_bot import run_monitor
        run_monitor(headless=headless, cycles=1)

    elif task in ("4", "search"):
        from tasks.task_04_search_bot import run_search_bot
        run_search_bot(headless=headless)

    elif task in ("5", "all"):
        print("\n🚀 Running ALL tasks sequentially...\n")
        from tasks.task_01_web_scraper import run_scraper
        from tasks.task_02_form_filler import run_form_filler
        from tasks.task_03_monitor_bot import run_monitor
        from tasks.task_04_search_bot import run_search_bot

        run_scraper(headless=True, pages=2)
        run_form_filler(headless=headless)
        run_monitor(headless=True, cycles=1)
        run_search_bot(headless=True)
        print("\n✅ All tasks completed!\n")

    else:
        print(f"❌ Unknown task: '{task}'")
        print("   Valid options: scraper | form | monitor | search | all")
        sys.exit(1)


def interactive_menu(headless: bool = False):
    """Show interactive task selection menu."""
    print(BANNER)
    print(MENU)

    choice = input("  Enter choice [0-5]: ").strip()

    task_map = {
        "1": "scraper",
        "2": "form",
        "3": "monitor",
        "4": "search",
        "5": "all",
        "0": "exit",
    }

    if choice == "0":
        print("\n👋 Exiting. Goodbye!\n")
        sys.exit(0)

    if choice not in task_map:
        print(f"\n❌ Invalid choice: '{choice}'. Enter 0–5.\n")
        sys.exit(1)

    run_task(task_map[choice], headless=headless)


def main():
    parser = argparse.ArgumentParser(
        description="🤖 Task Automation Bot — Python Project #100 | Project #05"
    )
    parser.add_argument(
        "--task",
        type=str,
        default=None,
        help="Task to run: scraper | form | monitor | search | all",
    )
    parser.add_argument(
        "--headless",
        action="store_true",
        default=False,
        help="Run browser in headless mode (no visible window)",
    )
    args = parser.parse_args()

    print(BANNER)

    if args.task:
        run_task(args.task, headless=args.headless)
    else:
        interactive_menu(headless=args.headless)


if __name__ == "__main__":
    main()
