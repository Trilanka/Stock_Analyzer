import requests
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
}

url = "https://economynext.com/more-news/"

try:
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    
    soup = BeautifulSoup(response.text, "html.parser")

    articles = soup.select("article")
    for article in articles:
        title = article.find("h3")
        if title:
            print(title.text.strip())
except requests.exceptions.RequestException as e:
    print(f"[ERROR] News scraping failed: {e}")
