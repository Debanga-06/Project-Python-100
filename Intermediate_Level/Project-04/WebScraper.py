import requests
from bs4 import BeautifulSoup

URL = "http://feeds.bbci.co.uk/news/rss.xml"

def fetch_page(url):
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.text

def parse_xml(xml_content):
    soup = BeautifulSoup(xml_content, "xml")
    items = soup.find_all("item")

    titles = [item.title.get_text(strip=True) for item in items]
    links = [item.link.get_text(strip=True) for item in items]

    return titles, links

def main():
    xml_content = fetch_page(URL)
    titles, links = parse_xml(xml_content)

    print("\n📰 Extracted Headlines:")
    for i, title in enumerate(titles[:10], start=1):
        print(f"{i}. {title}")

    print("\n🔗 Extracted Links:")
    for link in links[:10]:
        print(link)

if __name__ == "__main__":
    main()