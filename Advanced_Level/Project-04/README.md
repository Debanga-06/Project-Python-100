# 🤖 Project 05 — Task Automation Bot

> **Python Project #100** | Advanced Level | Selenium · Web Automation · Data Extraction

A powerful, modular web automation framework built with Selenium. Includes 4 ready-to-run tasks: web scraping, form filling, website monitoring, and search automation.

---

## 🚀 Tasks Included

| # | Task | Target | Output |
|---|---|---|---|
| 1 | 🕷️ **Web Scraper** | quotes.toscrape.com | JSON + CSV |
| 2 | 📝 **Form Filler** | demoqa.com practice form | Screenshots |
| 3 | 🖥️ **Website Monitor** | Hacker News, Python.org, Wikipedia | Change report |
| 4 | 🔍 **Search Bot** | DuckDuckGo | JSON + CSV |

> ✅ All targets are **public sandbox/test sites** — no credentials required for most tasks.

---

## 🗂️ Project Structure

```
project-05-task-automation-bot/
├── main.py                          # Interactive CLI entry point
├── bot/
│   ├── __init__.py
│   └── base_bot.py                  # TaskBot base class (all Selenium logic)
├── tasks/
│   ├── __init__.py
│   ├── task_01_web_scraper.py       # Scrapes quotes (titles, authors, tags)
│   ├── task_02_form_filler.py       # Fills DemoQA multi-step form
│   ├── task_03_monitor_bot.py       # Monitors URLs for content changes
│   └── task_04_search_bot.py        # DuckDuckGo search + result extractor
├── config/
│   ├── __init__.py
│   └── settings.py                  # BotConfig dataclass
├── logs/
│   └── bot.log                      # Auto-generated log file
├── screenshots/                     # Auto-saved screenshots per task step
├── data/                            # Scraped/extracted output files
├── requirements.txt
└── .env.example
```

---

## ⚙️ Setup & Installation

### 1. Prerequisites
- Python 3.11+
- **Google Chrome** installed (latest version)
- ChromeDriver is auto-installed via `webdriver-manager`

### 2. Clone & Navigate
```bash
cd python-project-100/project-05-task-automation-bot
```

### 3. Create Virtual Environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Configure (Optional)
```bash
cp .env.example .env
# Only needed for social login tasks
```

---

## ▶️ Running the Bot

### Interactive Menu
```bash
python main.py
```
```
╔══════════════════════════════════════════════════════════╗
║         🤖  TASK AUTOMATION BOT                          ║
║         Python Project #100  |  Project #05             ║
╚══════════════════════════════════════════════════════════╝

  [1] 🕷️  Web Scraper      — Scrape quotes from toscrape.com
  [2] 📝  Form Filler      — Auto-fill DemoQA practice form
  [3] 🖥️  Website Monitor  — Track content changes on 3 sites
  [4] 🔍  Search Bot       — DuckDuckGo search + result extractor
  [5] 🚀  Run All Tasks    — Execute all tasks sequentially
  [0] ❌  Exit
```

### CLI Flags
```bash
python main.py --task scraper        # Run web scraper
python main.py --task form           # Run form filler
python main.py --task monitor        # Run website monitor
python main.py --task search         # Run search bot
python main.py --task all            # Run all tasks
python main.py --task scraper --headless   # Headless (no browser window)
```

### Run Individual Tasks Directly
```bash
python tasks/task_01_web_scraper.py
python tasks/task_02_form_filler.py
python tasks/task_03_monitor_bot.py
python tasks/task_04_search_bot.py
```

---

## 🧩 TaskBot Base Class

The `TaskBot` base class in `bot/base_bot.py` provides all reusable Selenium helpers:

```python
from bot.base_bot import TaskBot
from selenium.webdriver.common.by import By

class MyBot(TaskBot):
    def run(self):
        self.go_to("https://example.com")
        self.type_text(By.ID, "search", "hello world")
        self.click(By.CSS_SELECTOR, "button[type='submit']")
        text = self.get_text(By.CLASS_NAME, "result")
        self.screenshot("my_result")
        print(text)

with MyBot(headless=False) as bot:
    bot.run()
```

