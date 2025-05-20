import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json
import os

CSE_API_URL = "https://www.cse.lk/api/tradeSummary"

TODAY = datetime.today().strftime("%Y-%m-%d")


def fetch_cse_summary():
    try:
        response = requests.post(CSE_API_URL)
        response.raise_for_status()
       
        return response.json()
    except Exception as e:
        print(f"[ERROR] CSE API failed: {e}")
        return None


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
    if market_data:
        save_daily_report(market_data)
    else:
        print("[SKIP] Market data not available. Report not saved.")
