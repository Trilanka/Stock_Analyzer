import requests
from bs4 import BeautifulSoup
from datetime import datetime
import os
import json

BASE_URL = "https://economynext.com"
SECTION_URL = f"{BASE_URL}/finance/"
TODAY = datetime.now().strftime("%B %d, %Y")  # e.g., "May 22, 2025"
DATE_FILENAME = datetime.now().strftime("%Y-%m-%d")
NEWS_FOLDER = "news"
OUTPUT_FILE = f"{NEWS_FOLDER}/{DATE_FILENAME}.json"

os.makedirs(NEWS_FOLDER, exist_ok=True)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
}

response = requests.get("https://economynext.com/finance/", headers=HEADERS)
if response.status_code != 200:
    print(f"Failed to fetch the page: {SECTION_URL}")
    exit()

soup = BeautifulSoup(response.content, "html.parser")

top_story_divs = soup.find_all("div", class_="top-story")

article_links = set()

for div in top_story_divs:
    for a_tag in div.find_all("a", href=True):
        href = a_tag["href"]
        full_url = href if href.startswith("http") else BASE_URL + href
        article_links.add(full_url)


def extract_article_details(url):
    try:
        res = requests.get(url)
        if res.status_code != 200:
            print(f"Failed to fetch article: {url}")
            return None
        article_soup = BeautifulSoup(res.content, "html.parser")

        # Extract publication date
        date_span = article_soup.find("span", class_="article-publish-date")
        if not date_span:
            return None
        article_date = date_span.text.strip()
        if article_date != TODAY:
            return None

        # Extract title
        title_tag = article_soup.find("h1")
        if not title_tag:
            return None
        title = title_tag.get_text(strip=True)

        # Extract content
        content_div = article_soup.find("div", class_="article-content")
        if not content_div:
            return None
        paragraphs = content_div.find_all("p")
        content = "\n".join(p.get_text(strip=True) for p in paragraphs)

        return {
            "date": TODAY,
            "article_title": title,
            "article_content": content
        }
    except Exception as e:
        print(f"Error processing {url}: {e}")
        return None
    
def extract_article_details(url):
  try:
    res = requests.get(url, headers=HEADERS)

    if res.status_code != 200:
      return None

    article_soup = BeautifulSoup(res.content, "html.parser")

    date_container = article_soup.find("div", class_="story-page-pulish-datetime")
    if not date_container:
        return None

    date_p = date_container.find("p")
    if not date_p:
      print("no p as date")
      return None

    raw_date_str = date_p.text.strip()  # e.g., "Thursday May 22, 2025 2:30 pm"

    try:
      article_datetime = datetime.strptime(raw_date_str, "%A %B %d, %Y %I:%M %p")
    except ValueError as ve:
      print(f"Date parsing failed for: {raw_date_str} ({ve})")
      return None

    if article_datetime.date() != datetime.today().date():
      print("check")
      return None

    title_tag = article_soup.find("h1", class_="story-page-header")
    title = title_tag.get_text(strip=True) if title_tag else "No title found"

    content_div = article_soup.find("div", class_="story-page-text-content")
    paragraphs = content_div.find_all("p") if content_div else []
    content = "\n".join(p.get_text(strip=True) for p in paragraphs)

    return {
        "date": article_datetime.strftime("%Y-%m-%d"),
        "article_title": title,
        "article_content": content
    }
  except Exception as e:
    print(f"Failed to parse {url}: {e}")
    return None



articles = []
print(article_links)
for link in article_links:
  article_data = extract_article_details(link)
  if article_data:
    articles.append(article_data)

# Save to JSON file
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
  json.dump(articles, f, ensure_ascii=False, indent=4)

print(f"Saved {len(articles)} article(s) to {OUTPUT_FILE}")