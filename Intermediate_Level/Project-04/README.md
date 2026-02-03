# 🕸️ Web Scraper (BBC RSS Feed)

![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)
![Requests](https://img.shields.io/badge/Library-Requests-green.svg)
![BeautifulSoup](https://img.shields.io/badge/Parser-BeautifulSoup-orange.svg)
![Status](https://img.shields.io/badge/Build-Passing-brightgreen.svg)

A simple **Web Scraper** built in Python using `requests` and `BeautifulSoup`.  
It fetches and parses the **BBC News RSS Feed (XML)** and displays headlines with links in the console.

---

## ✨ Features
- Fetches live RSS feed from BBC.
- Parses XML data using `BeautifulSoup` with `lxml` parser.
- Extracts **title** and **link** from each news item.
- Displays clean console output with emojis for readability.
- Robust error handling for failed requests.

---

## 📂 Project Structure
```
WebScraper/
│── WebScraper.py   # Main script
│── README.md       # Documentation
│── requirements.txt # Dependencies list
│── tests/           # Unit tests
```

---

## ⚙️ Requirements
- Python 3.8+
- Libraries:
  - `requests`
  - `beautifulsoup4`
  - `lxml`

Install dependencies:
```bash
pip install -r requirements.txt
```

---

## 🚀 Usage
Run the script directly:
```bash
python WebScraper.py
```

---

## 🧩 Code Overview
- **fetch_page(url)** → Downloads XML feed from BBC.
- **parse_xml(xml_content)** → Parses XML and extracts `<item>` tags.
- **main()** → Displays top 10 headlines and links.

---

## 🖥️ Sample Output
```
📰 Extracted Headlines:
1. Thousands of Epstein documents taken down after victims identified
2. Sarah Ferguson emails to Epstein show increasing desperation
...

🔗 Extracted Links:
https://www.bbc.com/news/articles/cn0k65pnxjxo?at_medium=RSS&at_campaign=rss
https://www.bbc.com/news/articles/cpdyg117gl2o?at_medium=RSS&at_campaign=rss
...
```

---

## 🔧 Future Improvements
- Extract **description** and **pubDate** for full article summary.
- Save feed data to JSON/CSV for later use.
- Add support for multiple RSS feeds (CNN, Reuters, etc.).
- Build a GUI or web interface for better visualization.
- Add search/filter functionality for headlines.
- Schedule automatic scraping with cron jobs.

---

## 🧪 Testing
Unit tests are included in the `tests/` folder.  
Run tests with:
```bash
pytest
```

Example test:
```python
def test_fetch_page():
    xml_data = fetch_page("http://feeds.bbci.co.uk/news/rss.xml")
    assert "<rss" in xml_data
```

---

## 🤝 Contribution
Contributions are welcome!  
1. Fork the repository  
2. Create a new branch (`feature-xyz`)  
3. Commit changes  
4. Push to branch  
5. Open a Pull Request  

---

## 📜 License
This project is licensed under the MIT License – feel free to use and modify.

---

## 👨‍💻 Author
Developed by **Jiban**  
Focused on **clean parsing, robust error handling, and professional documentation**.
