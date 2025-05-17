import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json
import time
import os

CSE_API_URL = "https://www.cse.lk/api/tradeSummary"
NEWS_URL = "https://economynext.com/more-news/"
TODAY = datetime.today().strftime("%Y-%m-%d")


def fetch_cse_summary():
    try:
        response = requests.post(CSE_API_URL)
        response.raise_for_status()
       
        return response.json()
    except Exception as e:
        print(f"[ERROR] CSE API failed: {e}")
        return None


# def fetch_news():
#     headers = {
#         "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
#     }
#     try:
#         response = requests.get(NEWS_URL, headers=headers)
#         response.raise_for_status()
#         soup = BeautifulSoup(response.text, 'html.parser')

#         articles = soup.select("div.story-grid-single-story")
#         news_list = []

#         for a in articles[:10]: 
#             title_tag = a.select_one("h3.recent-top-header > a")
#             if not title_tag:
#                 continue
#             title = title_tag.get_text(strip=True)
#             url = title_tag['href']
#             if not url.startswith("http"):
#                 url = "https://economynext.com" + url  

          
#             news_list.append({
#                 "title": title,
#             })
#             time.sleep(1) 

#         return news_list

#     except Exception as e:
#         print(f"[ERROR] News scraping failed: {e}")
#         return []



def save_daily_report(market_data):
    
    folder_path = "/home/ubuntu/Scrapper/Stock_Analyzer/daily_reports"
    os.makedirs(folder_path, exist_ok=True)
    filename = os.path.join(folder_path, f"{TODAY}.json")
    
    if os.path.exists(filename):
        print(f"Report for {TODAY} already exists. Skipping save.")
        return
    
    full_data = {
        "date": TODAY,
        "market_summary": market_data,
    }
    
    with open(filename, "w") as f:
        json.dump(full_data, f, indent=2)

    print(f"Saved report to {filename}")

if __name__ == "__main__":
    market_data = fetch_cse_summary()
    # news_data = fetch_news()
    if market_data:
        save_daily_report(market_data)
    else:
        print("[SKIP] Market data not available. Report not saved.")
