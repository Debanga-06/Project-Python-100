# 📰 RSS Feed Reader (Python)

![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)
![Requests](https://img.shields.io/badge/Library-Requests-green.svg)
![XML](https://img.shields.io/badge/Parser-XML-orange.svg)
![Status](https://img.shields.io/badge/Build-Passing-brightgreen.svg)

A lightweight **RSS Feed Reader** built in Python using `requests` and `xml.etree.ElementTree`.  
It fetches and parses RSS feeds from major news sources (CNN as primary, BBC as fallback) and displays headlines in a clean, console‑friendly format.

---

## ✨ Features
- Fetches live RSS feeds using `requests`.
- Parses XML data with Python’s built‑in `xml.etree.ElementTree`.
- Automatic **fallback logic**: if CNN feed fails, switches to BBC feed.
- Displays feed title, publication date, link, and description.
- Clean console output with emojis for readability.

---

## 📂 Project Structure
```
rss_reader/
│── rss_reader.py   # Main script
│── README.md       # Documentation
```

---

## ⚙️ Requirements
- Python 3.8+
- Libraries:
  - `requests` (install via pip)

Install dependencies:
```bash
pip install requests
```

---

## 🚀 Usage
Run the script directly:
```bash
python rss_reader.py
```

---

## 🧩 Code Overview

### 1. Fetch RSS Feed
```python
def fetch_rss(url):
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.content
```
- Uses `requests.get()` with a timeout.
- Raises exception if feed is unavailable.

### 2. Parse XML Feed
```python
def parse_rss(xml_data):
    root = ET.fromstring(xml_data)
    channel = root.find("channel")
    feed_title = channel.find("title").text
    ...
```
- Extracts `<channel>` and `<item>` tags.
- Collects title, link, description, and publication date.

### 3. Display Feed
```python
def display_feed(feed_title, items):
    print(f"\n📰 {feed_title}\n" + "=" * 50)
    for i, item in enumerate(items, start=1):
        ...
```
- Prints feed title and items in a formatted way.

### 4. Main Logic
```python
def main():
    try:
        xml_data = fetch_rss(RSS_URL)
    except Exception:
        print("⚠️ CNN feed failed, switching to BBC...")
        xml_data = fetch_rss(FALLBACK_URL)

    feed_title, items = parse_rss(xml_data)
    display_feed(feed_title, items)
```
- Attempts CNN feed first.
- Falls back to BBC if CNN fails.

---

## 🖥️ Sample Output
```
📰 CNN.com - RSS Channel
==================================================

1. Breaking News Headline
📅 Tue, 03 Feb 2026 18:30:00 GMT
🔗 https://cnn.com/news/article
📝 Short description of the article...
```

---

## 🔧 Future Improvements
- Add support for multiple feeds.
- Save feed data to JSON/CSV.
- GUI or web interface for better visualization.
- Add search/filter functionality.

---

## 📜 License
This project is licensed under the MIT License – feel free to use and modify.

---

## 👨‍💻 Author
Developed by **Jiban**  
Focused on **robust error handling, clean output, and professional documentation**.