### Available Methods

| Method | Description |
|---|---|
| `start()` / `stop()` | Launch/quit Chrome |
| `go_to(url)` | Navigate to URL |
| `find(by, value)` | Wait + return element |
| `find_clickable(by, value)` | Wait for clickable |
| `click(by, value)` | Click an element |
| `type_text(by, value, text)` | Type into input |
| `get_text(by, value)` | Get element text |
| `get_attribute(by, value, attr)` | Get HTML attribute |
| `element_exists(by, value)` | Bool — element present? |
| `scroll_to_bottom()` | Scroll to page bottom |
| `scroll_to_element(el)` | Scroll element into view |
| `screenshot(name)` | Save timestamped screenshot |
| `execute_js(script)` | Run JavaScript |
| `switch_to_new_tab()` | Switch to latest tab |
| `wait_for_url_change(url)` | Wait for navigation |

---

## 📋 Task Details

### Task 1: Web Scraper
- **URL:** `http://quotes.toscrape.com` (safe scraping sandbox)
- **Extracts:** Quote text, author, tags, page number
- **Output:** `data/quotes_<timestamp>.json` + `.csv`
- **Screenshots:** One per page scraped

### Task 2: Form Filler
- **URL:** `https://demoqa.com/automation-practice-form`
- **Fills:** Name, email, gender, phone, DOB, subjects, hobbies, address, state, city
- **Output:** Screenshots at each step + confirmation screenshot
- **Technique:** React datepicker, `Select` dropdowns, checkbox JS click

### Task 3: Website Monitor
- **Targets:** Hacker News · Python.org · Wikipedia Main Page
- **Logic:** Hashes element text → compares with last check → detects changes
- **Output:** `data/monitor_report_<timestamp>.json` + `data/monitor_history.json`
- **Supports:** Multi-cycle loop with configurable interval

### Task 4: Search Bot
- **Engine:** DuckDuckGo (privacy-respecting, no bot blocks)
- **Extracts:** Rank, title, URL, snippet for each result
- **Output:** `data/search_results_<timestamp>.json` + `.csv`
- **Supports:** Multiple queries in one run

---

## ⚙️ BotConfig Settings

Edit `config/settings.py` or `.env`:

```python
WAIT_TIMEOUT = 15       # Max seconds to wait for elements
PAGE_LOAD_DELAY = 1.5   # Delay after navigation
TYPING_DELAY = 0.03     # Per-character typing speed
ACTION_DELAY = 0.8      # Between actions
MAX_RETRIES = 3         # Retry failed actions
```

---

## 🛡️ Anti-Detection Features

- Custom `user-agent` string (mimics real browser)
- `webdriver` property overridden via JS
- `AutomationControlled` flag disabled
- Human-like character-by-character typing
- Random delays between actions

---

## 📦 Output Files

```
data/
├── quotes_20240415_143022.json        # Scraped quotes
├── quotes_20240415_143022.csv
├── search_results_20240415_143155.json
├── search_results_20240415_143155.csv
├── monitor_report_20240415_143300.json
└── monitor_history.json               # Persistent change tracking

screenshots/
├── scraper_page_1_20240415_143022.png
├── form_step_1_personal_...png
├── form_submitted_success_...png
└── check_Hacker_News_...png

logs/
└── bot.log                            # Timestamped log file
```

---

## 🧠 Concepts Practiced

- Selenium WebDriver setup & management
- Explicit vs Implicit waits (`WebDriverWait`, `EC`)
- CSS Selector & XPath element targeting
- Handling React dynamic components
- `Select` dropdowns & checkbox automation
- JavaScript injection for element interaction
- Screenshot capture & file management
- Content hashing for change detection
- Dataclass-based configuration
- Context manager pattern (`__enter__`/`__exit__`)
- CSV & JSON data persistence
- Logging to file + console

---

*Part of the **Python Project #100** series — Advanced Level Projects*